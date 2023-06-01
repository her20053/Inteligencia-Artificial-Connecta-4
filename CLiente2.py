from socketIO_client import SocketIO
import sys

from Minimax2 import obtener_movida, print_board

server_url = "http://localhost"
server_port = 4000

socketIO = SocketIO(server_url, server_port)

def on_connect():
    print("Connected to server")
    socketIO.emit('signin', {
        'user_name': sys.argv[1],
        'tournament_id': 80000,
        'user_role': 'player'
    })

def on_ok_signin():
    print("Login")

def on_finish(data):
    game_id = data['game_id']
    player_turn_id = data['player_turn_id']
    winner_turn_id = data['winner_turn_id']
    board = data['board']
    # Your logic for handling 'finish' event here

def on_ready(data):
    game_id = data['game_id']
    player_turn_id = data['player_turn_id']
    board = data['board']
    # print("I'm player:", player_turn_id)
    # print(board)
    
    # Your logic / user input here
    move = obtener_movida(board, player_turn_id)
    socketIO.emit('play', {
        'tournament_id': 80000,
        'player_turn_id': player_turn_id,
        'game_id': game_id,
        'movement': move
    })

def on_finish(data):
    game_id = data['game_id']
    player_turn_id = data['player_turn_id']
    winner_turn_id = data['winner_turn_id']
    board = data['board']
    
    # Your cleaning board logic here
    
    print("Winner:", winner_turn_id)
    print(board)
    print_board(board=board)
    socketIO.emit('player_ready', {
        'tournament_id': 80000,
        'player_turn_id': player_turn_id,
        'game_id': game_id
    })

socketIO.on('connect', on_connect)
socketIO.on('ok_signin', on_ok_signin)
socketIO.on('finish', on_finish)
socketIO.on('ready', on_ready)
socketIO.on('finish', on_finish)

socketIO.wait()