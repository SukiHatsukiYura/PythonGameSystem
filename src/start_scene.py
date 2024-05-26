import pygame
import scene
import button
import scene_manager as sm  # 导入场景管理器
from colorRGB import color


class StartScene(scene.Scene):
    """
    :开始场景,继承自场景基类(scene.Scene)
    :包含两个按钮,一个是开始按钮,一个是退出按钮
    """
    size = (800, 633)  # 场景尺寸
    title = "Game Start"  # 标题
    bg_path = "img/bg.jpg"  # 背景图片路径
    btn_start = button.Button(300, 300, 200, 100, color.WHITE, "开始",
                              color.BLACK, 50)  # 开始按钮
    btn_quit = button.Button(300, 420, 200, 100, color.WHITE, "退出",
                             color.BLACK, 50)  # 退出按钮

    def draw(self):  # 绘制场景
        self.screen.fill(color.BLACK)  # 填充背景色,清屏
        pygame.display.set_caption(self.title)  # 设置标题
        if self.bg_path:  # 判断是否有背景图片
            bg = pygame.image.load(self.bg_path).convert()  # 加载背景图片
            self.screen.blit(bg, (0, 0))  # 将背景图片覆盖到屏幕上

        self.btn_start.draw(self.screen, 120)  # 画出开始按钮
        self.btn_quit.draw(self.screen, 120)  # 画出退出按钮

    def handle_event(self):  # 处理事件
        # 如果光标在开始按钮上，则设置按钮背景色为灰色，否则恢复为白色
        if self.btn_start.is_clicked(pygame.mouse.get_pos()) == True:
            self.btn_start.color = (127, 127, 127)  # 设置按钮颜色为灰色
            if pygame.event.poll().type == pygame.MOUSEBUTTONUP:  # 检测到鼠标按下
                sm.scenemanager.change_scene("mode_scene")  # 切换到游戏场景
        else:
            self.btn_start.color = (255, 255, 255)  # 恢复按钮颜色为白色
        self.btn_start.draw(self.screen, 120)  # 重新绘制开始按钮

        # 如果光标在退出按钮上，则设置按钮背景色为灰色，否则恢复为白色
        if self.btn_quit.is_clicked(pygame.mouse.get_pos()) == True:
            self.btn_quit.color = (127, 127, 127)  # 设置按钮颜色为灰色
            if pygame.event.poll().type == pygame.MOUSEBUTTONUP:  # 检测到鼠标按下
                pygame.quit()  # 退出pygame
                exit()  # 退出程序
        else:            
            self.btn_quit.color = (255, 255, 255)  # 恢复按钮颜色为白色
        self.btn_quit.draw(self.screen, 120)  # 重新绘制退出按钮
