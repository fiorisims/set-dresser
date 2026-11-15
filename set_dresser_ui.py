# set_dresser_ui.py - the window. It reads its controls and calls the engine.
# Nothing in here makes Maya objects or decides where things go.
#
#   import set_dresser_ui
#   set_dresser_ui.show()

import maya.cmds as cmds

import set_dresser

WIN = "setDresserAgentWin"
SIZE = (420, 275)


def read_controls():
    """The four values the set dresser chose in the window."""
    return dict(
        rocks=cmds.intSliderGrp("sdaRocks", q=True, v=True),
        trees=cmds.intSliderGrp("sdaTrees", q=True, v=True),
        area=cmds.floatSliderGrp("sdaArea", q=True, v=True),
        keep_clear=cmds.checkBox("sdaKeepClear", q=True, v=True),
    )


def on_scatter(*_):
    c = read_controls()
    set_dresser.build_ground()
    set_dresser.scatter(c["rocks"], c["trees"], c["area"], c["keep_clear"])


def on_clear(*_):
    set_dresser.clear()


def show():
    """Open the window. Running it again replaces the window instead of adding one."""
    if cmds.window(WIN, exists=True):
        cmds.deleteUI(WIN)

    cmds.window(WIN, title="Set Dresser", widthHeight=SIZE)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=6, columnOffset=("both", 10))

    cmds.frameLayout(label="How many", marginWidth=6, marginHeight=6)
    cmds.intSliderGrp("sdaRocks", label="Rocks", field=True, min=0, max=200, value=30)
    cmds.intSliderGrp("sdaTrees", label="Trees", field=True, min=0, max=60, value=12)
    cmds.setParent("..")

    cmds.frameLayout(label="Where", marginWidth=6, marginHeight=6)
    cmds.floatSliderGrp("sdaArea", label="Area", field=True, min=4.0, max=20.0, value=set_dresser.AREA)
    cmds.checkBox("sdaKeepClear", label="Keep the path and pond clear", value=True)
    cmds.setParent("..")

    cmds.separator(height=8, style="none")
    cmds.button(label="Scatter", height=36, command=on_scatter)
    cmds.button(label="Clear", command=on_clear)

    cmds.showWindow(WIN)
    # Maya remembers a window's size by name; set it after showing so the buttons are never cut off.
    cmds.window(WIN, e=True, widthHeight=SIZE)
