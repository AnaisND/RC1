import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 3333
SECRET = 'key2'

def listen_for_messages(sock):
    try:
        while True:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                print("Server closed.")
                break
            print("\n✉ from The Server: ", message)
            print("> ", end='', flush=True)
    except Exception as e:
        print("Error receiving the message: ", e)

def send_command(sock, command):
    try:
        sock.sendall(command.encode('utf-8'))
    except Exception as e:
        print("Error sending request: ", e)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print(f"\nYou are online!\nConnect: login <<key>> \nDisconnect: logout \nRequest rights: rights <<client>> <<file>> \nGive rights: yes <<client>> \nKeep rights: no <<client>> \nDownload file: download <<client>> <<file>> \nRead file: read <<client>> <<file>> \nDelete file: delete <<file>> \nList files 'Librarie Publica': listall \nList files 'Librarie Privata': list <<file>> \nTerminate: exit\n\n")

        listen_thread = threading.Thread(target=listen_for_messages, args=(sock,))
        listen_thread.start()

        while True:
            user_input = input("> ").strip()
            if user_input == 'exit':
                os._exit(0)

            parts = user_input.split(' ', 2)
            command = parts[0]
            params = parts[1:]

            if command == "login":
                if params and params[0] == SECRET:
                    send_command(sock, user_input)
                else:
                    print("Wrong command or secret.")
            elif command in ["rights", "yes", "no", "download", "read", "delete", "listall", "list", "logout"]:
                send_command(sock, user_input)
            else:
                print("Unknown request.")

        listen_thread.join()

if __name__ == '__main__':
    main()
