import pygame
import pygame_menu
import global_variables as gv
from Command import invoker


class Menu:
    def __init__(self):
        self.menu = pygame_menu.Menu(gv.WINSIZE + 60, gv.WINSIZE + 20, '', theme=gv.zxc, )
        self.menu.add_button('Играть', invoker.start_the_game)
        self.menu.add_selector('Звук:',
                               [('Вкл.', True),
                                ('Выкл.', False)],
                               onchange=invoker.change_volume)
        self.menu.add_selector('Музыка:',
                               [('Вкл.', True),
                                ('Выкл.', False)],
                               onchange=invoker.change_music_volume)
        self.menu.add_button('Помощь', invoker.help)
        self.menu.add_button('Выход', pygame_menu.events.EXIT)
        while True:
            gv.surface.blit(gv.bg_img, (0, 0))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            if self.menu.is_enabled():
                self.menu.update(events)
                self.menu.draw(gv.surface)
            pygame.display.update()


if __name__ == '__main__':
    zxc = Menu()
