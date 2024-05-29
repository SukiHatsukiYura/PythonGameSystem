import pygame
import scene
import scene_manager as sm


# 定义GameSudoku类，继承自scene.Scene
class GameSudoku(scene.Scene):
    # 定义类变量size和，current_grid初始值为(0, 0)
    size = (651, 651)
    current_grid = (0, 0)
    #定义上一次选中格子的位置
    last_grid = (0, 0)

    # 初始化方法
    def __init__(self):
        super().__init__()
        self.screen.fill((255, 255, 255))  # 填充背景色

    # 绘制整个游戏界面
    def draw(self):
        #self.draw_grid()  # 绘制当前选择格子的效果
        self.draw_line()  # 绘制网格线

    # 绘制网格线
    def draw_line(self):
        # 绘制水平和垂直的网格线
        for i in range(10, 641, 70):
            if (i - 10) % (70 * 3) == 0:
                pygame.draw.line(self.screen, (0, 0, 0), (i, 10), (i, 640), 1)
                pygame.draw.line(self.screen, (0, 0, 0), (10, i), (640, i), 1)
            else:
                pygame.draw.line(self.screen, (211, 211, 211), (i, 11),
                                 (i, 640), 1)
                pygame.draw.line(self.screen, (211, 211, 211), (11, i),
                                 (640, i), 1)

        # 绘制整个游戏界面的边框
        #pygame.draw.rect(self.screen, (0, 0,0), (0, 0, 651, 651), 10)

    # 绘制当前选择格子的效果
    def draw_grid(self):
        #清除上一次选中的格子效果
        if self.last_grid != self.current_grid:
            last_x, last_y = self.last_grid
            last_x = max(0, min(last_x, 8))
            last_y = max(0, min(last_y, 8))
            screen_x, screen_y = 11 + last_x * 70, 11 + last_y * 70
            screen_x = max(11, min(screen_x, 640 - 68))
            screen_y = max(11, min(screen_y, 640 - 68))
            # 绘制上一次选择格子的矩形
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (screen_x, screen_y, 69, 69))
        x, y = self.current_grid
        x = max(0, min(x, 8))
        y = max(0, min(y, 8))
        screen_x, screen_y = 11 + x * 70, 11 + y * 70
        screen_x = max(11, min(screen_x, 640 - 68))
        screen_y = max(11, min(screen_y, 640 - 68))
        # 绘制当前选择格子的矩形
        pygame.draw.rect(self.screen, (255, 225, 255),
                         (screen_x, screen_y, 69, 69))

    # 处理游戏事件
    def handle_event(self):
        pos = pygame.mouse.get_pos()
        x, y = pos
        x = (x - 10) // 70
        y = (y - 10) // 70
        self.current_grid = (x, y)  # 更新当前选择的格子位置
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sm.scenemanager.change_scene("mode_scene")  # 切换到模式选择场景
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.draw_grid()  # 绘制当前选择格子的效果
                self.last_grid = self.current_grid  # 更新上一次选中的格子位置
