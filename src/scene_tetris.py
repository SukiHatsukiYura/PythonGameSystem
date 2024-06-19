import pygame
import random
import scene
import scene_manager as sm
import button
from tkinter import messagebox


class Block:
    """
    俄罗斯方块类
    包含了方块的形状、颜色、位置、旋转、移动等方法
    以及绘制方块、绘制阴影、计算阴影偏移量等方法    
    """

    def __init__(self, board, x=4, y=0, block_size=35):
        """
        初始化方块
        :param board: 俄罗斯方块棋盘
        :param x: 方块左上角x坐标
        :param y: 方块左上角y坐标
        :param block_size: 方块大小
        """
        self.board = board #
        self.x = x
        self.y = y
        self.block_size = block_size  # 方块大小

        # 方块形状
        self.shapes = [
            [[1, 1, 1, 1]],
            [[1, 1, 1], [0, 1, 0]],
            [[1, 1, 1], [1, 0, 0]],
            [[1, 1, 1], [0, 0, 1]],
            [[1, 1, 0], [0, 1, 1]],
            [[0, 1, 1], [1, 1, 0]],
            [[1, 1], [1, 1]],
            [[1, 1], [1, 0]],
            [[1]]
        ]
        self.rotation = 0  # 方块旋转状态
        # 方块权重，用于随机选择方块
        self.shape_weigths = [2, 1, 1, 1, 1, 1, 1, 2, 1]
        # 随机选择一个方块
        self.shape = random.choices(self.shapes, weights=self.shape_weigths, k=1)[0]
        # self.shape = random.choice(self.shapes)

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

    def draw(self, screen):
        for i in range(len(self.shape)):  # 遍历行
            for j in range(len(self.shape[i])):  # 遍历列
                if self.shape[i][j] == 1:  # 如果该位置有方块
                    # 绘制方块
                    pygame.draw.rect(screen, self.color,
                                     (self.x * self.block_size + j * self.block_size,
                                      self.y * self.block_size + i * self.block_size,
                                      self.block_size, self.block_size))
        # 绘制该方块在底部的阴影
        self.draw_shadow(screen)

    def draw_shadow(self, screen):
        # 计算阴影的垂直偏移量
        y_offset = self.calculate_shadow_offset()

        # 创建一个与方块大小相同的表面作为阴影
        shadow_rect = pygame.Surface((self.block_size, self.block_size))
        shadow_rect.set_alpha(100)  # 设置阴影透明度
        shadow_rect.fill(self.color)  # 填充颜色与方块颜色相同的颜色

        # 遍历方块形状的每个单元格
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                # 如果单元格为1，表示形状的一部分，将阴影绘制到屏幕上
                if self.shape[i][j] == 1:
                    screen.blit(shadow_rect,
                                (self.x * self.block_size + j * self.block_size,
                                 (self.y + y_offset) * self.block_size + i * self.block_size))

    def calculate_shadow_offset(self):
        # 计算阴影的偏移量
        y_offset = 0
        while self.can_move(0, y_offset + 1, self.board):  # 当可以向下移动时
            y_offset += 1  # 增加偏移量直到无法向下移动
        return y_offset  # 返回y方向偏移量

    def can_move(self, dx, dy, board):
        # 提前计算新位置的坐标
        new_x = self.x + dx
        new_y = self.y + dy
        # 检查当前方块是否能够在指定的偏移量下移动到新位置
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell == 1:
                    if self.is_out_of_bound(new_x + j, new_y + i, board) or self.is_collision(new_x + j, new_y + i, board):
                        return False  # 如果发现有方块无法移动，则立即返回False
        return True

    # 检查坐标是否超出边界
    def is_out_of_bound(self, x, y, board):
        return x < 0 or x >= len(board[0]) or y >= len(board)

    # 检查是否发生了碰撞
    def is_collision(self, x, y, board):
        return y >= 0 and board[y][x] != 0

    # 旋转方块的方法
    def rotate(self):
        # 更新方块旋转状态
        self.rotation = (self.rotation + 1) % len(self.shape)
        old_shape = self.shape
        # 旋转shape矩阵
        self.shape = [list(row) for row in zip(*reversed(self.shape))]
        if not self.can_move(0, 0, self.board):
            # 如果旋转后位置无效，恢复原来的形状
            self.shape = old_shape

    # 移动方块的方法
    def move(self, dx, dy):
        # 如果可以移动，更新方块的位置
        if self.can_move(dx, dy, self.board):
            self.x += dx
            self.y += dy
            return True
        return False


