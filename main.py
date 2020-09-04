import pygame
from game import TicTacToe

game = TicTacToe()

while game.isRunning:
    game.startNewGame()

pygame.quit()
