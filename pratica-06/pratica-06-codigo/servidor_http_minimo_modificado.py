import socket

HOST = "0.0.0.0"
PORTA = 5050

def gerar_resposta(caminho):
    if caminho == "/":
        corpo = """<!DOCTYPE html>
        <html lang="pt-br">
        <head><meta charset="utf-8"><title>Servidor Python</title></head>
        <body>
        <h1>Servidor HTTP minimo com sockets</h1>
        <p>Turma: 5º período - Sistemas de Informação</p>
        <p>Integrantes: Henrique Leão & Rhuan Victor</p>
        </body>
        </html>"""
        status = "200 OK"
    elif caminho == "/sobre":
        corpo = "<h1>Sobre</h1><p>Pratica 6 - Redes de Computadores</p>"
        status = "200 OK"
    elif caminho == "/status":
        corpo = "<h1>Status: servidor ativo</h1>"
        status = "200 OK"
    else:
        corpo = "<h1>404 Pagina nao encontrada</h1>"
        status = "404 Not Found"

    resposta = (
        f"HTTP/1.1 {status}\r\n"
        "Server: ServidorSockets Python/1.0\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(corpo.encode('utf-8'))}\r\n"
        "Connection: close\r\n"
        "\r\n"
        f"{corpo}"
    )
    return resposta

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen(5)
    print(f"Acesse no navegador: http://127.0.0.1:{PORTA}")

    while True:
        conexao, endereco = servidor.accept()
        with conexao:
            requisicao = conexao.recv(2048).decode("utf-8", errors="replace")
            if not requisicao:
                continue

            print("=" * 60)
            print(f"Requisição de {endereco}:")
            print(requisicao)

            linhas = requisicao.splitlines()
            if linhas:
                linha_inicial = linhas[0]
                partes = linha_inicial.split()
                if len(partes) >= 2:
                    caminho = partes[1]
                    resposta = gerar_resposta(caminho)
                    conexao.sendall(resposta.encode("utf-8"))