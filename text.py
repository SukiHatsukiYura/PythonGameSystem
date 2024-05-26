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
