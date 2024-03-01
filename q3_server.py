import socket
import threading
import pickle

class ChatServer:
    """
    A simple chat server that accepts connections from multiple clients
    and facilitates communication among them.
    """

    def __init__(self, host, port):
        """
        Initialize the chat server.

        Parameters:
        - host (str): The host address to bind the server.
        - port (int): The port number to bind the server.
        """
        self.host = host
        self.port = port
        self.clients = []  # List to store connected clients
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

    def handle_client(self, client_socket, client_address):
        """
        Handle communication with a client.

        Parameters:
        - client_socket (socket): The socket object for the client connection.
        - client_address (tuple): The address of the client (host, port).
        """
        try:
            username = pickle.loads(client_socket.recv(4096))
            if not username:
                print("Empty username received. Disconnecting client.")
                client_socket.close()
                return

            self.clients.append((username, client_socket))
            print(f"Connected: {username} from {client_address}")

            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                self.broadcast(data, username)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()
            self.clients.remove((username, client_socket))
            print(f"Disconnected: {username} from {client_address}")

    def broadcast(self, message, sender_username):
        """
        Broadcast a message from a client to all other connected clients.

        Parameters:
        - message (bytes): The message to broadcast.
        - sender_username (str): The username of the client sending the message.
        """
        for username, client_socket in self.clients:
            if username != sender_username:
                try:
                    client_socket.sendall(message)
                except Exception as e:
                    print(f"Error broadcasting message: {e}")

    def start(self):
        """
        Start the chat server and handle incoming client connections.
        """
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()
        except KeyboardInterrupt:
            print("Shutting down the server...")
            self.server_socket.close()

if __name__ == "__main__":
    server = ChatServer('localhost', 5555)
    server.start()
