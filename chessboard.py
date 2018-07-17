# -*- coding:utf-8 -*-
import time
import math
import random
import CONFIG
import copy


class Board(object):
    """
    board for game
    0：空
    1：player1
    2：player2
    """

    def __init__(self, width=9, height=9, n_in_row=5):
        self.width = width
        self.height = height
        self.states = {}  # 记录当前棋盘的状态，键是位置，值是棋子，这里用玩家来表示棋子类型
        self.n_in_row = n_in_row  # 表示几个相同的棋子连成一线算作胜利

    def init_board(self):
        if self.width < self.n_in_row or self.height < self.n_in_row:
            raise Exception('board width and height can not less than %d' % self.n_in_row)  # 棋盘不能过小

        self.availables = list(range(self.width * self.height))  # 表示棋盘上所有合法的位置，这里简单的认为空的位置即合法

        for m in self.availables:
            self.states[m] = -1 # 0表示当前位置为空

    def move_to_location(self, move):
        h = move // self.width
        w = move % self.width
        return [h, w]

    def location_to_move(self, location):
        if len(location) != 2:
            return -1
        h = location[0]
        w = location[1]
        move = h * self.width + w
        if move not in range(self.width * self.height):
            return -1
        return move

    def update(self, player, move):  # player在move处落子，更新棋盘
        self.states[move] = player
        self.availables.remove(move)


class Human(object):
    """
    human player
    """

    def __init__(self, board, player):
        self.board = board
        self.player = player

    def get_action(self):
        # noinspection PyBroadException
        try:
            location = [int(n, 10) for n in raw_input("Your move: ").split(",")]
            move = self.board.location_to_move(location)
        except Exception as e:
            print e
            move = -1
        if move == -1 or move not in self.board.availables:
            print("invalid move")
            move = self.get_action()
        return move

    def has_a_winner(self, board):
        """
        检查是否有玩家获胜
        """
        moved = list(set(range(board.width * board.height)) - set(board.availables))
        if len(moved) < 5 + 2:
            return False, -1

        width = board.width
        height = board.height
        states = board.states
        n = 5
        for m in moved:
            h = m // width
            w = m % width
            player = states[m]

            if (w in range(width - n + 1) and
                    len(set(states[i] for i in range(m, m + n))) == 1):  # 横向连成一线
                return True, player

            if (h in range(height - n + 1) and
                    len(set(states[i] for i in range(m, m + n * width, width))) == 1):  # 竖向连成一线
                return True, player

            if (w in range(width - n + 1) and h in range(height - n + 1) and
                    len(set(states[i] for i in range(m, m + n * (width + 1), width + 1))) == 1):  # 右斜向上连成一线
                return True, player

            if (w in range(n - 1, width) and h in range(height - n + 1) and
                    len(set(states[i] for i in range(m, m + n * (width - 1), width - 1))) == 1):  # 左斜向下连成一线
                return True, player

        return False, -1


    def __str__(self):
        return "Human"


class Node(object):
    def __init__(self, board, player):
        self.board = board
        self.player = player
        self.expandableNum = 0
        self.width = board.width
        self.height = board.height
        self.visitedNum = 0
        self.profit = 0
        self.father = None
        self.expandableNode = []
        self.expandableNode = self.findMoveArea(board)
        self.expandableNum = len(self.expandableNode)
        self.children = {}
        # for i in range(self.width * self.height):
            # if self.board.states[i] == -1:
            #     # expandableNode记录可落子位置
            #     self.expandableNode.append(i)
            #     self.expandableNum += 1
        # self.children = [Node(board, self.player) \
        #                  for i in range(len(board.availables))]
        # for child in (self.children):
        #     child.father = self
    def findMoveArea(self, board):
        specifications = board.height
        states = board.states
        bottom = left = specifications
        top = right = -1
        moveAreaList = []
        for index, key in enumerate(states):
            if states[key] is not -1:
                if key // specifications < bottom:
                    bottom = key // specifications
                if key // specifications > top:
                    top = key // specifications
                if key % specifications < left:
                    left = key % specifications
                if key % specifications > right:
                    right = key % specifications
        if bottom is not 0:
            bottom -= 1
        if left is not 0:
            left -= 1
        if top is not specifications - 1:
            top += 1
        if right is not specifications - 1:
            right += 1
        for i in  xrange(specifications):
            if left <= i <= right:
                for j in xrange(specifications):
                    if bottom <= j <= top:
                        if board.states[j * specifications + i]  is -1:
                            moveAreaList.append(j * specifications + i)
        return moveAreaList

    def isExpandable(self):
        return self.expandableNum > 0

    def rightChange(self,player):
        if player is CONFIG.ELSA:
            return CONFIG.HUMAN
        if player is CONFIG.HUMAN:
            return CONFIG.ELSA

    def expand(self):
        win, player = self.hasWinner(self.board)
        if win:
            return self
        index = random.randint(0,self.expandableNum - 1)
        copyBoard = copy.deepcopy(self.board)
        self.expandableNum -= 1
        move = self.expandableNode.pop(index)
        self.expandableNode.append(move)
        player = self.rightChange(self.player)
        copyBoard.update(player, move)
        self.children[move] = Node(copyBoard, player)
        self.children[move].father = self
        return self.children[move]

    def hasWinner(self, board):
        """
        检查是否有玩家获胜
        """
        moved = list(set(range(board.width * board.height)) - set(board.availables))
        if (len(moved) < 9):
            return False, -1

        width = board.width
        height = board.height
        states = board.states
        n = 5
        for m in moved:
            h = m // width
            w = m % width
            player = states[m]
            states = board.states
            if (w in range(width - n + 1) and
                    len(set(states[i] for i in range(m, m + n))) == 1):  # 横向连成一线
                return True, player

            if (h in range(height - n + 1) and
                    len(set(states[i] for i in range(m, m + n * width, width))) == 1):  # 竖向连成一线
                return True, player

            if (w in range(width - n + 1) and h in range(height - n + 1) and
                    len(set(states[i] for i in range(m, m + n * (width + 1), width + 1))) == 1):  # 右斜向上连成一线
                return True, player

            if (w in range(n - 1, width) and h in range(height - n + 1) and
                    len(set(states[i] for i in range(m, m + n * (width - 1), width - 1))) == 1):  # 左斜向下连成一线
                return True, player

        return False, -1

