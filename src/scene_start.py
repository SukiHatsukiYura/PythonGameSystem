import pygame
import scene
import button
import scene_manager as sm


class StartScene(scene.Scene):
    """
    :开始场景,继承自场景基类(scene.Scene)
    :包含两个按钮,一个是开始按钮,一个是退出按钮
    """
    size = (800, 633)  # 场景尺寸
    title = "开始"  # 标题
    bg_path = "img/bg.jpg"  # 背景图片路径
    btn_start = button.Button(300, 300, 200, 100, (255, 255, 255), "开 始",
                              (0, 0, 0), 50)  # 开始按钮
    btn_quit = button.Button(300, 420, 200, 100, (255, 255, 255), "退 出",
                             (0, 0, 0), 50)  # 退出按钮

    pygame.mixer.music.load('mus/03_悪役令嬢の顛末.mp3')  # 加载背景音乐
    pygame.mixer.music.set_volume(0.5)  # 设置音量
    pygame.mixer.music.play(-1)  # 循环播放背景音乐

    def __init__(self):
        super().__init__()
        self.icon = pygame.image.load(self.bg_path)
        self.text_font = pygame.font.Font(pygame.font.match_font("SimHei"), 20)  # 设置文本字体

    def Draw(self):  # 绘制场景
        self.screen.fill((0, 0, 0))  # 填充背景色,清屏
        bg = pygame.image.load(self.bg_path).convert()  # 加载背景图片
        scaled_bg = pygame.transform.smoothscale(bg, self.size)  # 缩放背景图片
        self.screen.blit(scaled_bg, (0, 0))  # 将背景图片覆盖到屏幕上

        self.btn_start.draw(self.screen, 120)  # 画出开始按钮
        self.btn_quit.draw(self.screen, 120)  # 画出退出按钮
        # 绘制文本信息
        self.screen.blit(self.text_font.render("Enter To Start", True, (0, 0, 0)), (332, 373))
        self.screen.blit(self.text_font.render("ESC To Quit", True, (0, 0, 0)), (344, 493))

    def Handle_Event(self):  # 处理事件
        self.btn_start.btn_click(self.screen, sm.scenemanager.change_scene, mode="scene_mode")
        self.btn_quit.btn_click(self.screen, pygame.quit, exit)
        if pygame.event.poll().type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_RETURN]:  # 按下回车键
                sm.scenemanager.change_scene("scene_mode")  # 切换到游戏场景
            elif pygame.key.get_pressed()[pygame.K_m]:  # 按下m键
                pygame.mixer.music.pause()  # 暂停背景音乐
            elif pygame.key.get_pressed()[pygame.K_n]:  # 按下n键
                pygame.mixer.music.unpause()  # 恢复背景音乐
            elif pygame.key.get_pressed()[pygame.K_ESCAPE]:  # 按下ESC键
                pygame.quit()  # 退出pygame
                exit()  # 退出程序
