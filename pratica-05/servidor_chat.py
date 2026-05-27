import socket
import threading

HOST = "0.0.0.0"
PORTA = 5004

clientes = []
lock = threading.Lock()

def enviar_para_todos(mensagem, remetente=None):
    # Envia uma mensagem para todos os usuários conectados
    with lock:
        for cliente in clientes:
            if cliente != remetente:
                try:
                    cliente.sendall(mensagem.encode("utf-8"))
                except OSError:
                    pass

def atender_cliente(conexao, endereco):
    try:
        # Mensagem de boas-vindas com instruções
        boas_vindas = (
            "\n=========================================\n"
            "   Bem-vindo ao Servidor de Chat!\n"
            "   Comando disponivel:\n"
            "   /SAIR - Sai do chat\n"
            "=========================================\n\n"
            "Digite seu nome: "
        )
        conexao.sendall(boas_vindas.encode("utf-8"))

        nome = conexao.recv(1024).decode("utf-8").strip()
        if not nome:
            nome = f"cliente-{endereco[1]}"

        entrada = f"[SERVIDOR] {nome} entrou no chat.\n"
        print(entrada.strip())
        enviar_para_todos(entrada, remetente=conexao)

        while True:
            dados = conexao.recv(1024)
            if not dados:
                break

            texto = dados.decode("utf-8").strip()
            if not texto:
                continue

            if texto.upper() == "/SAIR":
                break

            # Mensagem normal para todos
            mensagem = f"[{nome}] {texto}\n"
            print(mensagem.strip())
            enviar_para_todos(mensagem, remetente=conexao)

    finally:
        with lock:
            if conexao in clientes:
                clientes.remove(conexao)
        conexao.close()
        saida = f"[SERVIDOR] {nome} saiu do chat.\n"
        print(saida.strip())
        enviar_para_todos(saida)

# Inicialização do Servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen(10)
    print(f"Servidor de chat rodando em {HOST}:{PORTA}")

    while True:
        conexao, endereco = servidor.accept()
        with lock:
            clientes.append(conexao)
        threading.Thread(target=atender_cliente, args=(conexao, endereco), daemon=True).start()