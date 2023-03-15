# Import Modules & Libraries
import chess
import random
import time
import display_gui as gui
import global_vars as G

# Select Random Move
def select_random():
    move_list=list(G.BOARD.legal_moves)
    move_count=len(move_list)
    random_num=random.randint(0,move_count-1)
    return move_list[random_num]


# Get Game Status
def calc_game_status():
    if G.BOARD.is_checkmate():
        if G.BOARD.turn:
            return -9999
        else:
            return 9999
    elif G.BOARD.is_stalemate():
        return 0
    elif G.BOARD.is_insufficient_material():
        return 0
    elif G.BOARD.is_seventyfive_moves():
        return 0
    elif G.BOARD.is_fivefold_repetition():
        return 0
    else:
        return None
# Get Board Score
def calc_board_score():
    game_status = calc_game_status()
    if game_status != "CONTINUE":
        return game_status
    w_pawns = G.BOARD.pieces(chess.PAWN,chess.WHITE)
    w_knights = G.BOARD.pieces(chess.KNIGHT,chess.WHITE)
    w_bishops = G.BOARD.pieces(chess.BISHOP, chess.WHITE)
    w_rooks = G.BOARD.pieces(chess.ROOK, chess.WHITE)
    w_queens = G.BOARD.pieces(chess.QUEEN, chess.WHITE)
    w_kings = G.BOARD.pieces(chess.KING, chess.WHITE)

    w_score_p = sum([G.pawn_score[p] for p in w_pawns])

def board_score():
    status = calc_game_status()
    if status is not None: return status #game is over
    points = {chess.PAWN: 100, chess.BISHOP: 300, chess.KNIGHT: 350, chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 9999}
    score = 0
    for color in [chess.WHITE, chess.BLACK]:
        for ptype, pvalue in points.items():
            pieces = G.BOARD.pieces(ptype, color) #get all pieces with the specified type and color
            if color is chess.WHITE:
                score += sum([G.piece_heatmap[ptype][p] for p in pieces])
                score += len(pieces) * pvalue
            else:
                score -= sum([G.piece_heatmap[ptype][chess.square_mirror(p)] for p in pieces])
                score -= len(pieces) * pvalue
    if G.BOARD.turn: return score
    else: return -score
# Select Positional Move
def select_positional():
    best_move = select_random()
    best_score = -9999
    for move in G.BOARD.legal_moves:
        G.BOARD.push(move)
        score = -board_score()
        G.BOARD.pop()
        if score > best_score:
            best_score = score
            best_move = move
    return best_move
# Negamax with Alpha-Beta Pruning
def negamax(alpha, beta, depth, scores):
    best_score = -9999
    if depth == 0: return board_score()
    for move in G.BOARD.legal_moves:
        uci = move.uci()
        G.BOARD.push(move)
        if uci in scores:
            score = scores[uci]
        else:
            score = -negamax(-beta, -alpha, depth - 1, scores)
            scores[uci] = score
        G.BOARD.pop()
        if score >= beta: return score
        if score > best_score: best_score = score
        if score > alpha: alpha = score
    return best_score
# Quiescence Search

# Select Predictive Move
def select_predictive(depth):
    alpha = -100000
    beta = 100000
    best_score = -9999
    best_move = select_random()
    for move in G.BOARD.legal_moves:
        move_scores = {}
        G.BOARD.push(move)
        score = -negamax(-beta, -alpha, depth - 1, move_scores)
        G.BOARD.pop()
        if score > best_score:
            best_score = score
            best_move = move
        if score > alpha: alpha = score
    return best_move
# Complete AI Move
def make_ai_move(move, delay):
    time.sleep(delay)
    if move != chess.Move.null():
        gui.draw_board()
        gui.draw_select_square(move.from_square)
        gui.draw_select_square(move.to_square)
    gui.print_san(move)
    G.BOARD.push(move)
