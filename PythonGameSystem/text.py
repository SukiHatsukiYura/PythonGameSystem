# import pygame

# # 初始化pygame
# pygame.init()

# # 设置窗口宽度和高度
# width = 800
# height = 600
# window = pygame.display.set_mode((width, height))

# # 背景图片路径
# bg_path = "img/bg.jpg"
# bg = pygame.image.load(bg_path).convert()  # 加载背景图片并转换为pygame.Surface对象
# window.blit(bg, (0, 0))  # 绘制背景图片

# # 设置窗口标题
# pygame.display.set_caption("Transparent Rectangle")

# # 设置透明矩形颜色和大小
# transparent_color = (100, 100, 100, 200)
# rect = pygame.Surface((200, 200), pygame.SRCALPHA)
# rect.fill(transparent_color)
# window.blit(rect, (200, 200))

# # 游戏运行循环
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     pygame.display.update()

# # 退出pygame
# pygame.quit()

import pygame

pygame.init()

width = 800
height = 600
window = pygame.display.set_mode((width, height))
bg_path = "img/bg.jpg"  # 背景图片路径
bg = pygame.image.load(bg_path).convert()  # 加载背景图片并转换为pygame.Surface对象
window.blit(bg, (0, 0))  # 绘制背景图片
pygame.display.set_caption("Transparent Rectangle")

rect_surface = pygame.Surface((200, 100),
                              pygame.SRCALPHA)  # 创建一个带有Alpha通道的Surface对象
pygame.draw.rect(rect_surface, (100, 100, 100, 128),
                 (0, 0, 200, 100))  # 在Surface对象上绘制半透明矩形
window.blit(rect_surface, (100, 250))  # 将带有半透明矩形的Surface对象绘制到窗口中

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()

pygame.quit()
