import concurrent
import socket
import sys
import threading
import random


class QuizServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_sockets = []
        self.current_question = 0
        self.current_chase_question = 0
        self.money = 0
        self.level = 0
        self.lifeline = 1
        self.chaiser_level = 1
        self.first_level_questions = [
            {
                'question': 'Who was the first President of the United States?',
                'options': ['George Washington', 'Thomas Jefferson', 'Abraham Lincoln', 'John Adams'],
                'answer': 0
            },
            {
                'question': 'What is the capital of the United States?',
                'options': ['New York City', 'Washington D.C.', 'Los Angeles', 'Chicago'],
                'answer': 1
            },
            {
                'question': 'What is the largest state in the United States by land area?',
                'options': ['Alaska', 'Texas', 'California', 'Florida'],
                'answer': 0
            }
        ]
        self.chase_questions = [
            {
                'question': 'Which state is known as the Sunshine State?',
                'options': ['California', 'Florida', 'Texas', 'Hawaii'],
                'answer': 1
            },
            {
                'question': 'What is the largest ocean in the world?',
                'options': ['Pacific Ocean', 'Atlantic Ocean', 'Arctic Ocean', 'Indian Ocean'],
                'answer': 0
            },
            {
                'question': 'Which planet is known as the Red Planet?',
                'options': ['Venus', 'Mars', 'Jupiter', 'Saturn'],
                'answer': 1
            },
            {
                'question': 'Who painted the Mona Lisa?',
                'options': ['Vincent van Gogh', 'Leonardo da Vinci', 'Pablo Picasso', 'Michelangelo'],
                'answer': 1
            },
            {
                'question': 'Which country is famous for the Taj Mahal?',
                'options': ['India', 'China', 'Egypt', 'Italy'],
                'answer': 0
            },
            {
                'question': 'Which animal is known as the "King of the Jungle"?',
                'options': ['Lion', 'Tiger', 'Elephant', 'Giraffe'],
                'answer': 0
            },
            {
                'question': 'Which sea is located on the western coast of Israel?',
                'options': ['Mediterranean Sea', 'Red Sea', 'Dead Sea', 'Galilee Sea'],
                'answer': 0
            },
            {
                'question': 'What is the official language of Israel?',
                'options': ['English', 'Hebrew', 'Arabic', 'Russian'],
                'answer': 1
            },
            {
                'question': 'Which historical site in Jerusalem is considered holy by Jews, Christians, and Muslims?',
                'options': ['Western Wall', 'Church of the Holy Sepulchre', 'Al-Aqsa Mosque', 'Dome of the Rock'],
                'answer': 0
            },
            {
                'question': 'Which Israeli city is known as the "City of Innovation" and a major center for technology startups?',
                'options': ['Tel Aviv', 'Haifa', 'Beersheba', 'Netanya'],
                'answer': 0
            },
            {
                'question': 'What is the national bird of Israel?',
                'options': ['Eagle', 'Dove', 'Hoopoe', 'Peacock'],
                'answer': 2
            },
            {
                'question': 'Which Israeli leader signed the Oslo Accords in 1993?',
                'options': ['Benjamin Netanyahu', 'Ariel Sharon', 'Ehud Barak', 'Yitzhak Rabin'],
                'answer': 3
            },
            {
                'question': 'Which desert covers a significant part of southern Israel?',
                'options': ['Negev Desert', 'Sahara Desert', 'Gobi Desert', 'Atacama Desert'],
                'answer': 0
            },
            {
                'question': 'What is the currency of Israel?',
                'options': ['Euro', 'Pound', 'Shekel', 'Dollar'],
                'answer': 2
            },
            {
                'question': 'Which Israeli actress won an Academy Award for Best Actress for her role in the film "Black Swan"?',
                'options': ['Gal Gadot', 'Natalie Portman', 'Bar Refaeli', 'Ayelet Zurer'],
                'answer': 1
            },
            {
                'question': 'What is the national flower of Israel?',
                'options': ['Rose', 'Sunflower', 'Tulip', 'Anemone'],
                'answer': 3
            },
            {
                'question': 'Which Israeli scientist won the Nobel Prize in Chemistry in 2004 for his work on the discovery of quasicrystals?',
                'options': ['Ada Yonath', 'Aaron Ciechanover', 'Avram Hershko', 'Daniel Shechtman'],
                'answer': 3
            },
            {
                'question': 'Which Israeli city is home to the Technion-Israel Institute of Technology, a renowned university?',
                'options': ['Jerusalem', 'Tel Aviv', 'Haifa', 'Beer Sheva'],
                'answer': 2
            },
            {
                'question': 'Which Israeli dish consists of mashed chickpeas, tahini sauce, and spices?',
                'options': ['Falafel', 'Shawarma', 'Hummus', 'Tabbouleh'],
                'answer': 2
            }
        ]

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(3)  # Allowing up to 3 connections
        print('Quiz server started.')

        while True:
            client_socket, address = self.server_socket.accept()
            print(f'New connection from {address}')
            self.client_sockets.append(client_socket)

            if len(self.client_sockets) > 3:
                print('Maximum number of connections reached. Closing new connections.')
                client_socket.send(b'Sorry, maximum number of connections reached. Try again later.')
                client_socket.close()
                self.client_sockets.remove(client_socket)
            else:
                thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                thread.start()

    def handle_client(self, client_socket):
        client_socket.send(b'Welcome to the Chase!\n')

        current_question = self.current_question
        current_chase_question = self.current_chase_question
        money = self.money
        level = self.level
        lifeline = self.lifeline
        chaiser_level = self.chaiser_level

        while True:
            question = self.first_level_questions[current_question]
            question_text = f'{question["question"]}\n'
            for i, option in enumerate(question['options']):
                question_text += f'{i + 1}. {option}\n'

            client_socket.send(question_text.encode())
            client_answer = client_socket.recv(1024).decode().strip()

            try:
                client_answer = int(client_answer)
            except ValueError:
                client_socket.send(b'Invalid answer. Please choose a number from the options.')
                continue

            # first stage - three questions
            if client_answer == question['answer'] + 1:
                client_socket.send(b'Correct answer! you have gained 5000\n')
                money += 5000
                current_question += 1
            else:
                client_socket.send(b'Wrong answer!\n')
                if current_question != len(self.first_level_questions):
                    current_question += 1

            # second stage - a choice
            if current_question == len(self.first_level_questions):
                client_socket.send(b'Level one is complete!\nChoose one of the options:\n1. Start from level 3 with the current amount\n2. Get one step to the chaiser and start from level 2 with double amount\n3. Get one step away from the chaiser and start from level 4 with half the amount\n')
                client_answer = client_socket.recv(1024).decode().strip()
                client_answer = int(client_answer)
                if client_answer == 1:
                    level = 3
                elif client_answer == 2:
                    level = 2
                    money *= 2
                elif client_answer == 3:
                    level = 4
                    money /= 2
                current_chase_question = 0
                chaiser_level = 1
                break

        # chase stage
        while True:
            if current_chase_question >= 18:
                current_chase_question = 0
            chase_questions = self.chase_questions[current_chase_question]
            chase_question_text = f'{chase_questions["question"]}\n'
            for i, option in enumerate(chase_questions['options']):
                chase_question_text += f'{i + 1}. {option}\n'
            if lifeline > 0:
                chase_question_text += f'{5}. Lifeline\n'

            client_socket.send(chase_question_text.encode())
            client_answer = client_socket.recv(1024).decode().strip()

            try:
                client_answer = int(client_answer)
            except ValueError:
                client_socket.send(b'Invalid answer. Please choose a number from the options.')
                continue

            if client_answer == 5:
                chase_questions_lifeline = self.chase_questions[current_chase_question]
                chase_question_text_lifeline = f'{chase_questions["question"]}\n'
                chase_question_text_lifeline += f'{chase_questions["answer"] + 1}. {chase_questions["options"][chase_questions["answer"]]}\n'
                next_option_index = (chase_questions['answer'] + 1) % len(chase_questions['options'])
                next_option = chase_questions['options'][next_option_index]
                chase_question_text_lifeline += f'{chase_questions["answer"] + 2}. {next_option}\n'
                client_socket.send(chase_question_text_lifeline.encode())
                client_answer = client_socket.recv(1024).decode().strip()

                try:
                    client_answer = int(client_answer)
                    print(client_answer, )
                except ValueError:
                    client_socket.send(b'Invalid answer. Please choose a number from the options.')
                    continue

                lifeline = 0

            if client_answer == chase_questions['answer'] + 1:
                print(level)
                level += 1
                money += 5000
                if random.random() <= 0.8:
                    chaiser_level += 1
                    client_socket.send(b'Correct answer!you have gained 5000\nBoth you and the chaiser answer correctly and go to the next level\nMoney: '+ str(self.money).encode() + b'\nLevel: ' + str(self.level).encode() + b'\nChaiser level: ' + str(self.chaiser_level).encode() + b'\nLifeline: ' + str(self.lifeline).encode() + b'\n\n')
                else:
                    if chaiser_level - 1 > 0:
                        chaiser_level -= 1
                    client_socket.send(b'Correct answer!you have gained 5000\nThe chaiser answered wrong and go to the previous level\nMoney: '+ str(self.money).encode() + b'\nLevel: ' + str(self.level).encode() + b'\nChaiser level: ' + str(self.chaiser_level).encode() + b'\nLifeline: ' + str(self.lifeline).encode() + b'\n\n')
                if level == 7:
                    client_socket.send(b'Congratulations! You have reached the bank.')
                    break
            else:
                level -= 1
                money -= 5000
                if random.random() <= 0.8:
                    chaiser_level += 1
                    client_socket.send(b'Wrong answer!you have lost 5000\nThe chaiser answer correctly and go to the next level\nMoney: '+ str(self.money).encode() + b'\nLevel: ' + str(self.level).encode() + b'\nChaiser level: ' + str(self.chaiser_level).encode() + b'\nLifeline: ' + str(self.lifeline).encode() + b'\n\n')
                else:
                    if chaiser_level - 1 > 0:
                        chaiser_level -= 1
                    client_socket.send(b'Wrong answer!you have lost 5000\nThe chaiser also answered wrong\nMoney: '+ str(self.money).encode() + b'\nLevel: ' + str(self.level).encode() + b'\nChaiser level: ' + str(self.chaiser_level).encode() + b'\nLifeline: ' + str(self.lifeline).encode() + b'\n\n')

            if level <= chaiser_level:
                client_socket.send(b'You have lost the game.')
                break

            current_chase_question += 1

    def close(self):
        for client_socket in self.client_sockets:
            client_socket.close()
        if self.server_socket:
            self.server_socket.close()
        print('Quiz server closed.')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python server_b.py <host> <port>")
        exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    server = QuizServer(host, port)
    try:
        server.start()
    except KeyboardInterrupt:
        server.close()
