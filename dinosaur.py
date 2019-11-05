import pygame
import random
from pygame.locals import *  # 导入pygame中的常量
from itertools import cycle  # 导入迭代工具

# 窗体宽度
SCREENWIDTH = 878
# 窗体高度
SCREENHEIGHT = 500
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
    bg2 = MyMap(878, 0)
    # 创建恐龙对象
    dinosaur = Dinosaur()
    # 添加障碍物时间
    addObstacleTimer = 0
    # 障碍物对象列表
    list = []
    while True:
        # 判断是否单击了关闭
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN and event.type == K_SPACE:
                # 如果恐龙在地上，开启恐龙跳跃
                if dinosaur.rect.y >= dinosaur.lowest_y:
                    dinosaur.jump()
                    # dinosaur.jump_audio.play()
        if not over:
            # 绘制地图起到更新作用
            bg1.map_update()
            # 地图移动
            bg1.map_rolling()
            bg2.map_update()
            bg2.map_rolling()
            # 绘制恐龙
            dinosaur.draw_dinosaur()
            # 计算障碍物间隔时间
            if addObstacleTimer >= 1300:
                r = random.randint(0, 100)
                if r > 40:
                    # 创建障碍物对象
                    obstacle = Obstacle()
                    # 将障碍物对象添加到列表中
                    list.append(obstacle)
                # 重置障碍物时间
                addObstacleTimer = 0
            # 循环遍历障碍物
            for i in range(len(list)):
                # 障碍物移动
                list[i].obstacle_move()
                # 绘制障碍物
                list[i].draw_obstacle()
        addObstacleTimer += 20
        # 更新窗体
        pygame.display.update()
        # 循环多次时间运行一次
        FPSCLOCK.tick(FPS)


# 定义滚动地图类
class MyMap:
    def __init__(self, x, y):
        # 加载背景图片
        self.bg = pygame.image.load('image/bg.png').convert_alpha()
        self.x = x
        self.y = y

    # 判断是否移动出窗体，移动出后重新放置背景
    def map_rolling(self):
        if self.x < -878:
            # 小于890说明地图移动完毕，重置新坐标
            self.x = 878
        else:
            # 5个像素向左移动
            self.x -= 5

    # 实现背景无限滚动
    def map_update(self):
        SCREEN.blit(self.bg, (self.x, self.y))


# 恐龙类（角色）
class Dinosaur:
    def __init__(self):
        # 初始化恐龙矩形
        self.rect = pygame.Rect(0, 0, 0, 0)
        # 跳跃状态
        self.jumpState = False
        # 跳跃高度
        self.jumpHeight = 130
        # 最低坐标
        self.lowest_y = 300
        # 跳跃增变量
        self.jumpValue = 0
        # 恐龙动图索引
        self.dinosaurIndex = 0
        self.dinosaurIndexGen = cycle([0, 1, 2])
        # 加载小恐龙图片
        self.dinosaur_img = (
            pygame.image.load('image/dinosaur1.png').convert_alpha(),
            pygame.image.load('image/dinosaur2.png').convert_alpha(),
            pygame.image.load('image/dinosaur3.png').convert_alpha(),
        )
        # 加载跳跃声音
        # pygame.mixer.Sound('audio/jump.mp3')
        self.rect.size = self.dinosaur_img[0].get_size()
        # 绘制恐龙
        self.x = 50
        self.y = self.lowest_y
        self.rect.topleft = (self.x, self.y)

    def jump(self):
        self.jumpState = True

    # 小恐龙移动
    def move(self):
        # 当跳跃时
        if self.jumpState:
            # 如果站在地上
            if self.rect.y >= self.lowest_y:
                # 以5像素向上移动
                self.jumpValue = -5
            # 到达顶部，以5像素回落
            if self.rect.y <= self.lowest_y - self.jumpHeight:
                self.jumpValue = 5
            self.rect.y += self.jumpValue
            # 回到地面，关闭跳跃
            if self.rect.y >= self.lowest_y:
                self.jumpState = False

    # 绘制恐龙
    def draw_dinosaur(self):
        # 匹配恐龙动图
        dinosaurIndex = next(self.dinosaurIndexGen)
        # 绘制恐龙
        SCREEN.blit(self.dinosaur_img[dinosaurIndex],
                    (self.x, self.rect.y))


# 障碍物类
class Obstacle:
    # 记录分数
    score = 1

    def __init__(self):
        # 初始化障碍物矩形
        self.rect = pygame.Rect(0, 0, 0, 0)
        # 加载障碍物图片
        self.stone = pygame.image.load('image/stone.png').convert_alpha()
        self.cacti = pygame.image.load('image/cacti.png').convert_alpha()
        # 加载分数图片
        self.numbers = (
            pygame.image.load('image/0.png').convert_alpha(),
            pygame.image.load('image/1.png').convert_alpha(),
            pygame.image.load('image/2.png').convert_alpha(),
            pygame.image.load('image/3.png').convert_alpha(),
            pygame.image.load('image/4.png').convert_alpha(),
            pygame.image.load('image/5.png').convert_alpha(),
            pygame.image.load('image/6.png').convert_alpha(),
            pygame.image.load('image/7.png').convert_alpha(),
            pygame.image.load('image/8.png').convert_alpha(),
            pygame.image.load('image/9.png').convert_alpha()
        )
        # 加载分数音效
        # self.score_audio = pygame.mixer.Sound('audio/score.wav')
        # 0和1随机数
        r = random.randint(0, 1)
        # 如果是0显示石头，非0显示仙人掌
        if r == 0:
            self.image = self.stone
        else:
            self.image = self.cacti
        # 根据障碍物位图宽高来设置矩形
        self.rect.size = self.image.get_size()
        # 获取位图宽高
        self.width, self.height = self.rect.size
        # 障碍物绘制坐标
        self.x = 800
        self.y = 500 - (self.height / 2)
        self.rect.center = (self.x, self.y)

    # 障碍物移动
    def obstacle_move(self):
        self.rect.x -= 5

    # 绘制障碍物
    def draw_obstacle(self):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

    # 获取分数
    def getScore(self):
        self.score
        tmp = self.score
        if tmp == 1:
            # self.score_audio.play()
            pass
        self.score = 0
        return tmp

    # 显示分数
    def showScore(self, score):
        # 在窗体中间显示分数
        self.scoreDigits = [int(x) for x in list(str(score))]
        totalWidth = 0
        for digit in self.scoreDigits:
            # 获取积分图片的宽度
            totalWidth += self.numbers[digit].get_width()
        # 分数横向位置
        Xoffest = (SCREENWIDTH - totalWidth) / 2
        for digit in self.scoreDigits:
            # 绘制分数
            SCREEN.blit(self.numbers[digit], (Xoffest, SCREENHEIGHT * 0.1))
            # 随着数字增加改变位置
            Xoffest += self.numbers[digit].get_width()


if __name__ == '__main__':
    mainGame()
