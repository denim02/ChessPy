def is_possible_move(board, piece, new_position):
    """
    Check if a move is possible (if there isn't a blocking piece in the way).

    Parameters:
        board (Board): board on which the move is being made.
        piece (Piece): piece to be moved.
        new_position (tuple): new position on the board in (x, y) format, where x is the row and y is the column.

    Returns:
        bool: True if the move is legal, False otherwise.
    """
    return new_position in piece.possible_moves


def is_check(board, color):
    """
    Check if a king of a given color is in check.

    Parameters:
        board (Board): board on which the move is being made.
        color (str): color of the king to be checked.

    Returns:
        bool: True if the king is in check, False otherwise.
    """
    king = [piece for piece in board.piece_list if piece.color ==
            color and piece.name == "King"][0]
    for piece in board.piece_list:
        if piece.color != color and king.position in piece.legal_moves:
            return True
    return False


def is_checkmate(board, color):
    """
    Check if a king of a given color is in checkmate.

    Parameters:
        board (Board): board on which the move is being made.
        color (str): color of the king to be checked.

    Returns:
        bool: True if the king is in checkmate, False otherwise.
    """
    king = [piece for piece in board.piece_list if piece.color ==
            color and piece.name == "King"][0]
    if is_check(board, color):
        for piece in board.piece_list:
            if piece.color == color:
                for move in piece.legal_moves:
                    if not is_check(board, color):
                        return False
    return True


def is_stalemate(board, color):
    """
    Check if a king of a given color is in stalemate.

    Parameters:
        board (Board): board on which the move is being made.
        color (str): color of the king to be checked.

    Returns:
        bool: True if the king is in stalemate, False otherwise.
    """
    king = [piece for piece in board.piece_list if piece.color ==
            color and piece.name == "King"][0]
    if not is_check(board, color):
        for piece in board.piece_list:
            if piece.color == color:
                for move in piece.legal_moves:
                    if not is_check(board, color):
                        return False
    return True


def is_legal_move(board, piece, new_position):
    """
    Check if a move is legal (if the king is not in check after the move).

    Parameters:
        board (Board): board on which the move is being made.
        piece (Piece): piece to be moved.
        new_position (tuple): new position on the board in (x, y) format, where x is the row and y is the column.

    Returns:
        bool: True if the move is legal, False otherwise.
    """
    if board.get_piece_at_square(new_position) is not None and board.get_piece_at_square(
            new_position).color == piece.color:
        return False
    if piece.name == "Knight" and not board.is_square_occupied(new_position):
        return True
    return not board.is_path_blocked(piece.position, new_position)
