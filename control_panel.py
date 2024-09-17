import os
from logging import root
import sys
import tkinter as tk
from game import command_queue
import threading
from pynput import keyboard
import serial

game_instance = None

def quit_game():
    global root
    root.quit()
    root.destroy()
    os._exit(0)



def restart_game():
    global root
    root.quit()
    root.destroy()
    python = sys.executable
    os.execl(python, f'"{python}"', *sys.argv)


# Initialize Serial Connection
#ser = serial.Serial('COM3', 9600)  # Replace with actual COM port

# Function to post commands to the game
def post_command(ship, command):
    command_queue.put((ship, command))

"""def check_serial():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        if line == "PARTIAL":
            post_command(ship_name, "PARTIAL")
        # Add more checks as needed
    root.after(50, check_serial)  # Continuously check the serial port every 50ms
"""
def update_target_list(ship_name, target_listbox, radius=100):
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

        current_ship = game_instance.ships[ship_name]
        selected_target = current_ship.selected_target

        # Check if selected_target is None before attempting to call startswith
        if selected_target:
            for i in range(target_listbox.size()):
                if target_listbox.get(i).startswith(selected_target):
                    target_listbox.selection_set(i)
                    break



def create_control_panel(ship_name, position_index):
    global root
    root = tk.Tk()
    root.title(f"Control Panel - {ship_name}")

    # Set window position
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 400
    window_height = 600
    columns = 2
    x = (position_index % columns) * window_width
    y = (position_index // columns) * window_height
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

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

    def on_select(evt):
        w = evt.widget
        if w.curselection():
            index = int(w.curselection()[0])
            selected_target = w.get(index).split()[0]
            current_ship = game_instance.ships[ship_name]
            current_ship.selected_target = selected_target  # Set selected target for this ship
            post_command(ship_name, f"SELECT {selected_target}")


    target_listbox.bind('<<ListboxSelect>>', on_select)

    def fire_command():
        current_ship = game_instance.ships[ship_name]  # Get the ship instance
        selected_target = current_ship.selected_target  # Get the selected target for this ship

        if selected_target and " (target unavailable)" not in selected_target:
            post_command(ship_name, f"FIRE {selected_target}")


    fire_button = tk.Button(weapons_frame, text="Fire", command=fire_command)
    fire_button.pack()

    repair_weapons_button = tk.Button(weapons_frame, text="Repair Weapons", command=lambda: post_command(ship_name, "REPAIR weapons"))
    repair_weapons_button.pack()

    def update_weapons_buttons():
        ship = game_instance.ships[ship_name]
        state = "normal" if not ship.deactivated and not ship.disabled_consoles["weapons"] else "disabled"
        fire_button.config(state=state)
        
        # Repair button is always enabled
        repair_weapons_button.config(state="normal")
        
        root.after(1000, update_weapons_buttons)


    root.after(1000, update_weapons_buttons)

    # Science section
    shield_button = tk.Button(science_frame, text="Raise Shields", command=lambda: post_command(ship_name, "TOGGLE_SHIELDS"))
    shield_button.pack()

    repair_shields_button = tk.Button(science_frame, text="Repair Shields", command=lambda: post_command(ship_name, "REPAIR shields"))
    repair_shields_button.pack()

    def update_science_buttons():
        ship = game_instance.ships[ship_name]
        state = "normal" if not ship.deactivated and not ship.disabled_consoles["shields"] else "disabled"
        shield_button.config(state=state)
        
        # Repair button is always enabled
        repair_shields_button.config(state="normal")
        
        root.after(1000, update_science_buttons)


    root.after(1000, update_science_buttons)

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

    repair_helm_button = tk.Button(helm_frame, text="Repair Helm", command=lambda: post_command(ship_name, "REPAIR helm"))
    repair_helm_button.pack()

    def update_helm_buttons():
        ship = game_instance.ships[ship_name]
        state = "normal" if not ship.deactivated and not ship.disabled_consoles["helm"] else "disabled"
        stop_button.config(state=state)
        partial_speed_button.config(state=state)
        full_speed_button.config(state=state)
        left_button.config(state=state)
        right_button.config(state=state)
        
        # Repair button is always enabled
        repair_helm_button.config(state="normal")
        
        root.after(1000, update_helm_buttons)


    root.after(1000, update_helm_buttons)

    # Engineering section
    def activate_powerup(powerup_type, button):
        post_command(ship_name, f"ACTIVATE {powerup_type}")
        button.destroy()

    powerup_buttons = {}

    def update_powerup_buttons():
        ship = game_instance.ships[ship_name]
        for powerup_type in ship.collected_powerups:
            if powerup_type not in powerup_buttons:
                def make_command(pt=powerup_type):
                    return lambda: activate_powerup(pt, powerup_buttons[pt])
                button = tk.Button(engineering_frame, text=f"Activate {powerup_type}", command=make_command())
                button.pack()
                powerup_buttons[powerup_type] = button
        ship.collected_powerups.clear()
        root.after(1000, update_powerup_buttons)

    root.after(1000, update_powerup_buttons)

    def collect_powerup():
        post_command(ship_name, "COLLECT_POWERUP")

    collect_powerup_button = tk.Button(engineering_frame, text="Collect Powerup", command=collect_powerup)
    collect_powerup_button.pack()

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
        update_target_list(ship_name, target_listbox)
        root.after(1000, update_targets)  # Schedule next update

    root.after(1000, update_targets)  # Start the first update

    # Key bindings
    def key_pressed(event):
        key = event.keysym.lower()
        if key == 'space':
            fire_command()
        elif key == 'r':
            shield_button.invoke()
        elif key == 's':
            stop_button.invoke()
        elif key == 'w':
            partial_speed_button.invoke()
        elif key == 'f':
            full_speed_button.invoke()
        elif key == 'a':
            left_button.invoke()
        elif key == 'd':
            right_button.invoke()
        elif key == 'h':
            repair_helm_button.invoke()
        elif key == 'e':
            repair_shields_button.invoke()
        elif key == 'q':
            repair_weapons_button.invoke()
        elif key == 'c':
            collect_powerup_button.invoke()
        elif key == 'p':
            restore_power_button.invoke()

    root.bind("<Key>", key_pressed)

    # check_serial()
    
    # Quit Button
    quit_button = tk.Button(root, text="Quit", command=quit_game)
    quit_button.pack(side=tk.BOTTOM, fill=tk.X)

    # Restart Button
    restart_button = tk.Button(root, text="Restart", command=restart_game)
    restart_button.pack(side=tk.BOTTOM, fill=tk.X)

    root.mainloop()

def start_control_panel(ship_name):
    threading.Thread(target=create_control_panel, args=(ship_name, 0)).start()
