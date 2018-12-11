from functools import partial
from random import randint, random

from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.graphics import Color, Mesh, Rectangle
from kivy.graphics.instructions import RenderContext
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget

from Star import Star


Builder.load_string("""
<CustomLabel@Label>:
    text_size: self.size
    halign: 'left'
    valign: 'top'
    

<StarfieldControlPanel>:
    speed_slider:_speed_slider
    size_slider:_size_slider

    size_hint: 0.25, 0.25
    pos_hint: {'x': 0, 'y': 0}

    Slider:
        id: _speed_slider 
        min: 0.05
        max: 10.0
        value: 2
        pos_hint: {'x':0, 'y':0.5}
        size_hint: 1, 0.5
        on_value: root.change_star_speed(self.value)
    
    Slider:
        id: _size_slider
        min: 0.05
        max: 0.75
        value: 0.1
        pos_hint: {'x':0, 'y':0}
        size_hint: 1, 0.5
        on_value: root.change_star_size(self.value)
        
    CustomLabel:
        text: 'Star Speed:'
        pos_hint: {'x':0, 'y':0.5}
        size_hint: 0.5, 0.5
        
    CustomLabel:
        text: 'Star Size Inc:'
        pos_hint: {'x':0, 'y':0.0}
        size_hint: 0.5, 0.5
""")

NSTARS = randint(500, 1000)


class Starfield(Widget):
    speed = 0.5
    size_inc = 0.25

    def __init__(self, **kwargs):
        super(Starfield, self).__init__(**kwargs)
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.source = 'starfield.glsl'

        self.vfmt = (
            (b'vCenter',         2,  'float'),
            (b'vScale',          1,  'float'),
            (b'vPosition',       2,  'float'),
            (b'vTexCoords0',     2,  'float'),
        )

        self.vsize = sum(attr[1] for attr in self.vfmt)

        self.indices = []
        for i in range(0, 4 * NSTARS, 4):
            self.indices.extend((
                i, i + 1, i + 2, i + 2, i + 3, i
            ))

        self.vertices = []
        for i in range(NSTARS):
            self.vertices.extend((
                0, 0, 1, -24, -24, 0, 1,
                0, 0, 1,  24, -24, 1, 1,
                0, 0, 1,  24,  24, 1, 0,
                0, 0, 1, -24,  24, 0, 0,
            ))

        self.texture = CoreImage('star.png').texture
        self.stars = [Star(self, i) for i in range(NSTARS)]

    # def load_shaders(self):
    #     self.canvas = RenderContext(use_parent_projection=True)
    #     self.canvas.shader.source = 'starfield.glsl'
    #
    #     self.vfmt = (
    #         (b'vCenter',         2,  'float'),
    #         (b'vScale',          1,  'float'),
    #         (b'vPosition',       2,  'float'),
    #         (b'vTexCoords0',     2,  'float'),
    #     )
    #
    #     self.vsize = sum(attr[1] for attr in self.vfmt)
    #
    #     self.indices = []
    #     for i in range(0, 4 * NSTARS, 4):
    #         self.indices.extend((
    #             i, i + 1, i + 2, i + 2, i + 3, i
    #         ))
    #
    #     self.vertices = []
    #     for i in range(NSTARS):
    #         self.vertices.extend((
    #             0, 0, 1, -16, -16, 0, 1,
    #             0, 0, 1,  16, -16, 1, 1,
    #             0, 0, 1,  16,  16, 1, 0,
    #             0, 0, 1, -16,  16, 0, 0,
    #         ))
    #
    #     self.texture = CoreImage('star.png').texture
    #     self.stars = [Star(self, i) for i in range(NSTARS)]

    def update_glsl(self, game_speed):
        x0, y0 = self.center
        # max_distance = 1.1 * max(x0, y0)
        max_distance = max(Window.width, Window.height) * 1.1

        # ---Set Starts in Motion---
        for star in self.stars:
            star.distance *= self.speed * game_speed + 1
            star.size += self.size_inc * game_speed

            # ---Capture Stars that have Escaped---
            if star.distance > max_distance:
                star.reset()
            else:
                star.update(x0, y0)

        self.canvas.clear()
        self.canvas['opacity'] = random()

        with self.canvas:
            Mesh(fmt=self.vfmt, mode='triangles',
                 indices=self.indices, vertices=self.vertices,
                 texture=self.texture
                 )


class StarfieldControlPanel(FloatLayout):

    speed_slider = ObjectProperty(None)
    size_slider = ObjectProperty(None)

    def __init__(self, starfield, **kwargs):
        super(StarfieldControlPanel, self).__init__(**kwargs)
        self.starfield = starfield

        with self.canvas.before:
            Color(0, 0.5, 0.5, 0.25)
            rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=partial(self.update_bg, rect), size=partial(self.update_bg, rect))

    def change_star_speed(self, val):
        self.starfield.speed = val

    def change_star_size(self, val):
        self.starfield.size_inc = val

    def update_bg(self, rect, *args):
        rect.pos = self.pos
        rect.size = self.size
