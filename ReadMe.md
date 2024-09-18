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