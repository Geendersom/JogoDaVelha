"""
Jogo da Velha (Tic-Tac-Toe)
Criado por Geêndersom Araújo
Linguagem principal: Python

Este jogo foi desenvolvido usando Pyodide para executar Python diretamente no navegador.
Toda a lógica do jogo, incluindo cálculos matemáticos, validações e manipulação do DOM,
está implementada em Python, mantendo a linguagem como raiz do projeto.

Arquitetura:
- Python (JogoDaVelha.py): Lógica principal do jogo, cálculos, validações e manipulação do DOM
- HTML (index.html, selecao.html): Estrutura e interface do usuário
- CSS (styles.css): Estilização e animações visuais
- JavaScript: Apenas funções auxiliares mínimas (sons, helpers)

O arquivo Python é o maior arquivo do projeto, contendo toda a lógica central.
"""

# Importações do Pyodide para interação com JavaScript/DOM
from js import document, console, window  # type: ignore
from pyodide.ffi import create_proxy  # type: ignore

class JogoDaVelha:
    """
    Classe principal do Jogo da Velha
    
    Esta classe gerencia todo o estado e lógica do jogo, incluindo:
    - Gerenciamento do tabuleiro
    - Validação de jogadas
    - Verificação de vitória/empate
    - Atualização visual do DOM
    - Cálculo e animação da linha de vitória
    - Gerenciamento de turnos
    
    Atributos:
        tabuleiro (dict): Dicionário representando o tabuleiro 3x3
        turno (str): Símbolo do jogador atual ('X' ou 'O')
        jogo_ativo (bool): Indica se o jogo está em andamento
    """
    
    def __init__(self, jogador_inicial="X"):
        """
        Inicializa uma nova instância do jogo
        
        Args:
            jogador_inicial (str): Símbolo do jogador inicial (sempre 'X' por padrão)
        """
        # Tabuleiro representado como dicionário com chaves de '1' a '9'
        # Layout numérico do teclado:
        # 7 8 9
        # 4 5 6
        # 1 2 3
        self.tabuleiro = {
            '7': ' ', '8': ' ', '9': ' ',
            '4': ' ', '5': ' ', '6': ' ',
            '1': ' ', '2': ' ', '3': ' '
        }
        
        # Sempre começa com X (regra do jogo)
        self.turno = "X"
        self.jogo_ativo = True
        
        # Configura a interface e event listeners
        self._configurar_interface()

    def _configurar_interface(self):
        """Configura a interface do jogo manipulando o DOM diretamente do Python"""
        # Atualiza o tabuleiro visual
        self.atualizar_tabuleiro_visual()
        
        # Atualiza o turno inicial
        self.atualizar_turno()
        
        # Configura os event listeners das células
        celulas = document.querySelectorAll('.celula')
        for i in range(celulas.length):
            celula = celulas[i]
            posicao = celula.getAttribute('data-pos')
            # Cria uma função closure para capturar a posição corretamente
            def criar_callback(pos):
                def callback(event):
                    self.fazer_jogada(pos)
                return callback
            callback = create_proxy(criar_callback(posicao))
            celula.addEventListener('click', callback)

    def atualizar_tabuleiro_visual(self, posicoes_vencedoras=None):
        """Atualiza o tabuleiro visual no navegador usando Python"""
        if posicoes_vencedoras is None:
            posicoes_vencedoras = []
        
        celulas = document.querySelectorAll('.celula')
        for i in range(celulas.length):
            celula = celulas[i]
            posicao = celula.getAttribute('data-pos')
            valor = self.tabuleiro[posicao]
            
            # Limpa o conteúdo e classes
            celula.textContent = '' if valor == ' ' else valor
            celula.className = 'celula'
            
            # Verifica se esta célula faz parte da sequência vencedora
            is_vencedor = posicao in posicoes_vencedoras
            
            # Adiciona classes específicas para X e O
            if valor == 'X':
                celula.classList.add('x')
                if is_vencedor:
                    celula.classList.add('vencedor')
                elif posicoes_vencedoras:  # Se há vencedor mas esta célula não é vencedora
                    celula.classList.add('escurecido')
            elif valor == 'O':
                celula.classList.add('o')
                if is_vencedor:
                    celula.classList.add('vencedor')
                elif posicoes_vencedoras:  # Se há vencedor mas esta célula não é vencedora
                    celula.classList.add('escurecido')

    def atualizar_status(self, mensagem, tipo=''):
        """Atualiza a mensagem de status no navegador usando Python"""
        status_el = document.getElementById('status')
        status_el.textContent = mensagem
        status_el.className = 'status'
        
        if tipo == 'vencedor':
            status_el.classList.add('vencedor')
        elif tipo == 'empate':
            status_el.classList.add('empate')
    
    def atualizar_turno(self):
        """Atualiza o display de turno"""
        try:
            window.atualizarTurno(self.turno)
        except:
            pass

    def habilitar_celulas(self, habilitado):
        """Habilita ou desabilita as células do tabuleiro usando Python"""
        celulas = document.querySelectorAll('.celula')
        for i in range(celulas.length):
            celula = celulas[i]
            if habilitado:
                celula.classList.remove('disabled')
            else:
                celula.classList.add('disabled')

    def verificar_jogada(self, jogada):
        """Verifica se uma jogada é válida"""
        if jogada in self.tabuleiro.keys():
            if self.tabuleiro[jogada] == " ":
                return True
        return False

    def verificar_tabuleiro(self):
        """Verifica o estado atual do tabuleiro e retorna o resultado e posições vencedoras"""
        # Verificações das 3 verticais
        if self.tabuleiro['7'] == self.tabuleiro['4'] == self.tabuleiro['1'] != ' ':
            return (self.tabuleiro['7'], ['7', '4', '1'])
        elif self.tabuleiro['8'] == self.tabuleiro['5'] == self.tabuleiro['2'] != ' ':
            return (self.tabuleiro['8'], ['8', '5', '2'])
        elif self.tabuleiro['9'] == self.tabuleiro['6'] == self.tabuleiro['3'] != ' ':
            return (self.tabuleiro['9'], ['9', '6', '3'])

        # Verificações das 3 horizontais
        elif self.tabuleiro['7'] == self.tabuleiro['8'] == self.tabuleiro['9'] != ' ':
            return (self.tabuleiro['7'], ['7', '8', '9'])
        elif self.tabuleiro['4'] == self.tabuleiro['5'] == self.tabuleiro['6'] != ' ':
            return (self.tabuleiro['4'], ['4', '5', '6'])
        elif self.tabuleiro['1'] == self.tabuleiro['2'] == self.tabuleiro['3'] != ' ':
            return (self.tabuleiro['1'], ['1', '2', '3'])

        # Verificações das 2 diagonais
        elif self.tabuleiro['7'] == self.tabuleiro['5'] == self.tabuleiro['3'] != ' ':
            return (self.tabuleiro['7'], ['7', '5', '3'])
        elif self.tabuleiro['1'] == self.tabuleiro['5'] == self.tabuleiro['9'] != ' ':
            return (self.tabuleiro['1'], ['1', '5', '9'])

        # Verificando empate
        if [*self.tabuleiro.values()].count(' ') == 0:
            return ("empate", [])
        else:
            return ([*self.tabuleiro.values()].count(' '), [])

    def fazer_jogada(self, posicao):
        """Processa uma jogada do jogador - toda a lógica em Python"""
        if not self.jogo_ativo:
            return
        
        # Verifica se a jogada é válida
        if not self.verificar_jogada(posicao):
            return

        # Faz a jogada
        self.tabuleiro[posicao] = self.turno
        
        # Toca som de clique
        try:
            window.tocarSomClique()
        except:
            pass
        
        self.atualizar_tabuleiro_visual()

        # Verifica o estado do jogo
        resultado = self.verificar_tabuleiro()
        
        # Verifica se é uma tupla (vencedor) ou número (jogo em andamento)
        if isinstance(resultado, tuple):
            estado, posicoes_vencedoras = resultado
        else:
            estado = resultado
            posicoes_vencedoras = []

        if estado == "X" or estado == "O":
            # Atualiza o tabuleiro destacando a sequência vencedora
            self.atualizar_tabuleiro_visual(posicoes_vencedoras)
            
            # Cria animação de linha de vitória (lógica em Python)
            self.criar_linha_vitoria(posicoes_vencedoras)
            
            # Toca som de vitória
            try:
                window.tocarSomVitoria()
            except:
                pass
            
            self.atualizar_status(f"{estado} é o vencedor!!! 🎉", 'vencedor')
            self.habilitar_celulas(False)
            self.jogo_ativo = False
            
            # Adiciona vitória e agenda reinício automático
            try:
                window.adicionarVitoria(estado)
            except:
                pass
        elif estado == "empate":
            self.atualizar_status("EMPATE!!! 🤝", 'empate')
            self.habilitar_celulas(False)
            self.jogo_ativo = False
            
            # Em caso de empate, reinicia após 2 segundos sem adicionar vitória
            try:
                def reiniciar_empate():
                    self.reiniciar()
                # Usa setTimeout do JavaScript
                window.setTimeout(create_proxy(reiniciar_empate), 2000)
            except:
                pass
        else:
            # Troca o turno
            self.turno = "X" if self.turno == "O" else "O"
            self.atualizar_turno()

    def criar_linha_vitoria(self, posicoes):
        """
        Cria animação de linha de vitória - cálculo matemático preciso em Python
        Calcula posições usando bounding boxes reais das células para alinhamento perfeito
        """
        from js import Math  # type: ignore
        import math
        
        linha_el = document.getElementById('linha-vitoria')
        tabuleiro_el = document.getElementById('tabuleiro')
        
        if not linha_el or not posicoes or len(posicoes) != 3 or not tabuleiro_el:
            return
        
        # Remove classes anteriores e reseta estilos
        linha_el.className = 'linha-vitoria'
        linha_el.style.display = 'none'
        linha_el.style.transform = ''
        linha_el.style.transformOrigin = ''
        
        # Obtém as células vencedoras usando data-pos
        celulas = []
        for pos in posicoes:
            celula = document.querySelector(f'.celula[data-pos="{pos}"]')
            if celula:
                celulas.append(celula)
        
        if len(celulas) != 3:
            console.error("Não foi possível encontrar todas as células vencedoras")
            return
        
        # Obtém bounding boxes relativos ao tabuleiro (onde a linha está posicionada)
        tabuleiro_rect = tabuleiro_el.getBoundingClientRect()
        rects = []
        
        for celula in celulas:
            rect = celula.getBoundingClientRect()
            rects.append({
                'left': rect.left - tabuleiro_rect.left,
                'top': rect.top - tabuleiro_rect.top,
                'right': rect.right - tabuleiro_rect.left,
                'bottom': rect.bottom - tabuleiro_rect.top,
                'centerX': (rect.left + rect.right) / 2 - tabuleiro_rect.left,
                'centerY': (rect.top + rect.bottom) / 2 - tabuleiro_rect.top,
                'width': rect.width,
                'height': rect.height
            })
        
        # Ordena rects por posição (top-left para bottom-right)
        def ordenar_rects(a, b):
            if abs(a['top'] - b['top']) < 5:
                return a['left'] - b['left']
            return a['top'] - b['top']
        
        # Ordena usando JavaScript sort (mais eficiente)
        rects_sorted = sorted(rects, key=lambda r: (r['top'], r['left']))
        
        tipo = ''
        left = 0
        top = 0
        width = 0
        height = 0
        transform = ''
        transform_origin = ''
        
        # PRIMEIRO: Verifica se é diagonal pelas posições (mais confiável)
        sorted_pos = sorted([int(p) for p in posicoes])
        pos_str = ''.join([str(p) for p in sorted_pos])
        is_diagonal = pos_str == '357' or pos_str == '159'
        
        if is_diagonal:
            # Diagonal - cálculo matemático preciso
            console.log('Verificando diagonal:', {'posicoes': posicoes, 'sortedPos': sorted_pos, 'posStr': pos_str})
            
            # Calcula pontos inicial e final usando os centros das células extremas
            first_rect = rects_sorted[0]
            last_rect = rects_sorted[2]
            
            # Centros exatos das células extremas
            start_x = first_rect['centerX']
            start_y = first_rect['centerY']
            end_x = last_rect['centerX']
            end_y = last_rect['centerY']
            
            # Calcula o comprimento da linha diagonal usando teorema de Pitágoras
            dx = end_x - start_x
            dy = end_y - start_y
            length = math.sqrt(dx * dx + dy * dy)
            
            # Calcula o ângulo de rotação em radianos e converte para graus
            angle_rad = math.atan2(dy, dx)
            angle = angle_rad * 180 / math.pi
            
            tipo = 'diagonal-1' if pos_str == '357' else 'diagonal-2'
            
            # Altura da linha (espessura)
            line_height = 4
            
            # Posição inicial: centro da primeira célula
            # Ajusta para centralizar verticalmente a linha
            left = start_x
            top = start_y - (line_height / 2)
            
            # Largura da linha = comprimento da diagonal
            width = length
            height = line_height
            
            # Transform: rotaciona a linha para alinhar com a diagonal
            transform = f'rotate({angle}deg)'
            # Transform origin: ponto inicial (centro da primeira célula)
            transform_origin = 'left center'
        else:
            # DEPOIS: Verifica se é horizontal ou vertical
            # Verifica se é horizontal (mesma linha - Y similar)
            is_horizontal = (abs(rects_sorted[0]['centerY'] - rects_sorted[1]['centerY']) < 5 and 
                           abs(rects_sorted[1]['centerY'] - rects_sorted[2]['centerY']) < 5)
            
            # Verifica se é vertical (mesma coluna - X similar)
            is_vertical = (abs(rects_sorted[0]['centerX'] - rects_sorted[1]['centerX']) < 5 and 
                         abs(rects_sorted[1]['centerX'] - rects_sorted[2]['centerX']) < 5)
            
            if is_horizontal:
                tipo = 'horizontal'
                # Usa média dos centros Y para alinhamento perfeito
                center_y = (rects_sorted[0]['centerY'] + rects_sorted[1]['centerY'] + rects_sorted[2]['centerY']) / 3
                min_left = min(rects_sorted[0]['left'], rects_sorted[1]['left'], rects_sorted[2]['left'])
                max_right = max(rects_sorted[0]['right'], rects_sorted[1]['right'], rects_sorted[2]['right'])
                
                left = min_left
                top = center_y - 2  # Metade da altura da linha (4px / 2)
                width = max_right - min_left
                height = 4
            elif is_vertical:
                tipo = 'vertical'
                # Usa média dos centros X para alinhamento perfeito
                center_x = (rects_sorted[0]['centerX'] + rects_sorted[1]['centerX'] + rects_sorted[2]['centerX']) / 3
                min_top = min(rects_sorted[0]['top'], rects_sorted[1]['top'], rects_sorted[2]['top'])
                max_bottom = max(rects_sorted[0]['bottom'], rects_sorted[1]['bottom'], rects_sorted[2]['bottom'])
                
                left = center_x - 2  # Metade da largura da linha (4px / 2)
                top = min_top
                width = 4
                height = max_bottom - min_top
            else:
                console.error("Tipo de linha não reconhecido:", posicoes)
                return
        
        if tipo:
            linha_el.className = f'linha-vitoria {tipo}'
            linha_el.style.left = f'{left}px'
            linha_el.style.top = f'{top}px'
            
            # Define variáveis CSS para animação
            if tipo == 'horizontal':
                linha_el.style.setProperty('--linha-width', f'{width}px')
                linha_el.style.width = '0'
                linha_el.style.height = f'{height}px'
            elif tipo == 'vertical':
                linha_el.style.setProperty('--linha-height', f'{height}px')
                linha_el.style.width = f'{width}px'
                linha_el.style.height = '0'
            else:
                # Para diagonais, aplica transformação e configura animação
                console.log('Diagonal detectada:', {
                    'posicoes': posicoes,
                    'posStr': pos_str,
                    'angle': angle,
                    'length': length,
                    'startX': start_x,
                    'startY': start_y,
                    'endX': end_x,
                    'endY': end_y,
                    'width': width,
                    'height': height,
                    'transform': transform,
                    'transformOrigin': transform_origin
                })
                
                # Armazena o ângulo e origem como variáveis CSS (sempre, mesmo sem transform)
                linha_el.style.setProperty('--linha-angle', f'{angle}deg')
                linha_el.style.setProperty('--linha-transform-origin', transform_origin or 'left center')
                
                # Define variável para animação (comprimento da diagonal)
                linha_el.style.setProperty('--linha-width', f'{width}px')
                
                # Inicializa com width 0 e height fixo para animação crescer
                linha_el.style.width = '0'
                linha_el.style.height = f'{height}px'
                
                console.log('Linha diagonal configurada:', {
                    'angle': f'{angle}deg',
                    'width': f'{width}px',
                    'height': f'{height}px',
                    'left': f'{left}px',
                    'top': f'{top}px',
                    'transformOrigin': transform_origin or 'left center'
                })
            
            linha_el.style.display = 'block'
            
            # Força a aplicação das variáveis CSS antes da animação
            _ = linha_el.offsetHeight  # Trigger reflow
            
            # Ativa animação após pequeno delay para garantir que o CSS foi aplicado
            def ativar_animacao():
                linha_el.classList.add('ativa')
                console.log('Animação ativada para:', tipo)
            
            window.setTimeout(create_proxy(ativar_animacao), 100)
    
    def esconder_linha_vitoria(self):
        """Esconde a linha de vitória"""
        linha_el = document.getElementById('linha-vitoria')
        if linha_el:
            linha_el.classList.remove('ativa')
            linha_el.className = 'linha-vitoria'
            linha_el.style.display = 'none'

    def reiniciar(self):
        """Reinicia o jogo - toda a lógica em Python"""
        # Remove linha de vitória
        self.esconder_linha_vitoria()
        
        self.tabuleiro = {'7': ' ', '8': ' ', '9': ' ', '4': ' ', '5': ' ', '6': ' ', '1': ' ', '2': ' ', '3': ' '}
        # Sempre começa com X
        self.turno = "X"
        self.jogo_ativo = True
        self.atualizar_tabuleiro_visual([])  # Limpa todas as classes de vencedor
        self.atualizar_turno()
        self.habilitar_celulas(True)
        
        # Limpa status
        status_el = document.getElementById('status')
        status_el.textContent = ''
        status_el.className = 'status'

