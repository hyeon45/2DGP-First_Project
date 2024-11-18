from pico2d import *

import game_framework
from dungeon import Dungeon
from healer import Healer

import game_world


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            healer.handle_event(event)


def init():
    global dungeon
    global healer

    dungeon = Dungeon()
    game_world.add_object(dungeon, 0)

    healer = Healer()
    game_world.add_object(healer, 1)



def finish():
    game_world.clear()
    pass

def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass
