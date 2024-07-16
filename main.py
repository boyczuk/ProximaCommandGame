import threading
from game import Game
import control_panel
import multiprocessing

def start_game():
    game_instance = Game()
    threading.Thread(target=game_instance.run).start()

def start_control_panel():
    control_panel.start_control_panels()

if __name__ == "__main__":
    start_game()
    start_control_panel()
