import pygame
from segment import Segment
import sys
import random
import global_variables as gv


class Snake:
    """Игра 'Змейка'."""
    def __init__(self):
        self.setup()
        self.clock = pygame.time.Clock()

    def setup(self):
        self.fps = 8
        self.cap = 0

        self.snake_pos = Segment(10 + 2 * gv.SIZE, 50 + gv.SIZE)
        self.snake_body = [Segment(10 + (2 - i) * gv.SIZE, 50 + gv.SIZE, 1, 1) for i in range(3)]
        self.snake_body[-1].r = 3
        self.snake_pos.r = 3
        self.is_food_spawn = False

        self.spawn_food()

        self.d = (1, 0)
        self.t = (1, 0)
        self.score = 0

        self.kq = []

    def run(self):
        """Запуск игры."""
        self.draw()
        while True:
            try:
                self.pass_frame()
                self.draw()
                self.clock.tick(self.fps)
            except Exception as e:
                if str(e) == gv.GAME_OVER_TYPES[0]:
                    sys.exit()
                elif str(e) == gv.GAME_OVER_TYPES[1]:
                    gv.load_bg_music('sounds\\bg_music.mp3')
                    if not gv.music_volume:
                        pygame.mixer.music.pause()
                    break
                elif str(e) == gv.GAME_OVER_TYPES[2]:
                    self.setup()
                    self.draw()
                else:
                    print('Что-то ещё.')
                    print(str(e))
                    gv.load_bg_music('sounds\\bg_music.mp3')
                    if not gv.music_volume:
                        pygame.mixer.music.pause()
                    break

    def draw(self):
        gv.surface.blit(gv.background_img, (0, 0))
        for pos in self.snake_body[1:-1]:
            gv.surface.blit(pygame.transform.rotate(gv.Snake_images[pos.t], 90 * pos.r), (pos.x, pos.y))

        gv.surface.blit(pygame.transform.rotate(gv.Snake_images[0], 90 * self.snake_pos.r),
                        (self.snake_pos.x, self.snake_pos.y))

        gv.surface.blit(pygame.transform.rotate(gv.Snake_images[3], 90 * self.snake_body[-1].r),
                        (self.snake_body[-1].x, self.snake_body[-1].y))

        gv.surface.blit(gv.apple, (self.food_pos[0], self.food_pos[1]))

        score_surface = pygame.font.SysFont('consolas', 22).render('Счёт : ' + str(self.score), True, gv.white)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (10 + gv.WINSIZE / 10, 15)
        gv.surface.blit(score_surface, score_rect)

        pygame.display.update()

    def move(self):
        if len(self.kq):
            if self.kq[0] == pygame.K_UP:
                self.t = (0, -1)

            if self.kq[0] == pygame.K_DOWN:
                self.t = (0, 1)

            if self.kq[0] == pygame.K_LEFT:
                self.t = (-1, 0)

            if self.kq[0] == pygame.K_RIGHT:
                self.t = (1, 0)

            self.kq.pop(0)

        if self.t == (0, -1) and self.d != (0, 1):
            self.d = (0, -1)

        if self.t == (0, 1) and self.d != (0, -1):
            self.d = (0, 1)

        if self.t == (-1, 0) and self.d != (1, 0):
            self.d = (-1, 0)

        if self.t == (1, 0) and self.d != (-1, 0):
            self.d = (1, 0)

        self.snake_pos.t = 1
        self.snake_pos.r = gv.RS[self.d]

        self.snake_pos.x += gv.SIZE * self.d[0]
        self.snake_pos.y += gv.SIZE * self.d[1]
        self.snake_body.insert(0, Segment(self.snake_pos.x, self.snake_pos.y, r=self.snake_pos.r, t=self.snake_pos.t))

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise Exception(gv.GAME_OVER_TYPES[0])
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    if pygame.K_UP not in self.kq:
                        self.kq.append(pygame.K_UP)

                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    if pygame.K_DOWN not in self.kq:
                        self.kq.append(pygame.K_DOWN)

                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    if pygame.K_LEFT not in self.kq:
                        self.kq.append(pygame.K_LEFT)

                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    if pygame.K_RIGHT not in self.kq:
                        self.kq.append(pygame.K_RIGHT)
                if event.key == pygame.K_ESCAPE:
                    self.pause()

    def spawn_food(self):
        if not self.is_food_spawn:
            self.food_pos = [10 + random.randrange(1, (gv.WINSIZE // gv.SIZE)) * gv.SIZE,
                             50 + random.randrange(1, (gv.WINSIZE // gv.SIZE)) * gv.SIZE]
            while Segment(self.food_pos[0], self.food_pos[1]) in self.snake_body:
                self.food_pos = [10 + random.randrange(0, (gv.WINSIZE // gv.SIZE)) * gv.SIZE,
                                 50 + random.randrange(0, (gv.WINSIZE // gv.SIZE)) * gv.SIZE]
            self.is_food_spawn = True

    def pass_frame(self):
        self.check_events()
        self.move()

        self.determine_second_segment_direction()
        self.check_eating_apple()

        self.spawn_food()
        self.determine_tail_direction()
        self.check_collision()

    def check_collision(self):
        if self.snake_pos.x < 10 or self.snake_pos.x > 10 + gv.WINSIZE - gv.SIZE:
            self.game_over()

        if self.snake_pos.y < 50 or self.snake_pos.y > 50 + gv.WINSIZE - gv.SIZE:
            self.game_over()

        for segment in self.snake_body[1:]:
            if self.snake_pos.x == segment.x and self.snake_pos.y == segment.y:
                self.game_over()

    def check_eating_apple(self):
        if self.snake_pos.x == self.food_pos[0] and self.snake_pos.y == self.food_pos[1]:
            self.score += 1
            self.cap += 1
            self.fps = min(22, self.fps + (self.cap >= 10))
            self.cap %= 10
            self.is_food_spawn = False
            if gv.volume:
                gv.pick.play()
        else:
            self.snake_body.pop()
        if self.score == int((gv.WINSIZE / gv.SIZE) ** 2) - 3:
            self.game_over()

    def pause(self):
        z = []

        def leave_to_menu():
            raise Exception(gv.GAME_OVER_TYPES[1])

        def pause_break():
            k = pygame.event.Event(pygame.KEYDOWN, key=27)
            z.append(k)

        menu = gv.pygame_menu.Menu(gv.WINSIZE + 60, gv.WINSIZE + 20, '', theme=gv.zxc, )
        menu.add_button('Возобновить игру', pause_break)

        menu.add_button('Выйти в главное меню', leave_to_menu)

        while True:
            gv.surface.blit(gv.bg_img, (0, 0))

            events = pygame.event.get()
            for event in events + z:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise Exception(gv.GAME_OVER_TYPES[0])
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            if menu.is_enabled():
                menu.update(events)
                menu.draw(gv.surface)
            pygame.display.update()

    def game_over(self):
        if gv.volume:
            gv.game_over_music.play()
        gv.pick.stop()

        def leave_to_menu():
            gv.game_over_music.stop()
            raise Exception(gv.GAME_OVER_TYPES[1])

        def restart():
            gv.game_over_music.stop()
            raise Exception(gv.GAME_OVER_TYPES[2])

        menu = gv.pygame_menu.Menu(gv.WINSIZE + 60, gv.WINSIZE + 20, '', theme=gv.zxc, )
        menu.add_label('Победа\n' + f'Счёт : {self.score}\n' if self.score == int((gv.WINSIZE / gv.SIZE) ** 2) - 3
                       else 'Игра окончена\n' + f'Счёт : {self.score}\n')
        menu.add_button('Начать заново', restart)

        menu.add_button('Выйти в главное меню', leave_to_menu)

        while True:
            gv.surface.blit(gv.bg_img, (0, 0))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    gv.game_over_music.stop()
                    pygame.quit()
                    raise Exception(gv.GAME_OVER_TYPES[0])
            if menu.is_enabled():
                menu.update(events)
                menu.draw(gv.surface)
            pygame.display.update()

    def determine_second_segment_direction(self):
        if self.snake_body[0].x > self.snake_body[2].x and self.snake_body[0].y > self.snake_body[2].y:
            if self.snake_body[0].x == self.snake_body[1].x and self.snake_body[0].y > self.snake_body[1].y:
                self.snake_body[1].r = 0
            else:
                self.snake_body[1].r = 2
            self.snake_body[1].t = 2

        if self.snake_body[0].x > self.snake_body[2].x and self.snake_body[0].y < self.snake_body[2].y:
            if self.snake_body[0].x == self.snake_body[1].x and self.snake_body[0].y < self.snake_body[1].y:
                self.snake_body[1].r = 3
            else:
                self.snake_body[1].r = 1
            self.snake_body[1].t = 2

        if self.snake_body[0].x < self.snake_body[2].x and self.snake_body[0].y < self.snake_body[2].y:
            if self.snake_body[0].x == self.snake_body[1].x and self.snake_body[0].y < self.snake_body[1].y:
                self.snake_body[1].r = 2
            else:
                self.snake_body[1].r = 0
            self.snake_body[1].t = 2

        if self.snake_body[0].x < self.snake_body[2].x and self.snake_body[0].y > self.snake_body[2].y:
            if self.snake_body[0].x == self.snake_body[1].x and self.snake_body[0].y > self.snake_body[1].y:
                self.snake_body[1].r = 1
            else:
                self.snake_body[1].r = 3
            self.snake_body[1].t = 2

    def determine_tail_direction(self):
        if self.snake_body[-1].x < self.snake_body[-2].x and self.snake_body[-1].y == self.snake_body[-2].y:
            self.snake_body[-1].r = 3
        if self.snake_body[-1].x > self.snake_body[-2].x and self.snake_body[-1].y == self.snake_body[-2].y:
            self.snake_body[-1].r = 1
        if self.snake_body[-1].x == self.snake_body[-2].x and self.snake_body[-1].y < self.snake_body[-2].y:
            self.snake_body[-1].r = 2
        if self.snake_body[-1].x == self.snake_body[-2].x and self.snake_body[-1].y > self.snake_body[-2].y:
            self.snake_body[-1].r = 0
