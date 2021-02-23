from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.text import Label as CoreLabel
from kivy.graphics import (Color, Ellipse, Rectangle, Line)
from random import randint as random_int


class GeometryPushWidget(Widget):
    def __init__(self, **kwargs):
        self.grid = 20
        self.width = self.size[0] / self.grid
        self.height = self.size[1] / self.grid
        self.fps = 60
        self.level_data = None
        self.cube_pos = None
        self.camera_pos = None
        self.blocks = None
        self.t = None
        self.cube_s = 40
        self.is_jumping = False
        self.jump_count = 0
        self.pop = 0
        self.last = None
        self.reset()
        super(GeometryPushWidget, self).__init__(**kwargs)

    def reset(self):
        Clock.unschedule(self.main_loop)
        self.level_data = self.generate_level()
        temp_data = self.data_to_mas(self, self.level_data)
        self.blocks = temp_data[0]
        self.t = temp_data[1]
        self.cube_pos = 0
        self.camera_pos = 0
        self.is_jumping = False
        self.jump_count = 0
        self.last = 'ground'
        self.pop += 1
        Clock.schedule_interval(self.main_loop, 1 / self.fps)

    def generate_level(self):
        width = 200
        height = int(self.size[1] / self.grid)
        result = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0]
        ]
        return result

    @staticmethod
    def data_to_mas(self, data):
        result1 = []
        result2 = []
        for i in range(len(data)):
            for j in range(len(data[0])):
                if data[i][j] == 1:
                    result1.append((j * self.grid, int(len(data) - 1 - i) * self.grid))
        for i in range(len(data)):
            for j in range(len(data[0])):
                if data[i][j] == 2:
                    result2.append((j * self.grid, int(len(data) - 1 - i) * self.grid))
        return result1, result2

    @staticmethod
    def regen_blocks_data(self, data):
        result = []
        for i in data:
            result.append((i[0] - self.camera_pos, i[1]))
        return result

    @staticmethod
    def regen_t_data(self, data):
        result = []
        for i in data:
            result.append((i[0] - self.camera_pos, i[1]))
        return result

    def main_loop(self, e):
        with self.canvas:
            self.canvas.clear()
            Color(0, 1, 0, 1)
            if self.is_jumping:
                if self.cube_pos < 0:
                    self.is_jumping = False
                    self.jump_count = 100
                    self.cube_pos = 0
                else:
                    self.cube_pos += int(0.25 * self.jump_count)
                    self.jump_count -= 1
            Rectangle(pos=(self.cube_s, int(self.cube_pos)), size=(self.grid, self.grid))
            Color(1, 1, 0, 1)
            regen_blocks = self.regen_blocks_data(self, self.blocks)
            is_collider = False
            for i in regen_blocks:
                Rectangle(
                    pos=(i[0], i[1]),
                    size=(self.grid, self.grid)
                )
                if self.cube_s + self.grid >= i[0] and self.cube_s <= i[0] + self.grid and self.cube_pos + self.grid >= i[
                        1] and self.cube_pos <= i[1] + self.grid:
                    is_collider = True
                    if self.cube_pos >= i[1]:
                        if self.is_jumping:
                            self.jump_count = i[1] + self.grid
                            self.is_jumping = False
                    else:
                        self.reset()
            if not is_collider and not self.cube_pos == 0 and not self.is_jumping:
                if self.jump_count > 0:
                    self.jump_count = -int(0.1 * self.jump_count)
                self.is_jumping = True
            Color(1, 0, 0, 1)
            for i in self.regen_t_data(self, self.t):
                Rectangle(
                    pos=(i[0], i[1]),
                    size=(self.grid, self.grid)
                )
                if self.cube_s + self.grid > i[0] > self.cube_s:
                    if self.cube_pos < i[1] + self.grid and self.cube_pos + self.grid > i[1]:
                        self.reset()
            if self.camera_pos < 800:
                Color(0, 1, 0, 1)
                attempt_label = CoreLabel(text=f'Attempt №{self.pop}', font_size=25, color=(0, 1, 0, 1))
                attempt_label.refresh()
                Rectangle(
                    texture=attempt_label.texture,
                    size=(100, 30),
                    pos=(200 - int(self.camera_pos), self.size[1] - 230)
                )
            self.camera_pos += 2

    def on_touch_down(self, touch):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_count = 30
        if touch.x < 50:
            self.reset()


class GeometryPushApp(App):
    def build(self):
        return GeometryPushWidget()


if __name__ == '__main__':
    GeometryPushApp().run()
