import threading
from game import Game
import control_panel
import tkinter as tk

def start_game():
    game_instance = Game()
    threading.Thread(target=game_instance.run).start()
    return game_instance

def start_control_panel_for_ship(ship_name):
    control_panel.game_instance = game_instance
    control_panel.create_control_panel(ship_name, 0)

def choose_ship():
    root = tk.Tk()
    root.title("Choose Ship to Control")

    ships = ["Enterprise", "Voyager", "Voq'leth", "Negh'Var"]

    def select_ship(ship_name):
        root.destroy() 
        start_control_panel_for_ship(ship_name)

    for ship in ships:
        tk.Button(root, text=ship, command=lambda s=ship: select_ship(s)).pack()

    root.mainloop()

if __name__ == "__main__":
    game_instance = start_game()
    choose_ship()
