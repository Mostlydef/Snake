import pygame
from segment import Segment
import global_variables as gv


class Snake:
    def __init__(self):
        self.setup()

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
        pass

    def draw(self):
        pass

    def move(self):
        pass

    def spawn_food(self):
        pass

if __name__ == '__main__':
    snake = Snake()
    snake.run()
