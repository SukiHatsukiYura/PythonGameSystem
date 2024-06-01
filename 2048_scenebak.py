import pygame
import random


# 定义游戏类
class Game2048():

    def __init__(self, grid_size=4, cell_size=100):
        self.GRID_SIZE = grid_size
        self.CELL_SIZE = cell_size
        self.GRID_WIDTH = self.GRID_SIZE * self.CELL_SIZE
        self.GRID_HEIGHT = self.GRID_SIZE * self.CELL_SIZE
        self.BACKGROUND_COLOR = (187, 173, 160)
        self.TEXT_COLOR = (255, 255, 255)
        self.score = 0
        self.grid = [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)]
        self.font = pygame.font.Font(None, 48)

    def draw(self, window):
        # 绘制游戏界面网格
        window.fill(self.BACKGROUND_COLOR)
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                cell_value = self.grid[row][col]
                cell_color = self.get_cell_color(cell_value)
                cell_rect = pygame.Rect(col * self.CELL_SIZE,
                                        row * self.CELL_SIZE, self.CELL_SIZE,
                                        self.CELL_SIZE)
                pygame.draw.rect(window, cell_color, cell_rect)
                if cell_value != 0:
                    self.draw_text(window, str(cell_value), cell_rect)

        # 绘制积分
        score_text = self.font.render("Score: " + str(self.score), True,
                                      self.TEXT_COLOR)
        window.blit(score_text, (10, self.GRID_HEIGHT + 10))

    def draw_text(self, window, text, rect):
        # 在单元格内绘制数字
        text_surface = self.font.render(text, True, self.TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = rect.center
        window.blit(text_surface, text_rect)

    def get_cell_color(self, value):
        # 根据方块的值获取对应的颜色
        colors = {
            0: (205, 193, 180),
            2: (238, 228, 218),
            4: (237, 224, 200),
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46),
        }
        return colors.get(value, (0, 0, 0))

    def add_new_tile(self):
        # 在随机空位置生成一个新数字（2或4）
        empty_cells = [(i, j) for i in range(self.GRID_SIZE)
                       for j in range(self.GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.grid[row][col] = random.choice([2, 4])

    def move_tiles_left(self):
        # 向左移动所有数字块
        for row in range(self.GRID_SIZE):
            merged = [False] * self.GRID_SIZE
            for col in range(1, self.GRID_SIZE):
                if self.grid[row][col] != 0:
                    k = col
                    while k > 0 and self.grid[row][k - 1] == 0:
                        self.grid[row][k - 1] = self.grid[row][k]
                        self.grid[row][k] = 0
                        k -= 1
                    if k > 0 and not merged[k - 1] and self.grid[row][
                            k - 1] == self.grid[row][k]:
                        self.grid[row][k - 1] *= 2
                        self.grid[row][k] = 0
                        merged[k - 1] = True
                        self.score += self.grid[row][k - 1]  # 更新积分

    def move_tiles_up(self):
        # 向上移动所有数字块

        for col in range(self.GRID_SIZE):
            merged = [False] * self.GRID_SIZE
            for row in range(1, self.GRID_SIZE):
                if self.grid[row][col] != 0:
                    k = row
                    while k > 0 and self.grid[k - 1][col] == 0:
                        self.grid[k - 1][col] = self.grid[k][col]
                        self.grid[k][col] = 0
                        k -= 1
                    if k > 0 and not merged[k - 1] and self.grid[
                            k - 1][col] == self.grid[k][col]:
                        self.grid[k - 1][col] *= 2
                        self.grid[k][col] = 0
                        merged[k - 1] = True
                        self.score += self.grid[k - 1][col]  # 更新积分

    def move_tiles_right(self):
        # 向右移动所有数字块

        for row in range(self.GRID_SIZE):
            merged = [False] * self.GRID_SIZE
            for col in range(self.GRID_SIZE - 2, -1, -1):
                if self.grid[row][col] != 0:
                    k = col
                    while k < self.GRID_SIZE - 1 and self.grid[row][k +
                                                                    1] == 0:
                        self.grid[row][k + 1] = self.grid[row][k]
                        self.grid[row][k] = 0
                        k += 1
                    if k < self.GRID_SIZE - 1 and not merged[
                            k + 1] and self.grid[row][k +
                                                      1] == self.grid[row][k]:
                        self.grid[row][k + 1] *= 2
                        self.grid[row][k] = 0
                        merged[k + 1] = True
                        self.score += self.grid[row][k + 1]  # 更新积分

    def move_tiles_down(self):
        # 向下移动所有数字块

        for col in range(self.GRID_SIZE):
            merged = [False] * self.GRID_SIZE
            for row in range(self.GRID_SIZE - 2, -1, -1):
                if self.grid[row][col] != 0:
                    k = row
                    while k < self.GRID_SIZE - 1 and self.grid[k +
                                                               1][col] == 0:
                        self.grid[k + 1][col] = self.grid[k][col]
                        self.grid[k][col] = 0
                        k += 1
                    if k < self.GRID_SIZE - 1 and not merged[
                            k + 1] and self.grid[k +
                                                 1][col] == self.grid[k][col]:
                        self.grid[k + 1][col] *= 2
                        self.grid[k][col] = 0
                        merged[k + 1] = True
                        self.score += self.grid[k + 1][col]  # 更新积分

    def is_game_over(self):
        # 检查游戏是否结束（无法再移动数字块）
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                if self.grid[row][col] == 0:
                    return False
                if col < self.GRID_SIZE - 1 and self.grid[row][
                        col] == self.grid[row][col + 1]:
                    return False
                if row < self.GRID_SIZE - 1 and self.grid[row][
                        col] == self.grid[row + 1][col]:
                    return False
        return True

    def draw_grid(self):
        # 绘制游戏界面网格
        window.fill(self.BACKGROUND_COLOR)
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                cell_value = self.grid[row][col]
                cell_color = self.get_cell_color(cell_value)
                cell_rect = pygame.Rect(col * self.CELL_SIZE,
                                        row * self.CELL_SIZE, self.CELL_SIZE,
                                        self.CELL_SIZE)
                pygame.draw.rect(window, cell_color, cell_rect)
                if cell_value != 0:
                    self.draw_text(cell_value, cell_rect)

        # 绘制积分
        score_text = self.font.render("Score: " + str(self.score), True,
                                      self.TEXT_COLOR)
        window.blit(score_text, (10, self.GRID_HEIGHT + 10))

    def update_score(self, points):
        # 更新积分

        self.score += points


# 初始化Pygame
pygame.init()
# 创建游戏窗口
window = pygame.display.set_mode((400, 400 + 50))
pygame.display.set_caption("2048")
# 创建游戏实例
game = Game2048()
game.add_new_tile()
game.add_new_tile()
# 游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game.is_game_over():
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    game.move_tiles_left()
                    game.add_new_tile()
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    game.move_tiles_right()
                    game.add_new_tile()
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    game.move_tiles_up()
                    game.add_new_tile()
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    game.move_tiles_down()
                    game.add_new_tile()  # 在移动后生成新数字块

    # 绘制游戏界面
    game.draw(window)
    pygame.display.update()

pygame.quit()