class UCT(object):
    def __init__(self, board, player):
        self.board = board
        self.startTime = time.time()
        self.player = player

    def BestChild(self, node):
        maxProfitRatio = float('-Inf')
        best = -1
        for index, child in node.children.items():
            print index,
            if child.player is CONFIG.ELSA:
                modifiedProfit = child.profit
            else :
                modifiedProfit = child.profit * -1
            # print index , child.player ,modifiedProfit
            childVisitedNum = child.visitedNum
            # 计算综合收益率
            tempProfitRatio = modifiedProfit * 1.0 / childVisitedNum + \
                math.sqrt(2 * math.log(node.visitedNum) / childVisitedNum) * CONFIG.VITALITY_COEFFICIENT
            print modifiedProfit, childVisitedNum,node.visitedNum,
            print tempProfitRatio
            if tempProfitRatio > maxProfitRatio:
                maxProfitRatio = tempProfitRatio
                best = index
        print
        return best, node.children[best]

    def finallyBestChild(self, node):
        maxProfitRatio = float('-Inf')
        best = -1
        print "final"
        for index, child in node.children.items():
            print index,
            modifiedProfit = child.profit if child.player is CONFIG.ELSA else (child.profit * -1)
            childVisitedNum = child.visitedNum
            print modifiedProfit,childVisitedNum,
            # 计算综合收益率
            tempProfitRatio = modifiedProfit * 1.0 / childVisitedNum + \
                math.sqrt(math.log(node.visitedNum) / childVisitedNum) * CONFIG.VITALITY_COEFFICIENT_F
            print tempProfitRatio
            if tempProfitRatio > maxProfitRatio:
                maxProfitRatio = tempProfitRatio
                best = index
        return best, node.children[best]

    def TreePolicy(self,node):
        while not (node.hasWinner(node.board)[0] and len(node.board.availables) is 0):
            if node.isExpandable():
                # if node.father:
                #     if node.father.father:
                #         print "deep: ",
                #         print node
                return self.Expand(node)
            else:
                index, node = self.BestChild(node)
                # print node,node.expandableNum
        return node
    def Expand(self,node):
        return node.expand()
    def Profit(self, node):
        win, player = node.hasWinner(node.board)
        if win:
            if player is CONFIG.ELSA:
                return 1
            else:
                return -1
        return CONFIG.NOWIN
    def Simulation(self,node):
        currentNode = copy.deepcopy(node)
        profit = self.Profit(currentNode)
        print "profit " + str(profit)
        while profit is CONFIG.NOWIN:
            # 随机落子
            if len(currentNode.board.availables) is 0:
                return 0
            area = currentNode.findMoveArea(currentNode.board)
            move = random.choice(area)
            currentNode.player = currentNode.rightChange(currentNode.player)
            currentNode.board.update(currentNode.player, move)
            profit = self.Profit(currentNode)
            currentNode.profit = profit
        print currentNode.board.states
        return profit
    def Backup(self,node,profit):
        while node:
            node.visitedNum += 1
            node.profit += profit
            node = node.father

    def expandedLayer(self, node):
        layer = 0
        childNodes = copy.deepcopy(node.children)
        while len(childNodes) is not 0:
            print "len(childNodes)  "+str(len(childNodes))
            childNodesCopy = childNodes
            childNodes = []
            for key in childNodesCopy:
                if childNodesCopy[key].expandableNum is not 0 :
                    childNodes.extend(childNodesCopy[key])
            layer += 1
        return layer

    def UCTsearch(self):
        self.root = Node(self.board, self.player)
        while time.time() - self.startTime <= CONFIG.TIME_LIMITATION:
        # while self.expandLayer(self.root) < 3:
            node = self.TreePolicy(self.root)
            deltaProfit = self.Simulation(node)
            self.Backup(node,deltaProfit)
        move, bestNode = self.finallyBestChild(self.root)
        return move


