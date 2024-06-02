import pygame
import scene
import button
import scene_manager as sm


class ModeScene(scene.Scene):
    size = (800, 633)
    title = "菜单"

    bg_path = "img/bg.jpg"
    icon_2048 = "img/2048.jpg"
    icon_sudoku = "img/sudoku.jpg"
    icon_gobang = "img/gobang.jpg"
    btn_2048 = button.Button(200, 40, 500, 120, (255, 255, 255), "2048",
                             (0, 0, 0), 50)
    btn_gobang = button.Button(200, 185, 500, 120, (255, 255, 255), "五子棋",
                               (0, 0, 0), 50)
    btn_sudoku = button.Button(200, 330, 500, 120, (255, 255, 255), "数独",
                               (0, 0, 0), 50)
    btn_back = button.Button(50, 490, 200, 100, (255, 255, 255), "返 回",
                             (0, 0, 0), 50)

    def __init__(self):
        super().__init__()
        bg = pygame.image.load(self.bg_path).convert()  # 加载背景图片
        self.scaled_bg = pygame.transform.smoothscale(bg, self.size)  # 缩放背景图片
        self.icon = pygame.image.load(self.bg_path)
        self.text_font = pygame.font.Font(pygame.font.match_font("SimHei"), 20)  # 设置文本字体

    def draw(self):
        self.screen.fill((0, 0, 0))  # 填充背景色
        self.screen.blit(self.scaled_bg, (0, 0))
        self.screen.blit(pygame.image.load(self.icon_2048),
                         (80, 50))  # 加载2048图标
        self.screen.blit(pygame.image.load(self.icon_sudoku),
                         (80, 195))  # 加载数独图标
        self.screen.blit(pygame.image.load(self.icon_gobang),
                         (80, 340))  # 加载五子棋图标
        self.btn_2048.draw(self.screen, 120)  # 画出2048按钮
        self.btn_gobang.draw(self.screen, 120)  # 画出五子棋按钮
        self.btn_sudoku.draw(self.screen, 120)  # 画出数独按钮
        self.btn_back.draw(self.screen, 120)  # 画出返回按钮
        self.screen.blit(self.text_font.render("ESC To Back", True, (0, 0, 0)), (95, 564))

    def handle_event(self):  # 处理事件
        # 选择跳转2048游戏
        self.btn_2048.btn_click(self.screen,
                                sm.scenemanager.change_scene,
                                mode="scene_2048")
        # 选择跳转五子棋游戏

        # 选择跳转数独游戏
        self.btn_sudoku.btn_click(self.screen,
                                  sm.scenemanager.change_scene,
                                  mode="scene_sudoku")
        # 选择返回
        self.btn_back.btn_click(self.screen,
                                sm.scenemanager.change_scene,
                                mode="scene_start")

        if pygame.event.poll().type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:  # 按下ESC键
                sm.scenemanager.change_scene("scene_start")