# ============================================
# FUNÇÕES UTILITÁRIAS E HELPERS
# ============================================

def validar_posicao(posicao):
    """
    Valida se uma posição é válida no tabuleiro
    Retorna True se válida, False caso contrário
    """
    posicoes_validas = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    return posicao in posicoes_validas

def obter_posicoes_adjacentes(posicao):
    """
    Retorna as posições adjacentes a uma posição dada
    Útil para análises futuras de estratégia
    """
    adjacentes = {
        '1': ['2', '4', '5'],
        '2': ['1', '3', '4', '5', '6'],
        '3': ['2', '5', '6'],
        '4': ['1', '2', '5', '7', '8'],
        '5': ['1', '2', '3', '4', '6', '7', '8', '9'],
        '6': ['2', '3', '5', '8', '9'],
        '7': ['4', '5', '8'],
        '8': ['4', '5', '6', '7', '9'],
        '9': ['5', '6', '8']
    }
    return adjacentes.get(posicao, [])

def calcular_centro_celula(celula):
    """
    Calcula o centro de uma célula usando getBoundingClientRect
    Retorna um dicionário com centerX e centerY
    """
    rect = celula.getBoundingClientRect()
    return {
        'centerX': (rect.left + rect.right) / 2,
        'centerY': (rect.top + rect.bottom) / 2,
        'width': rect.width,
        'height': rect.height
    }

