import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(("127.0.0.1", 9999))
server_socket.listen(5)

print("[*] Agent Multithread aktif di port 9999...")

clients = []
results = []

lock = threading.Lock()
done_lock = threading.Lock()

done_count = 0


def handle_client(client_socket, client_addr, thread_name):
    global done_count

    try:
        data = client_socket.recv(1024)
        decoded = data.decode()

        port, task, command = decoded.split(":")

        with lock:
            results.append(f"[!] [{thread_name}] PORT:{port} | {task} | {command}")

    except:
        with lock:
            results.append(f"[!] [{thread_name}] ERROR")

    finally:
        client_socket.close()

    with done_lock:
        done_count += 1


while True:
    client_socket, client_addr = server_socket.accept()

    thread_id = len(clients) + 1
    thread_name = f"Thread-{thread_id}"

    print(f"[+] [{thread_name}] Menangani Controller-{chr(64+thread_id)} {client_addr}")

    clients.append(client_socket)

    t = threading.Thread(
        target=handle_client,
        args=(client_socket, client_addr, thread_name)
    )

    t.start()

    # tunggu 2 controller
    if len(clients) == 2:

        while True:
            with done_lock:
                if done_count == 2:
                    break

        # output batch
        for r in results:
            print(r)

        # 🔥 INI SEKARANG BISA BERULANG
        print("[-] [Thread-1] Selesai melayani SN-001. Koneksi ditutup.\n")

        clients.clear()
        results.clear()
        done_count = 0