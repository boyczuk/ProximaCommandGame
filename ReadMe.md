### Proxima Command
This project was a proof-of-concept software designed to work with CircuitPython-coded Raspberry PIs. The overall goal was to have 4-8 players in two physically separate rooms as teams each controlling one ship in a starship simulation battlefield. The code in this repository is designed to be a foundation or general structure to manage the game state as well as the individual actions of the players on the hardware consoles (controlled with Raspberry PIs).

### Run app
`python.exe main.py`

main.py connects and runs everything together

game.py stores the actual games data and information about the ships

control_panel.py will need to be modified to connect to the physical consoles, but curently has the controls for the ships

to package as .exe run `python -m PyInstaller --onefile --windowed main.py` from root

### Questions
What are the input/output methods on the hardware?
Do we need specific communication protocols (e.g., serial, USB, TCP/IP)?
What data formats will I be receiving/sending?
Will any drivers or middleware be needed?
Are there any hardware limitations that could affect performance?

[https://github.com/boyczuk/ProximaCommandGame]
