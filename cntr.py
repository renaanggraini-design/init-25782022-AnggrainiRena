import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

task = input("Masukkan perintah otomatisasi (Format:PORT: TASK:CMD): ")

task_bytes = task.encode()
print(f"[SENDING] Mengirim task byte: {task_bytes}")

client_socket.connect(("127.0.0.1", 9999))
client_socket.send(task_bytes)

client_socket.close()