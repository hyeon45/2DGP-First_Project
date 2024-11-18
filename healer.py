from pico2d import get_time, load_image, draw_rectangle

import game_framework
import game_world
from state_machine import StateMachine, start_event, right_down, left_up, left_down, right_up, space_down, time_out

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Idle:
    @staticmethod
    def enter(healer, e):
        healer.action = 7
        if start_event(e):
            healer.face_dir = 1
        elif right_down(e) or left_up(e):
            healer.face_dir = -1
        elif left_down(e) or right_up(e):
            healer.face_dir = 1

        healer.frame = 0
        healer.wait_time = get_time()

    @staticmethod
    def exit(healer, e):
        if space_down(e):
            pass

    @staticmethod
    def do(healer):
        healer.frame = (healer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        if get_time() - healer.wait_time > 2:
            healer.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(healer):
        if healer.face_dir == 1:
            healer.image.clip_composite_draw(int(healer.frame) * 80, healer.action * 125, 80, 125, 0, 'h', healer.x, healer.y, 80, 125)
        else:
            healer.image.clip_draw(int(healer.frame) * 80, healer.action * 125, 80, 125, healer.x, healer.y)



class Sleep:
    @staticmethod
    def enter(healer, e):
        if start_event(e):
            healer.face_dir = 1
            healer.action = 7
        healer.frame = 0

    @staticmethod
    def exit(healer, e):
        pass

    @staticmethod
    def do(healer):
        healer.frame = (healer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6


    @staticmethod
    def draw(healer):
        if healer.face_dir == 1:
            healer.image.clip_composite_draw(int(healer.frame) * 80, healer.action * 125, 80, 125,
                                             3.141592 / 2, 'h', healer.x - 25, healer.y - 25, 80, 125)
        else:
            healer.image.clip_composite_draw(int(healer.frame) * 80, healer.action * 125, 80, 125,
                                             -3.141592 / 2, '', healer.x + 25, healer.y - 25, 80, 125)


class Run:
    @staticmethod
    def enter(healer, e):
        healer.action = 5
        if right_down(e) or left_up(e):
            healer.dir, healer.face_dir = 1, 1
        elif left_down(e) or right_up(e):
            healer.dir, healer.face_dir = -1, -1

    @staticmethod
    def exit(healer, e):
        pass


    @staticmethod
    def do(healer):
        healer.frame = (healer.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        healer.x += healer.dir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(healer):
        if healer.face_dir == 1:
            healer.image.clip_composite_draw(int(healer.frame) * 80, healer.action * 125, 80, 125, 0, 'h', healer.x, healer.y, 80, 125)
        else:
            healer.image.clip_draw(int(healer.frame) * 80, healer.action * 125, 80, 125, healer.x, healer.y)


class Jump:
    @staticmethod
    def enter(healer, event):
        healer.velocity_y = 500
        healer.action = 4
        healer.frame = 0

    @staticmethod
    def exit(healer, event):
        pass

    @staticmethod
    def do(healer):
        healer.velocity_y -= 9.8 * 100 * game_framework.frame_time
        healer.y += healer.velocity_y * game_framework.frame_time

        if healer.y <= 90:
            healer.y = 90

    @staticmethod
    def draw(healer):
        healer.image.clip_draw(int(healer.frame) * 100, healer.action * 100, 100, 100, healer.x, healer.y)



class Healer:
    def __init__(self):
        self.x, self.y = 400, 90
        self.face_dir = 1
        self.velocity_y = 0
        self.image = load_image('image\\Healer.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Sleep, space_down: Jump},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Jump},
                Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle},
                Jump: {time_out: Idle, right_down: Run, left_down: Run}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - 50, self.x + 20, self.y + 50

    def handle_collision(self, group, other):
        game_framework.quit()
