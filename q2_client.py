import socket
import pickle



def some_function(arg1, arg2):

    return arg1 + arg2


def send_task(task, args, worker_address):

    try:

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(worker_address)


        data = pickle.dumps((task, args))


        client_socket.sendall(data)


        response = receive_complete_message(client_socket)


        return pickle.loads(response)
    except socket.error as e:
        print(f"Socket error: {e}")
        return None
    except pickle.PickleError as e:
        print(f"Pickling error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        # Close the client socket
        if client_socket:
            client_socket.close()


def receive_complete_message(sock):

    data = b''
    while True:
        part = sock.recv(4096)
        if not part:
            break
        data += part
    return data


# Example usage:
if __name__ == "__main__":
    # Define arguments for the task
    arg1 = 5
    arg2 = 3

    # Define the address of the worker node
    worker_address = ('localhost', 3000)

    # Send the task to the worker node
    result = send_task(some_function, (arg1, arg2), worker_address)

    # Print the result
    print("Result:", result)

