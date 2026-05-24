import socket
import random
from datetime import datetime

HOST = "0.0.0.0"
PORTA = 5003

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor:
    servidor.bind((HOST, PORTA))
    print("Simulação de Perda Ativa")
    print(f"Servidor UDP escutando em {HOST}:{PORTA} ")

    while True:
        dados, endereco = servidor.recvfrom(1024)
        mensagem = dados.decode("utf-8").strip()
        print(f"Datagrama recebido de {endereco}: {mensagem}")

        # Simula 30% de perda de pacote para testar timeout/retransmissão no cliente
        if random.random() < 0.3:
            print("-> Pacote ignorado propositalmente (simulação de perda).")
            continue

        # Lógica de processamento
        if "HORA" in mensagem:
            resposta = datetime.now().strftime("%H:%M:%S")
            servidor.sendto(resposta.encode("utf-8"), endereco)
        elif "CONFIRMA" in mensagem:
            resposta = f"ACK: {mensagem}"
            servidor.sendto(resposta.encode("utf-8"), endereco)
        else:
            # Não envia nada se não exigir confirmação ou hora
            print("-> Nenhuma resposta exigida pelo protocolo da aplicação.")