def obter_todas_sequencias_vencedoras():
    """
    Retorna todas as sequências possíveis de vitória no jogo da velha
    Útil para análises e estratégias
    """
    return [
        # Horizontais
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        # Verticais
        ['7', '4', '1'],
        ['8', '5', '2'],
        ['9', '6', '3'],
        # Diagonais
        ['7', '5', '3'],
        ['1', '5', '9']
    ]

def verificar_sequencia_quase_completa(tabuleiro, simbolo):
    """
    Verifica se há uma sequência quase completa (2 de 3 células)
    Retorna a posição que falta para completar, ou None
    """
    sequencias = obter_todas_sequencias_vencedoras()
    for seq in sequencias:
        valores = [tabuleiro[pos] for pos in seq]
        if valores.count(simbolo) == 2 and valores.count(' ') == 1:
            # Encontrou sequência quase completa, retorna a posição vazia
            for i, pos in enumerate(seq):
                if tabuleiro[pos] == ' ':
                    return pos
    return None

def obter_estatisticas_tabuleiro(tabuleiro):
    """
    Retorna estatísticas detalhadas do tabuleiro atual
    Útil para análises, debug e estatísticas do jogo
    
    Args:
        tabuleiro (dict): Dicionário representando o tabuleiro
        
    Returns:
        dict: Dicionário com estatísticas do tabuleiro
    """
    total_celulas = 9
    celulas_vazias = list(tabuleiro.values()).count(' ')
    celulas_x = list(tabuleiro.values()).count('X')
    celulas_o = list(tabuleiro.values()).count('O')
    celulas_preenchidas = total_celulas - celulas_vazias
    
    # Calcula percentuais
    percentual_x = (celulas_x / total_celulas) * 100 if total_celulas > 0 else 0
    percentual_o = (celulas_o / total_celulas) * 100 if total_celulas > 0 else 0
    percentual_vazias = (celulas_vazias / total_celulas) * 100 if total_celulas > 0 else 0
    
    return {
        'total': total_celulas,
        'vazias': celulas_vazias,
        'x': celulas_x,
        'o': celulas_o,
        'preenchidas': celulas_preenchidas,
        'percentual_x': round(percentual_x, 2),
        'percentual_o': round(percentual_o, 2),
        'percentual_vazias': round(percentual_vazias, 2)
    }

