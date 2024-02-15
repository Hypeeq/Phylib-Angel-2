import math
import Physics

def print_object(object):
    if object is None:
        print("NULL;")
        return

    if object.type == PHYLIB_STILL_BALL:
        print(f"STILL_BALL ({object.obj.still_ball.number},{object.obj.still_ball.pos.x},{object.obj.still_ball.pos.y})")
    elif object.type == PHYLIB_ROLLING_BALL:
        print(f"ROLLING_BALL ({object.obj.rolling_ball.number},{object.obj.rolling_ball.pos.x},{object.obj.rolling_ball.pos.y},{object.obj.rolling_ball.vel.x},{object.obj.rolling_ball.vel.y},{object.obj.rolling_ball.acc.x},{object.obj.rolling_ball.acc.y})")
    elif object.type == PHYLIB_HOLE:
        print(f"HOLE ({object.obj.hole.pos.x},{object.obj.hole.pos.y})")
    elif object.type == PHYLIB_HCUSHION:
        print(f"HCUSHION ({object.obj.hcushion.y})")
    elif object.type == PHYLIB_VCUSHION:
        print(f"VCUSHION ({object.obj.vcushion.x})")


def print_table(table):
    if table is None:
        print("NULL")
        return

    print(f"time = {table.time};")
    for i in range(MAX_OBJECTS):
        print(f"  [{i:02d}] = ", end="")
        print_object(table.object[i])


def main():
    table = Physics.Table()  # Corrected line

    # create a still ball 1/4 of the way "down" the middle of the table,
    # shift it up, and to the left just a little bit
    pos = Coordinate(6.0, 1.0)  # Provide x and y coordinates
    pos.x = TABLE_WIDTH / 2.0 - (BALL_DIAMETER ** 0.5 / 2.0)
    pos.y = TABLE_WIDTH / 2.0 - (BALL_DIAMETER ** 0.5 / 2.0)
    sb = StillBall(1, pos)

    # create a rolling ball 3/4 of the way "down the table,
    # rolling up along the centre
    pos.x = TABLE_WIDTH / 2.0
    pos.y = TABLE_LENGTH - TABLE_WIDTH / 2.0
    vel = Coordinate(7.0, 10.0)  # Provide x and y coordinates for velocity
    acc = Coordinate(3.0, 4.0)  # Provide x and y coordinates for acceleration
    vel.x = 0.0
    vel.y = -1000.0  # 1m/s (medium speed)
    acc.x = 0.0
    acc.y = 180.0
    rb = RollingBall(0, pos, vel, acc)

    table += sb
    table += rb

    print_table(table)

    while table:
        new_table = table.segment()
        table = new_table
        print_table(table)


if __name__ == "__main__":
    main()
