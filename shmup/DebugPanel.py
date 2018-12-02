from kivy.lang import Builder
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty


import Hoverlayout
import ParticleSystem


Builder.load_string("""
<CustomLabel@Label>:
    text_size: self.size
    halign: 'left'
    valign: 'top'
    
    
<StarfieldSettings>:
    speed_slider:_speed_slider
    size_slider:_size_slider
    bullet_speed_slider:_bullet_speed_slider
    bullet_delay_slider:_bullet_delay_slider
    
    BoxLayout:
        orientation: 'vertical'
        size_hint: 1, 1
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}

        Slider:
            id: _speed_slider 
            min: 5
            max: 1200
            step: 1
            value: 40
            on_value: root.change_star_speed(self.value)
        
        Slider:
            id: _size_slider
            min: 0.01
            max: 0.25
            step: 0.01
            value: 0.1
            on_value: root.change_star_size(self.value)
        
        Slider:
            id: _bullet_speed_slider
            min: 250
            max: 1000
            step: 10
            value: 250
            on_value: root.change_bullet_speed(self.value)
        
        Slider:
            id: _bullet_delay_slider
            min: 0.01
            max: 5.0
            value: 0.5
            on_value: root.change_bullet_delay(self.value)
            
    
    BoxLayout:
        orientation: 'vertical'
        size_hint: 1, 1
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        
        CustomLabel:
            text: 'Star Speed:'
            
        CustomLabel:
            text: 'Star Size Inc:'
        
        CustomLabel:
            text: 'Bullet Speed:'
            
        CustomLabel:
            text: 'Bullet Delay:'
""")


class StarfieldSettings(Hoverlayout.HoverLayout):
    speed_slider = ObjectProperty(None)
    size_slider = ObjectProperty(None)
    bullet_speed_slider = ObjectProperty(None)
    bullet_delay_slider = ObjectProperty(None)

    def __init__(self, game_screen, **kwargs):
        super(StarfieldSettings, self).__init__(**kwargs)
        self.game_screen = game_screen
        self.size_hint = 0.25, 1
        self.pos_hint = {'x': .9}
        with self.canvas:
            Color(0, 0.5, 0.5, 0.5)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

    def change_star_speed(self, val):
        # self.game_screen.speed = val
        for particle in self.game_screen.particles:
            if isinstance(particle, ParticleSystem.Star):
                particle.speed = val
                # particle.default_speed = int(40 * val)

    def change_star_size(self, val):
        # self.game_screen.size_inc = val
        for particle in self.game_screen.particles:
            if isinstance(particle, ParticleSystem.Star):
                particle.default_size = val

    def change_bullet_speed(self, val):
        # self.game_screen.size_inc = val
        for particle in self.game_screen.particles:
            if isinstance(particle, ParticleSystem.Bullet):
                particle.speed = val

    def change_bullet_delay(self, val):
        # self.game_screen.size_inc = val
        for particle in self.game_screen.particles:
            if isinstance(particle, ParticleSystem.Bullet):
                particle.delay = val

    def left_click(self):
        # print('StarfieldSettings left click')
        pass

    def right_click(self):
        # print('StarfieldSettings right click')
        pass

    def double_click(self):
        # print('StarfieldSettings double click')
        pass

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
