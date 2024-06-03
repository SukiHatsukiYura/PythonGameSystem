import pygame
import scene
import scene_manager as sm
import random
import copy
from tkinter import messagebox
import button as btn
import numpy as np


class GridRect():
    """
    网格矩形类
    初始化：
    x,y,w,h: 矩形左上角坐标和矩形宽高
    color: 矩形颜色，默认为白色
    """

    def __init__(self, x, y, w, h, color=(255, 255, 255)):
        self.x = x  # 左上角x坐标
        self.y = y  # 左上角y坐标
        self.w = w  # 矩形宽度
        self.h = h  # 矩形高度
        # 所在行列
        self.__x_index = (x + 2) // w
        self.__y_index = (y + 2) // h
        self.col = (x - (self.__x_index * 2)) // w  # 所在行
        self.row = (y - (self.__y_index * 2)) // h  # 所在列
        self.color = color  # 矩形颜色
        self.num = 0  # 数字
        self.num_font = pygame.font.Font(pygame.font.match_font("SimHei"),
                                         48)  # 设置数字字体
        self.text_color = (0, 0, 0)  # 矩形内文本颜色

    def draw(self, screen, number):
        # 绘制矩形
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
        # 如果 self.num 不等于0，则将 text 渲染到屏幕上的 text_rect 位置
        if self.num != 0:
            # 转换数字为对象
            text = self.num_font.render(str(number), True, self.text_color)
            text_rect = text.get_rect()
            # 设置文本位置居中
            text_rect.center = (self.x + self.w / 2, self.y + self.h / 2)
            screen.blit(text, text_rect)


