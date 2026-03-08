import json
import os
import socket

CHUNK_SIZE = 64
NUM_CHUNK_SERVERS = 5
METADATA_FILE = "metadata.json"
CHUNK_SERVER_PORTS = [8001, 8002, 8003, 8004, 8005]

if not os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, "w") as f:
        json.dump({}, f)

def load_metadata():
    with open(METADATA_FILE, "r") as f:
        return json.load(f)

def save_metadata(metadata):
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=4)

def handle_create_file(filename):
    metadata = load_metadata()

    if filename in metadata:
        return "File already exists."

    metadata[filename] = {"total_chunks": 0}
    save_metadata(metadata)

    return f"File {filename} created."

def handle_write_file(filename, content, append=False):
    metadata = load_metadata()

    if filename not in metadata:
        return "File does not exist."

    existing_chunks = metadata[filename]
    total_chunks = existing_chunks["total_chunks"]

    chunks = [content[i:i+CHUNK_SIZE] for i in range(0, len(content), CHUNK_SIZE)]

    for i, chunk in enumerate(chunks):

        chunk_id = f"chunk{total_chunks}_{filename}"

        primary_server = CHUNK_SERVER_PORTS[total_chunks % NUM_CHUNK_SERVERS]
        replicas = [
            CHUNK_SERVER_PORTS[(total_chunks + 1) % NUM_CHUNK_SERVERS],
            CHUNK_SERVER_PORTS[(total_chunks + 2) % NUM_CHUNK_SERVERS],
            CHUNK_SERVER_PORTS[(total_chunks + 3) % NUM_CHUNK_SERVERS]
        ]

        existing_chunks[chunk_id] = primary_server
        existing_chunks[f"{chunk_id}_replica1"] = replicas[0]
        existing_chunks[f"{chunk_id}_replica2"] = replicas[1]
        existing_chunks[f"{chunk_id}_replica3"] = replicas[2]

        for server in [primary_server] + replicas:

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(("localhost", server))
                s.sendall(f"WRITE {chunk_id} {chunk}".encode())
                s.recv(1024)

        total_chunks += 1

    existing_chunks["total_chunks"] = total_chunks
    metadata[filename] = existing_chunks

    save_metadata(metadata)

    return "Write successful"

def handle_upload(file_path):

    with open(file_path, "r") as f:
        content = f.read()

    filename = os.path.basename(file_path)

    handle_create_file(filename)

    return handle_write_file(filename, content)

def handle_read(filename):

    metadata = load_metadata()

    if filename not in metadata:
        return json.dumps({"error": "File not found"})

    file_chunks = metadata[filename]

    chunk_map = {}

    for chunk, server in file_chunks.items():

        if "_replica" not in chunk and chunk != "total_chunks":

            replicas = [
                server,
                file_chunks.get(f"{chunk}_replica1"),
                file_chunks.get(f"{chunk}_replica2"),
                file_chunks.get(f"{chunk}_replica3")
            ]

            chunk_map[chunk] = replicas

    return json.dumps(chunk_map)

def master_server():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.bind(("localhost", 8000))
        s.listen(5)

        print("Master server running on port 8000")

        while True:

            conn, addr = s.accept()

            with conn:

                data = conn.recv(4096).decode()

                command, *args = data.split(" ", 1)

                if command == "CREATE":
                    response = handle_create_file(args[0])

                elif command == "WRITE":
                    filename, content = args[0].split(" ", 1)
                    response = handle_write_file(filename, content)

                elif command == "UPLOAD":
                    response = handle_upload(args[0])

                elif command == "READ":
                    response = handle_read(args[0])

                else:
                    response = "Unknown command"

                conn.sendall(response.encode())

if __name__ == "__main__":
    master_server()