from flask import Flask, request, jsonify, render_template
from game import TicTacToe, SmartComputerPlayer, HumanPlayer, get_randomized_players

app = Flask(__name__)

# Store the game state globally for simplicity
current_game = None
x_player = None
o_player = None
current_letter = 'X'


@app.route('/')
def index():
    global current_game, x_player, o_player, current_letter
    # Start a new game
    current_game = TicTacToe()
    x_player, o_player = get_randomized_players()
    current_letter = 'X'
    
    # If the computer is the first player, make its move immediately
    if isinstance(x_player, SmartComputerPlayer):
        move = x_player.get_move(current_game)
        current_game.make_move(move, current_letter)
        current_letter = 'O'  # Switch to human's turn

    return render_template('index.html')  # Render the frontend


@app.route('/make_move', methods=['POST'])
def make_move():
    global current_game, x_player, o_player, current_letter

    # Retrieve data from the frontend
    square = request.json.get('square')

    # Ensure the move is valid
    if not current_game or square not in current_game.available_moves():
        return jsonify({'error': 'Invalid move'}), 400

    # Make the move and check for winner
    current_game.make_move(square, current_letter)
    winner = current_game.current_winner
    board = current_game.board

    # Prepare the response
    response = {
        'board': board,
        'winner': winner,
        'is_tie': not current_game.empty_squares() and not winner
    }

    # Switch the turn
    current_letter = 'O' if current_letter == 'X' else 'X'

    return jsonify(response)


@app.route('/get_move', methods=['POST'])
def get_computer_move():
    global current_game, x_player, o_player, current_letter

    # Get the move based on the current player
    if current_letter == 'X':
        move = x_player.get_move(current_game)
    else:
        move = o_player.get_move(current_game)

    # Make the move and check for winner
    current_game.make_move(move, current_letter)
    winner = current_game.current_winner
    board = current_game.board

    # Prepare the response
    response = {
        'move': move,
        'board': board,
        'winner': winner,
        'is_tie': not current_game.empty_squares() and not winner
    }

    # Switch the turn
    current_letter = 'O' if current_letter == 'X' else 'X'

    return jsonify(response)

@app.route('/restart', methods=['POST'])
def restart():
    global current_game, x_player, o_player, current_letter
    # Reset the game state
    current_game = TicTacToe()
    x_player, o_player = get_randomized_players()
    current_letter = 'X'

    # If the computer is the first player, make its move immediately
    if isinstance(x_player, SmartComputerPlayer):
        move = x_player.get_move(current_game)
        current_game.make_move(move, current_letter)
        current_letter = 'O'  # Switch to human's turn

    return jsonify({
        'board': current_game.board, 
        'current_letter': current_letter,
        'x_player' : 'Computer' if isinstance(x_player, SmartComputerPlayer) else 'Human',
        'o_player' : 'Computer' if isinstance(o_player, SmartComputerPlayer) else 'Human'
        })

if __name__ == '__main__':
    app.run(debug=True)
