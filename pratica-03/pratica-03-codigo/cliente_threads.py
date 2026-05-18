
import socket

HOST = input("IP do servidor [127.0.0.1]: ").strip() or "127.0.0.1"
PORTA = 5002

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORTA))
    print("Conectado. Digite mensagens ou SAIR.")
    while True:
        msg = input("> ")
        cliente.sendall((msg + "\n").encode("utf-8"))
        resposta = cliente.recv(1024).decode("utf-8").strip()
        print(resposta)
        if msg.upper() == "SAIR":
            break