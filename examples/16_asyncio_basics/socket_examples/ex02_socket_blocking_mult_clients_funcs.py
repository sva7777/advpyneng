import socket


def accept(server_socket):
    print("Waiting accept...")
    client_socket, client_address = server_socket.accept()
    print(f"{client_socket=}")
    print(f"{client_address=}")
    return client_socket


def read(client_socket):
    client_data = b""
    while True:
        if b"close" in client_data:
            client_socket.close()
            break
        else:
            data = client_socket.recv(4096) # blocking
            print(f'{data=}')
            client_data += data

        client_socket.send(data.upper())
    print(f"client done")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind(("localhost", 9000))
server_socket.listen()

while True:
    client_socket = accept(server_socket)
    read(client_socket)
