import pygame
import scene
import button
import scene_manager
import scene_sudoku
from colorRGB import color


class ModeScene(scene.Scene):
    size = (800, 633)

    title = "ModeScene"
    bg_path = "img/bg.jpg"
    icon_2048 = "img/2048.jpg"
    icon_sudoku = "img/sudoku.jpg"
    icon_gobang = "img/gobang.jpg"

    def __init__(self):
        super().__init__()
        bg = pygame.image.load(self.bg_path).convert()  # 加载背景图片
        self.scaled_bg = pygame.transform.smoothscale(bg, self.size)  # 缩放背景图片

    btn_2048 = button.Button(200, 50, 500, 100, color.WHITE, "2048",
                             color.BLACK, 50)
    btn_gobang = button.Button(200, 175, 500, 100, color.WHITE, "五子棋",
                               color.BLACK, 50)
    btn_sudoku = button.Button(200, 300, 500, 100, color.WHITE, "数独",
                               color.BLACK, 50)
    btn_back = button.Button(50, 450, 200, 100, color.WHITE, "返 回",
                             color.BLACK, 50)

    def draw(self):
        self.screen.fill(color.BLACK)  # 填充背景色
        self.screen.blit(self.scaled_bg, (0, 0))
        pygame.display.set_caption(self.title)  # 设置标题
        self.screen.blit(pygame.image.load(self.icon_2048),
                         (50, 50))  # 加载2048图标
        self.screen.blit(pygame.image.load(self.icon_sudoku),
                         (50, 175))  # 加载数独图标
        self.screen.blit(pygame.image.load(self.icon_gobang),
                         (50, 300))  # 加载五子棋图标
        self.btn_2048.draw(self.screen, 120)  # 画出2048按钮
        self.btn_gobang.draw(self.screen, 120)  # 画出五子棋按钮
        self.btn_sudoku.draw(self.screen, 120)  # 画出数独按钮
        self.btn_back.draw(self.screen, 120)  # 画出返回按钮

    def handle_event(self):  # 处理事件
        # 选择跳转2048游戏
        self.btn_2048.btn_click(self.screen,
                                scene_manager.scenemanager.change_scene,
                                "scene_2048")
        # 选择跳转五子棋游戏
        if self.btn_gobang.is_clicked(pygame.mouse.get_pos()) == True:
            self.btn_gobang.color = color.GRAY
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pygame.quit()
                    exit()
        else:
            self.btn_gobang.color = color.WHITE
        self.btn_gobang.draw(self.screen, 120)

        # 选择跳转数独游戏
        self.btn_sudoku.btn_click(self.screen,
                                  scene_manager.scenemanager.change_scene,
                                  "scene_sudoku")
        # 选择返回
        if self.btn_back.is_clicked(pygame.mouse.get_pos()) == True:
            self.btn_back.color = color.GRAY
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    scene_manager.scenemanager.change_scene("start_scene")
        else:
            self.btn_back.color = color.WHITE
        self.btn_back.draw(self.screen, 120)

        if pygame.event.poll().type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:  # 按下ESC键
                scene_manager.scenemanager.change_scene("start_scene")
