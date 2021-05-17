from unittest import TestCase

import pygame.event

from Snake import Snake
import Segment


def return_states(game):
    return (game.food_pos, game.score, game.d, game.is_food_spawn, [game.snake_pos.x, game.snake_pos.y],
            [[x.x, x.y] for x in game.snake_body])


class TestGame(TestCase):
    def setUp(self):
        pass

    def test_move(self):
        game = Snake()
        game.food_pos = [599, 639]
        z = [[103, 81], [72, 81], [41, 81]]
        x = [103, 81]
        for _ in range(17):
            game.pass_frame()
            self.assertEqual(return_states(game),
                             ([599, 639], 0, (1, 0), True, x, z))
            x = [x[0] + 31, x[1]]
            z = [[u[0] + 31, u[1]] for u in z]

    def test_grow(self):
        # Движение слева.
        game = Snake()
        game.food_pos = [103, 81]

        game.pass_frame()
        self.assertEqual(return_states(game),
                         (game.food_pos, 1, (1, 0), True, [103, 81], [[103, 81], [72, 81], [41, 81], [10, 81]]))
        # Движение справа.
        game = Snake()
        game.food_pos = [289, 174]
        game.d = (-1, 0)
        game.t = (-1, 0)
        game.snake_body = [Segment.Segment(x, 174) for x in [320, 351, 382]]
        game.snake_pos = Segment.Segment(320, 174)

        game.pass_frame()
        self.assertEqual(return_states(game), (
            game.food_pos, 1, (-1, 0), True, [289, 174], [[289, 174], [320, 174], [351, 174], [382, 174]]))

        # Движение сверху.
        game = Snake()
        game.food_pos = [475, 453]
        game.d = (0, 1)
        game.t = (0, 1)
        game.snake_body = [Segment.Segment(475, y) for y in [422, 391, 360]]
        game.snake_pos = Segment.Segment(475, 422)

        game.pass_frame()
        self.assertEqual(return_states(game), (
            game.food_pos, 1, (0, 1), True, [475, 453], [[475, 453], [475, 422], [475, 391], [475, 360]]))

        # Движение снизу.
        game = Snake()
        game.food_pos = [475, 453]
        game.d = (0, -1)
        game.t = (0, -1)
        game.snake_body = [Segment.Segment(475, y) for y in [484, 515, 546]]
        game.snake_pos = Segment.Segment(475, 484)

        game.pass_frame()
        self.assertEqual(return_states(game), (
            game.food_pos, 1, (0, -1), True, [475, 453], [[475, 453], [475, 484], [475, 515], [475, 546]]))

    def test_collision(self):
        # В правую стенку.
        game = Snake()
        game.food_pos = [599, 639]
        game.snake_body = [Segment.Segment(x, 174) for x in [599, 568, 537]]
        game.snake_pos = Segment.Segment(599, 174)

        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                             {'unicode': '\r', 'key': 13, 'mod': 4096, 'scancode': 40, 'window': None}))
        game.change_direction()
        game.move()
        game.determine_second_segment_direction()
        game.check_eating_apple()
        game.spawn_food()
        game.determine_tail_direction()
        self.assertRaises(Exception, game.check_collision)

        # В левую стенку.
        game = Snake()
        game.food_pos = [599, 639]
        game.snake_body = [Segment.Segment(x, 174) for x in [10, 41, 72]]
        game.snake_pos = Segment.Segment(10, 174)
        game.d = (-1, 0)
        game.t = (-1, 0)

        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                             {'unicode': '\r', 'key': 13, 'mod': 4096, 'scancode': 40, 'window': None}))
        game.change_direction()
        game.move()
        game.determine_second_segment_direction()
        game.check_eating_apple()
        game.spawn_food()
        game.determine_tail_direction()
        self.assertRaises(Exception, game.check_collision)

        # В верхнюю стенку.
        game = Snake()
        game.food_pos = [599, 639]
        game.snake_body = [Segment.Segment(10, y) for y in [50, 81, 112]]
        game.snake_pos = Segment.Segment(10, 50)
        game.d = (0, -1)
        game.t = (0, -1)

        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                             {'unicode': '\r', 'key': 13, 'mod': 4096, 'scancode': 40, 'window': None}))
        game.change_direction()
        game.move()
        game.determine_second_segment_direction()
        game.check_eating_apple()
        game.spawn_food()
        game.determine_tail_direction()
        self.assertRaises(Exception, game.check_collision)

        # В нижнюю стенку.
        game = Snake()
        game.food_pos = [599, 639]
        game.snake_body = [Segment.Segment(10, y) for y in [639, 608, 577]]
        game.snake_pos = Segment.Segment(10, 639)
        game.d = (0, 1)
        game.t = (0, 1)

        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                             {'unicode': '\r', 'key': 13, 'mod': 4096, 'scancode': 40, 'window': None}))
        game.change_direction()
        game.move()
        game.determine_second_segment_direction()
        game.check_eating_apple()
        game.spawn_food()
        game.determine_tail_direction()
        self.assertRaises(Exception, game.check_collision)

        # В себя.
        game = Snake()
        game.food_pos = [599, 639]
        game.snake_body = [Segment.Segment(x, y) for x, y in
                           [[320, 267], [351, 267]] + [[x, 236] for x in [351, 320, 289]]]
        game.snake_pos = Segment.Segment(320, 267)
        game.d = (0, -1)
        game.t = (0, -1)

        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                             {'unicode': '\r', 'key': 13, 'mod': 4096, 'scancode': 40, 'window': None}))
        game.change_direction()
        game.move()
        game.determine_second_segment_direction()
        game.check_eating_apple()
        game.spawn_food()
        game.determine_tail_direction()
        self.assertRaises(Exception, game.check_collision)

    def test_change_direction(self):
        # вправо->вниз.
        game = Snake()
        game.food_pos = [599, 639]
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                             {'unicode': '', 'key': 1073741905, 'mod': 4096, 'scancode': 81,
                                              'window': None}))
        game.pass_frame()
        self.assertEqual(return_states(game), ([599, 639], 0, (0, 1), True, [72, 112], [[72, 112], [72, 81], [41, 81]]))

        # вправо->влево.
        game = Snake()
        game.food_pos = [599, 639]
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                             {'unicode': '', 'key': 1073741904, 'mod': 4096, 'scancode': 80,
                                              'window': None}))
        game.pass_frame()
        self.assertEqual(return_states(game), ([599, 639], 0, (1, 0), True, [103, 81], [[103, 81], [72, 81], [41, 81]]))

        # вправо->вверх.
        game = Snake()
        game.food_pos = [599, 639]
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                             {'unicode': '', 'key': 1073741906, 'mod': 4096, 'scancode': 82,
                                              'window': None}))
        game.pass_frame()
        self.assertEqual(return_states(game), ([599, 639], 0, (0, -1), True, [72, 50], [[72, 50], [72, 81], [41, 81]]))

        # вправо->вправо.
        game = Snake()
        game.food_pos = [599, 639]
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                             {'unicode': '', 'key': 1073741903, 'mod': 4096, 'scancode': 79,
                                              'window': None}))
        game.pass_frame()
        self.assertEqual(return_states(game), ([599, 639], 0, (1, 0), True, [103, 81], [[103, 81], [72, 81], [41, 81]]))

        # вправо->вниз->влево->вверх->вправо.
        game = Snake()
        game.food_pos = [599, 639]
        z = [(1073741905, 81), (1073741904, 80), (1073741906, 82), (1073741903, 79)]
        for x, y in z:
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                                 {'unicode': '', 'key': x, 'mod': 4096, 'scancode': y,
                                                  'window': None}))
            game.pass_frame()
        self.assertEqual(return_states(game), ([599, 639], 0, (1, 0), True, [72, 81], [[72, 81], [41, 81], [41, 112]]))
