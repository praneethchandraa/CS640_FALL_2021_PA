
import numpy as np
from NetworkManager import NetworkManager
from EnvironmentState import State, SnakeBodyAttr

from heapq import *


LEFT = bytes.fromhex('00')
UP = bytes.fromhex('01')
RIGHT =  bytes.fromhex('02')
DOWN =  bytes.fromhex('03')
NOOP =  bytes.fromhex('04')


class Controller:
    
    
    
    def __init__(self,ip='localhost',port=4668):
        #Do not Modify
        self.networkMgr=NetworkManager()
        State.col_dim,State.row_dim=self.networkMgr.initiateConnection(ip,port) # Initialize network manager and set environment dimensions
        self.state=State() # Initialize empty state
        self.myInit() # Initialize custom variables
        pass

    #define your variables here
    def myInit(self):
        #TODO

        self.cmds = []
        self.dirMap = {(1, 0): RIGHT, (-1, 0): LEFT, (0, 1): DOWN, (0, -1):UP}
        self.pOP = {
            RIGHT: (UP, DOWN, NOOP),
            LEFT: (UP, DOWN, NOOP),
            UP: (RIGHT, LEFT, NOOP),
            DOWN: (RIGHT, LEFT, NOOP)
        }

        self.cmdIncr = {
            RIGHT: (1, 0),
            LEFT: (-1, 0),
            UP: (0, -1),
            DOWN: (0, 1)
        }

        # Useful lambda functions
        self.collinear = lambda p, p1, p2: (p[0]==p1[0]==p2[0]) or (p[1]==p1[1]==p2[1])
        self.manhattan = lambda p1, p2: abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])
        self.eucledean = lambda p1, p2: ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5
        self.collide = lambda p, p1, p2: self.manhattan(p,p1) + self.manhattan(p,p2) == self.manhattan(p1,p2) \
             if  self.collinear(p, p1, p2) else False    
        self.collison = lambda p, lines: any([self.collide(p, i[0], i[1]) for i in lines])

    def getNextState(self, state, cmd, cmds):
        if cmd != NOOP:
            incr = self.cmdIncr[cmd]
            p = (state.body[0].x1, state.body[0].y1)
            p1 = (p[0]+incr[0], p[1]+incr[1])
            state.body = [SnakeBodyAttr((p1[0], p1[1], p[0], p[1], incr[0], incr[1], 0, 0))] + state.body
        else:
            state.body[0].x1 += state.body[0].x1_incr
            state.body[0].y1 += state.body[0].y1_incr
        
        state.body[-1].x2 += state.body[-1].x2_incr
        state.body[-1].y2 += state.body[-1].y2_incr

        if (state.body[-1].x1-state.body[-1].x2,state.body[-1].y1-state.body[-1].y2) == (0, 0):
            state.body.pop()
            if state.body[-1].x1 == state.body[-1].x2:
                a = state.body[-1].y1-state.body[-1].y2
                state.body[-1].y1_incr = a/abs(a)
            else:
                a = state.body[-1].x1-state.body[-1].x2
                state.body[-1].x1_incr = a/abs(a)

        p = (state.body[0].x1, state.body[0].y1)
        cmds.append(cmd)
        return self.eucledean(p, state.food), state, cmds


    def checkStatus(self, state):
        p = (state.body[0].x1, state.body[0].y1)
        lines = [((i.x1, i.y1), (i.x2, i.y2)) for i in state.body[1:]]

        if self.collison(p, lines):
            return False
        if p == state.food:
            return True

        return 'continue'


    def getCMD(self, state):
        curDir = self.dirMap[(state.body[0].x1_incr, state.body[0].y1_incr)]
        possibleOP = self.pOP[curDir]

        h = []
        for cmd in possibleOP:
            heappush(h, self.getNextState(state, cmd, [cmd]))

        c = 0
        while h:
            print("c: ",  c)
            print(list(zip(*h))[0])
            score, state_, cmd_ = heappop(h)
            print(score)

            truth = self.checkStatus(state_)
            if truth==True:
                self.cmds = cmd_
                return truth
            elif truth == 'continue':
                curDir = self.dirMap[(state_.body[0].x1_incr, state_.body[0].y1_incr)]
                possibleOP = self.pOP[curDir]
                for cmd in possibleOP:
                    heappush(h, self.getNextState(state_, cmd, cmd_))
            c += 1
            if c==10:
                break

        self.cmds.append(NOOP)
            

            


            

        

    #Returns next command selected by the agent.
    def getNextCommand(self):
        #TODO Implement an Intelligent agent that plays the game
        # Hint You will require a collision detection function.
        
        if not self.cmds:
            self.getCMD(self.state)
            self.cmds = self.cmds[::-1]
        return self.cmds.pop()

    def control(self):
        #Do not modify the order of operations.
        # Get current state, check exit condition and send next command.
        while(True):
            # 1. Get current state information from the server
            self.state.setState(self.networkMgr.getStateInfo())
            # 2. Check Exit condition
            if self.state.food==None:
                break
            # 3. Send next command
            self.networkMgr.sendCommand(self.getNextCommand())
        



cntrl=Controller()
cntrl.control()