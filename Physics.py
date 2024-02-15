import phylib

PHYLIB_BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
PHYLIB_HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS
PHYLIB_TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
PHYLIB_TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH
PHYLIB_SIM_RATE = phylib.PHYLIB_SIM_RATE
PHYLIB_VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON
PHYLIB_DRAG = phylib.PHYLIB_DRAG
PHYLIB_MAX_TIME = phylib.PHYLIB_MAX_TIME
PHYLIB_MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS

BALL_COLOURS = [
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",
    "MEDIUMPURPLE",
    "LIGHTSALMON",
    "LIGHTGREEN",
    "SANDYBROWN",
]

class Coordinate(phylib.phylib_coord):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass


class StillBall(phylib.phylib_object):
    """
    Python StillBall class.
    """

    def __init__(self, number, pos):
        phylib.phylib_object.__init__(
            self,
            phylib.PHYLIB_STILL_BALL,
            number,
            pos,
            None,
            None,
            0.0,
            0.0,
        )
        self.__class__ = StillBall

    def svg(self):
        return f"<circle cx='{self.pos.x}' cy='{self.pos.y}' r='{PHYLIB_BALL_DIAMETER/2}' fill='{BALL_COLOURS[self.number]}' />\n"


class RollingBall(phylib.phylib_object):
    """
    Python RollingBall class.
    """

    def __init__(self, number, pos, vel, acc):
        phylib.phylib_object.__init__(
            self,
            phylib.PHYLIB_ROLLING_BALL,
            number,
            pos,
            None,
            None,
            vel,
            acc,
        )
        self.__class__ = RollingBall

    def svg(self):
        return f"<circle cx='{self.pos.x}' cy='{self.pos.y}' r='{PHYLIB_BALL_DIAMETER/2}' fill='{BALL_COLOURS[self.number]}' />\n"


class Hole(phylib.phylib_object):
    """
    Python Hole class.
    """

    def __init__(self, pos):
        phylib.phylib_object.__init__(
            self, phylib.PHYLIB_HOLE, None, pos, None, None, None, None
        )
        self.__class__ = Hole

    def svg(self):
        return f"<circle cx='{self.pos.x}' cy='{self.pos.y}' r='{PHYLIB_HOLE_RADIUS}' fill='black' />\n"


class HCushion(phylib.phylib_object):
    """
    Python HCushion class.
    """

    def __init__(self, y):
        phylib.phylib_object.__init__(
            self, phylib.PHYLIB_HCUSHION, None, None, None, None, None, None
        )
        self.obj.hcushion.y = y
        self.__class__ = HCushion

    def svg(self):
        return (
            f"<rect width='1400' height='25' x='-25' y='{self.obj.hcushion.y}' fill='darkgreen' />\n"
        )


class VCushion(phylib.phylib_object):
    """
    Python VCushion class.
    """

    def __init__(self, x):
        phylib.phylib_object.__init__(
            self, phylib.PHYLIB_VCUSHION, None, None, None, None, None, None
        )
        self.obj.vcushion.x = x
        self.__class__ = VCushion

    def svg(self):
        return (
            f"<rect width='25' height='2750' x='{self.obj.vcushion.x}' y='-25' fill='darkgreen' />\n"
        )


class Table(phylib.phylib_table):
    """
    Pool table class.
    """

    def __init__(self):
        phylib.phylib_table.__init__(self)
        self.current = -1

    def __iadd__(self, other):
        self.add_object(other)
        return self

    def __iter__(self):
        return self

    def __next__(self):
        self.current += 1
        if self.current < PHYLIB_MAX_OBJECTS:
            return self[self.current]
        self.current = -1
        raise StopIteration

    def __getitem__(self, index):
        result = self.get_object(index)
        if result == None:
            return None
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion
        return result

    def __str__(self):
        result = ""
        result += "time = %6.1f;\n" % self.time
        for i, obj in enumerate(self):
            result += "  [%02d] = %s\n" % (i, obj)
        return result

    def segment(self):
        result = phylib.phylib_table.segment(self)
        if result:
            result.__class__ = Table
            result.current = -1
        return result

    def svg(self):
        svg_str = "<svg xmlns='http://www.w3.org/2000/svg' width='1400' height='2750'>\n"
        for obj in self:
            svg_str += obj.svg()
        svg_str += "</svg>"
        return svg_str


# Implement A2Test2.py to write the svg output to a file
if __name__ == "__main__":
    table = Table()
    # Add objects to the table here
    # Example: table += StillBall(number, Coordinate(x, y))
    with open("table-0.svg", "w") as file:
        file.write(table.svg())
