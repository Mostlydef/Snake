import pygame


volume = True
WINSIZE = 600
SIZE = WINSIZE // 20

pygame.init()

pygame.mixer.music.load('sounds\\bg_music.mp3')
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)

pick = pygame.mixer.Sound('sounds\\Pick.wav')
game_over_music = pygame.mixer.Sound('sounds\\game_over.wav')

pygame.display.set_caption('Змейка')

surface = pygame.display.set_mode((WINSIZE + 20, WINSIZE + 60))
bg_img = pygame.transform.scale(pygame.image.load('images\\bg.png').convert(), (WINSIZE + 20, WINSIZE + 60))
background_img = pygame.transform.scale(pygame.image.load('images\\background.png').convert(),
                                        (WINSIZE + 20, WINSIZE + 60))
apple = pygame.transform.scale(pygame.image.load('images\\Apple.png'), (SIZE, SIZE))
Snake_images = [pygame.transform.scale(pygame.image.load("images\\Snake_{}.png".format(i)),
                                       (SIZE, SIZE)) for i in range(4)]

pygame.transform.smoothscale(surface, (20, 20))
white = pygame.Color(255, 255, 255)
