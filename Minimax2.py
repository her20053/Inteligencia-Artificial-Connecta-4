import random
from colorama import Fore, Back, Style, init

init()

ROW_COUNT = 6  # Número de filas del tablero
COLUMN_COUNT = 7  # Número de columnas del tablero
EMPTY = 0  # Valor que indica una celda vacía en el tablero
DEPTH = 10  # Profundidad máxima del algoritmo minimax

def get_valid_locations(board):
    # Devuelve una lista de las columnas válidas (sin llenar) en el tablero
    return [c for c in range(COLUMN_COUNT) if board[ROW_COUNT-1][c] == EMPTY]

def get_next_open_row(board, col):
    # Devuelve la próxima fila abierta (sin ficha) en una columna dada
    for r in range(ROW_COUNT):
        if board[r][col] == EMPTY:
            return r
    return None

def drop_piece(board, row, col, piece):
    # Coloca una ficha en el tablero en la fila y columna especificadas
    board[row][col] = piece

def winning_move(board, piece):
    # Verifica si hay una jugada ganadora para el jugador especificado
    # Comprueba en horizontal, vertical y diagonalmente
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False

def is_terminal_node(board):
    # Verifica si el juego ha terminado en el tablero actual
    # El juego ha terminado si hay una jugada ganadora o no quedan movimientos válidos
    return winning_move(board, 1) or winning_move(board, 2) or len(get_valid_locations(board)) == 0

def evaluate_window(window, piece):
    # Evalúa una ventana de 4 celdas y devuelve una puntuación para el jugador especificado
    # La puntuación se basa en el número de fichas del jugador y espacios vacíos en la ventana
    score = 0
    opp_piece = 1 if piece == 2 else 2  # Identifica la ficha del oponente
    if window.count(piece) == 4:
        score += 100  # 4 fichas del jugador en la ventana
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5  # 3 fichas del jugador y 1 espacio vacío en la ventana
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2  # 2 fichas del jugador y 2 espacios vacíos en la ventana

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 80  # Penalización si el oponente tiene 3 fichas y 1 espacio vacío en la ventana
    elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
        score -= 2  # Penalización si el oponente tiene 2 fichas y 2 espacios vacíos en la ventana

    return score

def score_position(board, piece):
    # Evalúa la puntuación de la posición actual del tablero para el jugador especificado
    score = 0
    windows = []

    # Puntuación central
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3  # Incrementa la puntuación por tener fichas en el centro

    # Evaluar ventanas en horizontal, vertical y diagonal
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            windows.append([board[r+i][c] for i in range(4)])
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT-3):
            windows.append([board[r][c+i] for i in range(4)])
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            windows.append([board[r+i][c+i] for i in range(4)])
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            windows.append([board[r-i][c+i] for i in range(4)])

    # Evaluar cada ventana y sumar las puntuaciones
    for window in windows:
        score += evaluate_window(window, piece)

    return score


def minimax(board, depth, alpha, beta, maximizingPlayer, piece):
    # Implementación del algoritmo minimax para tomar decisiones de movimiento
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        # Si se alcanza la profundidad máxima o se llega a un estado terminal, se devuelve la puntuación actual
        # Si el estado terminal es una jugada ganadora, se asigna un valor muy alto o muy bajo para maximizar o minimizar la jugada
        if is_terminal:
            if winning_move(board, piece):
                return (random.randint(0,6), 10000000000000)  # Valor muy alto si el jugador actual gana
            else: 
                return (random.randint(0,6), 0)  # Valor neutro si hay un empate
        else: 
            return (random.randint(0,6), score_position(board, piece))  # Evaluar la posición actual del tablero

    if maximizingPlayer:
        # Es el turno del jugador maximizante
        value = float('-inf')
        column = valid_locations[0]
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = [r.copy() for r in board]
            drop_piece(b_copy, row, col, piece)
            new_score = minimax(b_copy, depth-1, alpha, beta, False, piece)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else: 
        # Es el turno del jugador minimizante (oponente)
        value = float('inf')
        column = valid_locations[0]
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = [r.copy() for r in board]
            drop_piece(b_copy, row, col, piece)
            new_score = minimax(b_copy, depth-1, alpha, beta, True, piece)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def print_board(board):
    # Imprime el tablero en la consola con colores según las fichas
    for fila in board:
        for cell in fila:
            if cell == 0:
                print(Fore.WHITE + '⚪ ', end='')
            elif cell == 1:
                print(Fore.RED + '🔴 ', end='')
            elif cell == 2:
                print(Fore.GREEN + '🟢 ', end='')
        print(Style.RESET_ALL)  # Restablece los colores al valor por defecto

def opponent_about_to_win(board, piece):
    # Verifica si el oponente está a punto de ganar en el próximo turno
    valid_locations = get_valid_locations(board)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        if row is not None:
            b_copy = [r.copy() for r in board]
            drop_piece(b_copy, row, col, piece)
            if winning_move(b_copy, piece):
                return col
    return None

def obtener_movida(board, playerTurnID):
    # Función principal para obtener la jugada a realizar por el jugador
    opponent_piece = 1 if playerTurnID == 2 else 2
    blocking_move = opponent_about_to_win(board, opponent_piece)
    if blocking_move is not None:
        print("\nEsta jugando player " + str(playerTurnID) + " y bloqueará al oponente en la columna: " + str(blocking_move))
        return blocking_move
    else:
        jugada = minimax(board, DEPTH, float('-inf'), float('inf'), True, playerTurnID)[0]
        print("\nEsta jugando player " + str(playerTurnID) + "\n")
        print("\nEl tablero actualmente es:\n")
        print_board(board)
        print("\nLa jugada que se ha hecho es en la columna: " + str(jugada))
        return jugada
