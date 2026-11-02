from pico2d import *
from boy import Boy
from grass import Grass
import game_world

# Game object class here

def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            boy.handle_event(event)

# 캐릭터 아래에 박혀있어야해?

def reset_world():
    global boy
    game_world.clear()

    grass1 = Grass()
    grass1.y = 60
    game_world.add_object(grass1, 0)

    grass2 = Grass()
    game_world.add_object(grass2, 2)

    boy = Boy()
    game_world.add_object(boy, 1)


def update_world():
    game_world.update()
    pass


def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()


running = True



open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
