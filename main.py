import threading
from game import Game
import control_panel

def start_game():
    game_instance = Game()
    threading.Thread(target=game_instance.run).start()
    return game_instance

def start_control_panel(game_instance):
    control_panel.game_instance = game_instance
    threading.Thread(target=control_panel.start_control_panels).start()

if __name__ == "__main__":
    game_instance = start_game()
    start_control_panel(game_instance)
