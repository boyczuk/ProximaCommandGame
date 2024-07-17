import tkinter as tk
from game import command_queue
import threading

game_instance = None  # This will be set in the main.py

def post_command(ship, command):
    command_queue.put((ship, command))

def update_target_list(ship_name, target_listbox, radius=100):
    target_listbox.delete(0, tk.END)
    if game_instance:
        targetable_enemies = game_instance.get_targetable_enemies(ship_name, radius)
        for enemy in targetable_enemies:
            target_listbox.insert(tk.END, enemy)

def create_control_panel(ship_name):
    root = tk.Tk()
    root.title(f"Control Panel - {ship_name}")

    tk.Button(root, text="Stop", command=lambda: post_command(ship_name, "STOP")).pack()
    tk.Button(root, text="Partial Speed", command=lambda: post_command(ship_name, "PARTIAL")).pack()
    tk.Button(root, text="Full Speed", command=lambda: post_command(ship_name, "FULL")).pack()

    target_listbox = tk.Listbox(root)
    target_listbox.pack()

    tk.Button(root, text="Update Targets", command=lambda: update_target_list(ship_name, target_listbox)).pack()
    tk.Button(root, text="Fire", command=lambda: post_command(ship_name, "FIRE" if target_listbox.curselection() else None)).pack()

    root.mainloop()

def start_control_panels():
    threading.Thread(target=create_control_panel, args=("Enterprise",)).start()
    threading.Thread(target=create_control_panel, args=("Voyager",)).start()

if __name__ == "__main__":
    start_control_panels()
