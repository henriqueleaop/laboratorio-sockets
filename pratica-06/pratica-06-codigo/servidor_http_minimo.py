import socket

HOST = "0.0.0.0"
PORTA = 5050

html = """<!DOCTYPE html> 
<html lang="pt-br"> 
<head><meta charset="utf-8"><title>Servidor Python</title></head> 
<body> 
  <h1>Servidor HTTP mínimo com sockets</h1> 
  <p>Esta página foi enviada por um programa Python usando sockets TCP.</p> 
</body> 
</html> 
"""

resposta = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(html.encode('utf-8'))}\r\n"
        "Connection: close\r\n"
        "\r\n"
        + html
)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen(5)
    print(f"Acesse no navegador: http://127.0.0.1:{PORTA}")

    while True:
        conexao, endereco = servidor.accept()
        with conexao:
            requisicao = conexao.recv(2048).decode("utf-8", errors="replace")
            print("=" * 60)
            print(f"Requisição de {endereco}:")
            print(requisicao)
            conexao.sendall(resposta.encode("utf-8"))