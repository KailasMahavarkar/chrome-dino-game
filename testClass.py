import os
import pygame
from PIL import Image
import random
from pygame.rect import *
from color import *

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
    def __init__(self):
        self.run = True
        self.gameover = False
        self.width = 800
        self.height = 350
        self.score = 0
        self.screen = pygame.display.set_mode((self.width, self.height))

        # load image as Path
        self.dinoImagePath = os.path.join(testPath, 'dinosaur_64.png')
        self.cactusImagePath = os.path.join(testPath, 'cactus_64.png')
        self.backgroundPath = os.path.join(testPath, 'lava.jpg')

        # set Images
        self.dinoImage = pygame.image.load(self.dinoImagePath).convert_alpha()
        self.cactusImage = pygame.image.load(self.cactusImagePath).convert_alpha()
        self.backgroundImage = pygame.image.load(self.backgroundPath).convert_alpha()

        # set Dino attributes
        dinosaur = Image.open(self.dinoImagePath)
        dinoW, dinoH = dinosaur.size
        self.dinoX = round(100)
        self.dinoY = round(self.height - dinoH)

        # set Cactus attributes
        cactus = Image.open(self.dinoImagePath)
        cactusW, cactusH = cactus.size
        self.cactusX = round(500)
        self.cactusY = round(self.height - cactusH)

    @property
    def dinosaur(self):
        self.screen.blit(self.dinoImage, (round(self.dinoX), round(self.dinoY)))
        hitboxDino = Rect(int((self.dinoX - 5)), int((self.dinoY - 5)), 70, 70)
        pygame.draw.rect(self.screen, getRGB("red"), hitboxDino, 2)
        return hitboxDino

    def cactus(self):
        self.screen.blit(self.cactusImage, (round(self.cactusX), round(self.cactusY)))
        hitboxCactus = Rect(int(self.cactusX - 5), int(self.cactusY - 5), 70, 70)
        pygame.draw.rect(self.screen, getRGB("red"), hitboxCactus, 2)
        return hitboxCactus

    def gameOver(self):
        # set font and text for gameover
        font = pygame.font.Font('freesansbold.ttf', 80)
        text = font.render('Score: ' + str(self.score), True, getRGB('white'), None)
        textRect = text.get_rect()
        textRect.center = (800 // 2, 400 // 2)

        # self.screen.fill(getRGB('white'))
        self.screen.blit(self.backgroundImage, (0, 0))
        self.screen.blit(text, textRect)

    # set font and text on scoreboard
    def scoreboard(self):
        font = pygame.font.Font('freesansbold.ttf', 40)
        score = font.render(str(self.score), True, getRGB("white"))
        self.screen.blit(score, (700, 50))

    def collideDetect(self, rect1, rect2) -> bool:
        """
        :param rect1: rectangle 1
        :param rect2: rectangle 2
        :return: Boolean
        """

        return rect1.colliderect(rect2)

    def gameLOOP(self):
        while self.run:
            self.dinoY += 0.2
            self.cactusX -= 0.25

            if self.dinoX <= 0:
                self.dinoX = 0
            elif self.dinoX >= round(self.width - 64):
                self.dinoX = round(self.width - 64)
            elif self.dinoY <= 0:
                self.dinoY = 0
            elif self.dinoY >= round(self.height - 64):
                self.dinoY = round(self.height - 64)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                #   check if arrow keys are pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False
                    if event.key == pygame.K_SPACE:
                        self.dinoY -= 300

            # self.screen.fill(getRGB("white"))
            self.screen.blit(self.backgroundImage, (0, 0))

            if not self.gameover:
                #   fill the screen with white color
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

            # updating the display
            pygame.display.update()


if __name__ == "__main__":
    Main().gameLOOP()
