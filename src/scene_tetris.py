import pygame
import random
import scene
import scene_manager as sm


class Block:
    # 俄罗斯方块类
    def __init__(self, board, x=4, y=0, block_size=35, screen_width=350, screen_height=700):
        self.board = board
        self.x = x
        self.y = y
        self.block_size = block_size  # 方块大小
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.shapes = [[[1, 1, 1, 1]], [[1, 1, 1], [0, 1, 0]],
                       [[1, 1, 1], [1, 0, 0]], [[1, 1, 0], [0, 1, 1]],
                       [[1, 1, 0], [1, 1, 0]], [[0, 1, 1], [1, 1, 0]],
                       [[1, 1], [1, 1]]]
        self.shape = random.choice(self.shapes)

        self.shuffle_shapes()
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
        self.colors = [
            self.CYAN, self.YELLOW, self.PURPLE, self.GREEN, self.BLUE,
            self.ORANGE, self.RED
        ]
        self.color = random.choice(self.colors)
        self.rotation = 0  # 用于跟踪方块的旋转状态

    def shuffle_shapes(self):
        random.shuffle(self.shapes)

    def get_next_shape(self):
        if not self.shapes:
            random.shuffle(self.shapes)
        return self.shapes.pop()

    def draw(self, screen):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j] == 1:
                    pygame.draw.rect(
                        screen, self.color,
                        (self.x * self.block_size + j * self.block_size,
                         self.y * self.block_size + i * self.block_size,
                         self.block_size, self.block_size))
        self.draw_shadow(screen)

    def draw_shadow(self, screen):
        y_offset = self.calculate_shadow_offset()
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j] == 1:
                    pygame.draw.rect(
                        screen, (128, 128, 128),
                        (self.x * self.block_size + j * self.block_size,
                         (self.y + y_offset) * self.block_size + i * self.block_size,
                         self.block_size, self.block_size))

    def calculate_shadow_offset(self):
        y_offset = 0
        while self.can_move(0, y_offset + 1, self.board):
            y_offset += 1
        return y_offset

    def can_move(self, dx, dy, board):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j] == 1:
                    new_x = self.x + j + dx
                    new_y = self.y + i + dy
                    if self.is_out_of_bound(new_x, new_y, board) or self.is_collision(new_x, new_y, board):
                        return False
        return True

    def is_out_of_bound(self, x, y, board):
        return x < 0 or x >= len(board[0]) or y >= len(board)

    def is_collision(self, x, y, board):
        return y >= 0 and board[y][x] != 0

    def rotate(self):
        # 旋转方块的方法
        # 更新方块旋转状态
        self.rotation = (self.rotation + 1) % len(self.shape)
        old_shape = self.shape
        # 旋转shape矩阵
        self.shape = [list(row) for row in zip(*reversed(self.shape))]
        if not self.can_move(0, 0, self.board):
            # 如果旋转后位置无效，恢复原来的形状
            self.shape = old_shape

    def move(self, dx, dy):
        # 移动方块的方法
        if self.can_move(dx, dy, self.board):
            # 如果可以移动，更新方块的位置
            self.x += dx
            self.y += dy
            return True
        return False


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
        self.board = [[0 for _ in range(350 // 35)] for _ in range(700 // 35)]
        self.screen_width = 350
        self.screen_height = 700
        self.score = 0  # 分数
        self.clock = pygame.time.Clock()
        self.fall_time = 0  # 用于跟踪方块的下落时间
        self.paused = False  # 游戏是否暂停
        self.block = Block(self.board)  # 俄罗斯方块对象
        self.current_block = Block(self.board)  # 初始化当前的方块
        self.next_block = Block(self.board)  # 初始化下一个要下落的方块
        super().__init__()

    def Draw(self):
        self.screen.fill((0, 0, 0))
        # 绘制分隔线
        pygame.draw.line(self.screen, (255, 255, 255), (350, 0), (350, 700))
        # 绘制固定的方块
        for y, row in enumerate(self.board):
            for x, color in enumerate(row):
                if color != 0:
                    pygame.draw.rect(self.screen, color,
                                     (x * self.block_size, y * self.block_size,
                                      self.block_size, self.block_size))
        self.current_block.draw(self.screen)
        self.draw_next_block(self.screen)

    def draw_next_block(self, screen):
        next_block_x = self.screen_width + 15
        next_block_y = 100
        for i in range(len(self.next_block.shape)):
            for j in range(len(self.next_block.shape[i])):
                if self.next_block.shape[i][j] == 1:
                    pygame.draw.rect(
                        screen, self.next_block.color,
                        (next_block_x + j * self.block_size,
                         next_block_y + i * self.block_size,
                         self.block_size, self.block_size))

    def generate_next_block(self):
        self.current_block = self.next_block  # 当前方块变为下一个方块
        self.next_block = Block(self.board)  # 生成新的下一个方块

    def Handle_Event(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
            if event.type == pygame.QUIT:
                sm.scenemanager.change_scene("scene_mode")
        if not self.paused:
            for event in events:
                if event.type == pygame.USEREVENT:
                    self.clear_complete_rows()
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.current_block.rotate()
                    if event.key == pygame.K_SPACE:
                        while self.current_block.move(0, 1):  # 循环移动方块直到触底
                            pass
                        self.update_board()
                    if event.key == pygame.K_LEFT:
                        self.current_block.move(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        self.current_block.move(1, 0)
                    if event.key == pygame.K_DOWN:
                        self.current_block.move(0, 1)  # 循环移动方块直到触底

            self.check_game_over()
            current_time = pygame.time.get_ticks()
            if current_time - self.fall_time > self.block_speed * 1000:
                self.fall_time = current_time
                if not self.current_block.move(0, 1):
                    # 触底则固定方块并更新游戏区域数组
                    for event in events:
                        if event.type == pygame.USEREVENT:
                            self.clear_complete_rows()
                            pygame.time.set_timer(pygame.USEREVENT, 0)
                    self.update_board()

                    # self.check_game_over()

    def update_board(self):
        for i in range(len(self.current_block.shape)):
            for j in range(len(self.current_block.shape[i])):
                if self.current_block.shape[i][j] == 1:
                    self.board[self.current_block.y + i][self.current_block.x +
                                                         j] = self.current_block.color
        clear_rows = []
        for i in range(len(self.board)):
            if all(self.board[i]):
                clear_rows.append(i)
        if clear_rows:
            pygame.time.set_timer(pygame.USEREVENT, 200)

        self.current_block = Block(self.board)
        self.generate_next_block()

    def clear_complete_rows(self):
        for i in range(len(self.board)):
            if all(self.board[i]):
                del self.board[i]
                self.board.insert(0, [0 for _ in range(self.screen_width // self.block_size)])

    def reset_game(self):
        # 清空游戏区域
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.board[i][j] = 0
        self.score = 0
        self.current_block = Block(self.board)
        self.fall_time = 0

    def check_game_over(self):
        # 检查游戏是否结束
        if any(row for row in self.board[0]):
            self.reset_game()
