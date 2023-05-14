# ChessPy

ChessPy is a Python chess game that allows you to play chess in either offline or online multiplayer mode. It provides a user-friendly interface and supports both local and remote gameplay. This README file will guide you through the installation process and provide instructions on how to run the game, configure multiplayer settings, run unit tests, and generate coverage reports.

## Installation

To use ChessPy, you need to have Python 3.x installed on your machine. If you don't have it installed, you can download and install Python from the official website: [Python Downloads](https://www.python.org/downloads/)

Once you have Python installed, you can proceed with the following steps to set up ChessPy:

1. Clone the ChessPy repository to your local machine using Git or download the ZIP file and extract it.

   ```bash
   git clone https://github.com/your_username/ChessPy.git
   ```

2. Navigate to the project directory.

   ```bash
   cd ChessPy
   ```

3. Install the required dependencies using pip.

   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

To run the ChessPy game, navigate to the project directory and execute the following command:

```bash
python main.py
```

By default, the game runs in offline or local multiplayer mode. If you want to play online multiplayer, you need to modify the `START_IN_ONLINE_MODE` setting in the `chess_game/constants.py` file. Set it to `False` for offline/local multiplayer or `True` for online multiplayer.

### Online Multiplayer

In online multiplayer mode, one player acts as the server (playing as white) and the other as the client (playing as black). To start the game as the server, use the following command:

```bash
python main.py --server  # or -s
```

To start the game as the client, use the following command:

```bash
python main.py --client  # or -c
```

Note: The client should run the command after the server has started and they should set the `HOST` and `PORT` settings in the `chess_game/constants.py` file to those of the server.

## Running Unit Tests

ChessPy includes a set of unit tests to ensure the correctness of its functionality. To run the unit tests, follow these steps:

1. Navigate to the main directory (ChessPy).

   ```bash
   cd ChessPy
   ```

2. Execute the following command to run the unit tests.

   ```bash
   python -m unittest discover -s tests/
   ```

## Generating Coverage Reports

You can generate coverage reports to assess the code coverage of ChessPy's unit tests. To generate and view coverage reports, follow these steps:

1. Navigate to the main directory (ChessPy).

   ```bash
   cd ChessPy
   ```

2. Execute the following command to run coverage.

   ```bash
   coverage run
   ```

3. Once the tests finish running, generate the coverage report.

   ```bash
   coverage report -m
   ```

   This command will display a detailed report showing the coverage statistics.

That's it! You should now be able to run ChessPy, configure the multiplayer settings, run unit tests, and generate coverage reports. Enjoy playing chess with ChessPy!
