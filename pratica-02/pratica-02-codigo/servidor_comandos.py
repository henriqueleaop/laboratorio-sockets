import socket
from datetime import datetime

HOST = "0.0.0.0"
PORTA = 5001

def processar_comando(linha: str) -> str:
    linha = linha.strip()
    if linha == "PING":
        return "PONG"
    
    if linha == "HORA":
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if linha.startswith("MAIUSCULA "):
        texto = linha[len("MAIUSCULA "):]
        return texto.upper()
    
    if linha.startswith("MINUSCULA "):
        texto = linha[len("MINUSCULA "):]
        return texto.lower()
    
    if linha.startswith("TAMANHO "):
        texto = linha[len("TAMANHO "):]
        return str(len(texto))
    
    if linha.startswith("REVERSO "):
        texto = linha[len("REVERSO "):]
        return texto[::-1]

    if linha.startswith("SOMA "):
        termos = linha.split(" ")  

        if len(termos) != 3 or not str(termos[1]).isnumeric() or not str(termos[2]).isnumeric() : 
            return "Comando inválido" 
        
        a = int(termos[1])
        b = int(termos[2])
        return str(a + b)

    if linha == "SAIR":
        return "Encerrando conexão."
    return "ERRO: comando desconhecido"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen(1)
    print(f"Servidor de comandos em {HOST}:{PORTA}")

    conexao, endereco = servidor.accept()
    with conexao:
        print(f"Cliente conectado: {endereco}")
        while True:
            dados = conexao.recv(1024)
            if not dados:
                print("Cliente encerrou a conexão.")
                break
            comando = dados.decode("utf-8")
            print("Comando recebido:", comando.strip())
            resposta = processar_comando(comando)
            conexao.sendall((resposta + "\n").encode("utf-8"))
            if comando.strip() == "SAIR":
                break