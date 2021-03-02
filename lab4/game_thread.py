import pygame
from pygame.locals import *
from sys import exit
import threading
import time
import reinforce_learning as rl
import random
import math
import pygame.gfxdraw

random.seed(time.time())
SIZE = 30  # 棋盘每个点时间的间隔
Line_Points = 15  # 棋盘每行/每列点数
Outer_Width = 20  # 棋盘外宽度
Border_Width = 4  # 边框宽度
Inside_Width = 4  # 边框跟实际的棋盘之间的间隔
Border_Length = SIZE * (Line_Points - 1) + Inside_Width * 2 + Border_Width  # 边框线的长度
Start_X = Start_Y = Outer_Width + int(Border_Width / 2) + Inside_Width  # 网格线起点（左上角）坐标
SCREEN_HEIGHT = SIZE * (Line_Points - 1) + Outer_Width * 2 + Border_Width + Inside_Width * 2  # 游戏屏幕的高
SCREEN_WIDTH = SCREEN_HEIGHT + 200  # 游戏屏幕的宽


Stone_Radius = SIZE // 2 - 3  # 棋子半径
Stone_Radius2 = SIZE // 2 + 3
Checkerboard_Color = (0xFA, 0xEB, 0xD7)  # 棋盘颜色
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (200, 30, 30)
BLUE_COLOR = (30, 30, 200)
COLOR_DICT = {-1: (255, 255, 255), 1: (0, 0, 0)}
RIGHT_INFO_POS_X = SCREEN_HEIGHT + Stone_Radius2 * 2 + 10

