import unittest
from types import SimpleNamespace
from unittest.mock import patch

from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_SPACE

from ball import Ball
from boy import Boy
import game_world


class BallTest(unittest.TestCase):
    def setUp(self):
        game_world.clear()
        self.addCleanup(game_world.clear)
        for target, value in (
            ('boy.get_time', 0), ('boy.get_canvas_width', 800),
            ('ball.get_canvas_width', 800),
        ):
            mocked = patch(target, return_value=value)
            mocked.start()
            self.addCleanup(mocked.stop)
        for target in ('boy.load_image', 'ball.load_image'):
            mocked = patch(target)
            mocked.start()
            self.addCleanup(mocked.stop)
        image = patch.object(Ball, 'image', None)
        image.start()
        self.addCleanup(image.stop)
        self.boy = Boy()

    def event(self, event_type, key):
        self.boy.handle_event(SimpleNamespace(type=event_type, key=key))

    def test_idle_and_run_kick_in_facing_direction(self):
        for state in ('IDLE', 'RUN'):
            for key, direction in ((SDLK_LEFT, -1), (SDLK_RIGHT, 1)):
                with self.subTest(state=state, direction=direction):
                    game_world.clear()
                    self.boy = Boy()
                    game_world.append(self.boy, 1)
                    self.event(SDL_KEYDOWN, key)
                    if state == 'IDLE':
                        self.event(SDL_KEYUP, key)
                    self.event(SDL_KEYDOWN, SDLK_SPACE)
                    self.assertEqual(self.boy.state, state)
                    self.assertEqual(len(game_world.world[1]), 2)
                    ball = game_world.world[1][-1]
                    self.assertIsInstance(ball, Ball)
                    self.assertEqual(ball.direction, direction)
                    self.assertEqual((ball.x, ball.y), (400 + direction * 30, 70))
                    x = ball.x
                    game_world.update()
                    self.assertEqual(ball.x, x + direction * 10)
                    self.assertEqual(self.boy.x, 400 + (direction * 5 if state == 'RUN' else 0))
                    game_world.render()
                    ball.image.draw.assert_called_with(ball.x, ball.y)

    def test_sleep_space_only_wakes_and_next_space_kicks(self):
        self.boy.fall_asleep()
        self.event(SDL_KEYDOWN, SDLK_SPACE)
        self.assertEqual(self.boy.state, 'IDLE')
        self.assertEqual(game_world.world, [[], []])
        self.event(SDL_KEYDOWN, SDLK_SPACE)
        self.assertEqual(len(game_world.world[1]), 1)

    def test_key_release_and_other_transitions_do_not_kick(self):
        self.event(SDL_KEYUP, SDLK_SPACE)
        self.event(SDL_KEYDOWN, SDLK_LEFT)
        self.event(SDL_KEYUP, SDLK_SPACE)
        self.event(SDL_KEYUP, SDLK_LEFT)
        self.boy.fall_asleep()
        self.event(SDL_KEYUP, SDLK_SPACE)
        self.assertEqual(self.boy.state, 'SLEEP')
        self.assertEqual(game_world.world, [[], []])

    def test_ball_keeps_direction_after_character_turns(self):
        self.event(SDL_KEYDOWN, SDLK_RIGHT)
        self.event(SDL_KEYDOWN, SDLK_SPACE)
        ball = game_world.world[1][-1]
        self.event(SDL_KEYUP, SDLK_RIGHT)
        self.event(SDL_KEYDOWN, SDLK_LEFT)
        self.assertEqual(self.boy.face_dir, -1)
        x = ball.x
        game_world.update()
        self.assertEqual(ball.x, x + 10)
        self.assertEqual(ball.direction, 1)

    def test_removing_adjacent_offscreen_balls_does_not_skip_updates(self):
        left = Ball(-20, 70, -1)
        right = Ball(820, 70, 1)
        active = Ball(400, 70, 1)
        for ball in (left, right, active):
            game_world.append(ball, 1)
        game_world.update()
        self.assertEqual(game_world.world, [[], [active]])
        self.assertEqual(active.x, 410)

    def test_layer_order_and_bulk_add_remove(self):
        drawn = []

        class Object:
            def __init__(self, name):
                self.name = name

            def draw(self):
                drawn.append(self.name)

        background = Object('background')
        first, second = Object('first'), Object('second')
        game_world.add_objects([first, second], 1)
        game_world.add_object(background, 0)
        game_world.render()
        self.assertEqual(drawn, ['background', 'first', 'second'])
        game_world.remove_objects([first, second], 1)
        game_world.remove_object(background)
        self.assertEqual(game_world.world, [[], []])


if __name__ == '__main__':
    unittest.main()
