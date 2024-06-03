import pygame


class Scene:

    screen = None  # 场景对象
    size = None  # 场景大小
    title = None  # 场景标题
    bg_path = None  # 背景图片路径
    icon_path = None  # 图标路径

    def __init__(self):
        """
        :初始化场景对象
        """
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)

    def Draw(self):
        """
        绘制场景内容
        """
        pass

    def Handle_Event(self):
        """
        处理事件
        """
        pass