def analisar_posicoes_criticas(tabuleiro, simbolo):
    """
    Analisa o tabuleiro e identifica posições críticas
    Uma posição crítica é aquela que, se ocupada, completa uma sequência vencedora
    
    Args:
        tabuleiro (dict): Dicionário representando o tabuleiro
        simbolo (str): Símbolo a ser analisado ('X' ou 'O')
        
    Returns:
        list: Lista de posições críticas
    """
    posicoes_criticas = []
    sequencias = obter_todas_sequencias_vencedoras()
    
    for seq in sequencias:
        valores = [tabuleiro[pos] for pos in seq]
        # Se há 2 do símbolo e 1 vazio, a posição vazia é crítica
        if valores.count(simbolo) == 2 and valores.count(' ') == 1:
            for i, pos in enumerate(seq):
                if tabuleiro[pos] == ' ':
                    if pos not in posicoes_criticas:
                        posicoes_criticas.append(pos)
    
    return posicoes_criticas

def calcular_heuristica_tabuleiro(tabuleiro, simbolo):
    """
    Calcula uma heurística simples do tabuleiro para um símbolo
    Valor mais alto indica melhor posição para o símbolo
    
    Args:
        tabuleiro (dict): Dicionário representando o tabuleiro
        simbolo (str): Símbolo a ser avaliado ('X' ou 'O')
        
    Returns:
        int: Valor heurístico do tabuleiro
    """
    pontuacao = 0
    sequencias = obter_todas_sequencias_vencedoras()
    
    for seq in sequencias:
        valores = [tabuleiro[pos] for pos in seq]
        count_simbolo = valores.count(simbolo)
        count_vazio = valores.count(' ')
        count_oponente = 3 - count_simbolo - count_vazio
        
        # Se a sequência está bloqueada pelo oponente, não pontua
        if count_oponente > 0:
            continue
        
        # Pontuação baseada em quantas células já estão ocupadas
        if count_simbolo == 3:
            pontuacao += 100  # Vitória
        elif count_simbolo == 2 and count_vazio == 1:
            pontuacao += 10  # Quase vitória
        elif count_simbolo == 1 and count_vazio == 2:
            pontuacao += 1  # Possibilidade futura
    
    return pontuacao

