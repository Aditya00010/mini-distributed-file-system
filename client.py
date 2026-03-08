import socket
import json

MASTER_PORT = 8000

def send_request(command):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect(("localhost", MASTER_PORT))

        s.sendall(command.encode())

        response = s.recv(4096).decode()

    return response

def read_file(filename):

    response = send_request(f"READ {filename}")

    chunk_map = json.loads(response)

    final_data = []

    for chunk, servers in chunk_map.items():

        for port in servers:

            try:

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

                    s.connect(("localhost", port))

                    s.sendall(f"READ {chunk}".encode())

                    data = s.recv(4096).decode()

                    final_data.append(data)

                    break

            except:
                continue

    print("".join(final_data))

def client():

    while True:

        cmd = input("Enter command: ")

        if cmd.startswith("READ"):

            filename = cmd.split()[1]

            read_file(filename)

        else:

            response = send_request(cmd)

            print(response)

if __name__ == "__main__":
    client()