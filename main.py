import os
import pygame
from PIL import Image
import random
from pygame.rect import *
from color import *

WIDTH, HEIGHT = 800, 350
DINO_START_X, DINO_START_Y = 100, 200
CACTUS_START_X = 500

pygame.init()
clock = pygame.time.Clock()

# setting dynamic test path and rootPath
rootPath = os.path.abspath(os.path.dirname(__file__))
testPath = os.path.join(rootPath, 'images')

# setting icon and title caption
pygame.display.set_caption('Infinite Dino')
icon = pygame.image.load(os.path.join(testPath, 'dinosaur_32.png'))
pygame.display.set_icon(icon)


class Main:
    def __init__(self, adjustFrameFactor=2):
        self.run = True
        self.gameover = False
        self.width = WIDTH
        self.height = HEIGHT
        self.score = 0
        self.adjustFrameFactor = adjustFrameFactor
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # load image as Path
        self.dinoImagePath = os.path.join(testPath, 'dinosaur_64.png')
        self.cactusImagePath = os.path.join(testPath, 'cactus_64.png')
        self.backgroundPath = os.path.join(testPath, 'lava.jpg')

        # set Images
        self.dinoImage = pygame.image.load(self.dinoImagePath).convert_alpha()
        self.cactusImage = pygame.image.load(
            self.cactusImagePath).convert_alpha()
        self.backgroundImage = pygame.image.load(self.backgroundPath).convert()

        # set Dino attributes
        dinosaur = Image.open(self.dinoImagePath)
        dinoW, dinoH = dinosaur.size
        self.dinoX = DINO_START_X
        self.dinoY = self.height - dinoH

        # set Cactus attributes
        cactus = Image.open(self.cactusImagePath)
        cactusW, cactusH = cactus.size
        self.cactusX = CACTUS_START_X
        self.cactusY = self.height - cactusH

    @property
    def dinosaur(self):
        self.screen.blit(self.dinoImage, (self.dinoX, self.dinoY))
        hitboxDino = self.dinoImage.get_rect(topleft=(self.dinoX, self.dinoY))
        pygame.draw.rect(self.screen, getRGB("red"), hitboxDino, 2)
        return hitboxDino

    def cactus(self):
        self.screen.blit(self.cactusImage, (self.cactusX, self.cactusY))
        hitboxCactus = self.cactusImage.get_rect(
            topleft=(self.cactusX, self.cactusY))
        pygame.draw.rect(self.screen, getRGB("red"), hitboxCactus, 2)
        return hitboxCactus

    def gameOver(self):
        # set font and text for gameover
        font = pygame.font.Font('freesansbold.ttf', 80)
        text = font.render('Score: ' + str(self.score), True, getRGB('white'))
        textRect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(self.backgroundImage, (0, 0))
        self.screen.blit(text, textRect)

    # set font and text on scoreboard
    def scoreboard(self):
        font = pygame.font.Font('freesansbold.ttf', 40)
        score = font.render(str(self.score), True, getRGB("white"))
        self.screen.blit(score, (700, 50))

    def collideDetect(self, rect1, rect2) -> bool:
        return rect1.colliderect(rect2)

    def gameLOOP(self):
        while self.run:
            self.clock.tick(60)
            self.dinoY += 6 * self.adjustFrameFactor
            self.cactusX -= min(30, max(10, self.score //
                                10 + 1)) * self.adjustFrameFactor

            # Boundary conditions
            if self.dinoY >= self.height - 64:
                self.dinoY = self.height - 64

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False
                    if event.key == pygame.K_SPACE:
                        self.dinoY -= 300

            self.screen.blit(self.backgroundImage, (0, 0))

            if not self.gameover:
                rect1 = self.dinosaur
                rect2 = self.cactus()

                if self.cactusX <= 0:
                    self.score += 1
                    self.cactusX = random.randint(900, 1000)

                if self.collideDetect(rect1, rect2):
                    self.gameover = True
                else:
                    self.scoreboard()
            else:
                self.gameOver()

            pygame.display.update()


if __name__ == "__main__":
    Main(
        adjustFrameFactor=0.2
    ).gameLOOP()
    pygame.quit()