def obter_melhor_jogada(tabuleiro, simbolo):
    """
    Retorna a melhor jogada possível para um símbolo
    Usa heurística e análise de posições críticas
    
    Args:
        tabuleiro (dict): Dicionário representando o tabuleiro
        simbolo (str): Símbolo a ser analisado ('X' ou 'O')
        
    Returns:
        str: Posição da melhor jogada, ou None se não houver jogadas válidas
    """
    # Primeiro, verifica se pode ganhar
    posicoes_criticas_proprias = analisar_posicoes_criticas(tabuleiro, simbolo)
    if posicoes_criticas_proprias:
        return posicoes_criticas_proprias[0]
    
    # Depois, verifica se precisa bloquear o oponente
    simbolo_oponente = 'O' if simbolo == 'X' else 'X'
    posicoes_criticas_oponente = analisar_posicoes_criticas(tabuleiro, simbolo_oponente)
    if posicoes_criticas_oponente:
        return posicoes_criticas_oponente[0]
    
    # Se não há posições críticas, escolhe a melhor posição disponível
    posicoes_disponiveis = [pos for pos in tabuleiro.keys() if tabuleiro[pos] == ' ']
    if not posicoes_disponiveis:
        return None
    
    # Prioriza o centro (posição 5)
    if '5' in posicoes_disponiveis:
        return '5'
    
    # Prioriza cantos
    cantos = ['1', '3', '7', '9']
    cantos_disponiveis = [pos for pos in cantos if pos in posicoes_disponiveis]
    if cantos_disponiveis:
        return cantos_disponiveis[0]
    
    # Por último, escolhe qualquer posição disponível
    return posicoes_disponiveis[0]

