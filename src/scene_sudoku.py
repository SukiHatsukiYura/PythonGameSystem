import pygame
import scene
import scene_manager as sm
import random
import time


# 定义GameSudoku类，继承自scene.Scene
class GameSudoku(scene.Scene):
    # 定义属性
    GRID_SIZE: int  # 横纵格子数量
    GRID_WH: int  # 格子宽度高度
    LINE_W: int  # 网格线宽度
    # 数独界面外边框宽度
    BOX_W: int  # 数独界面外边框宽度
    BOX_H: int  # 数独界面外边框高度
    GRID_LINE_COLOR_1: tuple  # 网格线颜色1
    GRID_LINE_COLOR_2: tuple  # 网格线颜色2
    SELECT_COLOR: tuple  # 选中格子颜色
    num_color: tuple  # 数字颜色
    num_font = pygame.font.Font(pygame.font.match_font("SimHei"), 48)
    number_list: list  # 数字列表

    def __init__(self):
        self.GRID_SIZE = 9
        self.GRID_WH = 70
        self.LINE_W = 2
        self.BOX_W = 150
        self.BOX_H = 150
        self.GRID_LINE_COLOR_1 = (200, 200, 200)
        self.GRID_LINE_COLOR_2 = (0, 0, 0)
        self.SELECT_COLOR = (255, 225, 255)
        self.num_color = (0, 0, 0)
        self.last_grid = (0, 0)
        self.current_grid = (0, 0)
        self.number_list = [[0 for _ in range(9)] for _ in range(9)]
        self.last_grid
        self.current_grid
        self.generate_sudoku()
        self.remove_cells('medium')
        # 数独界面大小(9*50+2*(9+1),9*50+2*(9+1))=(470,470)
        self.size = (
            (self.GRID_SIZE * self.GRID_WH) + self.LINE_W *
            (self.GRID_SIZE + 1) + self.BOX_W,  #
            (self.GRID_SIZE * self.GRID_WH) + self.LINE_W *
            (self.GRID_SIZE + 1))  #

        self.selected_surface = pygame.Surface((self.GRID_WH, self.GRID_WH))
        super().__init__()
        pygame.display.set_caption("数独")  # 设置标题

    # 绘制整个游戏界面
    def draw(self):
        self.screen.fill((255, 255, 255))  # 填充背景色
        self.selected_surface.fill((255, 225, 255))  # 填充选中格子的背景色
        #self.screen.blit(self.selected_surface, (2, 2))  # 绘制选中格子的效果

        self.draw_line()  # 绘制网格线
        self.draw_number()  # 绘制数字
        self.draw_grid()  # 绘制当前选择格子的效果

    def draw_line(self):
        # 绘制游戏网格的水平和垂直线条
        for i in range(self.GRID_SIZE + 1):
            if i % 3 != 0:
                # 绘制灰色垂直线条
                pygame.draw.line(
                    self.screen, self.GRID_LINE_COLOR_1,
                    (i * self.GRID_WH + self.LINE_W * i, 0),
                    (i * self.GRID_WH + self.LINE_W * i, self.size[1] - 2),
                    self.LINE_W)
                # 绘制灰色水平线条
                pygame.draw.line(self.screen, self.GRID_LINE_COLOR_1,
                                 (0, i * self.GRID_WH + self.LINE_W * i),
                                 (self.size[0] - 2 - self.BOX_W,
                                  i * self.GRID_WH + self.LINE_W * i),
                                 self.LINE_W)

        # 绘制黑色垂直线条
        for i in range(self.GRID_SIZE + 1):
            if i % 3 == 0:
                # 绘制黑色垂直线条
                pygame.draw.line(
                    self.screen, self.GRID_LINE_COLOR_2,
                    (i * self.GRID_WH + self.LINE_W * i, 0),
                    (i * self.GRID_WH + self.LINE_W * i, self.size[1] - 2),
                    self.LINE_W)
                # 绘制黑色水平线条
                pygame.draw.line(self.screen, self.GRID_LINE_COLOR_2,
                                 (0, i * self.GRID_WH + self.LINE_W * i),
                                 (self.size[0] - 2 - self.BOX_W,
                                  i * self.GRID_WH + self.LINE_W * i),
                                 self.LINE_W)

    # 绘制数字
    def draw_number(self):
        # 绘制数独中的数字
        for i in range(9):
            for j in range(9):
                # 如果该位置上的数字不为0，则绘制数字
                if self.number_list[i][j] != 0:
                    # 创建文本对象
                    text = self.num_font.render(str(self.number_list[i][j]),
                                                True, self.num_color)
                    text_rect = text.get_rect()
                    # 设置文本的位置
                    text_rect.center = ((j + 0.5) * self.GRID_WH +
                                        self.LINE_W * (j + 1),
                                        (i + 0.5) * self.GRID_WH +
                                        self.LINE_W * (i + 1))
                    # 在屏幕上绘制文本
                    self.screen.blit(text, text_rect)

    # 绘制当前选择格子的效果
    def draw_grid(self):
        #清除上一次选中的格子效果
        last_y, last_x = self.last_grid
        if self.number_list[last_x][last_y] != 0:
            for x in range(self.GRID_SIZE):
                for y in range(self.GRID_SIZE):
                    if self.number_list[x][y] == self.number_list[last_x][
                            last_y]:
                        self.screen.blit(
                            self.selected_surface,
                            ((y + 0.5) * self.GRID_WH + self.LINE_W *
                             (y + 1) - self.GRID_WH / 2,
                             (x + 0.5) * self.GRID_WH + self.LINE_W *
                             (x + 1) - self.GRID_WH / 2))  # 绘制选中格子的效果
        else:
            last_x = (last_x + 0.5) * self.GRID_WH + self.LINE_W * (last_x + 1)
            last_y = (last_y + 0.5) * self.GRID_WH + self.LINE_W * (last_y + 1)
            self.screen.blit(self.selected_surface,
                             (last_y - self.GRID_WH / 2,
                              last_x - self.GRID_WH / 2))  # 绘制选中格子的效果

        # 绘制当前选择格子的效果
        current_y, current_x = self.current_grid
        if self.number_list[current_x][current_y] != 0:
            for x in range(self.GRID_SIZE):
                for y in range(self.GRID_SIZE):
                    if self.number_list[x][y] == self.number_list[current_x][
                            current_y]:
                        self.screen.blit(
                            self.selected_surface,
                            ((y + 0.5) * self.GRID_WH + self.LINE_W *
                             (y + 1) - self.GRID_WH / 2,
                             (x + 0.5) * self.GRID_WH + self.LINE_W *
                             (x + 1) - self.GRID_WH / 2))  # 绘制选中格子的效果
                        snum_color = (255, 0, 0)

                        # 创建文本对象
                        text = self.num_font.render(
                            str(self.number_list[x][y]), True, snum_color)
                        text_rect = text.get_rect()
                        # 设置文本的位置
                        text_rect.center = ((y + 0.5) * self.GRID_WH +
                                            self.LINE_W * (y + 1),
                                            (x + 0.5) * self.GRID_WH +
                                            self.LINE_W * (x + 1))
                        # 在屏幕上绘制文本
                        self.screen.blit(text, text_rect)
        else:
            current_x = (current_x +
                         0.5) * self.GRID_WH + self.LINE_W * (current_x + 1)
            current_y = (current_y +
                         0.5) * self.GRID_WH + self.LINE_W * (current_y + 1)
            self.screen.blit(self.selected_surface,
                             (current_y - self.GRID_WH / 2,
                              current_x - self.GRID_WH / 2))  # 绘制选中格子的效果

    # 处理事件
    def handle_event(self):
        # 处理用户交互事件
        pos = pygame.mouse.get_pos()  # 获取鼠标位置
        x, y = pos
        # 根据鼠标位置判断操作所在的区域
        if (x > self.LINE_W and y
                > self.LINE_W) or (x < self.size[0] - self.LINE_W - self.BOX_W
                                   and y < self.size[1] - self.LINE_W):
            x_index = (x + self.LINE_W) // self.GRID_WH
            y_index = (y + self.LINE_W) // self.GRID_WH
            x = (x - (x_index * self.LINE_W)) // self.GRID_WH
            y = (y - (y_index * self.LINE_W)) // self.GRID_WH
        else:
            x = 0
            y = 0

        for event in pygame.event.get():  # 遍历所有事件
            if event.type == pygame.QUIT:  # 如果事件为退出事件
                sm.scenemanager.change_scene("mode_scene")  # 切换场景为模式场景
            if event.type == pygame.MOUSEBUTTONDOWN and x < 9 and y < 9:  # 如果事件为鼠标按下事件且位置在有效区域内
                self.current_grid = (x, y)  # 更新当前选择的格子位置
                print(self.current_grid)
                self.last_grid = self.current_grid  # 更新上一次选中的格子位置

    # 数独的生成算法：
    # 1. 随机填充数字，直到没有唯一解
    # 2. 随机删除一些单元格，直到有唯一解
    # 3. 重复步骤1和步骤2，直到生成满意的数独
    def is_safe(self, row, col, num):
        # 检查数字在行中是否已被使用
        if num in self.number_list[row]:
            return False

        # 检查数字在列中是否已被使用
        if any(self.number_list[i][col] == num for i in range(9)):
            return False

        # 检查数字在3x3子网格中是否已被使用
        subgrid_row, subgrid_col = 3 * (row // 3), 3 * (col // 3)
        if any(num == self.number_list[subgrid_row + i][subgrid_col + j]
               for i in range(3) for j in range(3)):
            return False

        return True

    def solve_sudoku(self, row=0, col=0):
        if row == 9:  # 如果所有行都填满了，数独已解出
            return True

        next_row = row + 1 if col == 8 else row
        next_col = (col + 1) % 9
        grid_copy = [row[:] for row in self.number_list]
        if self.number_list[row][col] != 0:  # 跳过已填充的单元格
            return self.solve_sudoku(next_row, next_col)

        # 尝试不同的数字填入当前单元格
        for num in random.sample(range(1, 10), 9):
            if self.is_safe(row, col, num):
                self.number_list[row][col] = num
                if self.solve_sudoku(next_row, next_col):
                    return True
                self.number_list[row][col] = 0  # 如果填入的数字导致无解，则回溯

        return False  # 未找到解

    def generate_sudoku(self):
        self.number_list = [[0 for _ in range(9)] for _ in range(9)]
        self.solve_sudoku()  # 使用回溯法填充网格
        return self.number_list

    def remove_cells(self, difficulty='easy'):
        num_to_remove = 0
        if difficulty == 'easy':
            num_to_remove = 30
        elif difficulty == 'medium':
            num_to_remove = 40
        elif difficulty == 'hard':
            num_to_remove = 50

        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        for i, j in cells:
            if num_to_remove == 0:
                break
            temp = self.number_list[i][j]
            self.number_list[i][j] = 0
            # 检查数独谜题是否仍然有唯一解，如果没有，将该单元格的值还原
            if not self.has_unique_solution():
                self.number_list[i][j] = temp
            else:
                num_to_remove -= 1

    def has_unique_solution(self):
        return self.count_solutions() == 1

    def count_solutions(self, row=0, col=0):
        if row == 9:  # 如果所有行都填满了，找到一个解
            return 1

        next_row = row + 1 if col == 8 else row
        next_col = (col + 1) % 9
        if self.number_list[row][col] != 0:  # 跳过已填充的单元格
            return self.count_solutions(next_row, next_col)

        count = 0
        for num in random.sample(range(1, 10), 9):
            if self.is_safe(row, col, num):
                self.number_list[row][col] = num
                count += self.count_solutions(next_row, next_col)
                self.number_list[row][col] = 0  # 回溯
                if count > 1:
                    return count  # 如果找到多个解，立即返回，不再继续搜索

        return count
