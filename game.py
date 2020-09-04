import pygame
import settings as s


class TicTacToe:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode((s.WIDTH, s.HEIGHT))
        pygame.display.set_caption(s.TITLE)

        self.clock = pygame.time.Clock()
        self.isRunning = True

    def startNewGame(self):

        self.runGameLoop()

    def runGameLoop(self):

        self.playing = True
        while self.playing:
            self.clock.tick(s.FPS)
            self.handleEvents()
            self.updateAttributes()
            self.render()

    def handleEvents(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.isRunning = False

    def updateAttributes(self):
        pass

    def render(self):

        self.screen.fill((255, 255, 255))
        self.drawGrid()

        pygame.display.update()

    def drawGrid(self):

        pygame.draw.line(self.screen, (0, 0, 0), (s.WIDTH // 3, 0), (s.WIDTH // 3, s.HEIGHT), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (s.WIDTH * 2 // 3, 0), (s.WIDTH * 2 // 3, s.HEIGHT), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (0, s.HEIGHT // 3), (s.WIDTH, s.HEIGHT // 3), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (0, s.HEIGHT * 2 // 3), (s.WIDTH, s.HEIGHT * 2 // 3), 3)
