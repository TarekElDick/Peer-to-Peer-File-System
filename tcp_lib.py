import socket
import sys
import threading


def run_server(host, port):
    try:

        self.TCP_sock.listen(5)
        print('Echo server is listening at', port)
        while True:
            conn, addr = self.TCP_sock.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
            # Demon
    finally:
        self.TCP_sock.close()


def handle_client(conn, addr):
    print('New client from', addr)
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
    finally:
        conn.close()


def tcp_client(host, port):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((host, port))
        print("Type any thing then ENTER. Press Ctrl+C to terminate")
        while True:
            line = sys.stdin.readline(1024)
            request = line.encode("utf-8")
            conn.sendall(request)
            # MSG_WAITALL waits for full request or error
            response = conn.recv(len(request), socket.MSG_WAITALL)
            sys.stdout.write("Replied: " + response.decode("utf-8"))
    finally:
        conn.close()

