import pygame
import scene
import button
import scene_manager
from colorRGB import color


class ModeScene(scene.Scene):
    size = (800, 633)
    title = "ModeScene"
    bg_path = "img/bg.jpg"
    icon_2048 = "img/2048.jpg"
    icon_sudoku = "img/sudoku.jpg"
    icon_gobang = "img/gobang.jpg"

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
        #pygame.draw.rect(self.screen, color.WHITE, (0, 0, 800, 633))  # 画出背景矩形
        pygame.display.set_caption(self.title)  #设置标题
        if self.bg_path:  # 判断是否有背景图片
            bg = pygame.image.load(self.bg_path)  # 加载背景图片
            self.screen.blit(self.screen, (0, 0))
            self.screen.blit(bg, (0, 0))
        self.screen.blit(pygame.image.load(self.icon_2048),
                         (50, 50))  # 加载2048图标
        self.screen.blit(pygame.image.load(self.icon_sudoku),
                         (50, 175))  # 加载数独图标
        self.screen.blit(pygame.image.load(self.icon_gobang),
                         (50, 300))  # 加载五子棋图标
        self.btn_2048.draw(self.screen, 120)  #画出2048按钮
        self.btn_gobang.draw(self.screen, 120)  #画出五子棋按钮
        self.btn_sudoku.draw(self.screen, 120)  #画出数独按钮
        self.btn_back.draw(self.screen, 120)  #画出返回按钮

    def handle_event(self):  #处理事件
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
