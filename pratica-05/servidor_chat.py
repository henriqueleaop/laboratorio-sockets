import socket
import threading
import datetime

HOST = "0.0.0.0"
PORTA = 5004

clientes = []
lock = threading.Lock()
ARQUIVO_LOG = "historico_chat.txt"

def salvar_no_log(texto):
    # Salva as mensagens no arquivo de log com data e hora
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {texto}\n")

def enviar_para_todos(mensagem, remetente_conexao=None):
    # Envia uma mensagem para todos os usuários conectados
    salvar_no_log(mensagem.strip())
    with lock:
        for c in clientes:
            if c["conexao"] != remetente_conexao:
                try:
                    c["conexao"].sendall(mensagem.encode("utf-8"))
                except OSError:
                    pass

def enviar_mensagem_privada(mensagem, nome_destino, remetente_c):
    # Envia uma mensagem privada para um usuário específico
    enviado = False
    with lock:
        for c in clientes:
            if c["nome"].lower() == nome_destino.lower():
                try:
                    c["conexao"].sendall(mensagem.encode("utf-8"))
                    enviado = True
                except OSError:
                    pass
                break
    
    if enviado:
        # Envia uma confirmação visual para quem mandou a PM
        remetente_c.sendall(mensagem.encode("utf-8"))
        salvar_no_log(f"[PRIVADO] {mensagem.strip()}")
    else:
        remetente_c.sendall("[SERVIDOR] Usuário não encontrado.\n".encode("utf-8"))

def obter_lista_usuarios():
    # Retorna uma string com todos os usuários online
    with lock:
        nomes = [c["nome"] for c in clientes]
    return "[SERVIDOR] Usuários online: " + ", ".join(nomes) + "\n"

def nome_ja_existe(nome):
    # Verifica se o nome já está sendo usado por outro cliente
    with lock:
        return any(c["nome"].lower() == nome.lower() for c in clientes)

def atender_cliente(conexao, endereco):
    nome = f"cliente-{endereco[1]}"
    try:
        # [Variação 5] Mensagem de boas-vindas com instruções
        boas_vindas = (
            "\n=========================================\n"
            "   Bem-vindo ao Servidor de Chat!\n"
            "   Comandos disponíveis:\n"
            "   /LISTAR               - Lista usuários online\n"
            "   /MSG <nome> <msg>     - Mensagem privada\n"
            "   /SAIR                 - Sai do chat\n"
            "=========================================\n\n"
            "Digite seu nome: "
        )
        conexao.sendall(boas_vindas.encode("utf-8"))
        
        # [Variação 4] Impedir nomes duplicados
        while True:
            nome_usuario = conexao.recv(1024).decode("utf-8").strip()
            if not nome_usuario:
                nome_usuario = f"cliente-{endereco[1]}"
            
            # Garante que o nome não use comandos ou espaços extras
            if " " in nome_usuario or nome_usuario.startswith("/"):
                conexao.sendall("[SERVIDOR] Nome inválido. Não use espaços ou /. Tente outro: ".encode("utf-8"))
                continue

            if nome_ja_existe(nome_usuario):
                conexao.sendall("[SERVIDOR] Este nome já está em uso. Tente outro: ".encode("utf-8"))
            else:
                nome = nome_usuario
                break

        # Atualiza o nome correto na lista global
        with lock:
            for c in clientes:
                if c["conexao"] == conexao:
                    c["nome"] = nome
                    break

        entrada = f"[SERVIDOR] {nome} entrou no chat.\n"
        print(entrada.strip())
        enviar_para_todos(entrada, remetente_conexao=conexao)
        
        while True:
            dados = conexao.recv(1024)
            if not dados:
                break
            texto = dados.decode("utf-8").strip()
            if not texto:
                continue

            # Processamento de Comandos
            if texto.upper() == "/SAIR":
                break
            
            # [Variação 1] Comando /LISTAR
            elif texto.upper() == "/LISTAR":
                conexao.sendall(obter_lista_usuarios().encode("utf-8"))
            
            # [Variação 2] Mensagem Privada /MSG usuario mensagem
            elif texto.upper().startswith("/MSG "):
                partes = texto.split(" ", 2)
                if len(partes) >= 3:
                    nome_destino = partes[1]
                    msg_privada = partes[2]
                    formatada = f"[{nome} -> {nome_destino}]: {msg_privada}\n"
                    enviar_mensagem_privada(formatada, nome_destino, conexao)
                else:
                    conexao.sendall("[SERVIDOR] Uso correto: /MSG <usuario> <mensagem>\n".encode("utf-8"))
            
            # Mensagem normal para todos
            else:
                mensagem = f"[{nome}] {texto}\n"
                print(mensagem.strip())
                enviar_para_todos(mensagem, remetente_conexao=conexao)
            
    finally:
        with lock:
            # Remove o dicionário do cliente da lista
            for c in clientes:
                if c["conexao"] == conexao:
                    clientes.remove(c)
                    break
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
            # Inicializa na lista com o IP/Porta temporário até ele escolher o nome
            clientes.append({"conexao": conexao, "nome": f"cliente-{endereco[1]}"})
        threading.Thread(target=atender_cliente, args=(conexao, endereco), daemon=True).start()