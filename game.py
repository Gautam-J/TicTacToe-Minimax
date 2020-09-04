import time
import random
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
        self.currentPlayer = random.choice(self.players)
        self.winner = None

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
            self.updateStates(mouseX, mouseY)
            self.checkWinner()

    def updateStates(self, mouseX, mouseY):
        j = mouseX // (s.HEIGHT // 3)
        i = mouseY // (s.HEIGHT // 3)

        if self.states[i][j] is None:
            print(f'[INFO] {time.time()} {self.currentPlayer} clicked at {i = } {j = }')
            self.states[i][j] = self.currentPlayer
            self.switchPlayerTurns()

    def checkWinner(self):
        # refer js file
        pass

    def render(self):

        self.screen.fill((255, 255, 255))
        self.drawGrid()
        self.drawStates()

        pygame.display.update()

    def drawGrid(self):

        pygame.draw.line(self.screen, (0, 0, 0), (s.WIDTH // 3, 0), (s.WIDTH // 3, s.HEIGHT), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (s.WIDTH * 2 // 3, 0), (s.WIDTH * 2 // 3, s.HEIGHT), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (0, s.HEIGHT // 3), (s.WIDTH, s.HEIGHT // 3), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (0, s.HEIGHT * 2 // 3), (s.WIDTH, s.HEIGHT * 2 // 3), 3)

    def drawStates(self):

        for i in range(3):
            for j in range(3):
                spot = self.states[i][j]
                if spot is None:
                    continue

                x = (s.WIDTH // 3) * j + (s.WIDTH // 3) // 2
                y = (s.HEIGHT // 3) * i + (s.HEIGHT // 3) // 2
                r = (s.WIDTH // 3) // 4

                if spot == 'X':
                    pygame.draw.line(self.screen, (0, 0, 0), (x - r, y - r), (x + r, y + r), 2)
                    pygame.draw.line(self.screen, (0, 0, 0), (x + r, y - r), (x - r, y + r), 2)

                elif spot == 'O':
                    pygame.draw.circle(self.screen, (0, 0, 0), (x, y), r, 1)

    def switchPlayerTurns(self):

        currentPlayerIndex = self.players.index(self.currentPlayer)
        nextPlayerIndex = (currentPlayerIndex + 1) % 2
        self.currentPlayer = self.players[nextPlayerIndex]

    def getMousePosition(self):
        return pygame.mouse.get_pos()