class GameSudoku(scene.Scene):
    GridSideLength = 650  # 数独整个网格边长,包括网格宽度
    RegionWidth = 200  # 控制区域大小
    size = (GridSideLength + RegionWidth, GridSideLength)  # 窗口大小
    icon_path = "img/sudoku.jpg"
    # 难度切换按钮--简单
    btn_easy = btn.Button(670, 300, 160, 60, (255, 255, 255), "简单", (50, 205, 50), 32)
    # 难度切换按钮--中等
    btn_medium = btn.Button(670, 370, 160, 60, (255, 255, 255), "中等", (205, 149, 12), 32)
    # 难度切换按钮--困难
    btn_hard = btn.Button(670, 440, 160, 60, (255, 255, 255), "困难", (255, 0, 0), 32)
    # 新局按钮
    btn_reset = btn.Button(670, 510, 160, 60, (255, 255, 255), "新局", (0, 0, 0), 32)
    # 返回按钮
    btn_exit = btn.Button(670, 580, 160, 60, (255, 255, 255), "返回", (0, 0, 0), 32)

    def __init__(self):
        # 定义游戏网格相关参数
        self.GridSize70 = 70  # 网格边长
        self.GridLineWidth = 2  # 网格线条宽度
        self.GridLineColor_Black = (0, 0, 0)  # 网格线条颜色-黑色
        self.GridLineColor_Gray = (200, 200, 200)  # 网格线条颜色-灰色
        self.SELECT_COLOR = (255, 225, 255)  # 选中格子颜色
        self.UNSELECT_COLOR = (255, 255, 235)  # 未选中格子颜色
        # 定义游戏数字相关参数
        self.mode = 'easy'  # 数独难度模式,默认简单模式
        self.Number = [[0 for _ in range(9)] for _ in range(9)]  # 9x9的数字矩阵
        self.generate_sudoku()  # 生成数独
        self.NumberCompare = copy.deepcopy(self.Number)  # 保存当前数独的完整版本
        self.remove_cells(self.mode)  # 移除一些单元格，使数独难度变为简单
        self.NumberCpoy = copy.deepcopy(self.Number)  # 保存当前数独的难度版本(即移除的单元格)
        self.NumerColor = (0, 0, 0)  # 常规数字颜色
        self.NumerTrueColor = (0, 255, 0)  # 正确数字颜色
        self.NumerFalseColor = (255, 0, 0)  # 错误数字颜色
        # 定义文本信息相关参数
        self.text_font = pygame.font.Font(pygame.font.match_font("SimHei"), 20)  # 设置文本字体
        # 定义键盘事件映射字典
        self.key_mapping = {pygame.K_BACKSPACE: 0, pygame.K_1: 1,
                            pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4, pygame.K_5: 5,
                            pygame.K_6: 6, pygame.K_7: 7, pygame.K_8: 8, pygame.K_9: 9
                            }
        # 定义9x9的格子矩阵,存放81个矩形(格子)对象,每个网格的边长为70像素,网格线条宽度为2像素,网格颜色为白色
        self.GridRect81 = [[GridRect(x * self.GridSize70 + (2 * x + 2), y * self.GridSize70 + 2 * (y + 1),
                                     self.GridSize70, self.GridSize70) for y in range(9)] for x in range(9)]
        self.CurrentGrid = self.GridRect81[4][4]  # 保存当前选中的格子坐标
        super().__init__()  # 窗口初始化
        self.screen.fill((255, 255, 255))  # 填充背景颜色
        self.title = "数独"  # 设置标题
        self.icon = pygame.image.load(self.icon_path)  # 设置图标

    def Draw(self):
        self.screen.fill((255, 255, 235))
        self.draw_selected_grid()
        self.draw_number()
        self.draw_line()
        self.draw_text()

    def draw_text(self):
        # 使用numpy将矩阵转换为数组，并计算还需填入的格子数量
        lst_num = np.array(self.Number)
        # 如果场上还有空白格子，则在区域显示要填入的单元格还有多少
        self.screen.blit(self.text_font.render("还需填入  个格子", True, (0, 0, 0)), (670, 10))
        text_num = self.text_font.render(str((lst_num == 0).sum()), True, (255, 97, 0))
        # 让数字居中显示
        self.screen.blit(self.text_font.render(str((lst_num == 0).sum()), True, (255, 97, 0)), text_num.get_rect(center=((680 + 80), 20)))
        # 绘制当前模式
        self.screen.blit(self.text_font.render("当前模式: ", True, (0, 0, 0)), (670, 36))
        if self.mode == 'easy':
            mode_text = self.text_font.render("简单", True, (50, 205, 50))
        elif self.mode == 'medium':
            mode_text = self.text_font.render("中等", True, (205, 149, 12))
        else:
            mode_text = self.text_font.render("困难", True, (255, 0, 0))
        self.screen.blit(mode_text, (670 + 100, 36))

        # 绘制各数字还有多少个
        for i in range(1, 10):
            number = self.text_font.render(str((lst_num == i).sum()), True, (255, 97, 0))
            self.screen.blit(self.text_font.render("数字" + str(i) + ":   个", True, (0, 0, 0)), (670, 38 + 26 * i))
            self.screen.blit(number, number.get_rect(center=((670 + 75), 48 + 26 * i)))

    def draw_line(self):
        # 绘制游戏网格的水平和垂直线条
        for i in range(10):
            if i % 3 != 0:
                # 绘制灰色垂直线条
                pygame.draw.line(
                    self.screen, self.GridLineColor_Gray,
                    (i * self.GridSize70 + self.GridLineWidth * i, 0),
                    (i * self.GridSize70 + self.GridLineWidth * i, self.GridSideLength),
                    self.GridLineWidth)
                # 绘制灰色水平线条
                pygame.draw.line(
                    self.screen, self.GridLineColor_Gray,
                    (0, i * self.GridSize70 + self.GridLineWidth * i),
                    (self.GridSideLength, i * self.GridSize70 + self.GridLineWidth * i),
                    self.GridLineWidth)
        for i in range(10):
            if i % 3 == 0:
                # 绘制黑色垂直线条
                pygame.draw.line(
                    self.screen, self.GridLineColor_Black,
                    (i * self.GridSize70 + self.GridLineWidth * i, 0),
                    (i * self.GridSize70 + self.GridLineWidth * i,
                     self.GridSideLength - self.GridLineWidth), self.GridLineWidth)
                # 绘制黑色水平线条
                pygame.draw.line(
                    self.screen, self.GridLineColor_Black,
                    (0, i * self.GridSize70 + self.GridLineWidth * i),
                    (self.GridSideLength - self.GridLineWidth,
                     i * self.GridSize70 + self.GridLineWidth * i),
                    self.GridLineWidth)

    def draw_number(self):
        # 更改数字颜色
        for i in range(9):
            for j in range(9):
                # 判断是否是初始格子矩阵上不为0的格子
                if self.NumberCpoy[i][j] != 0:
                    self.GridRect81[i][j].num = self.NumberCpoy[i][j]
                    self.GridRect81[i][j].text_color = self.NumerColor
                else:
                    if self.Number[i][j] == self.NumberCompare[i][j]:
                        self.GridRect81[i][j].num = self.Number[i][j]
                        self.GridRect81[i][j].text_color = self.NumerTrueColor
                    else:
                        self.GridRect81[i][j].num = self.Number[i][j]
                        self.GridRect81[i][j].text_color = self.NumerFalseColor
                # 绘制数字
                self.GridRect81[i][j].draw(self.screen, self.Number[i][j])

    def draw_selected_grid(self):
        """
        更改选中格子所在的九宫格和行列的格子颜色
        """
        # 重置所有格子颜色为未选中颜色
        for i in range(9):
            for j in range(9):
                self.GridRect81[i][j].color = self.UNSELECT_COLOR
        if self.CurrentGrid is None:  # 未选中任何格子
            return
        # 选中当前格子所在的九宫格和行列的格子颜色
        colstart = (self.CurrentGrid.row // 3) * 3
        rowstart = (self.CurrentGrid.col // 3) * 3
        for i in range(3):
            for j in range(3):
                self.GridRect81[rowstart + i][colstart + j].color = self.SELECT_COLOR

        for i in range(9):
            # 绘制横向格子的效果
            self.GridRect81[i][self.CurrentGrid.row].color = self.SELECT_COLOR
            # 绘制纵向格子的效果
            self.GridRect81[self.CurrentGrid.col][i].color = self.SELECT_COLOR

        if self.CurrentGrid.num != 0:
            # 绘制所有与当前选中格子相同的格子
            for i in range(9):
                for j in range(9):
                    if self.Number[i][j] == self.CurrentGrid.num:
                        self.GridRect81[i][j].color = (135, 206, 235)
        elif self.CurrentGrid.num == 0:
            self.CurrentGrid.color = (135, 206, 235)

    def Handle_Event(self):
        """
        处理事件
        """
        # 按钮事件
        self.btn_easy.btn_click(self.screen, self.restart, mode="easy")
        self.btn_medium.btn_click(self.screen, self.restart, mode="medium")
        self.btn_hard.btn_click(self.screen, self.restart, mode="hard")
        self.btn_reset.btn_click(self.screen, self.restart, mode=self.mode)
        self.btn_exit.btn_click(self.screen, sm.scenemanager.change_scene, mode="scene_mode")
        if self.CurrentGrid is None:
            x, y = 0, 0
        else:
            x, y = (self.CurrentGrid.col, self.CurrentGrid.row)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sm.scenemanager.change_scene("scene_mode")
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                x, y = pos  # 获取鼠标位置
                # 根据鼠标位置判断操作所在的区域
                if (x > self.GridLineWidth and y > self.GridLineWidth) and (x < self.GridSideLength - self.GridLineWidth + self.RegionWidth and y < self.GridSideLength - self.GridLineWidth):
                    x_index = (x + self.GridLineWidth) // self.GridSize70
                    y_index = (y + self.GridLineWidth) // self.GridSize70
                    x = (x - (x_index * self.GridLineWidth)) // self.GridSize70
                    y = (y - (y_index * self.GridLineWidth)) // self.GridSize70
                else:
                    x = 0
                    y = 0
                if x < 9 and y < 9:
                    self.CurrentGrid = self.GridRect81[x][y]
                    print("当前格子坐标：", self.CurrentGrid.row, self.CurrentGrid.col)
                else:
                    self.CurrentGrid = None
                    print("区域外格子坐标:", x, y)

                # 如果游戏胜利，弹出提示框，点确定游戏重新开始，点取消显示完整的棋盘，且不能再进行游戏,再次点击棋盘才会弹出提示框
                if self.is_win() and x < 9 and y < 9:
                    self.draw_number()
                    if messagebox.askyesno("恭喜", "你已经完成本次数独!" + "\n是否重新开始?", icon="question") == True:  # 重新开始游戏
                        self.restart()
                    else:
                        pass
            if x < 9 and y < 9 and self.CurrentGrid is not None:
                if self.NumberCpoy[x][y] == 0:
                    if event.type == pygame.KEYDOWN and event.key in self.key_mapping:
                        self.Number[x][y] = self.key_mapping[event.key]

    # 判断是否胜利
    def is_win(self):
        for i in range(9):
            for j in range(9):
                if self.Number[i][j] != self.NumberCompare[i][j]:
                    return False    # 存在错误数字，游戏未结束
        return True

    # 重新开始游戏

    def restart(self, mode='easy'):
        self.mode = mode
        self.generate_sudoku()  # 生成数独
        self.NumberCompare = copy.deepcopy(self.Number)  # 保存当前数独的完整版本
        self.remove_cells(self.mode)  # 移除一些单元格，使数独难度变为简单
        self.NumberCpoy = copy.deepcopy(self.Number)  # 保存当前数独的难度版本(即移除的单元格)

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
        # grid_copy = [row[:] for row in self.Number]
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
        # 根据难度级别确定需要移除的单元格数量
        num_to_remove = 0
        if difficulty == 'easy':
            num_to_remove = 20
        elif difficulty == 'medium':
            num_to_remove = 30
        elif difficulty == 'hard':
            num_to_remove = 50

        # 生成数独单元格的坐标
        cells = [(i, j) for i in range(9) for j in range(9)]
        # 随机打乱单元格顺序
        random.shuffle(cells)
        # 遍历单元格并移除指定数量的单元格
        for i, j in cells:
            if num_to_remove == 0:
                break
            # temp = self.Number[i][j]
            self.Number[i][j] = 0
            # # 检查数独谜题是否仍然有唯一解，如果没有，将该单元格的值还原
            # if not self.has_unique_solution():
            #     self.Number[i][j] = temp
            # else:
            num_to_remove -= 1

    # def has_unique_solution(self):
    #     return self.count_solutions() == 1

    # def count_solutions(self, row=0, col=0):
    #     if row == 9:  # 如果所有行都填满了，找到一个解
    #         return 1

    #     next_row = row + 1 if col == 8 else row
    #     next_col = (col + 1) % 9
    #     if self.Number[row][col] != 0:  # 跳过已填充的单元格
    #         return self.count_solutions(next_row, next_col)

    #     count = 0
    #     for num in random.sample(range(1, 10), 9):
    #         if self.is_safe(row, col, num):
    #             self.Number[row][col] = num
    #             count += self.count_solutions(next_row, next_col)
    #             self.Number[row][col] = 0  # 回溯
    #             if count > 1:
    #                 return count  # 如果找到多个解，立即返回，不再继续搜索
    #     return count
