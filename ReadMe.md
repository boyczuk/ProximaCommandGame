### Proxima Command
This project was a proof-of-concept software designed to work with CircuitPython-coded Raspberry PIs. The overall goal was to have 4-8 players in two physically separate rooms as teams each controlling one ship in a starship simulation battlefield. The code in this repository is designed to be a foundation or general structure to manage the game state as well as the individual actions of the players on the hardware consoles (controlled with Raspberry PIs).

https://proximacommand.com/
![image](https://github.com/user-attachments/assets/81bc41b6-5f52-46de-aa42-2839da8299a4)
![image](https://github.com/user-attachments/assets/1e941d8f-ee71-40f1-becb-b82100d38df8)
![image](https://github.com/user-attachments/assets/2742ab4f-9043-43ab-bf0c-78b71eca1c9e)
![image](https://github.com/user-attachments/assets/bbff72c2-38d6-4fac-a3ff-81cc49eb804f)


### Run app
`python.exe main.py`

main.py connects and runs everything together

game.py stores the actual games data and information about the ships

control_panel.py will need to be modified to connect to the physical consoles, but curently has the controls for the ships

to package as .exe run `python -m PyInstaller --onefile --windowed main.py` from root
