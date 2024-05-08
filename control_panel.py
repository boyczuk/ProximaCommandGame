import tkinter as tk
from game import command_queue

def post_command(ship, command):
    command_queue.put((ship, command))

def control_panel():
    root = tk.Tk()
    root.title("Control Panel")

    tk.Button(root, text="Ship 1 Up", command=lambda: post_command("Enterprise", "UP")).pack()
    tk.Button(root, text="Ship 1 Down", command=lambda: post_command("Enterprise", "DOWN")).pack()
    tk.Button(root, text="Ship 1 Left", command=lambda: post_command("Enterprise", "LEFT")).pack()
    tk.Button(root, text="Ship 1 Right", command=lambda: post_command("Enterprise", "RIGHT")).pack()

    tk.Button(root, text="Ship 2 Up", command=lambda: post_command("Voyager", "UP")).pack()
    tk.Button(root, text="Ship 2 Down", command=lambda: post_command("Voyager", "DOWN")).pack()
    tk.Button(root, text="Ship 2 Left", command=lambda: post_command("Voyager", "LEFT")).pack()
    tk.Button(root, text="Ship 2 Right", command=lambda: post_command("Voyager", "RIGHT")).pack()

    root.mainloop()

if __name__ == "__main__":
    control_panel()
