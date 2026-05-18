import socket

HOST = input("IP do servidor [127.0.0.1]: ").strip() or "127.0.0.1"
PORTA = 5003
TENTATIVAS = 3

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
    cliente.settimeout(2.0)
    mensagem = input("Mensagem: ")
    for tentativa in range(1, TENTATIVAS + 1):
        print(f"Tentativa {tentativa} de {TENTATIVAS}")
        cliente.sendto(mensagem.encode("utf-8"), (HOST, PORTA))
        try:
            dados, endereco = cliente.recvfrom(1024)
            print("Resposta:", dados.decode("utf-8"))
            break
        except socket.timeout:
            print("Sem resposta nesta tentativa.")
        else:
            print("Falha: servidor não respondeu após as tentativas.")