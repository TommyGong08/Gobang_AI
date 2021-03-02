'''在alpha-beta剪枝之前单纯做的一个评估函数'''

from enum import IntEnum
import time
from collections import namedtuple

class CHESS_TYPE(IntEnum):
    NONE = 0,
    SLEEP_TWO = 1,
    LIVE_TWO = 2,
    SLEEP_THREE = 3
    LIVE_THREE = 4,
    CHONG_FOUR = 5,
    LIVE_FOUR = 6,
    LIVE_FIVE = 7,


CHESS_TYPE_NUM = 8

FIVE = CHESS_TYPE.LIVE_FIVE.value
FOUR, THREE, TWO = CHESS_TYPE.LIVE_FOUR.value, CHESS_TYPE.LIVE_THREE.value, CHESS_TYPE.LIVE_TWO.value
SFOUR, STHREE, STWO = CHESS_TYPE.CHONG_FOUR.value, CHESS_TYPE.SLEEP_THREE.value, CHESS_TYPE.SLEEP_TWO.value

offset = [(1, 0), (0, 1), (1, 1), (1, -1)]
Chessman = namedtuple('Chessman', 'Name Value Color')
Point = namedtuple('Point', 'X Y')
BLACK_CHESSMAN = Chessman('黑子', 1, (45, 45, 45))
WHITE_CHESSMAN = Chessman('白子', 2, (255, 255, 255))

