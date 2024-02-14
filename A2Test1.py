import math
import Physics

table = Physics.Table()

pos = Physics.Coordinate()
pos.x = Physics.PHYLIB_TABLE_WIDTH / 2.0 - math.sqrt(Physics.PHYLIB_BALL_DIAMETER * Physics.PHYLIB_BALL_DIAMETER / 2.0)
pos.y = Physics.PHYLIB_TABLE_WIDTH / 2.0 - math.sqrt(Physics.PHYLIB_BALL_DIAMETER * Physics.PHYLIB_BALL_DIAMETER / 2.0)
sb = Physics.StillBall(1, pos)

pos = Physics.Coordinate()
pos.x = Physics.PHYLIB_TABLE_WIDTH / 2.0
pos.y = Physics.PHYLIB_TABLE_LENGTH - Physics.PHYLIB_TABLE_WIDTH / 2.0
vel = Physics.Coordinate()
vel.x = 0.0
vel.y = -1000.0  # 1m/s (medium speed)
acc = Physics.Coordinate()
acc.x = 0.0
acc.y = 180.0
rb = Physics.RollingBall(0, pos, vel, acc)

table += sb
table += rb

print(table)

while table:
    table = table.segment()
    print(table)
