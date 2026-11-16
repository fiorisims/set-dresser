# set_dresser.py - the engine. No UI in here: the window only reads its
# controls and calls these functions.
#
#   import set_dresser
#   set_dresser.build_ground()
#   set_dresser.scatter(rocks=30, trees=12)

import math
import random

import maya.cmds as cmds

# Settings: the rules of this set, in one place.
GROUND_SIZE = 40.0            # the ground is GROUND_SIZE x GROUND_SIZE, centred on the origin
PATH_HALF_WIDTH = 2.0         # the path is 4 wide, along Z through x = 0
PATH_MARGIN = 1.0             # keep everything at least this far back from the path's edges
POND_CENTER = (10.0, 10.0)    # x, z
POND_RADIUS = 6.0
AREA = 18.0                   # rocks and trees land within -AREA..AREA


# ---------- one thing at a time ----------

def paint(obj, kind, r, g, b):
    """Give obj the flat colour for its kind. One shader per kind, made once."""
    shader = kind + "_mat"
    if not cmds.objExists(shader):
        shader = cmds.shadingNode("lambert", asShader=True, n=shader)
        cmds.setAttr(shader + ".color", r, g, b, type="double3")
        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, n=shader + "SG")
        cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader")
    cmds.sets(obj, e=True, forceElement=shader + "SG")


def make_rock(x, z, size=1.0):
    """A low-poly sphere, squashed and spun so it reads as a rock. Returns its name."""
    rock = cmds.polySphere(r=0.5, sx=6, sy=4, n="rock")[0]
    cmds.scale(size * random.uniform(0.8, 1.6),
               size * random.uniform(0.4, 0.9),
               size * random.uniform(0.8, 1.6), rock)
    cmds.rotate(0, random.uniform(0, 360), 0, rock)
    cmds.move(x, 0, z, rock)
    paint(rock, "rock", 0.42, 0.40, 0.37)
    return rock


def make_tree(x, z, height=3.0):
    """A trunk and a canopy, grouped so the tree moves as one thing. Returns the group."""
    trunk = cmds.polyCylinder(r=height * 0.06, h=height * 0.5, n="trunk")[0]
    cmds.move(0, height * 0.25, 0, trunk)
    canopy = cmds.polyCone(r=height * 0.35, h=height * 0.7, n="canopy")[0]
    cmds.move(0, height * 0.85, 0, canopy)
    paint(trunk, "trunk", 0.36, 0.24, 0.14)
    paint(canopy, "canopy", 0.18, 0.42, 0.20)
    tree = cmds.group(trunk, canopy, n="tree")
    cmds.move(x, 0, z, tree)
    return tree


def build_ground():
    """The ground, the path and the pond. Skips anything that already exists."""
    if not cmds.objExists("ground"):
        ground = cmds.polyPlane(w=GROUND_SIZE, h=GROUND_SIZE, sx=1, sy=1, n="ground")[0]
        paint(ground, "ground", 0.33, 0.38, 0.22)
    if not cmds.objExists("path"):
        path = cmds.polyPlane(w=PATH_HALF_WIDTH * 2, h=GROUND_SIZE, sx=1, sy=1, n="path")[0]
        cmds.move(0, 0.02, 0, path)
        paint(path, "path", 0.62, 0.55, 0.40)
    if not cmds.objExists("pond"):
        pond = cmds.polyCylinder(r=POND_RADIUS, h=0.04, n="pond")[0]
        cmds.move(POND_CENTER[0], 0.02, POND_CENTER[1], pond)
        paint(pond, "pond", 0.22, 0.36, 0.48)


# ---------- the rules ----------

def is_clear(x, z):
    """True when (x, z) is at least PATH_MARGIN back from the path and out of the pond."""
    on_path = abs(x) < PATH_HALF_WIDTH + PATH_MARGIN
    in_pond = math.hypot(x - POND_CENTER[0], z - POND_CENTER[1]) < POND_RADIUS
    return not on_path and not in_pond


def group_for(name):
    """The group that holds everything of one kind. Made on first use."""
    if not cmds.objExists(name):
        cmds.group(empty=True, n=name)
    return name


# ---------- many at once ----------

def scatter_rocks(count, area=AREA, keep_clear=True):
    """Place `count` rocks at random under `rocks`. Returns how many were placed."""
    grp = group_for("rocks")
    placed = 0
    tries = 0
    while placed < count and tries < count * 20:   # capped: never hangs Maya
        tries += 1
        x = random.uniform(-area, area)
        z = random.uniform(-area, area)
        if keep_clear and not is_clear(x, z):
            continue
        cmds.parent(make_rock(x, z, size=random.uniform(0.5, 1.5)), grp)
        placed += 1
    return placed


def scatter_trees(count, area=AREA, keep_clear=True):
    """Place `count` trees at random under `trees`. Returns how many were placed."""
    grp = group_for("trees")
    placed = 0
    tries = 0
    while placed < count and tries < count * 20:
        tries += 1
        x = random.uniform(-area, area)
        z = random.uniform(-area, area)
        if keep_clear and not is_clear(x, z):
            continue
        cmds.parent(make_tree(x, z, height=random.uniform(2.5, 4.5)), grp)
        placed += 1
    return placed


def scatter(rocks=30, trees=12, area=AREA, keep_clear=True, seed=None):
    """The whole scatter as one undo step. Returns (rocks placed, trees placed).
    The same seed with the same settings places the same set every time."""
    if seed is not None:
        random.seed(seed)   # every random.uniform after this follows the same sequence
    cmds.undoInfo(openChunk=True, chunkName="set_dresser_scatter")
    try:
        return scatter_rocks(rocks, area, keep_clear), scatter_trees(trees, area, keep_clear)
    finally:
        cmds.undoInfo(closeChunk=True)


def clear():
    """Delete only what scatter made: the rocks and trees groups. The ground stays."""
    gone = 0
    for name in ("rocks", "trees"):
        if cmds.objExists(name):
            cmds.delete(name)
            gone += 1
    if gone == 0:
        cmds.warning("Nothing to clear.")
