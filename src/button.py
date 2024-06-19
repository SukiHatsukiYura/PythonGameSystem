import pygame


class Button:
    """
    :按钮类
    :包含按钮的基本属性和方法
    :__init__(self, x, y, width, height, color, text, text_color, font_size): 初始化按钮属性
    :draw(self, screen, transparent_color=255): 绘制按钮
    :is_clicked(self, mouse_pos): 检查按钮是否被点击
    """

    def __init__(self, x, y,
                 width, height, color,
                 text, text_color, font_size,
                 font_name=pygame.font.match_font("SimHei")):
        pygame.init()
        # 初始化按钮的属性
        self.x = x  # 按钮左上角的x坐标

        self.y = y  # 按钮左上角的y坐标
        self.width = width  # 按钮的宽度
        self.height = height  # 按钮的高度
        self.color = color  # 按钮的颜色，默认为黑色
        self.text = text  # 按钮上显示的文本内容
        self.text_color = text_color  # 文本颜色，默认为黑色
        self.font_size = font_size  # 文本字体大小
        self.font_name = font_name  # 字体名称，默认为黑体
        self.font = pygame.font.Font(font_name, self.font_size)  # 字体对象

    def draw(self, screen, transparent_color=255):
        """
        绘制按钮
        screen: 当前屏幕对象
        transparent_color: 透明色,默认为255
        """
        # 绘制圆角按钮
        # 创建一个与矩形相同尺寸的表面
        rect_surface = pygame.Surface((self.width, self.height),
                                      pygame.SRCALPHA)

        # 在表面上绘制一个带有圆角的矩形
        pygame.draw.rect(rect_surface,
            (self.color[0], self.color[1], self.color[2], transparent_color),
            (0, 0, self.width, self.height), border_radius=15)
        # 在按钮四周加上边框
        pygame.draw.rect(rect_surface, (0, 0, 0),
                         (0, 0, self.width, self.height),
                         width=5,
                         border_radius=10)
        # 将绘制好的矩形表面放置在屏幕上的指定位置
        screen.blit(rect_surface, (self.x, self.y))
        text = self.font.render(self.text, True, (self.text_color))
        # 文本居中
        text_rect = text.get_rect(center=(self.x + self.width / 2,
                                          self.y + self.height / 2)) 
        screen.blit(text, text_rect) # 绘制文本

    def btn_click(self, screen, *args, mode=None, unclick_color=(237, 224, 200), click_color=(127, 127, 127)):
        """
        按钮点击事件
        :param screen: 当前屏幕对象
        :param args: 可变参数，包含所有需要切换的游戏模式的函数
        :param mode: 要切换的游戏模式(切换函数参数)，需用关键字参数传入
        """
        if self.is_clicked(pygame.mouse.get_pos()) == True:
            self.color = click_color  # 设置按钮颜色为灰色
            if pygame.event.poll().type == pygame.MOUSEBUTTONUP:  # 检测到鼠标按下
                for fun in args:  # 遍历所有切换函数
                    if mode is not None:  # 如果有传入函数参数
                        fun(mode)  # 调用函数并传入参数
                    else:
                        fun()  # 调用函数
        else:
            self.color = unclick_color  # 恢复按钮颜色为米黄色
        self.draw(screen, 120)  # 重新绘制按钮

    def is_clicked(self, mouse_pos):
        # 检查按钮是否被点击
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[
                1] < self.y + self.height:
            return True
        return False
