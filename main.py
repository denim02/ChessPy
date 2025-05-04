import asyncio
import pygame
from chess_game.game import ChessGame
from chess_game.graphics import ChessUI, PromotionBox
from chess_game import constants

# Initialize Pygame
pygame.init()
# Create the game window
window = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
pygame.display.set_caption("Chess Game")
clock = pygame.time.Clock()

async def main():
    # Create the game and UI objects
    game = ChessGame()
    ui = ChessUI(game.board)
    
    # Create flags for game state
    is_running = True
    is_game_over = False
    game_status = ""

    while is_running:
        clock.tick(constants.FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                
            if not is_game_over and is_running:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clicked_piece = game.board.get_piece_at_square(
                        ui.get_square_at_coords(event.pos)
                    )
                    if clicked_piece and clicked_piece.color == game.turn:
                        ui.dragged_piece = clicked_piece
                        ui.is_dragging = True
                        ui.original_coords = ui.dragged_piece.coords
                        ui.offset = (
                            event.pos[0] - ui.dragged_piece.coords[0],
                            event.pos[1] - ui.dragged_piece.coords[1],
                        )
                
                elif event.type == pygame.MOUSEMOTION:
                    if ui.is_dragging:
                        ui.dragged_piece.coords = (
                            event.pos[0] - ui.offset[0],
                            event.pos[1] - ui.offset[1],
                        )
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if ui.is_dragging:
                        ui.is_dragging = False
                        new_square = ui.get_square_at_coords(event.pos)
                        
                        if new_square:
                            if (
                                ui.dragged_piece.name == "Pawn"
                                and new_square[0] in (0, 7)
                                and new_square in ui.dragged_piece.legal_moves
                            ):
                                ui.promotion_box = PromotionBox(
                                    ui.window, ui.dragged_piece.color
                                )
                                game.promotion_choice = ui.promotion_box.final_choice
                                ui.promotion_box = None
                            
                            try:
                                game.make_move(ui.dragged_piece.position, new_square)
                            except Exception as ex:
                                print(ex)
                                ui.dragged_piece.coords = ui.original_coords
                            
                            ui.dragged_piece = None
                            
                            if (
                                game.is_checkmate
                                or game.is_stalemate
                                or game.is_threefold_repetition
                                or game.fifty_move_counter >= 50
                            ):
                                if game.is_checkmate:
                                    game_status = "checkmate"
                                elif game.is_stalemate:
                                    game_status = "stalemate"
                                elif game.is_threefold_repetition:
                                    game_status = "threefold repetition"
                                elif game.fifty_move_counter >= 50:
                                    game_status = "fifty move rule"
                                
                                is_game_over = True
                        else:
                            ui.dragged_piece.coords = ui.original_coords
        
        if is_game_over:
            winner = "White" if game.turn == "black" else "Black"
            ui.render_gameover(game_status, winner)
        else:
            ui.render_all()
        
        pygame.display.flip()
        await asyncio.sleep(0)  # Required for Pygbag

    pygame.quit()

asyncio.run(main())