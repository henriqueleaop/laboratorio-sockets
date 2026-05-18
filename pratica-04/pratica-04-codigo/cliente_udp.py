import socket

HOST = input("IP do servidor [127.0.0.1]: ").strip() or "127.0.0.1"
PORTA = 5003

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
    cliente.settimeout(3.0)
    while True:
        mensagem = input("Mensagem UDP ou SAIR: ")
        if mensagem.upper() == "SAIR":
            break
        cliente.sendto(mensagem.encode("utf-8"), (HOST, PORTA))
        try:
            dados, endereco = cliente.recvfrom(1024)
            print(f"Resposta de {endereco}: {dados.decode('utf-8')}")
        except socket.timeout:
        print("Tempo esgotado: nenhuma resposta recebida.")