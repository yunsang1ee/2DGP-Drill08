import math

from pico2d import get_time, Event
from sdl2 import *


class Idle:
    @staticmethod
    def enter(owner, event):
        if start_event(event):
            owner.action = 2
            owner.dir = -1
        elif rightDown(event) or leftUp(event):
            owner.action = 2
            owner.dir = -1
        elif leftDown(event) or rightUp(event):
            owner.action = 3
            owner.dir = 1
        elif timeOut(event):
            owner.action = 2 if owner.dir == -1 else 3
        owner.frame = 0
        print(f'Idle Enter{owner=}')
        owner.startTime = get_time()
        pass

    @staticmethod
    def exit(owner, event):
        print(f'Idle Exit {owner=}')
        pass

    @staticmethod
    def do(owner):
        owner.frame = (owner.frame + 1) % 8
        if get_time() - owner.startTime > 3:
            owner.state_machine.addEvent(('TIMEOUT', 0))
        pass

    @staticmethod
    def draw(owner):
        owner.image.clip_draw(owner.frame * 100, owner.action * 100, 100, 100
            , owner.x, owner.y)
        pass
    pass

class Sleep:
    @staticmethod
    def enter(owner, event):
        if start_event(event):
            owner.dir = -1
            owner.action = 2
        owner.frame = 0
        print(f'Sleep Enter {owner=} ')
        pass

    @staticmethod
    def exit(owner, event):
        print(f'Sleep Exit {owner=} ')
        pass

    @staticmethod
    def do(owner):
        owner.frame = (owner.frame + 1) % 8
        pass

    @staticmethod
    def draw(owner):
        owner.image.clip_composite_draw(
            owner.frame * 100, 300, 100, 100
            , math.pi / 2 if owner.dir == 1 else -math.pi / 2  # 90도 회전
            , ' ' if owner.dir == 1 else 'h'            # 좌우상하 반전 X
            , owner.x, owner.y - 25, 100, 100
        )
        pass
    pass

class AutoRun:
    @staticmethod
    def enter(owner, event):
        if aDown(event):
            owner.action = 1 if owner.dir == 1 else 0
        print(f'AutoRun Enter {owner=}')
        owner.startTime = get_time()
        pass

    @staticmethod
    def exit(owner, event):
        print(f'AutoRun Exit {owner=} ')
        pass
    pass

    @staticmethod
    def do(owner):
        owner.frame = (owner.frame + 1) % 8
        if owner.x > 800: owner.dir, owner.action = -1, 0
        elif owner.x < 0: owner.dir, owner.action = 1, 1
        owner.x += owner.dir * 50
        if get_time() - owner.startTime > 5:
            owner.state_machine.addEvent(('TIMEOUT', 0))
        pass

    @staticmethod
    def draw(owner):
        owner.image.clip_composite_draw(
            owner.frame * 100, owner.action * 100, 100, 100
            , 0
            , ' '
            , owner.x, owner.y + 50, 300, 300
        )
        pass
    pass

class Run:
    @staticmethod
    def enter(owner, event):
        print(f'Run Enter {owner=}')
        if rightDown(event) or leftUp(event):
            owner.dir, owner.action = 1, 1
        elif leftDown(event) or rightUp(event):
            owner.dir, owner.action = -1, 0
        pass

    @staticmethod
    def exit(owner, event):
        print(f'Run Exit {owner=} ')
        pass

    @staticmethod
    def do(owner):
        owner.frame = (owner.frame + 1) % 8
        owner.x += owner.dir * 10
        pass

    @staticmethod
    def draw(owner):
        owner.image.clip_draw(
            owner.frame * 100, owner.action * 100, 100, 100
            , owner.x, owner.y
        )
        pass
    pass

def start_event(e):
    return e[0] == 'START'
def timeOut(e):
    return e[0] == 'TIMEOUT'
def spaceDown(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
def rightDown(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def rightUp(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def leftDown(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def leftUp(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
def aDown(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def aUp(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a

class StateMachine:
    def __init__(self, own):
        self.owner = own
        self.state = None
        self.eventQueue = []
        self.transitions : dict = (
            {
                Idle : {
                    timeOut : Sleep,
                    rightDown : Run,
                    leftDown : Run,
                    rightUp : Run,
                    leftUp : Run,
                    aDown : AutoRun,
                },
                Sleep : {
                    spaceDown : Idle
                },
                Run : {
                    rightDown : Idle,
                    leftDown : Idle,
                    rightUp : Idle,
                    leftUp : Idle,
                },
                AutoRun : {
                    timeOut : Idle,
                    rightDown : Run,
                    leftDown : Run,
                },
            }
        )

    def Init(self, state):
        self.state = state
        self.state.enter(self.owner, ('START', 0))
        pass

    def update(self):
        self.state.do(self.owner)
        if self.eventQueue:
            event = self.eventQueue.pop(0)

            for checkEvent, nextState in self.transitions[self.state].items():
                if checkEvent(event):
                    # print(f'Exit {self.state=}')
                    self.state.exit(self.owner, event)
                    self.state = nextState
                    # print(f'Enter {self.state=}')
                    self.state.enter(self.owner, event)
                    return
                pass
            # assert False, f'Error {event}'
            pass
        pass

    def draw(self):
        self.state.draw(self.owner)
        pass

    def addEvent(self, event : tuple):
        # print(f'{type(self)} add Event {event}')
        self.eventQueue.append(event)
        pass

    def transition(self, transitions):
        self.transitions = transitions
        pass