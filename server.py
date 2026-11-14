import socket
import selectors



class RedisServer:
    def __init__(self, host = "127.0.0.1", port = 6379):
        self.host = host
        self.port = port

        self.selector = selectors.DefaultSelector()
        self.clients = {}

    def start(self):
        # AF_INET creates ipv4 (AF_INET6 for ipv6)
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # prevents adress already in use error (re uses the address)
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        tcp_socket.bind((self.host, self.port))
        tcp_socket.setblocking(False)
        tcp_socket.listen()

        self.selector.register(
            tcp_socket,
            selectors.EVENT_READ,
            self.accept_client
        )

        while True:
            events = self.selector.select()

            for key, mask in events:
                callback = key.data
                callback(key.fileobj)


    def handle_client(self, client_socket: socket.socket):
        
        data = client_socket.recv(4096)

        # close socket and break loop if client is disconnected
        if data == b"":
            print("Client disconnected")
            self.selector.unregister(client_socket)
            client_socket.close()
            del self.clients[client_socket]
            return

        self.clients[client_socket].extend(data)

        print(data)

    def accept_client(self, server_socket: socket.socket):
        client_socket, client_addr = server_socket.accept()
        print(f"Client connected ({client_addr})")

        client_socket.setblocking(False)
        self.clients[client_socket] = bytearray()

        self.selector.register(
            client_socket,
            selectors.EVENT_READ,
            self.handle_client
        )

server = RedisServer()
server.start()