class ChessAI:
    """
    param: line_points:每行有多少19个点
    chessman：当下下棋方
    """

    def __init__(self, line_points, chessman):
        self.len = line_points
        self._my = chessman
        self._opponent = BLACK_CHESSMAN if chessman == WHITE_CHESSMAN else WHITE_CHESSMAN
        # 水平、竖直、左右斜方向
        self.record = [[[0, 0, 0, 0] for x in range(line_points)] for y in range(line_points)]
        self.count = [[0 for x in range(CHESS_TYPE_NUM)] for i in range(2)]
        self.pos_score = [[(7 - max(abs(x - 7), abs(y - 7))) for x in range(line_points)] for y in range(line_points)]
        # 单纯循环整个棋盘
        self.board = [[0] * line_points for _ in range(line_points)]

    # 每次调用评估函数前都需要清一下之前的统计数据
    def reset(self):
        for y in range(self.len):
            for x in range(self.len):
                for i in range(4):
                    # 四个方向记录清空
                    self.record[y][x][i] = 0

        for i in range(len(self.count)):
            for j in range(len(self.count[0])):
                self.count[i][j] = 0

        self.save_count = 0

    """def isWin(self, board, turn):
        return self.evaluate(board, turn, True)"""

    # 获得对手的棋，也就是电脑玩家鼠标点击的地方
    def get_opponent_drop(self, point):
        self.board[point.Y][point.X] = self._opponent.Value # 1

    # 找到棋盘上空的位置
    def genmove(self,turn):
        moves = []
        for y in range(self.len):
            for x in range(self.len):
                if self.board[y][x] == 0:
                    score = self.pos_score[y][x]
                    moves.append((score, x, y))

        moves.sort(reverse=True)
        return moves

    # 纯依靠评估函数
    def search(self,turn): #turn=2
        moves = self.genmove(1)
        point = None
        max_score = -0x7fffffff
        for score, x, y in moves:
            # 假设下的是(y,x)
            self.board[y][x] = WHITE_CHESSMAN.Value
            # 评估局面
            score = self.evaluate(turn)
            print(score)
            self.board[y][x] = 0

            if score > max_score:
                max_score = score
                # point = Point(x, y)
        return score,x,y

    def findBestChess(self,turn): #turn = 2
        time1 = time.time()
        score, x, y = self.search(turn)
        point = Point(x,y)
        time2 = time.time()
        print('time[%f] (%d, %d), score[%d] save[%d]' % ((time2 - time1), x, y, score, self.save_count))
        self.board[y][x] = WHITE_CHESSMAN.Value
        return point

    #对黑棋白棋进行评分
    # calculate score, FIXME: May Be Improved
    def getScore(self, mine_count, opponent_count):
        mscore, oscore = 0, 0
        if mine_count[FIVE] > 0:
            return (10000, 0)
        if opponent_count[FIVE] > 0:
            return (0, 10000)

        if mine_count[SFOUR] >= 2:
            mine_count[FOUR] += 1

        if opponent_count[FOUR] > 0:
            return (0, 9050)
        if opponent_count[SFOUR] > 0:
            return (0, 9040)

        if mine_count[FOUR] > 0:
            return (9030, 0)
        if mine_count[SFOUR] > 0 and mine_count[THREE] > 0:
            return (9020, 0)

        if opponent_count[THREE] > 0 and mine_count[SFOUR] == 0:
            return (0, 9010)

        if (mine_count[THREE] > 1 and opponent_count[THREE] == 0 and opponent_count[STHREE] == 0):
            return (9000, 0)

        if mine_count[SFOUR] > 0:
            mscore += 2000

        if mine_count[THREE] > 1:
            mscore += 500
        elif mine_count[THREE] > 0:
            mscore += 100

        if opponent_count[THREE] > 1:
            oscore += 2000
        elif opponent_count[THREE] > 0:
            oscore += 400

        if mine_count[STHREE] > 0:
            mscore += mine_count[STHREE] * 10
        if opponent_count[STHREE] > 0:
            oscore += opponent_count[STHREE] * 10

        if mine_count[TWO] > 0:
            mscore += mine_count[TWO] * 4
        if opponent_count[TWO] > 0:
            oscore += opponent_count[TWO] * 4

        if mine_count[STWO] > 0:
            mscore += mine_count[STWO] * 4
        if opponent_count[STWO] > 0:
            oscore += opponent_count[STWO] * 4

        return (mscore, oscore)

    # 评估函数
    def evaluate(self,turn, checkWin=False):
        self.reset()
        # AI是白棋，对手是黑棋
        if turn == 1:
            mine = 1
            opponent = 2
        elif turn == 2:
            mine = 2
            opponent = 1

        for y in range(self.len):
            for x in range(self.len):
                if self.board[y][x] == mine:
                    print("白棋位于(",x,",",y,")")
                    #print(mine)
                    self.evaluatePoint(x, y, mine, opponent)
                elif self.board[y][x] == opponent:
                    print("黑棋位于(", x, ",", y, ")")
                    #print(opponent)
                    self.evaluatePoint(x, y, opponent, mine)

        mine_count = self.count[mine - 1]
        # print(mine_count)
        opponent_count = self.count[opponent - 1]
        # print(opponent_count)
        if checkWin:
            return mine_count[FIVE] > 0
        else:
            mscore, oscore = self.getScore(mine_count, opponent_count)
            return (mscore - oscore)

    # 对一个位置的四个方向进行检查
    def evaluatePoint(self, x, y, mine, opponent):
        dir_offset = [(1, 0), (0, 1), (1, 1), (1, -1)]  # direction from left to right
        for i in range(4):
            if self.record[y][x][i] == 0:
                self.analysisLine(x, y, i, dir_offset[i], mine, opponent, self.count[mine - 1])
            else:
                self.save_count += 1

    # line is fixed len 9: XXXXMXXXX
    def getLine(self, x, y, dir_offset, mine, opponent):
        line = [0 for i in range(9)]

        tmp_x = x + (-5 * dir_offset[0])
        tmp_y = y + (-5 * dir_offset[1])
        for i in range(9):
            tmp_x += dir_offset[0]
            tmp_y += dir_offset[1]
            if (tmp_x < 0 or tmp_x >= self.len or
                    tmp_y < 0 or tmp_y >= self.len):
                line[i] = opponent  # set out of range as opponent chess
            else:
                line[i] = self.board[tmp_y][tmp_x]

        return line

    def analysisLine(self, x, y, dir_index, dir, mine, opponent, count):
        def setRecord(self, x, y, left, right, dir_index, dir_offset):
            tmp_x = x + (-5 + left) * dir_offset[0]
            tmp_y = y + (-5 + left) * dir_offset[1]
            for i in range(left, right):
                tmp_x += dir_offset[0]
                tmp_y += dir_offset[1]
                self.record[tmp_y][tmp_x][dir_index] = 1

        empty = 0
        left_idx, right_idx = 4, 4

        line = self.getLine(x, y, dir, mine, opponent)

        while right_idx < 8:
            if line[right_idx + 1] != mine:
                break
            right_idx += 1
        while left_idx > 0:
            if line[left_idx - 1] != mine:
                break
            left_idx -= 1

        left_range, right_range = left_idx, right_idx
        while right_range < 8:
            if line[right_range + 1] == opponent:
                break
            right_range += 1
        while left_range > 0:
            if line[left_range - 1] == opponent:
                break
            left_range -= 1

        chess_range = right_range - left_range + 1
        if chess_range < 5:
            setRecord(self, x, y, left_range, right_range, dir_index, dir)
            return CHESS_TYPE.NONE

        setRecord(self, x, y, left_idx, right_idx, dir_index, dir)

        m_range = right_idx - left_idx + 1

        # M:mine chess, P:opponent chess or out of range, X: empty
        if m_range == 5:
            count[FIVE] += 1

        # Live Four : XMMMMX
        # Chong Four : XMMMMP, PMMMMX
        if m_range == 4:
            left_empty = right_empty = False
            if line[left_idx - 1] == empty:
                left_empty = True
            if line[right_idx + 1] == empty:
                right_empty = True
            if left_empty and right_empty:
                count[FOUR] += 1
            elif left_empty or right_empty:
                count[SFOUR] += 1

        # Chong Four : MXMMM, MMMXM, the two types can both exist
        # Live Three : XMMMXX, XXMMMX
        # Sleep Three : PMMMX, XMMMP, PXMMMXP
        if m_range == 3:
            left_empty = right_empty = False
            left_four = right_four = False
            if line[left_idx - 1] == empty:
                if line[left_idx - 2] == mine:  # MXMMM
                    setRecord(self, x, y, left_idx - 2, left_idx - 1, dir_index, dir)
                    count[SFOUR] += 1
                    left_four = True
                left_empty = True

            if line[right_idx + 1] == empty:
                if line[right_idx + 2] == mine:  # MMMXM
                    setRecord(self, x, y, right_idx + 1, right_idx + 2, dir_index, dir)
                    count[SFOUR] += 1
                    right_four = True
                right_empty = True

            if left_four or right_four:
                pass
            elif left_empty and right_empty:
                if chess_range > 5:  # XMMMXX, XXMMMX
                    count[THREE] += 1
                else:  # PXMMMXP
                    count[STHREE] += 1
            elif left_empty or right_empty:  # PMMMX, XMMMP
                count[STHREE] += 1

        # Chong Four: MMXMM, only check right direction
        # Live Three: XMXMMX, XMMXMX the two types can both exist
        # Sleep Three: PMXMMX, XMXMMP, PMMXMX, XMMXMP
        # Live Two: XMMX
        # Sleep Two: PMMX, XMMP
        if m_range == 2:
            left_empty = right_empty = False
            left_three = right_three = False
            if line[left_idx - 1] == empty:
                if line[left_idx - 2] == mine:
                    setRecord(self, x, y, left_idx - 2, left_idx - 1, dir_index, dir)
                    if line[left_idx - 3] == empty:
                        if line[right_idx + 1] == empty:  # XMXMMX
                            count[THREE] += 1
                        else:  # XMXMMP
                            count[STHREE] += 1
                        left_three = True
                    elif line[left_idx - 3] == opponent:  # PMXMMX
                        if line[right_idx + 1] == empty:
                            count[STHREE] += 1
                            left_three = True

                left_empty = True

            if line[right_idx + 1] == empty:
                if line[right_idx + 2] == mine:
                    if line[right_idx + 3] == mine:  # MMXMM
                        setRecord(self, x, y, right_idx + 1, right_idx + 2, dir_index, dir)
                        count[SFOUR] += 1
                        right_three = True
                    elif line[right_idx + 3] == empty:
                        # setRecord(self, x, y, right_idx+1, right_idx+2, dir_index, dir)
                        if left_empty:  # XMMXMX
                            count[THREE] += 1
                        else:  # PMMXMX
                            count[STHREE] += 1
                        right_three = True
                    elif left_empty:  # XMMXMP
                        count[STHREE] += 1
                        right_three = True

                right_empty = True

            if left_three or right_three:
                pass
            elif left_empty and right_empty:  # XMMX
                count[TWO] += 1
            elif left_empty or right_empty:  # PMMX, XMMP
                count[STWO] += 1

        # Live Two: XMXMX, XMXXMX only check right direction
        # Sleep Two: PMXMX, XMXMP
        if m_range == 1:
            left_empty = right_empty = False
            if line[left_idx - 1] == empty:
                if line[left_idx - 2] == mine:
                    if line[left_idx - 3] == empty:
                        if line[right_idx + 1] == opponent:  # XMXMP
                            count[STWO] += 1
                left_empty = True

            if line[right_idx + 1] == empty:
                if line[right_idx + 2] == mine:
                    if line[right_idx + 3] == empty:
                        if left_empty:  # XMXMX
                            # setRecord(self, x, y, left_idx, right_idx+2, dir_index, dir)
                            count[TWO] += 1
                        else:  # PMXMX
                            count[STWO] += 1
                elif line[right_idx + 2] == empty:
                    if line[right_idx + 3] == mine and line[right_idx + 4] == empty:  # XMXXMX
                        count[TWO] += 1

        return CHESS_TYPE.NONE
