#!/usr/bin/env python3
import socket
import threading
import Python_sml_ClientInterface as sml

HOST = "0.0.0.0"
PORT = 12122

kernel = sml.Kernel.CreateKernelInCurrentThread(True)
agent = kernel.CreateAgent("ServerAgent")
connections = []

print(f"SML Server running on {HOST}:{PORT}")

def send_to_clients(text):
    for conn in connections:
        try:
            conn.sendall((text + "\n").encode())
        except:
            pass

def handle_client(conn, addr):
    print(f"[+] Conexão de {addr}")
    connections.append(conn)
    buffer = ""
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            buffer += data.decode()
            
            # Regra: só executa se houver um terminador especial, ex: ';;' no final do comando
            while ';;' in buffer:
                command, buffer = buffer.split(';;', 1)  # pega tudo até o terminador
                command = command.strip()
                if not command:
                    continue
                try:
                    if "run" in command:
                        agent.ExecuteCommandLine("output log result.txt")
                    output = agent.ExecuteCommandLine(command, True)
                    send_to_clients(output.strip())
                    if "run" in command:
                        with open("result.txt") as result:
                            send_to_clients(f"Execution: {"\n".join(result.readlines())}")

                        agent.ExecuteCommandLine("output log --close")
                except Exception as e:
                    send_to_clients(f"ERROR: {e}")
    except ConnectionResetError:
        print(f"[-] Cliente {addr} desconectou")
    finally:
        connections.remove(conn)
        conn.close()
        print(f"[-] Conexão com {addr} fechada")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
