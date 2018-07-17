from random import *
import time
import CONFIG
import copy
import math
modifiedProfit = 7
childVisitedNum  = 12
states = {0: -1, 1: 1, 2: -1, 3: 0, 4: 0, 5: 0, 6: 1, 7: 1, 8: -1, 9: -1, 10: -1, 11: 0, 12: -1, 13: 1, 14: 0, 15: -1, 16: 1, 17: 0, 18: 1, 19: -1, 20: 1, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 1, 27: -1, 28: 0, 29: 1, 30: 0, 31: 1, 32: 0, 33: -1, 34: -1, 35: -1, 36: -1, 37: -1, 38: 1, 39: 0, 40: 1, 41: -1, 42: 1, 43: -1, 44: -1, 45: -1, 46: 0, 47: 1, 48: 0, 49: 1, 50: -1, 51: 0, 52: 1, 53: -1, 54: -1, 55: 1, 56: -1, 57: -1, 58: 1, 59: 1, 60: -1, 61: -1, 62: 0, 63: 1, 64: 1, 65: 0, 66: 1, 67: -1, 68: 0, 69: -1, 70: -1, 71: -1, 72: 0, 73: -1, 74: -1, 75: 1, 76: -1, 77: 0, 78: -1, 79: 1, 80: 0}

class board():
    def __init__(self, width=9, height=9, n_in_row=5):
        self.width = width
        self.height = height
        self.states = {}
def graphic():

    width = 9
    height = 9

    print "Human Player", 1, "with X".rjust(3)
    print "Elsa  Player", 0, "with O".rjust(3)
    print
    for x in range(width):
        print "{0:8}".format(x),
    print('\r\n')
    for i in range(height - 1, -1, -1):
        print "{0:4d}".format(i),
        for j in range(width):
            loc = i * width + j
            if states[loc] == 1:
                print 'X'.center(8),
            elif states[loc] == 0:
                print 'O'.center(8),
            else:
                print '_'.center(8),
        print '\r\n\r\n'

def has_a_winner(board):
    moved = list(set(range(board.width * board.height)) - set(board.availables))
    if len(moved) < 5 + 2:
        return False, -1
    print moved
    width = board.width
    height = board.height
    states = board.states
    n = 5
    for m in moved:
        h = m // width
        w = m % width
        player = states[m]


        if (w in range(width - n + 1) and
                len(set(states[i] for i in range(m, m + n))) == 1):
            return True, player

        if (h in range(height - n + 1) and
                len(set(states[i] for i in range(m, m + n * width, width))) == 1):
            return True, player

        if (w in range(width - n + 1) and h in range(height - n + 1) and
                len(set(states[i] for i in range(m, m + n * (width + 1), width + 1))) == 1):
            return True, player

        if (w in range(n - 1, width) and h in range(height - n + 1) and
                len(set(states[i] for i in range(m, m + n * (width - 1), width - 1))) == 1):
            return True, player

    return False, -1

graphic()
b = board()
b.availables  = []
b.states = states
for k in states:
    if states[k] ==-1:
        b.availables.append(k)
print has_a_winner(b)[0]
