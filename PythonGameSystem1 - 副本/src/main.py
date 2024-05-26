import pygame
from scene_manager import scenemanager

running = True  #游戏运行标志
FPS = 60  #帧率
colck = pygame.time.Clock()  #创建时钟对象
pygame.init()  #初始化pygame

while running:
    scenemanager.draw_scene()
    scenemanager.handle_event()
    if pygame.event.poll().type == pygame.QUIT:
        running = False
    pygame.display.update()
    colck.tick(FPS)

pygame.quit()
