import pygame
import pygame_menu

volume = True
music_volume = True
WINSIZE = 620
SIZE = WINSIZE // 20

pygame.init()


def load_bg_music(path):
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)


load_bg_music('sounds\\bg_music.mp3')

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

GAME_OVER_TYPES = ['quit', 'leave', 'restart']
RS = {
    (0, 1): 2,
    (0, -1): 0,
    (-1, 0): 1,
    (1, 0): 3
}

zxc = pygame_menu.themes.THEME_BLUE.copy()
zxc.widget_font_size = 48
zxc.widget_font_color = (255, 255, 255)
zxc.selection_color = (255, 255, 255)
zxc.set_background_color_opacity(0.0)
zxc.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
