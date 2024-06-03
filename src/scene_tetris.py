import pygame
import random
import scene
import scene_manager as sm

board = [[0 for _ in range(350 // 35)] for _ in range(700 // 35)]


class Tetris:
    # 俄罗斯方块类
    def __init__(self):
        self.x = 5
        self.y = 0
        self.block_size = 35  # 方块大小
        self.screen_width = 350
        self.screen_height = 700

        self.shapes = [
            [[1, 1, 1, 1]],
            [[1, 1, 1], [0, 1, 0]],
            [[1, 1, 1], [1, 0, 0]],
            [[1, 1, 0], [0, 1, 1]],
            [[1, 1, 0], [1, 1, 0]],
            [[0, 1, 1], [1, 1, 0]],
            [[1, 1], [1, 1]]
        ]
        self.shape = random.choice(self.shapes)
        # 颜色相关参数
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.RED = (255, 0, 0)
        self.CYAN = (0, 255, 255)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (128, 0, 128)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.ORANGE = (255, 165, 0)
        self.colors = [self.CYAN, self.YELLOW, self.PURPLE, self.GREEN, self.BLUE, self.ORANGE, self.RED]
        self.color = random.choice(self.colors)
        self.rotation = 0  # 用于跟踪方块的旋转状态

    def draw(self, screen):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j] == 1:
                    pygame.draw.rect(screen, self.color, (self.x * self.block_size + j * self.block_size,
                                     self.y * self.block_size + i * self.block_size, self.block_size, self.block_size))

    def rotate(self):
        # 旋转方块的方法
        # 更新方块旋转状态
        self.rotation = (self.rotation + 1) % len(self.shape)
        old_shape = self.shape
        # 旋转shape矩阵
        self.shape = [list(row) for row in zip(*reversed(self.shape))]
        if not self.can_move(0, 0):
            # 如果旋转后位置无效，恢复原来的形状
            self.shape = old_shape

    def move(self, dx, dy):
        # 移动方块的方法
        if self.can_move(dx, dy):
            # 如果可以移动，更新方块的位置
            self.x += dx
            self.y += dy
            return True
        return False

    def can_move(self, dx, dy):
        # 检查方块是否可以移动到指定位置
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j] == 1:
                    # 检查方块的每个格子是否可以移动
                    if self.x + j + dx < 0 or self.x + j + dx >= self.screen_width / self.block_size or self.y + i + dy >= self.screen_height / self.block_size:
                        return False
                    if self.y + i + dy >= 0 and board[self.y + i + dy][self.x + j + dx] != 0:
                        return False
        return True


class GameTetris(scene.Scene):

    size = (350, 700)
    title = "俄罗斯方块"

    def __init__(self):
        # 方块相关参数
        self.row_cells = 10  # 行数
        self.col_cells = 20  # 列数
        self.block_size = 35  # 方块大小
        self.block_speed = 0.8  # 方块下落速度
        self.rotation = 0  # 用于跟踪方块的旋转状态
        # 界面显示相关参数
        self.screen_width = 350
        self.screen_height = 700
        self.score = 0  # 分数
        self.clock = pygame.time.Clock()
        self.fall_time = 0  # 用于跟踪方块的下落时间
        self.tetris = Tetris()  # 俄罗斯方块对象
        self.paused = False  # 初始化游戏为未暂停状态
        self.cached_screen = None
        super().__init__()

    def Draw(self):
        if not self.paused:
            self.screen.fill((255, 255, 255))
    
            for x in range(0, self.screen_width+1, self.block_size):
                pygame.draw.line(self.screen, (0, 0, 0), (x, 0), (x, self.screen_height), 1)
            for y in range(0, self.screen_height+1, self.block_size):
                pygame.draw.line(self.screen, (0, 0, 0), (0, y), (self.screen_width, y), 1)
            # 绘制固定的方块
            for y, row in enumerate(board):
                for x, color in enumerate(row):
                    if color != 0:
                        pygame.draw.rect(self.screen, color, (x * self.block_size, y * self.block_size, self.block_size, self.block_size))
            self.tetris.draw(self.screen)
        else:
            if self.cached_screen is not None:
                self.screen.blit(self.cached_screen, (0, 0))

    def pause_game(self):
        self.paused = True
        self.cached_screen = self.screen.copy()  # 缓存当前屏幕状态
        # 其他暂停逻辑...

    def resume_game(self):
        self.paused = False
        self.cached_screen = None  # 清除屏幕缓存
    def Handle_Event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sm.scenemanager.change_scene("scene_mode")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.tetris.rotate()
                if event.key == pygame.K_p:  # 检测是否按下了暂停键
                    if self.paused:
                        self.resume_game()  # 恢复游戏
                    else:
                        self.pause_game()  # 暂停游戏
                if event.key == pygame.K_SPACE:
                    while self.tetris.move(0, 1):  # 循环移动方块直到触底
                        pass
                    self.update_board_and_clear_lines()
                if event.key == pygame.K_LEFT:
                    self.tetris.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    self.tetris.move(1, 0)
        self.check_game_over()
        current_time = pygame.time.get_ticks()
        if current_time - self.fall_time > self.block_speed * 1000:
            self.fall_time = current_time
            if not self.tetris.move(0, 1):
                # 触底则固定方块并更新游戏区域数组
                self.update_board_and_clear_lines()
                # self.check_game_over()

    def update_board_and_clear_lines(self):
        for i in range(len(self.tetris.shape)):
            for j in range(len(self.tetris.shape[i])):
                if self.tetris.shape[i][j] == 1:
                    board[self.tetris.y + i][self.tetris.x + j] = self.tetris.color
        clear_rows = []
        for i in range(len(board)):
            if all(board[i]):
                clear_rows.append(i)
        for row in clear_rows:
            del board[row]
            board.insert(0, [0 for _ in range(self.screen_width // self.block_size)])
        self.tetris = Tetris()

    def reset_game(self):
        # 清空游戏区域
        for i in range(len(board)):
            for j in range(len(board[i])):
                board[i][j] = 0
        self.score = 0
        self.tetris = Tetris()
        self.fall_time = 0

    def check_game_over(self):
        # 检查游戏是否结束
        if any(row for row in board[0]):

            self.reset_game()
