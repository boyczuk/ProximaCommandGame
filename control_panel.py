import tkinter as tk
from game import command_queue
import threading

game_instance = None  # This will be set in the main.py

def post_command(ship, command):
    command_queue.put((ship, command))

def update_target_list(ship_name, target_listbox, selected_target, radius=100):
    target_listbox.delete(0, tk.END)
    if game_instance:
        targetable_enemies = game_instance.get_targetable_enemies(ship_name, radius)
        for enemy in game_instance.ships:
            if enemy == ship_name:
                continue
            display_name = enemy
            if enemy not in targetable_enemies:
                display_name += " (target unavailable)"
            target_listbox.insert(tk.END, display_name)

        # Reselect the previously selected target if it still exists
        for i in range(target_listbox.size()):
            if target_listbox.get(i).startswith(selected_target):
                target_listbox.selection_set(i)
                break

def create_control_panel(ship_name):
    root = tk.Tk()
    root.title(f"Control Panel - {ship_name}")

    tk.Button(root, text="Stop", command=lambda: post_command(ship_name, "STOP")).pack()
    tk.Button(root, text="Partial Speed", command=lambda: post_command(ship_name, "PARTIAL")).pack()
    tk.Button(root, text="Full Speed", command=lambda: post_command(ship_name, "FULL")).pack()
    tk.Button(root, text="Turn Left", command=lambda: post_command(ship_name, "LEFT")).pack()
    tk.Button(root, text="Turn Right", command=lambda: post_command(ship_name, "RIGHT")).pack()

    target_listbox = tk.Listbox(root)
    target_listbox.pack()

    selected_target = ""

    def on_select(evt):
        nonlocal selected_target
        w = evt.widget
        if w.curselection():
            index = int(w.curselection()[0])
            selected_target = w.get(index).split()[0]  # Store the selected target's name
            post_command(ship_name, f"SELECT {selected_target}")  # Send SELECT command to game

    target_listbox.bind('<<ListboxSelect>>', on_select)

    def fire_command():
        if selected_target and " (target unavailable)" not in selected_target:
            post_command(ship_name, f"FIRE {selected_target}")

    tk.Button(root, text="Fire", command=fire_command).pack()

    def update_targets():
        update_target_list(ship_name, target_listbox, selected_target)
        root.after(1000, update_targets)  # Schedule next update

    root.after(1000, update_targets)  # Start the first update
    root.mainloop()

def start_control_panels():
    threading.Thread(target=create_control_panel, args=("Enterprise",)).start()
    threading.Thread(target=create_control_panel, args=("Voyager",)).start()
    threading.Thread(target=create_control_panel, args=("Voq'leth",)).start()
    threading.Thread(target=create_control_panel, args=("Negh'Var",)).start()

if __name__ == "__main__":
    start_control_panels()
