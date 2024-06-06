import pygame
from scene_manager import scenemanager

# 创建模式选择场景
running = True  # 游戏运行标志
FPS = 60  # 帧率
colck = pygame.time.Clock()  # 创建时钟对象
pygame.init()  # 初始化pygame
pygame.mixer.init()  # 初始化音频

while running:
    scenemanager.Draw_Scene()
    scenemanager.Handle_Event()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    colck.tick(FPS)

pygame.mixer.music.stop()  # 停止背景音乐
pygame.mixer.quit()  # 关闭音频
pygame.quit()
