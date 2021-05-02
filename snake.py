import pygame
from segment import Segment
import sys
import random
import global_variables as gv


class Snake:
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
                    break
                elif str(e) == gv.GAME_OVER_TYPES[2]:
                    self.setup()
                    self.draw()
                else:
                    print('Что-то ещё.')
                    print(str(e))
                    break

    def draw(self):
        pass

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

        self.check_eating_apple()
        self.spawn_food()
        self.check_collision()

    def check_collision(self):
        pass

    def check_eating_apple(self):
        if self.snake_pos.x == self.food_pos[0] and self.snake_pos.y == self.food_pos[1]:
            self.score += 1
            self.cap += 1
            self.fps = min(24, self.fps + (self.cap >= 8))
            self.cap %= 8
            self.is_food_spawn = False
            if gv.volume:
                gv.pick.play()
        else:
            self.snake_body.pop()
        if self.score == int((gv.WINSIZE / gv.SIZE) ** 2) - 3:
            self.game_over()

    def pause(self):
        pass

    def game_over(self):
        pass


if __name__ == '__main__':
    snake = Snake()
    snake.run()