class Elsa(object):
    """
    AI Eisa
    """
    def __init__(self, board, player):
        self.board = board
        self.player = player

    def get_action(self):
        print "Elsa is thinking..."
        ElsaThinking = UCT(self.board, CONFIG.HUMAN)
        move = ElsaThinking.UCTsearch()
        if move == -1 or move not in self.board.availables:
            print("invalid move")
            move = self.get_action()
        return move
    def has_a_winner(self, board):
        """
        检查是否有玩家获胜
        """
        moved = list(set(range(board.width * board.height)) - set(board.availables))
        if (len(moved) < 5 + 2):
            return False, -1

        width = board.width
        height = board.height
        states = board.states
        n = 5
        for m in moved:
            h = m // width
            w = m % width
            player = states[m]

            if (w in range(width - n + 1) and
                    len(set(states[i] for i in range(m, m + n))) == 1):  # 横向连成一线
                return True, player

            if (h in range(height - n + 1) and
                    len(set(states[i] for i in range(m, m + n * width, width))) == 1):  # 竖向连成一线
                return True, player

            if (w in range(width - n + 1) and h in range(height - n + 1) and
                    len(set(states[i] for i in range(m, m + n * (width + 1), width + 1))) == 1):  # 右斜向上连成一线
                return True, player

            if (w in range(n - 1, width) and h in range(height - n + 1) and
                    len(set(states[i] for i in range(m, m + n * (width - 1), width - 1))) == 1):  # 左斜向下连成一线
                return True, player

        return False, -1

class Game(object):
    """
    game server
    """

    def __init__(self, board):
        self.board = board
        self.player = {0:'Elsa', 1:"Challenger"} # player1 and player2
        # self.n_in_row = int(kwargs.get('n_in_row', 5))
        # self.time = float(kwargs.get('time', 5))
        # self.max_actions = int(kwargs.get('max_actions', 1000))
    #
    def start(self):

        self.board.init_board()

        # ai = MCTS(self.board, [p1, p2], self.n_in_row, self.time, self.max_actions)
        # elsa = Elsa()
        human = Human(self.board, CONFIG.HUMAN)
        elsa = Elsa(self.board, CONFIG.ELSA)
        players = {}
        players[CONFIG.ELSA] = elsa
        players[CONFIG.HUMAN] = human
        turn = [CONFIG.ELSA, CONFIG.HUMAN]

        turn.reverse() # 玩家和电脑的交换先手

        while(1):
            p = turn.pop(0)
            turn.append(p)
            player_in_turn = players[p]
            move = player_in_turn.get_action()
            self.board.update(p, move)
            self.graphic(self.board, human, elsa)
            end, winner = self.game_end(elsa)
            if end:
                if winner != -1:
                    print("Game end. Winner is", players[winner])
                break

    def init_player(self):
        plist = list(range(len(self.player)))
        index1 = self.choice(plist)
        plist.remove(index1)
        index2 = self.choice(plist)

        return self.player[index1], self.player[index2]

    def game_end(self, ai):
        """
        检查游戏是否结束
        """
        win, winner = ai.has_a_winner(self.board)
        if win:
            return True, winner
        elif not len(self.board.availables):
            print("Game end. Tie")
            return True, -1
        return False, -1

    def graphic(self, board, human, ai):
        """
        在终端绘制棋盘，显示棋局的状态
        """
        width = board.width
        height = board.height

        print "Human Player", human.player, "with X".rjust(3)
        print "Elsa  Player", ai.player, "with O".rjust(3)
        print
        for x in range(width):
            print "{0:8}".format(x),
        print('\r\n')
        for i in range(height - 1, -1, -1):
            print "{0:4d}".format(i),
            for j in range(width):
                loc = i * width + j
                if board.states[loc] == human.player:
                    print 'X'.center(8),
                elif board.states[loc] == ai.player:
                    print 'O'.center(8),
                else:
                    print '_'.center(8),
            print '\r\n\r\n'
def main():
    b = Board()
    g = Game(b)
    g.start()
if __name__ == '__main__':
    main()