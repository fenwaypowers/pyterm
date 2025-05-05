# pyterm

**pyterm** is a "virtual terminal" that runs inside Python. It collects user input and executes it via subprocess calls, simulating a simplified shell interface.

This tool is especially useful for interacting with serial or legacy terminals that do not support modern terminal emulation. For example, it was designed to work with the **Wyse WY-50**, a terminal lacking VT-100 compatibility, where traditional shells like bash may render incorrectly. PyTerm tries to reduce or hide these visual glitches.

## Prerequisites

- [Python 3.10+](https://www.python.org/)

- [psutil](https://pypi.org/project/psutil/)  
  You can install it with:
  
  `pip install psutil`

## Example Usage

Run the program using:

`python pyterm.py`

## Custom Arguments

PyTerm supports two optional command-line arguments:

- `--no-fullscreen`  
  Disables the automatic screen clearing after running "fullscreen" applications (e.g., `top`, `vim`, `nano`). These are defined in the `.flscrn.json` file.

- `--og-neofetch`  
  Disables PyTerm's custom `neofetch` output (designed to display cleanly on older terminals) and falls back to no output or a basic stub.

## Features

- Cross-platform (Windows and Unix-like systems)

- Command history and history replay (`history`, `history run <index>`)

- Custom `neofetch` for system info (`neofetch` can cause visual glitches on old terminals)

- Supports adding new fullscreen apps using `add-flscrn <command>`

- Safe directory changes with `cd`

## Notes

- On first run, a `.flscrn.json` file will be created in the current directory to track commands considered fullscreen.

- Compatible with minimal environments; requires no external shell utilities beyond Python itself.
