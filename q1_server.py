import socket
import pickle


def save_file(filename, data):
    """
    Save data to the specified file.

    Parameters:
    - filename (str): The path of the file to be saved.
    - data (bytes): The data to be saved.
    """
    with open(filename, 'wb') as f:
        f.write(data)


def main():

    host = '192.168.2.138'
    port = 3000
    buffer_size = 4096


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:

        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} established.")

        try:

            data_size = int(client_socket.recv(16).strip())

            received_data = b""
            while len(received_data) < data_size:
                packet = client_socket.recv(buffer_size)
                if not packet:
                    break
                received_data += packet


            file_data = pickle.loads(received_data)


            save_path = input("Enter the path to save the file: ")

            save_file(save_path, file_data)
            print("File received and saved successfully.")
        except Exception as e:

            print("Error:", e)
        finally:

            client_socket.close()


if __name__ == "__main__":
    main()
