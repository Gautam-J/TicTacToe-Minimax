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

            if self.winner is not None:
                self.showGameoverScreen()
                self.playing = False

    def handleEvents(self):

        self.mouseClicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouseClicked = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()

    def updateAttributes(self):

        mouseX, mouseY = self.getMousePosition()
        if self.mouseClicked:
            self.updateStates(mouseX, mouseY)
            self.checkWinner()
            self.switchPlayerTurns()

    def updateStates(self, mouseX, mouseY):
        j = mouseX // (s.HEIGHT // 3)
        i = mouseY // (s.HEIGHT // 3)

        if self.states[i][j] is None:
            print(f'[INFO] {time.time()} {self.currentPlayer} clicked at {i = } {j = }')
            self.states[i][j] = self.currentPlayer

    @staticmethod
    def allEquals(x, y, z):
        return x is not None and x == y and y == z

    def checkWinner(self):

        # horizontal
        for i in range(3):
            if self.allEquals(self.states[i][0], self.states[i][1], self.states[i][2]):
                self.winner = self.states[i][0]

        # vertical
        for i in range(3):
            if self.allEquals(self.states[0][i], self.states[1][i], self.states[2][i]):
                self.winner = self.states[0][i]

        # diagonal
        if self.allEquals(self.states[0][0], self.states[1][1], self.states[2][2]):
            self.winner = self.states[0][0]

        if self.allEquals(self.states[2][0], self.states[1][1], self.states[0][2]):
            self.winner = self.states[2][0]

        openSpots = 0
        for i in range(3):
            for j in range(3):
                if self.states[i][j] is None:
                    openSpots += 1

        if self.winner is None and openSpots == 0:
            self.winner = 'Tie'

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

    def showGameoverScreen(self):

        if self.winner in self.players:
            self.drawTextToScreen(f'{self.winner} won!', s.WIDTH // 2, s.HEIGHT // 3)
        else:
            self.drawTextToScreen(f'{self.winner}!', s.WIDTH // 2, s.HEIGHT // 3)

        self.drawTextToScreen('Press any key to play again,\'q\' to quit ', s.WIDTH // 2, (s.HEIGHT * 2) // 3)

        pygame.display.update()

        pressed = False
        while not pressed:
            self.handleEvents()

            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    pressed = True

    def drawTextToScreen(self, text, x, y, size=18, color=(255, 0, 0)):
        """Draws text to screen.
        Args:
            text (str): Text to be displayed.
            size (int): Size of the text.
            color (tuple): Color of the text.
            x (int): x coordinate of the text.
            y (int): y coordinate of the text.
        """

        font = pygame.font.Font(pygame.font.match_font('Arial'), size)
        textSurface = font.render(text, True, color)  # antialiasing
        textRect = textSurface.get_rect()

        textRect.centerx = x
        textRect.centery = y

        self.screen.blit(textSurface, textRect)
