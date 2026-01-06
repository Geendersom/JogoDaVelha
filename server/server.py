#!/usr/bin/env python3
"""
Criado por Geêndersom Araújo

Servidor HTTP simples para executar o jogo da velha no navegador.
Execute este arquivo e acesse http://localhost:8000 no navegador.
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Muda o diretório de trabalho para a raiz do projeto
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.chdir(project_root)
        super().__init__(*args, **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    # Garante que estamos na raiz do projeto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🚀 Servidor iniciado em http://localhost:{PORT}")
        print(f"📂 Servindo arquivos de: {os.getcwd()}")
        print(f"🌐 Abrindo navegador automaticamente...")
        print(f"📄 Acesse: http://localhost:{PORT}/web/selecao.html")
        print(f"⏹️  Pressione Ctrl+C para parar o servidor\n")
        
        # Abrir navegador automaticamente na tela de seleção
        webbrowser.open(f'http://localhost:{PORT}/web/selecao.html')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Servidor encerrado.")

if __name__ == "__main__":
    main()
