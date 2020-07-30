import pygame
from pygame import K_UP, K_LEFT, K_DOWN, K_RIGHT
import numpy as np
from time import time
from random import choice

pygame.init()

# janela
Bsize = 40
Largura = 8
Altura = 16
janela = pygame.display.set_mode((Bsize * Largura, Bsize * Altura), pygame.RESIZABLE)

# fonte e pontos
fonte = pygame.font.SysFont('Agency FB', Bsize*3, True)
score = 0
scoreImg = fonte.render(str(score), True, (200, 200, 200))

# bloquinhos
LaranjaImg = pygame.transform.scale(pygame.image.load('Data/tetris.png'), (Bsize, Bsize))
AzulImg = pygame.transform.scale(pygame.image.load('Data/Blue.png'), (Bsize, Bsize))
VerdeImg = pygame.transform.scale(pygame.image.load('Data/Green.png'), (Bsize, Bsize))
VermelhoImg = pygame.transform.scale(pygame.image.load('Data/Red.png'), (Bsize, Bsize))
AmareloImg = pygame.transform.scale(pygame.image.load('Data/Yellow.png'), (Bsize, Bsize))
cores = (LaranjaImg, AzulImg, VerdeImg, VermelhoImg, AmareloImg)

# Peças
Z = np.array([[3, 3, 0],
              [0, 3, 3]])
S = np.array([[0, 3, 3],
              [3, 3, 0]])
L = np.array([[4, 4, 4],
              [4, 0, 0]])
J = np.array([[4, 4, 4],
              [0, 0, 4]])
T = np.array([[0, 1, 0],
              [1, 1, 1]])
Square = np.array([[5, 5],
                   [5, 5]])
Hero = np.array([[0, 0, 0, 0],
                 [2, 2, 2, 2],
                 [0, 0, 0, 0]])
tipos = (Z, S, L, J, T, Square, Hero)


class Peca:
    def __init__(self, formato, coordenadas=(0, 0)):
        self.formato = formato
        self.x = coordenadas[0]
        self.y = coordenadas[1]

    def direita(self, reverse=False):
        self.x += -1 if reverse else 1

    def esquerda(self, reverse=False):
        self.x += 1 if reverse else -1

    def cai(self, reverse=False):
        self.y += -1 if reverse else 1

    def rotate(self, reverse=False):
        self.formato = np.rot90(self.formato, 1) if reverse else np.rot90(self.formato, -1)

    def blit(self):
        for row, b in enumerate(self.formato):
            for column, value in enumerate(b):
                if value > 0:
                    janela.blit(cores[value - 1], ((self.x + column) * Bsize, (self.y + row) * Bsize))


def if_bateu(peca, tabuleiro):  # Função para detectar se a peça bateu
    for row, values in enumerate(peca.formato):
        for column, value in enumerate(values):
            if value:
                try:
                    tabuleiro.formato[peca.y + row, peca.x + column]
                except IndexError:
                    return True
                if tabuleiro.formato[peca.y + row, peca.x + column]:
                    return True
                if peca.x + column < 0:
                    return True
    return False


# Tabuleiro
Tabuleiro = Peca(np.zeros((Altura, Largura), dtype='int'))

# peça
current = Peca(choice(tipos), [1, 1])

# timers e comandos
comandos = {K_LEFT: (current.esquerda, 15), K_RIGHT: (current.direita, 15),   # chave: (função, velocidade de repetição)
            K_DOWN: (current.cai, 7), K_UP: (current.rotate, 40)}
keypress = list()
inicial = ini_acao = time()

running = True
while running:

    # ------------------------------------------- Inputs ---------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            width, height = event.size
            Bsize = width // Largura

            janela = pygame.display.set_mode((Bsize * Largura, Bsize * Altura), pygame.RESIZABLE)
            fonte = pygame.font.SysFont('Agency FB', Bsize * 3, True)
            LaranjaImg = pygame.transform.scale(pygame.image.load('Data/tetris.png'), (Bsize, Bsize))
            AzulImg = pygame.transform.scale(pygame.image.load('Data/Blue.png'), (Bsize, Bsize))
            VerdeImg = pygame.transform.scale(pygame.image.load('Data/Green.png'), (Bsize, Bsize))
            VermelhoImg = pygame.transform.scale(pygame.image.load('Data/Red.png'), (Bsize, Bsize))
            AmareloImg = pygame.transform.scale(pygame.image.load('Data/Yellow.png'), (Bsize, Bsize))
            cores = (LaranjaImg, AzulImg, VerdeImg, VermelhoImg, AmareloImg)
            scoreImg = fonte.render(str(score), True, (200, 200, 200))

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (K_DOWN, K_UP, K_LEFT, K_RIGHT):
                ini_acao = time()
                keypress.append(event.key)
        if event.type == pygame.KEYUP:
            if event.key in (K_DOWN, K_UP, K_LEFT, K_RIGHT):
                keypress.remove(event.key)

    # ------------------------------------------ Processos ---------------------------------------------------
    # execução de comandos de movimento
    if keypress:
        for i in keypress:
            if int((time() - ini_acao) * 100) % comandos[i][1] == 0:  # condicional do timer para repetição
                ini_acao -= 0.01
                comandos[i][0]()
                if i == K_DOWN:
                    score += 1
                if if_bateu(current, Tabuleiro):  # ele bateu enquanto executava um comando?
                    comandos[i][0](True)  # Reverte o comando
                    if i == K_DOWN:
                        score -= 1
                scoreImg = fonte.render(str(score), True, (200, 200, 200))

    if time() - inicial >= 0.7 and keypress != K_DOWN:
        current.cai()
        inicial = time()

        if if_bateu(current, Tabuleiro):  # ele bateu na descida
            current.cai(True)  # Sobe
            for camada, lista in enumerate(current.formato):  # for para adicionar current no tabuleiro
                for coluna, valor in enumerate(lista):
                    if valor > 0:
                        Tabuleiro.formato[current.y + camada, current.x + coluna] = valor

            # Criação da nova peça
            current.formato = choice(tipos)
            current.x = 0
            current.y = 0

            # Eliminação de camadas
            while any(all(b for b in i) for i in Tabuleiro.formato):  # enquanto tiver alguma coluna cheia de > 0
                for camada, i in enumerate(Tabuleiro.formato):
                    if all(b for b in i):
                        if camada == 0:
                            Tabuleiro.formato[0, :] = np.zeros((1, Largura))
                        else:
                            Tabuleiro.formato[camada, :] = Tabuleiro.formato[camada - 1, :]
                            Tabuleiro.formato[camada - 1, :] = np.ones((1, Largura))

            if any(b for b in Tabuleiro.formato[0]):
                running = False

    # ------------------------------------------ Display --------------------------------------------------------
    janela.fill((50, 50, 50))
    janela.blit(scoreImg, (Bsize, Bsize))
    current.blit()
    Tabuleiro.blit()
    pygame.display.update()
