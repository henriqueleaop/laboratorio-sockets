import socket
import threading

HOST = input("IP do servidor [127.0.0.1]: ").strip() or "127.0.0.1"
PORTA = 5004

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORTA))

def receber():
    while True:
        try:
            dados = cliente.recv(1024)
            if not dados:
                print("\nConexão encerrada pelo servidor.")
                break
            print(dados.decode("utf-8"), end="")
        except OSError:
            break

# Inicia a thread para receber mensagens do servidor em segundo plano
threading.Thread(target=receber, daemon=True).start()

try:
    while True:
        texto = input()
        cliente.sendall((texto + "\n").encode("utf-8"))
        if texto.upper() == "/SAIR":
            break
finally:
    cliente.close()