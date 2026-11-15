# Set Dresser

A Maya tool that scatters rocks and trees across a 40×40 ground, keeping them
off a 4-wide path down the middle and out of a round pond. A set dresser uses
it from a window and never needs to open the code.

**Maya 2027** (2026 works too), Python 3, `maya.cmds` only.

## Install

Copy `set_dresser.py` and `set_dresser_ui.py` into your Maya scripts folder.
To find it, run this in the Script Editor (Python tab):

```python
print(cmds.internalVar(userScriptDir=True))
```

## Run it

```python
import set_dresser_ui
set_dresser_ui.show()
```

- **Rocks / Trees**: how many to place.
- **Area**: they land within -Area..Area on X and Z.
- **Keep the path and pond clear**: untick to let them land anywhere.
- **Scatter** adds a set; one Ctrl+Z removes all of it.
- **Clear** deletes the `rocks` and `trees` groups and nothing else. The
  ground, path and pond stay.

## Files

- `set_dresser.py`: the engine. Settings at the top (`PATH_HALF_WIDTH`,
  `POND_CENTER`, `POND_RADIUS`, `AREA`, `GROUND_SIZE`); `make_rock`,
  `make_tree`, `build_ground`, `is_clear`, `scatter`, `clear`. No UI.
- `set_dresser_ui.py`: the window. Reads the controls, calls the engine.
- `send_to_maya.py`: sends one line of Python to an open Maya whose command
  port is on 7001 (`python send_to_maya.py "set_dresser.scatter(10, 4)"`).
- `CLAUDE.md`: the rules the agent followed when building this.
