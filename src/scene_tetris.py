import pygame
import random
import scene
import scene_manager as sm
import button
from tkinter import messagebox


class Block:
    # 俄罗斯方块类
    def __init__(self, board, x=4, y=0, block_size=35):
        self.board = board
        self.x = x
        self.y = y
        self.block_size = block_size  # 方块大小
        self.screen_width = block_size * 10
        self.screen_height = block_size * 20

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

    size = (350+35*4+40, 700)
    title = "俄罗斯方块"
    btn_back = button.Button(350+10, 630, 160, 60, (255, 255, 255), "返回", (0, 0, 0), 30)
    btn_restart = button.Button(350+10, 560, 160, 60, (255, 255, 255), "重新开始", (0, 0, 0), 30)
    btn_speed_add = button.Button(350+10, 490, 75, 60, (255, 255, 255), "速度+", (255, 0, 0), 22)
    btn_speed_reduce = button.Button(350+10+85, 490, 75, 60, (255, 255, 255), "速度-", (50, 205, 50), 22)

    def __init__(self):
        # 方块相关参数
        self.block_size = 35  # 方块大小
        self.block_speed = 10  # 方块下落速度
        # 界面显示相关参数
        self.screen_width = self.block_size * 10
        self.screen_height = self.block_size * 20
        self.board = [[0 for _ in range(self.screen_width // self.block_size)] for _ in range(self.screen_height // self.block_size)]
        self.score = 0  # 分数
        self.high_score = 0  # 最高分
        with open("score/score_tetris.txt", "r") as f:
            self.high_score = int(f.read())
        self.fall_time = 0  # 用于跟踪方块的下落时间
        self.paused = True  # 游戏是否暂停
        self.current_block = Block(self.board)  # 初始化当前的方块
        self.next_block = Block(self.board)  # 初始化下一个要下落的方块
        self.text_font = pygame.font.Font(pygame.font.match_font("SimHei"), 24)  # 字体
        self.key_img = pygame.image.load("img/ydlr.jpg")
        super().__init__()

    def Draw(self):
        self.screen.fill((255, 235, 205))
        # 绘制按键图标
        self.screen.blit(self.key_img, (self.screen_width + 20, 300))
        # 绘制分隔线
        pygame.draw.line(self.screen, (0, 0, 0), (350, 0), (350, 700), 2)
            
        # 绘制固定的方块        
        for y, row in enumerate(self.board):
            for x, color in enumerate(row):
                if color != 0:
                    pygame.draw.rect(self.screen, color,
                                     (x * self.block_size, y * self.block_size,
                                      self.block_size, self.block_size))
        self.current_block.draw(self.screen)
        self.draw_next_block(self.screen)
        self.draw_score(self.screen)
        self.draw_high_score(self.screen)

    def draw_next_block(self, screen):
        next_block_x = self.screen_width + 20
        next_block_y = 50
        for i in range(len(self.next_block.shape)):
            for j in range(len(self.next_block.shape[i])):
                if self.next_block.shape[i][j] == 1:
                    pygame.draw.rect(
                        screen, self.next_block.color,
                        (next_block_x + j * self.block_size,
                         next_block_y + i * self.block_size,
                         self.block_size, self.block_size))
        # 绘制包围下一个方块的框
        pygame.draw.rect(screen, (0, 0, 0),
                         (next_block_x - 20, next_block_y - 10,
                          self.block_size * 4 + 40, self.block_size * 4 + 20), 2)
        text = self.text_font.render("下一个方块", True, (0, 0, 0))
        # 绘制文本
        screen.blit(text, (next_block_x+10, 8))

        # 绘制速度
        text = self.text_font.render("速度:" + str(11-self.block_speed), True, (0, 0, 0))
        screen.blit(text, (self.screen_width + 5, 270))

    # 绘制分数
    def draw_score(self, screen):
        text = self.text_font.render("分数:" + str(self.score), True, (0, 0, 0))
        screen.blit(text, (self.screen_width + 5, 210))

    # 绘制最高分
    def draw_high_score(self, screen):
        text = self.text_font.render("最高分:" + str(self.high_score), True, (0, 0, 0))
        screen.blit(text, (self.screen_width + 5, 240))

    def generate_next_block(self):
        self.current_block = self.next_block  # 当前方块变为下一个方块
        self.next_block = Block(self.board)  # 生成新的下一个方块

    def update_score(self):
        self.score += 10
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_score()

    def save_score(self):
        with open("score/score_tetris.txt", "w", encoding="utf-8") as f:
            f.write(str(self.high_score))

    def Handle_Event(self):
        self.btn_back.btn_click(self.screen, sm.scenemanager.change_scene, mode="scene_mode")
        self.btn_restart.btn_click(self.screen, self.reset_game)
        self.btn_speed_add.btn_click(self.screen, self.set_speed, mode="add")
        self.btn_speed_reduce.btn_click(self.screen, self.set_speed, mode="reduce")
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                # 空格暂停游戏
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
            if event.type == pygame.QUIT:
                sm.scenemanager.change_scene("scene_mode")
        if not self.paused and not self.check_game_over():
            for event in events:
                # 定时器事件
                if event.type == pygame.USEREVENT:
                    self.clear_complete_rows()
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                if event.type == pygame.KEYDOWN:
                    # w/↑ 方块旋转
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.current_block.rotate()
                    # a/← 方块左移
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.current_block.move(-1, 0)
                    # d/→ 方块右移
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.current_block.move(1, 0)
                    # s/↓ 方块下移
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.current_block.move(0, 1)  # 移动方块直到触底
                    # enter 方块强降
                    if event.key == pygame.K_RETURN:
                        # 一次次地移动方块直到触底
                        for _ in range(self.screen_height // self.block_size):
                            if not self.current_block.move(0, 1):
                                break
                        self.update_board()

            current_time = pygame.time.get_ticks()

            time_interval = current_time - self.fall_time
            if time_interval > self.block_speed * 50:
                self.fall_time = current_time
                if not self.current_block.move(0, 1):
                    # 触底则固定方块并更新游戏区域数组
                    for event in pygame.event.get():
                        if event.type == pygame.USEREVENT:
                            self.clear_complete_rows()
                            pygame.time.set_timer(pygame.USEREVENT, 0)
                    self.update_board()
        elif self.check_game_over():
            messagebox.showinfo("游戏结束", "游戏结束！您的分数为：" + str(self.score)+"\n回车或点击确定按钮重新开始")
            self.reset_game()

    def update_board(self):
        # 更新游戏区域数组
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
                self.update_score()

    def set_speed(self, mode):
        match mode:
            case "add":
                self.block_speed = max(1, self.block_speed-1)
            case "reduce":
                self.block_speed = min(10, self.block_speed+1)
            case _:
                pass

    def reset_game(self):
        self.paused = True
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
            return True
        return False
