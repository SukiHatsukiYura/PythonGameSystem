import pygame
import start_scene
import mode_scene
import scene_2048
import scene_sudoku
import scene_sudoku2
import time


class SceneManager:
    """
    场景管理器，负责切换场景、绘制场景、处理事件
    """
    current_scene: object = None  #当前场景对象
    #场景字典
    scene_dict = {
        "start_scene": start_scene.StartScene,  #开始场景
        "mode_scene": mode_scene.ModeScene,  #模式选择场景
        "scene_2048": scene_2048.Game2048,  #2048游戏场景
        "scene_sudoku": scene_sudoku.GameSudoku,  #数独游戏场景
        "scene_sudoku2": scene_sudoku2.GameSudoku2  #数独游戏场景2
    }

    current_scene = scene_dict["scene_sudoku2"]()

    #current_scene = scene_dict["start_scene"]()

    def change_scene(self, scene_name):
        """
        切换场景
        """
        self.current_scene = self.scene_dict[scene_name]()

    def handle_event(self):
        """
        处理事件
        """
        self.current_scene.handle_event()

    def draw_scene(self):
        """
        绘制当前场景
        """
        self.current_scene.draw()


scenemanager = SceneManager()
