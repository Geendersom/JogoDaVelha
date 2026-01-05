# Jogo da velha
# Desenvolvido por Geêndersom Araújo
# Linguagem principal: Python

from js import document, console
from pyodide.ffi import create_proxy

class JogoDaVelha:
    def __init__(self, jogador_inicial="X"):
        self.tabuleiro = {'7': ' ', '8': ' ', '9': ' ', '4': ' ', '5': ' ', '6': ' ', '1': ' ', '2': ' ', '3': ' '}
        self.turno = jogador_inicial
        self.jogo_ativo = True
        self._configurar_interface()

    def _configurar_interface(self):
        """Configura a interface do jogo manipulando o DOM diretamente do Python"""
        # Atualiza o tabuleiro visual
        self.atualizar_tabuleiro_visual()
        
        # Atualiza o status inicial
        self.atualizar_status(f"Turno do {self.turno}")
        
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
        
        # Configura o botão de reiniciar
        btn_reiniciar = document.getElementById('reiniciar')
        def callback_reiniciar(event):
            self.reiniciar()
        btn_reiniciar.addEventListener('click', create_proxy(callback_reiniciar))

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
            self.atualizar_status(f"{estado} é o vencedor!!! 🎉", 'vencedor')
            self.habilitar_celulas(False)
            self.jogo_ativo = False
        elif estado == "empate":
            self.atualizar_status("EMPATE!!! 🤝", 'empate')
            self.habilitar_celulas(False)
            self.jogo_ativo = False
        else:
            # Troca o turno
            self.turno = "X" if self.turno == "O" else "O"
            self.atualizar_status(f"Turno do {self.turno}")

    def reiniciar(self):
        """Reinicia o jogo - toda a lógica em Python"""
        self.tabuleiro = {'7': ' ', '8': ' ', '9': ' ', '4': ' ', '5': ' ', '6': ' ', '1': ' ', '2': ' ', '3': ' '}
        self.turno = "X"
        self.jogo_ativo = True
        self.atualizar_tabuleiro_visual([])  # Limpa todas as classes de vencedor
        self.atualizar_status(f"Turno do {self.turno}")
        self.habilitar_celulas(True)

# Inicializa o jogo quando o código Python é carregado
def inicializar_jogo():
    """Função principal para inicializar o jogo - escrita em Python"""
    try:
        global jogo
        jogo = JogoDaVelha()
        console.log("✅ Jogo da Velha inicializado com Python!")
    except Exception as e:
        console.error(f"❌ Erro ao inicializar jogo: {e}")
        status_el = document.getElementById('status')
        if status_el:
            status_el.textContent = f"Erro ao inicializar: {str(e)}"
            status_el.style.background = '#f8d7da'
            status_el.style.color = '#721c24'

# Executa a inicialização
inicializar_jogo()
