"""The chess_logic module contains implementations of the basic logic and rules of chess.

It provides functions to check if a move is legal, if a king is in check, checkmate or stalemate."""
from typing import TYPE_CHECKING

# USED FOR TYPE HINTING ONLY
if TYPE_CHECKING:
    from chess_game.board import Board
    from chess_game.pieces import Piece


def is_check(board: "Board", color: str) -> bool:
    """Check if a king of a given color is in check.

    Parameters
    ----------
    board : Board
        Board on which the move is being made.
    color : str
        Color of the king to be checked. Must be either "white" or "black".

    Returns
    -------
    bool
        True if the king is in check, False otherwise.
    """
    king = [
        piece
        for piece in board.piece_list
        if piece.name == "King" and piece.color == color
    ][0]
    return board.is_square_attacked(king.position, color)


def is_checkmate(board: "Board", color: str) -> bool:
    """Check if a king of a given color is in checkmate.

    Parameters
    ----------
    board : Board
        Board on which the move is being made.
    color : str
        Color of the king to be checked. Must be either "white" or "black".

    Returns
    -------
    bool
        True if the king is in checkmate, False otherwise.
    """
    if is_check(board, color):
        for piece in board.piece_list:
            if piece.color == color:
                for move in piece.legal_moves:
                    if not is_king_in_check_after_move(board, piece, move):
                        return False

        return True
    return False


def is_king_in_check_after_move(
    board: "Board", piece: "Piece", new_position: tuple
) -> bool:
    """Check if a king of a given color is in check after a move.

    The method makes the move on the board, checks if the king is in check and then reverts the move.

    Parameters
    ----------
    board : Board
        Board on which the move is being made.
    piece : Piece
        Piece to be moved.
    new_position : tuple
        New position on the board in (x, y) format, where x is the rank and y is the file.

    Returns
    -------
    bool
        True if the king is in check after the move, False otherwise.
    """
    color = piece.color
    old_position = piece.position
    board.move_piece_to_square(piece, new_position, change_en_passant=False)
    is_checked = is_check(board, color)
    board.revert_move(piece, old_position)
    return is_checked


def is_stalemate(board: "Board", color: str) -> bool:
    """Check if a king of a given color is in stalemate.

    Parameters
    ----------
    board : Board
        Board on which the move is being made.
    color : str
        Color of the king to be checked. Must be either "white" or "black".

    Returns
    -------
    bool
        True if the king is in stalemate, False otherwise.
    """
    if not is_check(board, color):
        for piece in board.piece_list:
            if piece.color == color:
                for move in piece.legal_moves:
                    if not is_king_in_check_after_move(board, piece, move):
                        return False
        return True
    return False


def is_legal_move(board: "Board", piece: "Piece", new_position: tuple) -> bool:
    """Check if a move is legal.

    A move is defined as legal if:
    - the piece is moving to a position that is possible for it to move to (e.g. a rook can't move diagonally)
    - the piece is not moving to a square occupied by a piece of the same color
    - the piece is not moving through a square occupied by another piece (except for knights)
    - the piece is not moving to a square occupied by a piece of the opposite color, if it is a pawn

    Parameters
    ----------
    board : Board
        Board on which the move is being made.
    piece : Piece
        Piece to be moved.
    new_position : tuple
        New position on the board in (x, y) format, where x is the rank and y is the file.

    Returns
    -------
    bool
        True if the move is legal, False otherwise.
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
