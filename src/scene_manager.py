import pygame
import scene_start
import scene_mode
import scene_2048
import scene_sudoku
import scene_tetris


class SceneManager:
    """
    场景管理器，负责切换场景、绘制场景、处理事件
    """
    current_scene: object = None  # 当前场景对象
    # 场景字典
    scene_dict = {
        "scene_start": scene_start.StartScene(),  # 开始场景
        "scene_mode": scene_mode.ModeScene(),  # 模式选择场景
        "scene_2048": scene_2048.Game2048(),  # 2048游戏场景
        "scene_sudoku": scene_sudoku.GameSudoku(),  # 数独游戏场景
        "scene_tetris": scene_tetris.GameTetris()  # 俄罗斯方块游戏场景
    }

    def __init__(self):
        self.current_scene = self.scene_dict["scene_start"]
        pygame.display.set_mode((800, 633))
        pygame.display.set_icon(self.current_scene.icon)
        pygame.display.set_caption(self.current_scene.title)  # 设置标题

    def change_scene(self, scene_name):
        """
        切换场景
        """
        self.current_scene = self.scene_dict[scene_name]
        if scene_name == "scene_mode" or \
                scene_name == "scene_2048" or \
                scene_name == "scene_sudoku":
            pygame.display.set_mode(self.current_scene.size)
            pygame.display.set_icon(self.current_scene.icon)
            pygame.display.set_caption(self.current_scene.title)  # 设置标题
        elif scene_name == "scene_tetris":
            pygame.display.set_mode((500, 700))
            pygame.display.set_caption(self.current_scene.title)  # 设置标题
        else:
            pygame.display.set_caption(self.current_scene.title)  # 设置标题

        print(f"\r切换到场景:{scene_name}", end="")

    def Handle_Event(self):
        """
        处理事件
        """
        self.current_scene.Handle_Event()

    def Draw_Scene(self):
        """
        绘制当前场景
        """
        self.current_scene.Draw()


scenemanager = SceneManager()