def validar_integridade_tabuleiro(tabuleiro):
    """
    Valida a integridade do tabuleiro
    Verifica se o estado é válido (não há mais X que O, etc.)
    
    Args:
        tabuleiro (dict): Dicionário representando o tabuleiro
        
    Returns:
        tuple: (bool, str) - (é_válido, mensagem_erro)
    """
    valores = list(tabuleiro.values())
    count_x = valores.count('X')
    count_o = valores.count('O')
    
    # X sempre começa, então deve haver no máximo 1 X a mais que O
    diferenca = count_x - count_o
    if diferenca < 0 or diferenca > 1:
        return (False, f"Estado inválido: X={count_x}, O={count_o}")
    
    # Verifica se há caracteres inválidos
    valores_validos = ['X', 'O', ' ']
    for valor in valores:
        if valor not in valores_validos:
            return (False, f"Caractere inválido encontrado: {valor}")
    
    return (True, "Tabuleiro válido")

def formatar_mensagem_status(mensagem, tipo='info'):
    """
    Formata mensagens de status com emojis e cores apropriadas
    
    Args:
        mensagem (str): Mensagem a ser formatada
        tipo (str): Tipo da mensagem ('info', 'sucesso', 'erro', 'vencedor', 'empate', 'aviso')
        
    Returns:
        str: Mensagem formatada com emoji
    """
    emojis = {
        'info': 'ℹ️',
        'sucesso': '✅',
        'erro': '❌',
        'vencedor': '🎉',
        'empate': '🤝',
        'aviso': '⚠️'
    }
    emoji = emojis.get(tipo, '')
    return f"{emoji} {mensagem}" if emoji else mensagem

