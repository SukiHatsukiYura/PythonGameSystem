import pygame
import scene
import scene_manager as sm
import random
import copy


class GridRect():
    """
    网格矩形类
    """

    def __init__(self, x, y, w, h, color):
        self.x = x  #左上角x坐标
        self.y = y  #左上角y坐标
        self.w = w  #矩形宽度
        self.h = h  #矩形高度
        #所在行列
        self.__x_index = (x + 2) // 70
        self.__y_index = (y + 2) // 70
        self.col = (x - (self.__x_index * 2)) // 70  #所在行
        self.row = (y - (self.__y_index * 2)) // 70  #所在列
        self.color = color  #矩形颜色
        self.num = 0  #数字
        self.num_font = pygame.font.Font(pygame.font.match_font("SimHei"),
                                         48)  #设置数字字体
        self.text_color = (0, 0, 0)  #矩形内文本颜色
    
    def draw(self, screen, sudoku):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
        text = self.num_font.render(str(sudoku), True, self.text_color)
        text_rect = text.get_rect()
        text_rect.center = (self.x + self.w / 2, self.y + self.h / 2)
        screen.blit(text, text_rect)


class GameSudoku2(scene.Scene):
    GridEntireSideLength = 650 # 数独整个网格边长,包括网格宽度
    ControlRegionWidth = 150 # 控制区域大小
    size = (650 + 150, 650)

    def __init__(self):
        # 定义游戏网格相关参数
        self.GridSize70 = 70  # 网格边长
        self.GridLineWidth = 2  # 网格线条宽度
        self.GridLineColor_Black = (0, 0, 0)  # 网格线条颜色-黑色
        self.GridLineColor_Gray = (200, 200, 200)  # 网格线条颜色-灰色
        # 定义游戏数字相关参数
        self.Number = [[0 for _ in range(9)] for _ in range(9)]  # 9x9的数字矩阵
        self.generate_sudoku()  # 生成数独
        self.NumberCompare = copy.deepcopy(self.Number)  # 保存当前数独的完整版本
        self.remove_cells('easy')  # 移除一些单元格，使数独难度变为简单
        self.NumberCpoy = copy.deepcopy(self.Number)  #保存当前数独的难度版本(即移除的单元格)

        # 定义9x9的格子矩阵,存放81个矩形(格子)对象
        self.GridRect81 = [[None for _ in range(9)] for _ in range(9)]

        super().__init__()
        pygame.display.set_caption("数独")  # 设置标题
        # 定义游戏网格,每个网格的边长为70像素,网格线条宽度为2像素,网格颜色为白色
        for x in range(9):
            for y in range(9):
                self.GridRect81[x][y] = GridRect(
                    x * self.GridSize70 + 2 * (x + 1),
                    y * self.GridSize70 + 2 * (y + 1), self.GridSize70,
                    self.GridSize70, (255, 255, 255))
        self.CurrentGrid = self.GridRect81[4][4]  # 保存当前选中的格子坐标
        self.LastGrid = self.CurrentGrid  # 保存上一次选中的格子坐标

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.draw_grid()
        self.draw_number()
        self.draw_line()
    def draw_line(self):
        # 绘制游戏网格的水平和垂直线条
        for i in range(10):
            if i % 3 != 0:
                # 绘制灰色垂直线条
                pygame.draw.line(
                    self.screen, self.GridLineColor_Gray,
                    (i * self.GridSize70 + self.GridLineWidth * i, 0),
                    (i * self.GridSize70 + self.GridLineWidth * i, 650),
                    self.GridLineWidth)
                # 绘制灰色水平线条
                pygame.draw.line(
                    self.screen, self.GridLineColor_Gray,
                    (0, i * self.GridSize70 + self.GridLineWidth * i),
                    (650, i * self.GridSize70 + self.GridLineWidth * i),
                    self.GridLineWidth)
        for i in range(10):
            if i % 3 == 0:
                # 绘制黑色垂直线条
                pygame.draw.line(
                    self.screen, self.GridLineColor_Black,
                    (i * self.GridSize70 + self.GridLineWidth * i, 0),
                    (i * self.GridSize70 + self.GridLineWidth * i,
                     650 - self.GridLineWidth), self.GridLineWidth)
                # 绘制黑色水平线条
                pygame.draw.line(
                    self.screen, self.GridLineColor_Black,
                    (0, i * self.GridSize70 + self.GridLineWidth * i),
                    (650 - self.GridLineWidth,
                     i * self.GridSize70 + self.GridLineWidth * i),
                    self.GridLineWidth)

    def draw_number(self):
        # 绘制游戏数字
        for x in range(9):
            for y in range(9):
                if self.Number[x][y] != 0:
                    self.GridRect81[x][y].num = self.Number[x][y]
                    self.GridRect81[x][y].draw(self.screen, self.Number[x][y])

    #绘制选中格子所在的九宫格和行列
    def draw_selected_grid(self):

        self.LastGrid.color = (255, 255, 255)
        #绘制选中格子所在的九宫格
        subgrid_row, subgrid_col = 3 * (self.CurrentGrid.row //
                                        3), 3 * (self.CurrentGrid.col // 3)
        for i in range(3):
            for j in range(3):
                self.GridRect81[subgrid_row + i][subgrid_col + j].color = (255,
                                                                           255,
                                                                           255)
        #绘制选中格子所在的行列
        for i in range(9):
            self.GridRect81[i][self.CurrentGrid.col].color = (255, 255, 255)
            self.GridRect81[self.CurrentGrid.row][i].color = (255, 255, 255)
        #self.CurrentGrid.color = (255, 0, 0)
        #绘制当前选中格子所在的九宫格
        subgrid_row, subgrid_col = 3 * (self.CurrentGrid.row //
                                        3), 3 * (self.CurrentGrid.col // 3)
        for i in range(3):
            for j in range(3):
                self.GridRect81[subgrid_row + i][subgrid_col + j].color = (255,
                                                                           0,
                                                                           0)
        #绘制当前选中格子所在的行列
        for i in range(9):
            self.GridRect81[i][self.CurrentGrid.col].color = (255, 0, 0)
            self.GridRect81[self.CurrentGrid.row][i].color = (255, 0, 0)
        self.GridRect81[self.CurrentGrid.row][self.CurrentGrid.col].color = (
            255, 0, 0)

    # 绘制当前选择格子的效果
    def draw_grid(self):
        self.draw_selected_grid()
        # self.draw_selected_grid(self.LastGrid)
        # self.draw_selected_grid(self.CurrentGrid)

    def handle_event(self):

        # 处理用户交互事件
        pos = pygame.mouse.get_pos()  # 获取鼠标位置
        x, y = pos
        # 根据鼠标位置判断操作所在的区域
        if (x > 2 and y > 2) or (x < 650 - 2 + 150 and y < 650):  # 有效区域
            x_index = (x + self.GridLineWidth) // self.GridSize70
            y_index = (y + self.GridLineWidth) // self.GridSize70
            x = (x - (x_index * self.GridLineWidth)) // self.GridSize70
            y = (y - (y_index * self.GridLineWidth)) // self.GridSize70
        else:
            x = 0
            y = 0

        for event in pygame.event.get():  # 遍历所有事件

            if event.type == pygame.QUIT:  # 事件为退出事件
                sm.scenemanager.change_scene("mode_scene")  # 切换场景为模式场景
            if event.type == pygame.MOUSEBUTTONDOWN and x < 9 and y < 9:  # 鼠标按下事件且位置在有效区域内
                self.CurrentGrid = self.GridRect81[x][y]  # 记录当前选中的格子坐标
                print("当前选中的格子坐标：", self.CurrentGrid.row, self.CurrentGrid.col)
            if event.type == pygame.MOUSEBUTTONUP and x < 9 and y < 9:  # 鼠标松开事件且位置在有效区域内
                self.LastGrid = self.CurrentGrid  # 记录上一次选中的格子坐标
                #print(x, y)
                print("上次选中的格子坐标：", self.LastGrid.row, self.LastGrid.col)

            if event.type == pygame.KEYUP:
                if self.GridRect81[x][y].num == 0:
                    if event.key == pygame.K_BACKSPACE:
                        self.Number[x][y] = 0
                    if event.key == pygame.K_1:
                        self.Number[x][y] = 1
                    if event.key == pygame.K_2:
                        self.Number[x][y] = 2
                    if event.key == pygame.K_3:
                        self.Number[x][y] = 3
                    if event.key == pygame.K_4:
                        self.Number[x][y] = 4
                    if event.key == pygame.K_5:
                        self.Number[x][y] = 5
                    if event.key == pygame.K_6:
                        self.Number[x][y] = 6
                    if event.key == pygame.K_7:
                        self.Number[x][y] = 7
                    if event.key == pygame.K_8:
                        self.Number[x][y] = 8
                    if event.key == pygame.K_9:
                        self.Number[x][y] = 9

    # 数独的生成算法：

    # 1. 随机填充数字，直到没有唯一解
    # 2. 随机删除一些单元格，直到有唯一解
    # 3. 重复步骤1和步骤2，直到生成满意的数独
    def is_safe(self, row, col, num):
        # 检查数字在行中是否已被使用
        if num in self.Number[row]:
            return False

        # 检查数字在列中是否已被使用
        if any(self.Number[i][col] == num for i in range(9)):
            return False

        # 检查数字在3x3子网格中是否已被使用
        subgrid_row, subgrid_col = 3 * (row // 3), 3 * (col // 3)
        if any(num == self.Number[subgrid_row + i][subgrid_col + j]
               for i in range(3) for j in range(3)):
            return False

        return True

    def solve_sudoku(self, row=0, col=0):
        if row == 9:  # 如果所有行都填满了，数独已解出
            return True

        next_row = row + 1 if col == 8 else row
        next_col = (col + 1) % 9
        grid_copy = [row[:] for row in self.Number]
        if self.Number[row][col] != 0:  # 跳过已填充的单元格
            return self.solve_sudoku(next_row, next_col)

        # 尝试不同的数字填入当前单元格
        for num in random.sample(range(1, 10), 9):
            if self.is_safe(row, col, num):
                self.Number[row][col] = num
                if self.solve_sudoku(next_row, next_col):
                    return True
                self.Number[row][col] = 0  # 如果填入的数字导致无解，则回溯

        return False  # 未找到解

    def generate_sudoku(self):
        self.Number = [[0 for _ in range(9)] for _ in range(9)]
        self.solve_sudoku()  # 使用回溯法填充网格
        return self.Number

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
            temp = self.Number[i][j]
            self.Number[i][j] = 0
            # 检查数独谜题是否仍然有唯一解，如果没有，将该单元格的值还原
            if not self.has_unique_solution():
                self.Number[i][j] = temp
            else:
                num_to_remove -= 1

    def has_unique_solution(self):
        return self.count_solutions() == 1

    def count_solutions(self, row=0, col=0):
        if row == 9:  # 如果所有行都填满了，找到一个解
            return 1

        next_row = row + 1 if col == 8 else row
        next_col = (col + 1) % 9
        if self.Number[row][col] != 0:  # 跳过已填充的单元格
            return self.count_solutions(next_row, next_col)

        count = 0
        for num in random.sample(range(1, 10), 9):
            if self.is_safe(row, col, num):
                self.Number[row][col] = num
                count += self.count_solutions(next_row, next_col)
                self.Number[row][col] = 0  # 回溯
                if count > 1:
                    return count  # 如果找到多个解，立即返回，不再继续搜索

        return count
