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

        self.scores = {
            'O': 10,
            'X': -10,
            'Tie': 0,
        }

    def startNewGame(self):

        self.states = [[None for _ in range(3)] for _ in range(3)]
        self.players = ['O', 'X']  # 'O' is AI, 'X' is player
        self.currentPlayer = random.choice(self.players)
        self.printCurrentPlayer()
        self.winner = None

        self.runGameLoop()

    def printCurrentPlayer(self):
        player = 'AI' if self.currentPlayer == 'O' else 'Human'
        print(f'[INFO] {player}\'s turn...')

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

        if self.currentPlayer == self.players[0]:
            self.bestMove()
            self.winner = self.checkWinner()
            self.switchPlayerTurns()

        mouseX, mouseY = self.getMousePosition()

        if self.mouseClicked:
            self.updateStates(mouseX, mouseY)
            self.winner = self.checkWinner()
            self.switchPlayerTurns()

    def bestMove(self):
        print('[INFO] Minimax algorithm running...')
        bestScore = float('-inf')

        for i in range(3):
            for j in range(3):
                if self.states[i][j] is None:

                    self.states[i][j] = self.players[0]
                    score = self.minimax(0, float('-inf'), float('inf'), False)
                    self.states[i][j] = None

                    if score > bestScore:
                        bestScore = score
                        optimizedI, optimizedJ = i, j

        self.states[optimizedI][optimizedJ] = self.currentPlayer

    def minimax(self, depth, alpha, beta, is_maximizing):
        winner = self.checkWinner()
        if winner is not None:
            return self.scores[winner]

        if is_maximizing:
            bestScore = float('-inf')

            for i in range(3):
                for j in range(3):
                    if self.states[i][j] is None:

                        self.states[i][j] = self.players[0]
                        score = self.minimax(depth + 1, alpha, beta, False)
                        self.states[i][j] = None
                        bestScore = max(score, bestScore)

                        # alpha-beta pruning
                        alpha = max(alpha, bestScore)
                        if beta <= alpha:
                            return bestScore

            return bestScore

        else:
            bestScore = float('inf')

            for i in range(3):
                for j in range(3):
                    if self.states[i][j] is None:

                        self.states[i][j] = self.players[1]
                        score = self.minimax(depth + 1, alpha, beta, True)
                        self.states[i][j] = None
                        bestScore = min(score, bestScore)

                        # alpha-beta pruning
                        beta = min(beta, bestScore)
                        if beta <= alpha:
                            return bestScore

            return bestScore

    def updateStates(self, mouseX, mouseY):
        j = mouseX // (s.HEIGHT // 3)
        i = mouseY // (s.HEIGHT // 3)

        if self.states[i][j] is None:
            self.states[i][j] = self.currentPlayer

    @staticmethod
    def allEquals(x, y, z):
        return x is not None and x == y and y == z

    def checkWinner(self):
        winner = None

        # horizontal
        for i in range(3):
            if self.allEquals(self.states[i][0], self.states[i][1], self.states[i][2]):
                winner = self.states[i][0]

        # vertical
        for i in range(3):
            if self.allEquals(self.states[0][i], self.states[1][i], self.states[2][i]):
                winner = self.states[0][i]

        # diagonal
        if self.allEquals(self.states[0][0], self.states[1][1], self.states[2][2]):
            winner = self.states[0][0]

        if self.allEquals(self.states[2][0], self.states[1][1], self.states[0][2]):
            winner = self.states[2][0]

        openSpots = 0
        for i in range(3):
            for j in range(3):
                if self.states[i][j] is None:
                    openSpots += 1

        if winner is None and openSpots == 0:
            winner = 'Tie'

        return winner

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
        self.printCurrentPlayer()

    def getMousePosition(self):
        return pygame.mouse.get_pos()

    def showGameoverScreen(self):

        if self.winner in self.players:
            self.drawTextToScreen(f'{self.winner} won!', int(s.WIDTH * 0.5), int(s.HEIGHT * 0.25))
        else:
            self.drawTextToScreen(f'{self.winner}!', int(s.WIDTH * 0.5), int(s.HEIGHT * 0.25))

        self.drawTextToScreen('Press any key to play again,\'q\' to quit ', int(s.WIDTH * 0.5), int(s.HEIGHT * 0.75))

        pygame.display.update()

        pressed = False
        while not pressed:
            self.handleEvents()

            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    pressed = True

    def drawTextToScreen(self, text, x, y, size=18, color=(255, 0, 0)):

        font = pygame.font.Font(pygame.font.match_font('Arial'), size)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect()

        textRect.centerx = x
        textRect.centery = y

        self.screen.blit(textSurface, textRect)
