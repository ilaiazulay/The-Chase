# The Chase

The Multiplayer Quiz Chase Game is a Python-based interactive quiz game where players answer questions, outpace an AI chaser, and progress through levels. The game uses socket communication for multiplayer interactions.

## Features

- Players answer trivia questions.
- Outpace an AI chaser to advance levels.
- Choose different game strategies after the first level.
- Use a lifeline to reveal an answer.
- Multiplayer functionality with socket communication.
- Console-based gameplay.

## Getting Started

### Prerequisites

- Python 3.x

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ilaiazulay/The-Chase.git

### Usage

1. Run the server:

  python server.py <host> <port>
  * Replace <host> with the desired host IP address.
  * Replace <port> with the desired port number.

2. Run the client for each player:

   python client.py <host> <port>
   * Replace <host> with the same host IP address used for the server.
   * Replace <port> with the same port number used for the server.

3. Follow the on-screen instructions to play the game.

### Controls

* Players answer questions by entering a number corresponding to their choice.
* Lifeline is available during chase rounds.

### Gamplay Rules

* Answer questions correctly to progress.
* Outpace the AI chaser to advance levels.
* Use a lifeline to reveal an answer.