def exportar_estado_jogo(jogo):
    """
    Exporta o estado atual do jogo para um formato serializável
    Útil para salvar/carregar partidas ou debug
    
    Args:
        jogo (JogoDaVelha): Instância do jogo
        
    Returns:
        dict: Estado serializado do jogo
    """
    return {
        'tabuleiro': jogo.tabuleiro.copy(),
        'turno': jogo.turno,
        'jogo_ativo': jogo.jogo_ativo,
        'estatisticas': obter_estatisticas_tabuleiro(jogo.tabuleiro)
    }

def importar_estado_jogo(jogo, estado):
    """
    Importa um estado do jogo de um formato serializável
    Útil para restaurar partidas salvas
    
    Args:
        jogo (JogoDaVelha): Instância do jogo
        estado (dict): Estado serializado do jogo
        
    Returns:
        bool: True se importação foi bem-sucedida, False caso contrário
    """
    try:
        # Valida integridade do estado
        is_valid, msg = validar_integridade_tabuleiro(estado['tabuleiro'])
        if not is_valid:
            console.error(f"Estado inválido: {msg}")
            return False
        
        # Restaura o estado
        jogo.tabuleiro = estado['tabuleiro'].copy()
        jogo.turno = estado['turno']
        jogo.jogo_ativo = estado['jogo_ativo']
        
        # Atualiza a interface
        jogo.atualizar_tabuleiro_visual()
        jogo.atualizar_turno()
        
        return True
    except Exception as e:
        console.error(f"Erro ao importar estado: {e}")
        return False

