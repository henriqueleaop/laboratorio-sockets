import socket
import time

HOST = input("IP do servidor [127.0.0.1]: ").strip() or "127.0.0.1"
PORTA = 5003

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
    cliente.settimeout(2.0)

    contador_msg = 1
    while True:
        texto = input("Mensagem UDP ou SAIR: ")
        if texto.upper() == "SAIR":
            break

        # Adiciona numeração estruturada
        mensagem = f"MSG {contador_msg} | {texto}"
        contador_msg += 1

        t_inicio = time.time()
        cliente.sendto(mensagem.encode("utf-8"), (HOST, PORTA))

        try:
            dados, endereco = cliente.recvfrom(1024)
            t_fim = time.time()

            # Cálculo de RTT (Round-Trip Time)
            rtt_ms = (t_fim - t_inicio) * 1000
            print(f"Resposta de {endereco}: {dados.decode('utf-8')} [RTT: {rtt_ms} ms]")

        except socket.timeout:
            print("Tempo esgotado: pacote perdido, descartado pelo servidor ou confirmação não exigida.")