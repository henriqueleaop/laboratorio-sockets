import socket
import sys

PORT = 5555


def start_client(server_ip):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.settimeout(10.0)  # Timeout para evitar travamento
            client_socket.connect((server_ip, PORT))
            print(f"[*] Conectado ao servidor {server_ip}:{PORT}")
            print("Comandos disponíveis: SEARCH <termo>, LIST, QUIT")

            while True:
                comando = input("DICTP> ").strip()
                if not comando:
                    continue

                # Adiciona o \n exigido pelo protocolo
                mensagem = comando + "\n"
                client_socket.sendall(mensagem.encode('utf-8'))

                resposta = client_socket.recv(1024).decode('utf-8').strip()
                print(f"Servidor: {resposta}")

                if resposta == "BYE":
                    break

        except ConnectionRefusedError:
            print("[!] Erro: Conexão recusada. O servidor está rodando?")
        except socket.timeout:
            print("[!] Erro: Tempo de conexão esgotado.")
        except Exception as e:
            print(f"[!] Erro inesperado: {e}")


if __name__ == '__main__':
    ip = input("Digite o IP do servidor (ex: 192.168.1.10 ou 127.0.0.1): ").strip()
    start_client(ip)
