import pygame
import time
# 初始化pygame
pygame.init()

# 设置屏幕大小
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 创建一个用于绘制的离屏表面
offscreen_surface = pygame.Surface((screen_width, screen_height)).convert()


# 定义两个简单的界面函数
def draw_home_screen(surface):
    surface.fill((255, 255, 255))  # 白色背景
    pygame.draw.circle(surface, (0, 0, 255), (400, 300), 100)  # 画一个蓝色的圆


def draw_game_screen(surface):
    surface.fill((0, 255, 0))  # 绿色背景
    pygame.draw.rect(surface, (255, 0, 0), (100, 150, 300, 200))  # 画一个红色的矩形


running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 绘制新界面到离屏表面
    offscreen_surface.fill((0, 0, 0))  # 先清除离屏表面
    draw_game_screen(offscreen_surface)
    time.sleep(1)  # 模拟游戏过程
    # 切换屏幕显示到新界面
    screen.blit(offscreen_surface, (0, 0))

    # 更新屏幕显示
    pygame.display.update()

    # 控制游戏帧率
    clock.tick(60)

# 退出pygame
pygame.quit()
