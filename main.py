import threading
from game import Game
import control_panel

def start_game():
    game_instance = Game()
    game_instance.run()  # Run the game loop in the main thread

def start_control_panel(game_instance):
    control_panel.game_instance = game_instance  # Pass the game instance to the control panel module
    threading.Thread(target=control_panel.start_control_panels).start()

if __name__ == "__main__":
    game_instance = Game()
    threading.Thread(target=start_control_panel, args=(game_instance,)).start()
    start_game()
