# peg_solitaire
CS 449 Peg Solitaire Game

## Requirements and Setup

The GUI uses Python's built-in `tkinter` library. On macOS with Homebrew Python 3.14, install the matching Tkinter package before running the GUI:

```bash
brew install python@3.14
brew install python-tk@3.14
```

If Python 3.14 is already installed, only the second command is needed. The `python-tk@3.14` package provides the compiled `_tkinter` module; installing a package named `tkinter` with `pip` will not fix this error.

Create a project virtual environment (if you don't already have one), then run
the GUI from the project directory with:

```bash
python3 -m venv .venv
./.venv/bin/python GUI.py
```

To verify the installation before launching the GUI:

```bash
./.venv/bin/python -c "import tkinter; print(tkinter.TkVersion)"
```

VS Code is configured to use `.venv/bin/python` as this workspace's Python
interpreter. The same interpreter can be used to run the unit tests:

```bash
./.venv/bin/python test_unittest.py
```

## Playing

Choose an odd board size (5, 7, or 9) and a board type, then select
**Start Game**. Click a peg and then an empty hole two spaces away over another
peg to make a jump. English, European, and Diamond boards use horizontal and
vertical jumps; Hexagon boards also allow diagonal jumps along the hexagonal
grid. The counters show pegs remaining and moves made. Use **Undo** to restore
the previous board, or **New Game** to restart with the current settings. The
game ends when no legal jumps remain; leaving one peg is a win.

### Game modes (Sprint 3)

- **Manual**: you make every move. Use **Randomize** at any point to scatter
  the remaining pegs onto random holes without changing the peg count. It
  tries to leave at least one legal jump. **Undo** also reverses a randomize.
- **Automated**: after **Start Game** the computer makes one random legal
  jump every half second until no moves remain.

### Recording and replay

Tick **Record game** before playing. When the game ends it is saved as a text
file in `recordings/` (one line per move, randomize, or undo). Click
**Replay** and choose a file to watch the game play back step by step.

The rules and board state are implemented independently of Tkinter in
`game.py` (`PegSolitaireGame` base class with `ManualGame` and
`AutomatedGame` subclasses); `recorder.py` saves and replays games; `GUI.py`
handles only the user interface.
