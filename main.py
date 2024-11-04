from pico2d import *

from dungeon import Dungeon

import game_world


def handle_events():
    global game

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game = False
        else:
            # healer.handle_event(event)
            pass


def reset_world():
    global game

    game = True

    dungeon = Dungeon()
    game_world.add_object(dungeon, 0)


def update_world():
    game_world.update()


def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()

game_width, game_height = 960, 900
open_canvas(game_width, game_height)
reset_world()

while game:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()