class GameThread(threading.Thread):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('五子棋')
    font1 = pygame.font.SysFont('SimHei', 32)
    font2 = pygame.font.SysFont('SimHei', 72)
    fwidth, fheight = font2.size('黑方获胜')

    now_color = 1 # 1黑子 -1白子
    chess_board = [[0 for col in range(19)] for row in range(Line_Points)]

    history = []

    step_num = 0

    explore = 0.0005

    explore_value = 0.5

    is_explore = 0.8

    alpha = 0.9

    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.id = thread_id

    def loop(self):
        self.display()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
            self.display()
            time.sleep(0.2)

    def run(self):
        time.sleep(1)
        num = 0
        while True:
            print("------------------")

            # 生成赢的局面
            self.generate_data()
            print(rl.train_data['y'])
            print("###################")
            rl.train()
            num += 1
            print("train num %d " % (num, ))

    # 将棋子加入到棋盘中
    def place_pieces(self, x, y):
        self.chess_board[x][y] = self.now_color
        # 将copy_self接入history数组
        self.history.append(self.copy_self())
        self.step_num += 1
        if self.is_win(x, y, self.now_color):
            print("is win !")
            self.win()
            return
        self.now_color = -self.now_color

    # 如果赢了
    def win(self):
        print("step_num %d" % self.step_num)
        self.add_train_data()
        print("len(x) %d" % len(rl.train_data['x']))
        self.explore_value = 0.01
        print("explore %f, explore_value %f" % (self.explore, self.explore_value))
        self.init_board()

    # 将chess_board的内容复制到board_copy
    def copy_self(self):
        board_copy = [[0 for col in range(Line_Points)] for row in range(Line_Points)]
        length = len(self.chess_board)
        side = self.now_color
        for i in range(length):
            for j in range(length):
                board_copy[i][j] = side * self.chess_board[i][j]

        return board_copy

    def print_text(self, font, x, y, text, fcolor=(255, 255, 255)):
        imgText = font.render(text, True, fcolor)
        self.screen.blit(imgText, (x, y))

    def draw_chessman_pos(self, stone_color, pos):
        x = Start_X + SIZE * pos[0]
        y = Start_Y + SIZE * pos[1]
        xy = (int(x), int(y))
        color_num = COLOR_DICT[stone_color]
        pygame.draw.circle(self.screen, color_num, xy, Stone_Radius)
        # pygame.gfxdraw.aacircle(self.screen, int(pos[0]), int(pos[1]), Stone_Radius2, stone_color)
        # pygame.gfxdraw.filled_circle(self.screen, int(pos[0]), int(pos[1]), Stone_Radius2, stone_color)

    def draw_board(self):
        # 填充棋盘背景色
        self.screen.fill(Checkerboard_Color)
        # 画棋盘网格线外的边框
        pygame.draw.rect(self.screen, BLACK_COLOR, (Outer_Width, Outer_Width, Border_Length, Border_Length),
                             Border_Width)
        # 画网格线
        for i in range(Line_Points):
            pygame.draw.line(self.screen, BLACK_COLOR,(Start_Y, Start_Y + SIZE * i),
                            (Start_Y + SIZE * (Line_Points - 1), Start_Y + SIZE * i),
                            1)
        for j in range(Line_Points):
            pygame.draw.line(self.screen, BLACK_COLOR,
                            (Start_X + SIZE * j, Start_X),
                            (Start_X + SIZE * j, Start_X + SIZE * (Line_Points - 1)),
                            1)

    def draw_left_chessman_pos(self, pos, stone_color):
        pygame.gfxdraw.aacircle(self.screen, pos[0], pos[1], Stone_Radius2, stone_color)
        pygame.gfxdraw.filled_circle(self.screen, pos[0], pos[1], Stone_Radius2, stone_color)

    def draw_left_info(self,font):
        self.print_text(font, RIGHT_INFO_POS_X, Start_X + 3, '玩家', BLUE_COLOR)
        self.print_text(font, RIGHT_INFO_POS_X, Start_X + Stone_Radius2 * 3 + 3, '电脑', BLUE_COLOR)

        self.print_text(font, SCREEN_HEIGHT, SCREEN_HEIGHT - Stone_Radius2 * 8, '战况：', BLUE_COLOR)
        self.draw_left_chessman_pos((SCREEN_HEIGHT + Stone_Radius2, SCREEN_HEIGHT - int(Stone_Radius2 * 4.5)),
                                 BLACK_COLOR)
        self.draw_left_chessman_pos( (SCREEN_HEIGHT + Stone_Radius2, SCREEN_HEIGHT - Stone_Radius2 * 2),
                                 WHITE_COLOR)
        self.draw_left_chessman_pos((SCREEN_HEIGHT + Stone_Radius2, Start_X + Stone_Radius2),
                                    BLACK_COLOR)
        self.draw_left_chessman_pos((SCREEN_HEIGHT + Stone_Radius2, Start_X + Stone_Radius2 * 4),
                                    WHITE_COLOR)
        self.print_text(font, RIGHT_INFO_POS_X, SCREEN_HEIGHT - int(Stone_Radius2 * 5.5) + 3, f'{0} 胜',
                   BLUE_COLOR)
        self.print_text(font, RIGHT_INFO_POS_X, SCREEN_HEIGHT - Stone_Radius2 * 3 + 3, f'{0} 胜',
                   BLUE_COLOR)

    def init_board(self):
        length = len(self.chess_board)
        for i in range(length):
            for j in range(length):
                self.chess_board[i][j] = 0

        self.history = []
        self.now_color = 1
        self.step_num = 0

    def display(self):
        self.draw_board()
        self.draw_left_info(self.font1)
        for i in range(len(self.chess_board)):
            for j in range(len(self.chess_board[i])):
                if self.chess_board[i][j] != 0:
                    self.draw_chessman_pos(self.chess_board[i][j], (i, j))
        pygame.display.update()

    def add_train_data(self):
        y = 0.5
        side = self.now_color
        for i in range(self.step_num):
            a = math.pow(self.alpha, self.step_num - i - 1)/2
            y2 = 0.5 + a
            # 如果是白棋
            if side == -1:
                y2 = 1 - y2
            side = -side
            # 随机抽取部分样本加入train_data
            if random.random() > 2*a:
                continue
            rl.train_data['x'].append(self.to_input(self.history[i]))
            rl.train_data['y'].append([y2, 1 - y2])

    def to_input(self, board):
        # 输入二维棋盘
        c = [[[0.0 for col in range(2)] for col in range(Line_Points)] for row in range(Line_Points)]
        length = len(board)
        for i in range(length):
            for j in range(length):
                if board[i][j] == 1:
                    c[i][j][0] = 1.0
                elif board[i][j] == -1:
                    c[i][j][1] = 1.0
        return c

    def is_win(self, i, j, color):
        length = len(self.chess_board)
        a = 5
        count = 1
        for x in range(1, a):
            tx = i - x
            ty = j
            if tx < 0 or tx >= length:
                break
            if self.chess_board[tx][ty] == color:
                count += 1
            else:
                break

        for x in range(1, a):
            tx = i + x
            ty = j
            if tx < 0 or tx >= length:
                break
            if self.chess_board[tx][ty] == color:
                count += 1
            else:
                break

        if count >= 5:
            return True

        count = 1
        for x in range(1, a):
            tx = i - x
            ty = j - x
            if tx < 0 or tx >= length:
                break
            if ty < 0 or ty >= length:
                break
            if self.chess_board[tx][ty] == color:
                count += 1
            else:
                break

        for x in range(1, a):
            tx = i + x
            ty = j + x
            if tx < 0 or tx >= length:
                break
            if ty < 0 or ty >= length:
                break
            if self.chess_board[tx][ty] == color:
                count += 1
            else:
                break

        if count >= 5:
            return True

        count = 1
        for x in range(1, a):
            tx = i
            ty = j - x
            if ty < 0 or ty >= length:
                break
            if self.chess_board[tx][ty] == color:
                count += 1
            else:
                break

        for x in range(1, a):
            tx = i
            ty = j + x
            if ty < 0 or ty >= length:
                break
            if self.chess_board[tx][ty] == color:
                count += 1
            else:
                break

        if count >= 5:
            return True

        count = 1
        for x in range(1, a):
            tx = i - x
            ty = j + x
            if tx < 0 or tx >= length:
                break
            if ty < 0 or ty >= length:
                break
            if self.chess_board[tx][ty] == color:
                count += 1
            else:
                break

        for x in range(1, a):
            tx = i + x
            ty = j - x
            if tx < 0 or tx >= length:
                break
            if ty < 0 or ty >= length:
                break
            if self.chess_board[tx][ty] == color:
                count += 1
            else:
                break

        if count >= 5:
            return True
        return False

    def generate_data(self, ):
        rl.train_data = {"x": [], "y": []}
        # rl的训练集要到达100
        num = 100
        self.explore = 0
        self.explore_value = 0

        # 需要train_data有100个
        while len(rl.train_data['x']) < num:
            print("train_data length is ",len(rl.train_data['x']))
            self.next_move()

    def next_move(self):
        p = self.get_next_move()
        self.place_pieces(p[0], p[1])

    # 获得下一步棋
    def get_next_move(self, ):
        # 把当前棋盘chess_board的局面复制到board
        board = self.copy_self()
        # board2是三维的
        board2 = self.to_input(board)
        index = 0
        max_value = -2
        max_position = [0, 0]
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 0:
                    board2[i][j][index] = 1
                    value = rl.get_value(board2)
                    # value += random.random()*self.explore_value
                    # print(self.explore_value)
                    if value > max_value:
                        max_value = value
                        max_position = [i, j]
                    board2[i][j][index] = 0
        print(max_position[0], max_position[1], self.now_color, max_value)
        return max_position
