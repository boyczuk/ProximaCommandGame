import tkinter as tk
from game import command_queue
import threading

def post_command(ship, command):
    command_queue.put((ship, command))

def create_control_panel(ship_name):
    root = tk.Tk()
    root.title(f"Control Panel - {ship_name}")

    tk.Button(root, text=f"{ship_name} Up", command=lambda: post_command(ship_name, "UP")).pack()
    tk.Button(root, text=f"{ship_name} Down", command=lambda: post_command(ship_name, "DOWN")).pack()
    tk.Button(root, text=f"{ship_name} Left", command=lambda: post_command(ship_name, "LEFT")).pack()
    tk.Button(root, text=f"{ship_name} Right", command=lambda: post_command(ship_name, "RIGHT")).pack()

    root.mainloop()

def start_control_panels():
    threading.Thread(target=create_control_panel, args=("Enterprise",)).start()
    threading.Thread(target=create_control_panel, args=("Voyager",)).start()

if __name__ == "__main__":
    start_control_panels()
