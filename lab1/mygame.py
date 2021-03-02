"""人工智能五子棋"""
import sys
from pygame.locals import *
import pygame.gfxdraw
from AI_alpha_beta import *
from Checkboard import *
from DrawUI import *
from PIL import Image
import argparse
import matplotlib.image as mpimg
import cv2
from tiny_yolo import *
import matplotlib.pyplot as plt

FLAGS = None

Chessman = namedtuple('Chessman', 'Name Value Color')
Point = namedtuple('Point', 'X Y')
BLACK_CHESSMAN = Chessman('黑子', 1, (45, 45, 45))
WHITE_CHESSMAN = Chessman('白子', 2, (255, 255, 255))

offset = [(1, 0), (0, 1), (1, 1), (1, -1)]

def detect_img(yolo,image):
    r_image = yolo.detect_image(image)
    plt.imshow(r_image)  # 暂停５秒钟
    plt.pause(1) # 关闭当前显示的图像
    plt.close()
    #yolo.close_session()

def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('五子棋')

    font1 = pygame.font.SysFont('SimHei', 32)
    font2 = pygame.font.SysFont('SimHei', 72)
    fwidth, fheight = font2.size('黑方获胜')

    checkerboard = Checkerboard(Line_Points)
    cur_runner = BLACK_CHESSMAN
    winner = None
    computer = ChessAI(Line_Points, WHITE_CHESSMAN)

    black_win_count = 0
    white_win_count = 0

    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument(
        '--image', default=False, action="store_true",
        help='Image detection mode, will ignore all positional arguments'
    )
    FLAGS = parser.parse_args()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                print("玩家退出游戏")
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    # 一局结束的时候，按回车，会执行下面语句，重新初始化
                    if winner is not None:
                        winner = None
                        cur_runner = BLACK_CHESSMAN
                        checkerboard = Checkerboard(Line_Points)
                        # 把电脑设定为AI类，算法封装在AI
                        computer = ChessAI(Line_Points, WHITE_CHESSMAN)

            elif event.type == MOUSEBUTTONDOWN:
                # print("-------------")
                if winner is None:
                    pressed_array = pygame.mouse.get_pressed()

                    if pressed_array[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        # 根据鼠标点击返回游戏区坐标
                        click_point = DrawUI._get_clickpoint(mouse_pos)
                        # 点击区域有效
                        if click_point is not None:
                            # 如果该位置能够落子
                            if checkerboard.can_drop(click_point):
                                winner = checkerboard.drop(cur_runner, click_point)
                                if winner is None:
                                    cur_runner = _get_next(cur_runner)
                                    computer.get_opponent_drop(click_point)
                                    # AI生成白棋,findBestChess返回坐标
                                    AI_point, score = computer.findBestChess(WHITE_CHESSMAN.Value) #2

                                    # 判断是否赢得比赛
                                    winner = checkerboard.drop(cur_runner, AI_point)
                                    # 识别棋局
                                    pygame.image.save(screen, '1.jpg')
                                    image = Image.open("1.jpg")
                                    cropped = image.crop((13, 10, 580, 580))
                                    detect_img(YOLO(**vars(FLAGS)), cropped)
                                    if winner is not None:
                                        white_win_count += 1
                                    cur_runner = _get_next(cur_runner)
                                else:
                                    black_win_count += 1
                            else:
                                print('该位置已经被占')
                        else:
                            print('超出棋盘区域')

        # 画棋盘
        DrawUI._draw_checkerboard(screen)

        # 画棋盘上已有的棋子
        for i, row in enumerate(checkerboard.checkerboard):
            for j, cell in enumerate(row):
                if cell == BLACK_CHESSMAN.Value:
                    DrawUI._draw_chessman(screen, Point(j, i), BLACK_CHESSMAN.Color)
                elif cell == WHITE_CHESSMAN.Value:
                    DrawUI._draw_chessman(screen, Point(j, i), WHITE_CHESSMAN.Color)

        # 在右侧打印出战况
        DrawUI._draw_left_info(screen, font1, cur_runner, black_win_count, white_win_count,DrawUI)

        # 判断最终的冠军
        if winner:
            print_text(screen, font2, (SCREEN_WIDTH - fwidth)//2, (SCREEN_HEIGHT - fheight)//2, winner.Name + '获胜', RED_COLOR)

        pygame.display.flip()


def _get_next(cur_runner):
    if cur_runner == BLACK_CHESSMAN:
        return WHITE_CHESSMAN
    else:
        return BLACK_CHESSMAN

if __name__ == '__main__':
    main()