class GameTetris(scene.Scene):

    size = (350 + 35 * 4 + 40, 700)
    title = "俄罗斯方块"
    icon_path = "img/tetris.jpg"

    black = (0, 0, 0)
    white = (255, 255, 255)
    btn_back = button.Button(350 + 10, 630, 160, 60, white, "返回", black, 30)
    btn_restart = button.Button(350 + 10, 560, 160, 60, white, "重新开始", black, 30)
    btn_speed_add = button.Button(350 + 10, 490, 75, 60, white, "速度+", (255, 0, 0), 22)
    btn_speed_reduce = button.Button(350 + 10 + 85, 490, 75, 60, white, "速度-", (50, 205, 50), 22)

    def __init__(self):
        # 方块相关参数
        self.block_size = 35  # 方块大小
        self.block_speed = 10  # 方块下落速度
        # 界面显示相关参数
        self.screen_width = self.block_size * 10  # 350
        self.screen_height = self.block_size * 20  # 700
        # 网格
        self.board = [[0 for _ in range(self.screen_width // self.block_size)]
                      for _ in range(self.screen_height // self.block_size)]
        self.score = 0  # 分数
        self.high_score = 0  # 最高分
        # 获取最高分
        try:
            with open("score/score_tetris.txt", "r") as f:
                self.high_score = int(f.read())
        except FileNotFoundError:
            print("文件不存在")
        self.fall_time = 0  # 用于跟踪方块的下落时间
        self.paused = True  # 游戏是否暂停
        self.current_block = Block(self.board)  # 初始化当前的方块
        self.next_block = Block(self.board)  # 初始化下一个要下落的方块
        self.text_font = pygame.font.Font(pygame.font.match_font("SimHei"), 24)  # 字体
        self.icon = pygame.image.load(self.icon_path)
        super().__init__()

    def Draw(self):
        self.screen.fill((255, 235, 205))
        self.draw_line()

        # 绘制固定的方块
        # 遍历self.board中的每一行，同时获取行号y和行数据row
        for y, row in enumerate(self.board):
            # 对于每一行中的每个元素，获取列号x和颜色值color
            for x, color in enumerate(row):
                # 检查颜色值是否不为0，即该位置有方块
                if color != 0:
                    pygame.draw.rect(self.screen, color,
                                     (x * self.block_size, y * self.block_size,
                                      self.block_size, self.block_size))
        # 绘制当前方块
        self.current_block.draw(self.screen)
        # 绘制下一个方块
        self.draw_next_block(self.screen)
        # 绘制按键操作说明
        self.key_help(self.screen)
        # 绘制分数
        self.draw_score(self.screen)
        # 绘制速度
        self.screen.blit(self.text_font.render("速度:" + str(11 - self.block_speed), True, (0, 0, 0)),
                         (self.screen_width + 5, 270))

    def draw_line(self):
        # 绘制网格线
        for i in range(-1, self.screen_width+1, self.block_size):
            pygame.draw.line(self.screen, (200, 200, 200), (i, 0), (i, 700), 2)
        for i in range(-1, self.screen_height+1, self.block_size):
            pygame.draw.line(self.screen, (200, 200, 200), (0, i), (350, i), 2)
        # 绘制分隔线
        pygame.draw.line(self.screen, (0, 0, 0), (350, 0), (350, 700), 2)

    def draw_next_block(self, screen):
        next_block_x = self.screen_width + 20
        next_block_y = 50
        for i in range(len(self.next_block.shape)):
            for j in range(len(self.next_block.shape[i])):
                if self.next_block.shape[i][j] == 1:
                    pygame.draw.rect(screen, self.next_block.color,
                                     (next_block_x + j * self.block_size,
                                      next_block_y + i * self.block_size,
                                      self.block_size, self.block_size))
        # 绘制包围下一个方块的框
        pygame.draw.rect(screen, (0, 0, 0),
                         (next_block_x - 20, next_block_y - 10,
                          self.block_size * 4 + 40, self.block_size * 4 + 20), 2)
        # 绘制文本
        screen.blit(self.text_font.render("下一个方块", True, (0, 0, 0)), (next_block_x + 10, 8))

    # 绘制按键操作说明

    def key_help(self, screen):
        screen.blit(self.text_font.render("W/↑:方块旋转", True, (0, 0, 0)), (355, 300))
        screen.blit(self.text_font.render("A/←:方块左移", True, (0, 0, 0)), (355, 330))
        screen.blit(self.text_font.render("D/→:方块右移", True, (0, 0, 0)), (355, 360))
        screen.blit(self.text_font.render("S/↓:方块下移", True, (0, 0, 0)), (355, 390))
        screen.blit(self.text_font.render("空格:暂停/继续", True, (0, 0, 0)), (355, 420))
        screen.blit(self.text_font.render("回车:强降", True, (0, 0, 0)), (355, 450))

    # 绘制分数
    def draw_score(self, screen):
        screen.blit(self.text_font.render("分数:" + str(self.score), True, (0, 0, 0)), (self.screen_width + 5, 210))
        screen.blit(self.text_font.render("最高分:" + str(self.high_score), True, (0, 0, 0)), (self.screen_width + 5, 240))

    # 生成下一个方块
    def generate_next_block(self):
        self.current_block = self.next_block  # 当前方块变为下一个方块
        self.next_block = Block(self.board)  # 生成新的下一个方块

    # 更新分数
    def update_score(self):
        self.score += 10
        if self.score > self.high_score:
            self.high_score = self.score
            # 保存最高分
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
                # ESC退出游戏,返回菜单
                if event.key == pygame.K_ESCAPE:
                    sm.scenemanager.change_scene("scene_mode")
            if event.type == pygame.QUIT:
                sm.scenemanager.change_scene("scene_mode")
        if not self.paused and not self.check_game_over():
            for event in events:
                # 定时器事件
                if event.type == pygame.USEREVENT:
                    self.clear_complete_rows()
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                if event.type == pygame.KEYDOWN:
                    self.move_block(event)

            current_time = pygame.time.get_ticks()
            time_interval = current_time - self.fall_time
            if time_interval > self.block_speed * 120:
                self.fall_time = current_time
                if not self.current_block.move(0, 1):
                    # 触底则固定方块并更新游戏区域数组
                    for event in pygame.event.get():
                        if event.type == pygame.USEREVENT:
                            self.clear_complete_rows()
                            pygame.time.set_timer(pygame.USEREVENT, 0)
                    self.update_board()
        elif self.check_game_over():
            messagebox.showinfo(
                "游戏结束",
                "游戏结束！您的分数为：" + str(self.score) + "\n回车或点击确定按钮重新开始",
            )
            self.reset_game()

    def move_block(self, event):
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

    def update_board(self):
        # 更新游戏区域数组
        for i in range(len(self.current_block.shape)):
            for j in range(len(self.current_block.shape[i])):
                if self.current_block.shape[i][j] == 1:
                    self.board[self.current_block.y +
                               i][self.current_block.x +
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
                self.board.insert(
                    0,
                    [0 for _ in range(self.screen_width // self.block_size)])
                self.update_score()

    # 设置速度
    def set_speed(self, mode):
        match mode:
            case "add":
                self.block_speed = max(-2, self.block_speed - 1)
            case "reduce":
                self.block_speed = min(10, self.block_speed + 1)
    
    # 重置游戏
    def reset_game(self):
        self.paused = True
        # 清空游戏区域
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.board[i][j] = 0
        self.score = 0
        self.current_block = Block(self.board)
        self.fall_time = 0

    # 检查游戏是否结束
    def check_game_over(self):
        if any(row for row in self.board[0]):
            return True
        return False
