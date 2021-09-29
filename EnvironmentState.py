# DO NOT MODIFY SnakeBodyAttr
# A class to represent the lines that define the snake's current orientation.
# x1,y1 -> Starting coordinate of the line. For example, if it is the "head" line, (x1,y1) represent the tip of the head.
# x2,y2 -> End coordinate of the line.
# (x1_incr,y1_incr) and (x2_incr,y2_incr) determines the movement of the start point and end point of the line respectively. The movement based on the value is defined at the end.
# x1_incr ∊ [-1,0,1] This value will be added to x1 at every loop. 
# x2_incr ∊ [-1,0,1] This value will be added to x2 at every loop. 
# y1_incr ∊ [-1,0,1] This value will be added to y1 at every loop. 
# y2_incr ∊ [-1,0,1] This value will be added to y2 at every loop.
# x1_incr * y1_incr = x2_incr * y2_incr = 0 
# Example: If the snake has single line at (100,100) - (100,110), x1_incr=0,y1_incr=-1, x2_incr=0,y2_incr=-1. The length of the snake is 10 and it
# is moving upwards. After one loop, the new line will be (100,99) - (100,109).

#   x1_incr/x2_incr     |      y1_incr/y2_incr      |       Direction
#           0           |           1               |       Down
#           0           |          -1               |       Up
#           1           |           0               |       Right
#          -1           |           0               |       Left      
class SnakeBodyAttr:
    def __init__(self,data):
        self.x1=data[0]
        self.y1=data[1]
        self.x2=data[2]
        self.y2=data[3]
        self.x1_incr=data[4]
        self.y1_incr=data[5]
        self.x2_incr=data[6]
        self.y2_incr=data[7]


# A class to represent the state of the environment. 
# 1. It is a col_dim x row_dim area, whithin which our snake can roam freely. 
# 2. If the snake passes through the border, it will emerge from the opposite side.
# 3. The food will spawn randomly without colliding the snakes body.
#   Example: col_dim=5 row_dim=3
#   |   |   |   |   |   |
#   |   |   |   |   |   |
#   |   |   |   |   |   |

#You can modify the state class as you want. However, the 'data' parameter in setState function will not change.
class State:
    col_dim=-1
    row_dim=-1
    def __init__(self):
        self.food=(-1,-1)
        self.body=[]
    # data -> (food,list of lines)
    def setState(self,data):
        self.food=data[0]
        self.body=[SnakeBodyAttr(line) for line in data[1]]

    def getHeadLen(self):
        return abs(self.body[0].x1-self.body[0].x2) + abs(self.body[0].y1-self.body[0].y2)

    def __lt__(self, other):
        return self.getHeadLen() < other.getHeadLen()