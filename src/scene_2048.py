import pygame
import random
import scene
import scene_manager as sm
import button
import tkinter as tk
from tkinter import messagebox
import json


# 定义游戏类
class Game2048(scene.Scene):

    # 定义属性
    GRID_SIZE: int  # 格子数量
    CELL_SIZE: int  # 格子大小(正方形)
    GRID_WIDTH: int  # 格子宽度
    GRID_HEIGHT: int  # 格子高度
    BACKGROUND_COLOR: tuple  # 背景颜色
    TEXT_COLOR: tuple  # 文字颜色
    text_font: None  # 文字字体
    GRID_COLOR: tuple  # 格子字体颜色
    grid_font: None  # 格子数据字体
    score: int  # 积分
    grid: list  # 格子数据
    mode: str  # 游戏模式
    score_dict: dict  # 最高分字典
    high_scroe_4x4: int  # 4x4最高分
    high_scroe_5x5: int  # 5x5最高分
    high_scroe_6x6: int  # 6x6最高分
    # 定义按钮
    btn_4x4 = button.Button(665, 250, 170, 60, (237, 224, 200), "4x4",
                            (0, 0, 0), 32)
    btn_5x5 = button.Button(665, 330, 170, 60, (237, 224, 200), "5x5",
                            (0, 0, 0), 32)
    btn_6x6 = button.Button(665, 410, 170, 60, (237, 224, 200), "6x6",
                            (0, 0, 0), 32)
    btn_restart = button.Button(665, 490, 170, 60, (237, 224, 200), "重新开始",
                                (0, 0, 0), 32)
    btn_back = button.Button(665, 570, 170, 60, (237, 224, 200), "返回",
                             (0, 0, 0), 32)

    def __init__(self):
        # 初始化游戏属性
        # 4X4 4 150
        # 5X5 5 118
        # 6X6 6 96
        self.mode = "4x4"
        self.GRID_SIZE = 4
        self.CELL_SIZE = 150
        self.GRID_WIDTH = self.GRID_SIZE * self.CELL_SIZE
        self.GRID_HEIGHT = self.GRID_SIZE * self.CELL_SIZE
        self.BACKGROUND_COLOR = (187, 173, 160)
        self.TEXT_COLOR = (237, 204, 97)
        self.GRID_COLOR = (255, 255, 255)
        self.score = 0
        # 读取最高分
        with open("score/score_2048.json", encoding="utf-8") as f:
            self.score_dict = json.load(f)
            self.high_scroe_4x4 = self.score_dict["high_scroe_4x4"]
            self.high_scroe_5x5 = self.score_dict["high_scroe_5x5"]
            self.high_scroe_6x6 = self.score_dict["high_scroe_6x6"]

        self.grid = [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)]
        self.text_font = pygame.font.Font(pygame.font.match_font("SimHei"), 28)
        self.grid_font = pygame.font.Font(pygame.font.match_font("SimHei"), 48)
        self.screen = pygame.display.set_mode((600 + 50 + 200, 600 + 50))
        pygame.display.set_caption("2048")
        # 绘制按钮
        self.btn_back.draw(self.screen)
        self.btn_restart.draw(self.screen)
        self.btn_6x6.draw(self.screen)
        self.btn_5x5.draw(self.screen)
        self.btn_4x4.draw(self.screen)
        self.add_new_tile()
        self.add_new_tile()

    def restart(self, mode="4x4"):
        # 重新开始游戏
        self.mode = mode
        match mode:
            case "4x4":
                self.GRID_SIZE = 4
                self.CELL_SIZE = 150
            case "5x5":
                self.GRID_SIZE = 5
                self.CELL_SIZE = 118
            case "6x6":
                self.GRID_SIZE = 6
                self.CELL_SIZE = 96
        self.score = 0
        self.grid = [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)]
        self.add_new_tile()
        self.add_new_tile()

    def draw(self):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.draw_gird()
        self.draw_score()
        self.draw_lines()

    def draw_gird(self):
        # 绘制格子
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                cell_value = self.grid[row][col]
                cell_color = self.get_cell_color(cell_value)
                cell_rect = pygame.Rect(
                    col * (self.CELL_SIZE + 10) + 10,  # 绘制单元格
                    row * (self.CELL_SIZE + 10) + 10,
                    self.CELL_SIZE,
                    self.CELL_SIZE)
                pygame.draw.rect(self.screen, cell_color, cell_rect)
                if cell_value != 0:
                    self.draw_text(self.screen, str(cell_value), cell_rect)

    def draw_lines(self):
        # 绘制外框线
        pygame.draw.line(self.screen, (255, 225, 255), (648, 0), (648, 650), 2)
        pygame.draw.line(self.screen, (255, 225, 255), (0, 0), (648, 0), 2)
        pygame.draw.line(self.screen, (255, 225, 255), (0, 0), (0, 650), 2)
        pygame.draw.line(self.screen, (255, 225, 255), (0, 647), (647, 647), 2)

    def draw_score(self):
        # 绘制积分
        score_text = self.text_font.render("当前分数:", True, (255,225,255))
        score_text_num = self.text_font.render(str(self.score), True,
                                               self.TEXT_COLOR)
        # 绘制最高分

        self.screen.blit(score_text, (660, 10))
        self.screen.blit(score_text_num, (660, 50))

        self.screen.blit(self.text_font.render("最高分数:", True,(255,225,255)),
                         (660, 90))
        self.screen.blit(
            self.text_font.render("4x4:" + str(self.high_scroe_4x4).strip(),
                                  True, self.TEXT_COLOR), (660, 130))
        self.screen.blit(
            self.text_font.render("5x5:" + str(self.high_scroe_5x5).strip(),
                                  True, self.TEXT_COLOR), (660, 170))
        self.screen.blit(
            self.text_font.render("6x6:" + str(self.high_scroe_6x6).strip(),
                                  True, self.TEXT_COLOR), (660, 210))

    def draw_text(self, screen, text, rect):
        # 在单元格内绘制数字
        text_surface = self.grid_font.render(text, True, self.GRID_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = rect.center
        screen.blit(text_surface, text_rect)

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
                        self.update_score(self.grid[row][k - 1])  # 更新积分

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
                        self.update_score(self.grid[k - 1][col])  # 更新积分

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
                        self.update_score(self.grid[row][k + 1])  # 更新积分

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
                        self.update_score(self.grid[k + 1][col])  # 更新积分

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

    def handle_event(self):
        if self.btn_4x4.is_clicked(pygame.mouse.get_pos()) == True:
            self.btn_4x4.color = (127, 127, 127)  # 设置按钮颜色为灰色
            if pygame.event.poll().type == pygame.MOUSEBUTTONUP:  # 检测到鼠标按下
                self.restart("4x4")  # 切换到4x4游戏
        else:
            self.btn_4x4.color = (237, 224, 200)  # 恢复按钮颜色为白色
        self.btn_4x4.draw(self.screen)  # 重新绘制4x4按钮
        if self.btn_5x5.is_clicked(pygame.mouse.get_pos()) == True:
            self.btn_5x5.color = (127, 127, 127)  # 设置按钮颜色为灰色
            if pygame.event.poll().type == pygame.MOUSEBUTTONUP:  # 检测到鼠标按下
                self.restart("5x5")  # 切换到5x5游戏
        else:
            self.btn_5x5.color = (237, 224, 200)  # 恢复按钮颜色为白色
        self.btn_5x5.draw(self.screen)  # 重新绘制5x5按钮
        if self.btn_6x6.is_clicked(pygame.mouse.get_pos()) == True:
            self.btn_6x6.color = (127, 127, 127)  # 设置按钮颜色为灰色
            if pygame.event.poll().type == pygame.MOUSEBUTTONUP:  # 检测到鼠标按下
                self.restart("6x6")  # 切换到6x6游戏
        else:
            self.btn_6x6.color = (237, 224, 200)  # 恢复按钮颜色为白色
        self.btn_6x6.draw(self.screen)  # 重新绘制6x6按钮
        # 如果光标在返回按钮上，则设置按钮背景色为灰色，否则恢复为白色
        if self.btn_back.is_clicked(pygame.mouse.get_pos()) == True:
            self.btn_back.color = (127, 127, 127)  # 设置按钮颜色为灰色
            if pygame.event.poll().type == pygame.MOUSEBUTTONUP:  # 检测到鼠标按下
                sm.scenemanager.change_scene("mode_scene")  # 切换到游戏场景
        else:
            self.btn_back.color = (237, 224, 200)  # 恢复按钮颜色为白色
        self.btn_back.draw(self.screen)  # 重新绘制返回按钮
        # 如果光标在重新开始按钮上，则设置按钮背景色为灰色，否则恢复为白色
        if self.btn_restart.is_clicked(pygame.mouse.get_pos()) == True:
            self.btn_restart.color = (127, 127, 127)  # 设置按钮颜色为灰色
            if pygame.event.poll().type == pygame.MOUSEBUTTONUP:  # 检测到鼠标按下
                self.restart(self.mode)  # 重新开始游戏
        else:
            self.btn_restart.color = (237, 224, 200)  # 恢复按钮颜色为白色
        self.btn_restart.draw(self.screen)  # 重新绘制重新开始按钮
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sm.scenemanager.change_scene("mode_scene")  # 切换到游戏场景
            elif event.type == pygame.KEYDOWN:
                if not self.is_game_over():
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.move_tiles_left()
                        self.add_new_tile()
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.move_tiles_right()
                        self.add_new_tile()
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.move_tiles_up()
                        self.add_new_tile()
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.move_tiles_down()
                        self.add_new_tile()  # 在移动后生成新数字块
                else:
                    #self.popup("游戏结束!\n是否重新开始?")  # 弹出提示框
                    if self.popup("游戏结束!", "是否重新开始?") == True:  # 重新开始游戏
                        self.restart()  # 重新开始游戏
                    else:
                        pass

    def popup(self, title, message):
        # 弹出提示框
        return messagebox.askyesno(title, message)  # 返回True或False

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

    def update_score(self, points):
        # 更新积分
        self.score += points
        match self.mode:
            case "4x4":
                if self.score > int(self.high_scroe_4x4):
                    self.high_scroe_4x4 = self.score
                    self.score_dict["high_scroe_4x4"] = self.high_scroe_4x4
                    self.save_score()

            case "5x5":
                if self.score > int(self.high_scroe_5x5):
                    self.high_scroe_5x5 = self.score
                    self.score_dict["high_scroe_5x5"] = self.high_scroe_5x5
                    self.save_score()
            case "6x6":
                if self.score > int(self.high_scroe_6x6):
                    self.high_scroe_6x6 = self.score
                    self.score_dict["high_scroe_6x6"] = self.high_scroe_6x6
                    self.save_score()

    def save_score(self):
        # 保存积分
        with open("score/score_2048.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(self.score_dict))
