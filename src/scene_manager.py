import pygame
import start_scene
import mode_scene
import scene_2048
import scene_sudoku


class SceneManager:
    """
    场景管理器，负责切换场景、绘制场景、处理事件
    """
    current_scene: object = None  # 当前场景对象
    # 场景字典
    scene_dict = {
        "start_scene": start_scene.StartScene(),  # 开始场景
        "mode_scene": mode_scene.ModeScene(),  # 模式选择场景
        "scene_2048": scene_2048.Game2048(),  # 2048游戏场景
        "scene_sudoku": scene_sudoku.GameSudoku(),  # 数独游戏场景
    }

    #current_scene = scene_dict["scene_sudoku"]

    current_scene = scene_dict["start_scene"]
    pygame.display.set_mode((800, 633))
    def change_scene(self, scene_name):
        """
        切换场景
        """
        self.current_scene = self.scene_dict[scene_name]
        if scene_name == "mode_scene":
            pygame.display.set_mode(self.current_scene.size)
        if scene_name == "scene_2048":
            pygame.display.set_mode(self.current_scene.size)
            pygame.display.set_icon(self.current_scene.icon)
        if scene_name == "scene_sudoku":
            pygame.display.set_mode(self.current_scene.size)
            pygame.display.set_icon(self.current_scene.icon)

        print("切换到场景:", scene_name)

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
