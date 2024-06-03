import pygame
import random

# 初始化 pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# 设置游戏窗口
screen_width = 350
screen_height = 700
block_size = 35
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("俄罗斯方块")

# 定义方块类型形状
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 1, 0], [1, 1, 0]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1], [1, 1]]
]

# 定义方块颜色
colors = [CYAN, YELLOW, PURPLE, GREEN, BLUE, ORANGE, RED]

# 创建一个俄罗斯方块类
class Tetris:
    def __init__(self):
        self.x = 5
        self.y = 0
        self.shape = random.choice(shapes)
        self.color = random.choice(colors)
        self.rotation = 0  # 用于跟踪方块的旋转状态

    def draw(self):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j] == 1:
                    pygame.draw.rect(screen, self.color, (self.x * block_size + j * block_size,
                                     self.y * block_size + i * block_size, block_size, block_size))

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
                    if self.x + j + dx < 0 or self.x + j + dx >= screen_width / block_size or self.y + i + dy >= screen_height / block_size:
                        return False
                    if self.y + i + dy >= 0 and board[self.y + i + dy][self.x + j + dx] != 0:
                        return False
        return True


def clear_lines():
    # 如果有可以消除的行，则延迟一段时间再消除
    clear_rows = []
    for i in range(len(board)):
        if all(board[i]):
            clear_rows.append(i)
    if clear_rows:
        pygame.time.delay(900)  # 延迟300毫秒
        for row in clear_rows:
            del board[row]
            board.insert(0, [0 for _ in range(screen_width // block_size)])


# 在主循环中添加一个代表游戏区域的二维数组
board = [[0 for _ in range(screen_width // block_size)] for _ in range(screen_height // block_size)]

# 更新主循环中的方块下落逻辑


def main():
    clock = pygame.time.Clock()
    tetris = Tetris()
    fall_time = 0
    block_speed = 0.8

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    tetris.rotate()
                if event.key == pygame.K_SPACE:
                    while tetris.move(0, 1):  # 循环移动方块直到触底
                        pass
                    # 触底则固定方块并更新游戏区域数组
                    for i in range(len(tetris.shape)):
                        for j in range(len(tetris.shape[i])):
                            if tetris.shape[i][j] == 1:
                                board[tetris.y + i][tetris.x + j] = tetris.color
                    # 检查是否有可以消行的情况，并更新 board
                    clear_rows = []
                    for i in range(len(board)):
                        if all(board[i]):
                            clear_rows.append(i)
                    for row in clear_rows:
                        del board[row]
                        board.insert(0, [0 for _ in range(screen_width // block_size)])
                    tetris = Tetris()

                if event.key == pygame.K_LEFT:
                    tetris.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    tetris.move(1, 0)

        current_time = pygame.time.get_ticks()
        if current_time - fall_time > block_speed * 1000:
            fall_time = current_time
            if not tetris.move(0, 1):
                # 触底则固定方块并更新游戏区域数组
                for i in range(len(tetris.shape)):
                    for j in range(len(tetris.shape[i])):
                        if tetris.shape[i][j] == 1:
                            board[tetris.y + i][tetris.x + j] = tetris.color
                # 检查是否有可以消行的情况，并更新 board
                clear_rows = []
                for i in range(len(board)):
                    if all(board[i]):
                        clear_rows.append(i)
                for row in clear_rows:
                    del board[row]
                    board.insert(0, [0 for _ in range(screen_width // block_size)])
                tetris = Tetris()

        screen.fill((0, 0, 0))

        # 绘制固定的方块
        for x in range(0, screen_width, block_size):
            pygame.draw.line(screen, GRAY, (x, 0), (x, screen_height))
        for y in range(0, screen_height, block_size):
            pygame.draw.line(screen, GRAY, (0, y), (screen_width, y))
        for y, row in enumerate(board):
            for x, color in enumerate(row):
                if color != 0:
                    pygame.draw.rect(screen, color, (x * block_size, y * block_size, block_size, block_size))
        tetris.draw()
        clear_lines()
        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    print(board)
    main()
