# peg_solitaire
CS 449 Peg Solitaire Game

## Requirements and Setup

The GUI uses Python's built-in `tkinter` library. On macOS with Homebrew Python 3.14, install the matching Tkinter package before running the GUI:

```bash
brew install python@3.14
brew install python-tk@3.14
```

If Python 3.14 is already installed, only the second command is needed. The `python-tk@3.14` package provides the compiled `_tkinter` module; installing a package named `tkinter` with `pip` will not fix this error.

Run the GUI from the project directory with:

```bash
python3 GUI.py
```

To verify the installation before launching the GUI:

```bash
python3 -c "import tkinter; print(tkinter.TkVersion)"
```

Run the unit tests with:

```bash
python3 test_unittest.py
```
