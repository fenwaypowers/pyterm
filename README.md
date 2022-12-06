# pyterm
pyterm is a "virtual terminal" that runs inside of Python. It works by getting user input and then passing it to a subprocess.

This is intended for use with terminals that may not display a modern linux terminal correctly. In my case, my goal was to have this work with an old Wyse WY-50 terminal that doesn't have VT-100 emulation, making it difficult to run a modern linux terminal on it. There are many visual glitches, but this python script attempts to hide those glitches.

## Prerequisites: 

* [Python3](https://www.python.org/)

## Example Use:
To run, simply execute `python3 pyterm.py`

## Custom arguments:
There is one optional argument, which is `--no-fullscreen`. This makes it so that the terminal won't automatically clear after a "fullscreen" application (listed in the `.flscrn.json` file) is run.
