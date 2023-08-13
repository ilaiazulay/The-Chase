import socket
import sys


class QuizClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def start(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

        while True:
            response = self.client_socket.recv(1024).decode()
            print(response)

            if 'the game' in response:
                user_input_lose = input('Play again?(yes / no):\n')
                if user_input_lose == 'y' or user_input_lose == 'yes' or user_input_lose == 'Yes':
                    self.client_socket.close()
                    new_game = QuizClient('127.0.0.1', 8001)
                    new_game.start()
                else:
                    self.client_socket.close()

            if 'Congratulations! You have reached the bank' in response:
                user_input_win = input('Play again?(yes / no):\n')
                if user_input_win == 'y' or user_input_win == 'yes' or user_input_win == 'Yes':
                    self.client_socket.close()
                    new_game = QuizClient('127.0.0.1', 8001)
                    new_game.start()
                else:
                    self.client_socket.close()

            if not response.startswith('Welcome') and not response.startswith('Correct') and not response.startswith('Wrong'):
                answer = input('Your answer: ')
                self.client_socket.send(answer.encode())


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python client_b.py <host> <port>")
        exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    user_input = input('Do you want to play?(yes / no):\n')
    if user_input == 'y' or user_input == 'yes' or user_input == 'Yes':
       client = QuizClient(host, port)
       client.start()
    else:
        exit(0)
