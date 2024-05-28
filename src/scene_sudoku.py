import pygame
import scene


class GameSudoku(scene.Scene):
    size = (630, 630)
    gird_list=[()]
    def __init__(self):
        super().__init__()

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.darw_line()
        pass

    def darw_line(self):
        #pygame.draw.line(self.screen, (0, 0, 0), (0, 69), (630, 69), 3)
        for i in range(0, 631, 70):
            pygame.draw.line(self.screen, (0, 0, 0), (i, 0), (i, 630), 3)
        for i in range(0, 631, 70):
            pygame.draw.line(self.screen, (0, 0, 0), (0, i), (630, i), 3)
        pygame.draw.rect(self.screen, (255, 0, 255), (2 + 70, 2 + 70, 67, 67))
        #pygame.draw.line(self.screen, (0, 0, 0), (69, 0), (69, 630), 3)

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

        pass
