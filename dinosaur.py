import pygame
from pygame.locals import *  # 导入pygame中的常量

# 窗体宽度
SCREENWIDTH = 890
# 窗体高度
SCREENHEIGHT = 600
# 更新画面时间（帧率）
FPS = 30


def mainGame():
    # 记录得分
    score = 0
    # 判断游戏是否结束
    over = False
    global SCREEN, FPSCLOCK
    # 初始化pygame
    pygame.init()
    # 控制循环多次时间运行一次，初始化时钟
    FPSCLOCK = pygame.time.Clock()
    # 实例化窗体
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    # 窗体标题
    pygame.display.set_caption('小恐龙')
    # 创建地图对象
    # 显示一张，第二张在界面外准备，移动时同时移动
    bg1 = MyMap(0, 0)
    bg2 = MyMap(890, 0)
    while True:
        # 判断是否单击了关闭
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        if not over:
            # 绘制地图起到更新作用
            bg1.map_update()
            # 地图移动
            bg1.map_rolling()
            bg2.map_update()
            bg2.map_rolling()
        # 更新窗体
        pygame.display.update()
        # 循环多次时间运行一次
        FPSCLOCK.tick(FPS)


# 定义滚动地图类
class MyMap():
    def __init__(self, x, y):
        # 加载背景图片
        self.bg = pygame.image.load('image/bg.jpg').convert_alpha()
        self.x = x
        self.y = y

    # 判断是否移动出窗体，移动出后重新放置背景
    def map_rolling(self):
        if self.x < -890:
            # 小于890说明地图移动完毕，重置新坐标
            self.x = 890
        else:
            # 5个像素向左移动
            self.x -= 5

    # 实现背景无限滚动
    def map_update(self):
        SCREEN.blit(self.bg, (self.x, self.y))


if __name__ == '__main__':
    mainGame()
