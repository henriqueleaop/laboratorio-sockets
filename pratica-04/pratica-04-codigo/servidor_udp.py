import socket
from datetime import datetime
HOST = "0.0.0.0"
PORTA = 5003

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor:
    servidor.bind((HOST, PORTA))
    print(f"Servidor UDP escutando em {HOST}:{PORTA}")
    while True:
        dados, endereco = servidor.recvfrom(2048)
        mensagem = dados.decode("utf-8").strip()
        print(f"Datagrama de {endereco}: {mensagem}")
        if mensagem == "HORA":
            resposta = datetime.now().strftime("%H:%M:%S")
        else:
            resposta = f"ACK: {mensagem}"
        servidor.sendto(resposta.encode("utf-8"), endereco)