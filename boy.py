import math

from pico2d import *

from state_machine import *

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.Init(Idle)

    def update(self):
        self.state_machine.update()
        # self.frame = (self.frame + 1) % 8

    def handle_event(self, event : Event):
        self.state_machine.addEvent(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        # self.image.clip_draw(self.frame * 100, self.action * 100, 100, 100, self.x, self.y)
