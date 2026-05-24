import socket
import threading

HOST = "0.0.0.0"
PORTA = 5002

def atender_cliente(conexao, endereco):
    print(f"[{endereco}] conectado")
    with conexao:
        while True:
            dados = conexao.recv(1024)
            if not dados:
                break

            mensagem = dados.decode("utf-8").strip()
            print(f"[{endereco}] {mensagem}")

            if mensagem.upper() == "CLIENTES":
                qtd_clientes = threading.active_count() - 1
                resposta = f"Clientes ativos no momento: {qtd_clientes}\n"
            else:
                resposta = f"Servidor recebeu: {mensagem}\n"

            conexao.sendall(resposta.encode("utf-8"))

            if mensagem.upper() == "SAIR":
                break

    print(f"[{endereco}] desconectado")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen(5)
    print(f"Servidor concorrente escutando em {HOST}:{PORTA}")

    while True:
        conexao, endereco = servidor.accept()
        thread = threading.Thread(target=atender_cliente, args=(conexao, endereco))
        thread.daemon = True
        thread.start()
        print(f"Clientes ativos aproximadamente: {threading.active_count() - 1}")