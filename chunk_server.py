import os
import socket
import sys

CHUNK_STORAGE_DIR = "chunk_storage"

def setup_storage(port):

    server_dir = f"chunk_server_{port}"

    path = os.path.join(CHUNK_STORAGE_DIR, server_dir)

    if not os.path.exists(CHUNK_STORAGE_DIR):
        os.mkdir(CHUNK_STORAGE_DIR)

    if not os.path.exists(path):
        os.mkdir(path)

    return path

def chunk_server(port):

    storage_path = setup_storage(port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.bind(("localhost", port))
        s.listen(5)

        print(f"Chunk server running on port {port}")

        while True:

            conn, addr = s.accept()

            with conn:

                data = conn.recv(4096).decode()

                command, *args = data.split(" ", 1)

                if command == "WRITE":

                    chunk_id, chunk_data = args[0].split(" ", 1)

                    file_path = os.path.join(storage_path, chunk_id)

                    with open(file_path, "w") as f:
                        f.write(chunk_data)

                    conn.sendall("ACK".encode())

                elif command == "READ":

                    chunk_id = args[0]

                    file_path = os.path.join(storage_path, chunk_id)

                    if os.path.exists(file_path):

                        with open(file_path, "r") as f:
                            data = f.read()

                        conn.sendall(data.encode())

                    else:
                        conn.sendall("Chunk not found".encode())

                else:
                    conn.sendall("Unknown command".encode())

if __name__ == "__main__":

    port = int(sys.argv[1])

    chunk_server(port)