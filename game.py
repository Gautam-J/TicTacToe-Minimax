import time
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

        self.states = [[None for _ in range(3)] for _ in range(3)]
        self.players = ['X', 'O']
        self.currentPlayer = self.players[0]

        self.runGameLoop()

    def runGameLoop(self):

        self.playing = True
        while self.playing:
            self.clock.tick(s.FPS)
            self.handleEvents()
            self.updateAttributes()
            self.render()

    def handleEvents(self):

        self.mouseClicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.isRunning = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouseClicked = True

    def updateAttributes(self):

        mouseX, mouseY = self.getMousePosition()
        if self.mouseClicked:
            print(f'[INFO] {time.time()} {self.currentPlayer} clicked at {mouseX = } {mouseY  = }')
            self.switchPlayerTurns()

    def render(self):

        self.screen.fill((255, 255, 255))
        self.drawGrid()

        pygame.display.update()

    def drawGrid(self):

        pygame.draw.line(self.screen, (0, 0, 0), (s.WIDTH // 3, 0), (s.WIDTH // 3, s.HEIGHT), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (s.WIDTH * 2 // 3, 0), (s.WIDTH * 2 // 3, s.HEIGHT), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (0, s.HEIGHT // 3), (s.WIDTH, s.HEIGHT // 3), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (0, s.HEIGHT * 2 // 3), (s.WIDTH, s.HEIGHT * 2 // 3), 3)

    def switchPlayerTurns(self):

        currentPlayerIndex = self.players.index(self.currentPlayer)
        nextPlayerIndex = (currentPlayerIndex + 1) % 2
        self.currentPlayer = self.players[nextPlayerIndex]

    def getMousePosition(self):
        return pygame.mouse.get_pos()
