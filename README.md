# dune
Project for Grok to analyze Dune pycharm code
# Dune Board Game Simulator
Networked Python Dune (1979) reimplementation.

## Setup
- `venv\Scripts\activate`
- Server: `python dune_server.py`
- Client: `python dune_client.py --host localhost --house Atreides`

## Features
- Multiplayer (2-6 houses)
- Tkinter GUI with assets
- Mechanics: Spice, battles, treachery

## Modules
- Core: dune_game.py
- Net: dune_server.py/client.py
- Map: planetDune.py
- GUI: dune_gui.py