# ============================================
# INICIALIZAÇÃO DO JOGO
# ============================================

def inicializar_jogo():
    """
    Função principal para inicializar o jogo - escrita em Python
    Configura todos os componentes e valida o ambiente
    """
    try:
        # Valida se os elementos necessários existem no DOM
        tabuleiro_el = document.getElementById('tabuleiro')
        if not tabuleiro_el:
            raise Exception("Elemento tabuleiro não encontrado no DOM")
        
        status_el = document.getElementById('status')
        if not status_el:
            raise Exception("Elemento status não encontrado no DOM")
        
        # Verifica se há dados de jogadores
        try:
            jogador1_data = window.jogador1Data
            jogador2_data = window.jogador2Data
            if not jogador1_data or not jogador2_data:
                console.warn("⚠️ Dados de jogadores não encontrados")
        except:
            console.warn("⚠️ Dados de jogadores não disponíveis")
        
        # Inicializa o jogo
        global jogo
        jogo = JogoDaVelha()
        
        # Log de sucesso com estatísticas
        console.log("✅ Jogo da Velha inicializado com Python!")
        console.log("📊 Estatísticas iniciais:", obter_estatisticas_tabuleiro(jogo.tabuleiro))
        console.log("🎮 Sequências vencedoras possíveis:", len(obter_todas_sequencias_vencedoras()))
        
    except Exception as e:
        error_msg = f"Erro ao inicializar jogo: {str(e)}"
        console.error(f"❌ {error_msg}")
        
        status_el = document.getElementById('status')
        if status_el:
            status_el.textContent = error_msg
            status_el.style.background = '#f8d7da'
            status_el.style.color = '#721c24'
            status_el.style.padding = '20px'
            status_el.style.borderRadius = '10px'

# Executa a inicialização quando o módulo é carregado
inicializar_jogo()
