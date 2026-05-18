import socket

HOST = "10.90.36.48"
PORTA = 5001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORTA))
    print("Conectado ao servidor. Comandos: PING, HORA, MAIUSCULA texto, TAMANHO texto, SAIR")

    while True:
        comando = input("> ")
        cliente.sendall(comando.encode("utf-8"))
        resposta = cliente.recv(1024).decode("utf-8").strip()
        print("Servidor:", resposta)
        if comando.strip() == "SAIR":
            break