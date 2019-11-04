import pygame
from pygame.locals import *  # 导入pygame中的常量

# 窗体宽度
SCREENWIDTH = 822
# 窗体高度
SCREENHEIGHT = 260
# 更新画面时间（帧率）
FPS = 30


def mainGame():
    # 记录得分
    score = 0
    global SCREEN, FPSCLOCK
    # 初始化pygame
    pygame.init()
    # 控制循环多次时间运行一次，初始化时钟
    FPSCLOCK = pygame.time.Clock()
    # 实例化窗体
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    # 窗体标题
    pygame.display.set_caption('小恐龙')
    while True:
        # 判断是否单击了关闭
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        # 更新窗体
        pygame.display.update()
        # 循环多次时间运行一次
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    mainGame()
