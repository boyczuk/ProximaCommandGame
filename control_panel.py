import tkinter as tk
from game import command_queue
import threading

game_instance = None

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

        for i in range(target_listbox.size()):
            if target_listbox.get(i).startswith(selected_target):
                target_listbox.selection_set(i)
                break

def create_control_panel(ship_name):
    root = tk.Tk()
    root.title(f"Control Panel - {ship_name}")

    weapons_frame = tk.LabelFrame(root, text="Weapons")
    weapons_frame.pack(fill="both", expand="yes")
    science_frame = tk.LabelFrame(root, text="Science")
    science_frame.pack(fill="both", expand="yes")
    helm_frame = tk.LabelFrame(root, text="Helm")
    helm_frame.pack(fill="both", expand="yes")
    engineering_frame = tk.LabelFrame(root, text="Engineering")
    engineering_frame.pack(fill="both", expand="yes")

    # Weapons section
    target_listbox = tk.Listbox(weapons_frame)
    target_listbox.pack()

    selected_target = ""

    def on_select(evt):
        nonlocal selected_target
        w = evt.widget
        if w.curselection():
            index = int(w.curselection()[0])
            selected_target = w.get(index).split()[0]
            post_command(ship_name, f"SELECT {selected_target}")

    target_listbox.bind('<<ListboxSelect>>', on_select)

    def fire_command():
        if selected_target and " (target unavailable)" not in selected_target:
            post_command(ship_name, f"FIRE {selected_target}")

    tk.Button(weapons_frame, text="Fire", command=fire_command).pack()

    # Science section
    shield_button = tk.Button(science_frame, text="Raise Shields", command=lambda: post_command(ship_name, "TOGGLE_SHIELDS"))
    shield_button.pack()

    def update_shield_button():
        ship = game_instance.ships[ship_name]
        if ship.shield_cooldown or ship.deactivated or ship.disabled_consoles["shields"]:
            shield_button.config(state="disabled")
        else:
            shield_button.config(state="normal")
        root.after(1000, update_shield_button)

    root.after(1000, update_shield_button)

    # Helm section
    stop_button = tk.Button(helm_frame, text="Stop", command=lambda: post_command(ship_name, "STOP"))
    stop_button.pack()
    partial_speed_button = tk.Button(helm_frame, text="Partial Speed", command=lambda: post_command(ship_name, "PARTIAL"))
    partial_speed_button.pack()
    full_speed_button = tk.Button(helm_frame, text="Full Speed", command=lambda: post_command(ship_name, "FULL"))
    full_speed_button.pack()
    left_button = tk.Button(helm_frame, text="Turn Left", command=lambda: post_command(ship_name, "LEFT"))
    left_button.pack()
    right_button = tk.Button(helm_frame, text="Turn Right", command=lambda: post_command(ship_name, "RIGHT"))
    right_button.pack()

    def update_helm_buttons():
        ship = game_instance.ships[ship_name]
        state = "normal" if not ship.deactivated and not ship.disabled_consoles["helm"] else "disabled"
        stop_button.config(state=state)
        partial_speed_button.config(state=state)
        full_speed_button.config(state=state)
        left_button.config(state=state)
        right_button.config(state=state)
        root.after(1000, update_helm_buttons)

    root.after(1000, update_helm_buttons)

    # Engineering section
    def repair_console(console):
        post_command(ship_name, f"REPAIR {console}")

    tk.Button(engineering_frame, text="Repair Helm", command=lambda: repair_console("helm")).pack()
    tk.Button(engineering_frame, text="Repair Shields", command=lambda: repair_console("shields")).pack()
    tk.Button(engineering_frame, text="Repair Weapons", command=lambda: repair_console("weapons")).pack()

    def restore_power():
        post_command(ship_name, "RESTORE_POWER")

    restore_power_button = tk.Button(engineering_frame, text="Restore Power", command=restore_power)
    restore_power_button.pack()

    def update_restore_power_button():
        ship = game_instance.ships[ship_name]
        if ship.power_cooldown:
            restore_power_button.config(state="disabled")
        else:
            restore_power_button.config(state="normal")
        root.after(1000, update_restore_power_button)

    root.after(1000, update_restore_power_button)

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
