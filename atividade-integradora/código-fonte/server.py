import socket
import threading

HOST = '0.0.0.0'
PORT = 5555

# Banco de dados em memória
DICIONARIO = {
    "socket": "Ponto final de uma conexao de rede bidirecional.",
    "protocolo": "Conjunto de regras que governa a comunicacao entre computadores.",
    "tcp": "Protocolo de Controle de Transmissao, orientado a conexao e confiavel.",
    "hardware": "Parte fisica do computador.",
    "foco": "Capacidade de manter a atencao concentrada em um objetivo."
}


def handle_client(conn, addr):
    print(f"[+] Nova conexão de {addr}")
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break

                mensagem = data.decode('utf-8').strip()
                partes = mensagem.split(' ', 1)
                comando = partes[0].upper()

                if comando == 'SEARCH' and len(partes) > 1:
                    termo = partes[1].lower()
                    definicao = DICIONARIO.get(termo)
                    if definicao:
                        resposta = f"FOUND {definicao}\n"
                    else:
                        resposta = "NOTFOUND\n"

                elif comando == 'LIST':
                    termos = ", ".join(DICIONARIO.keys())
                    resposta = f"LISTING {termos}\n"

                elif comando == 'QUIT':
                    conn.sendall("BYE\n".encode('utf-8'))
                    print(f"[-] Conexão encerrada ativamente por {addr}")
                    break

                else:
                    resposta = "ERROR Invalid Command\n"

                conn.sendall(resposta.encode('utf-8'))

            except ConnectionResetError:
                break
            except Exception as e:
                print(f"[!] Erro com {addr}: {e}")
                break

    print(f"[-] Cliente {addr} desconectado.")


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"[*] Servidor DICTP/1.0 escutando em {HOST}:{PORT}")

        try:
            while True:
                conn, addr = server_socket.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.start()
                print(f"[*] Conexões ativas: {threading.active_count() - 1}")
        except KeyboardInterrupt:
            print("\n[*] Servidor encerrado.")


if __name__ == '__main__':
    start_server()
