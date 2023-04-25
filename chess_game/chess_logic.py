"""
chess_logic.py
This module contains the logic for the chess game.
"""

def is_check(board, color):
    """
    Check if a king of a given color is in check.

    Parameters:
        board (Board): board on which the move is being made.
        color (str): color of the king to be checked.

    Returns:
        bool: True if the king is in check, False otherwise.
    """
    king = [
        piece
        for piece in board.piece_list
        if piece.name == "King" and piece.color == color
    ][0]
    return board.is_square_attacked(king.position, color)


def is_checkmate(board, color):
    """
    Check if a king of a given color is in checkmate.

    Parameters:
        board (Board): board on which the move is being made.
        color (str): color of the king to be checked.

    Returns:
        bool: True if the king is in checkmate, False otherwise.
    """
    if is_check(board, color):
        for piece in board.piece_list:
            if piece.color == color:
                for move in piece.legal_moves:
                    if not is_king_in_check_after_move(board, piece, move):
                        return False

        return True
    return False


def is_king_in_check_after_move(board, piece, new_position):
    """
    Check if a king of a given color is in check after a move.

    Parameters:
        board (Board): board on which the move is being made.
        piece (Piece): piece to be moved.
        new_position (tuple): new position on the board
            in (x, y) format, where x is the row and y is the column.

    Returns:
        bool: True if the king is in check, False otherwise.
    """
    color = piece.color
    old_position = piece.position
    board.move_piece_to_square(piece, new_position, change_en_passant=False)
    is_checked = is_check(board, color)
    board.revert_move(piece, old_position)
    return is_checked


def is_stalemate(board, color):
    """
    Check if a king of a given color is in stalemate.

    Parameters:
        board (Board): board on which the move is being made.
        color (str): color of the king to be checked.

    Returns:
        bool: True if the king is in stalemate, False otherwise.
    """
    if not is_check(board, color):
        for piece in board.piece_list:
            if piece.color == color:
                for move in piece.legal_moves:
                    if not is_king_in_check_after_move(board, piece, move):
                        return False
        return True
    return False


def is_legal_move(board, piece, new_position):
    """
    Check if a move is legal (if the king is not in check after the move).

    Parameters:
        board (Board): board on which the move is being made.
        piece (Piece): piece to be moved.
        new_position (tuple): new position on the board
            in (x, y) format, where x is the row and y is the column.

    Returns:
        bool: True if the move is legal, False otherwise.
    """
    if (
        board.get_piece_at_square(new_position) is not None
        and board.get_piece_at_square(new_position).color == piece.color
    ):
        return False
    if piece.name == "Knight":  # Knights can jump over other pieces
        return True
    # En passant
    if (
        piece.name == "Pawn"
        and board.en_passant_piece is not None
        and new_position[1] == board.en_passant_piece.position[1]
        and abs(new_position[0] - board.en_passant_piece.position[0]) == 1
    ):
        return True
    return not board.is_path_blocked(piece.position, new_position)
