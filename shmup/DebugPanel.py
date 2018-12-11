from kivy.animation import Animation
from kivy.clock import Clock
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
            min: -1200
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
            
<ShipSettings>:
    ship_pos: _ship_pos
    ship_speed: _ship_speed
    switch_momentum:_switch_momentum
    
    BoxLayout:
        orientation: 'horizontal'
        size_hint: 1, 1
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        
        CustomLabel:
            id: _ship_speed
            text: 'Ship Velocity: (0, 0)'
            
        CustomLabel:
            id: _ship_pos
            text: 'Ship Position: (0, 0)'
            
        Switch:
            id: _switch_momentum
            active: False
            pos_hint: {'center_x': 0.5, 'top':1.0}
            on_active: root.switch_player_momentum(self.active)
            
    Label:
        text: 'Player Momentum'
        pos: _switch_momentum.pos
        
<EnemySpawnerSettings>:
    switch_continuous_enemies:_switch_continuous_enemies

    Button:
        text: '1 UFO'
        size_hint: 0.1, None
        size: 100, 25 
        pos_hint: {'x':0, 'y':0}
        on_press: root.spawn_ufo(1)
        
    Button:
        text: '5 UFOs'
        size_hint: 0.1, None
        size: 100, 25 
        pos_hint: {'x':0.1, 'y':0}
        on_press: root.spawn_ufo(5)
        
    Button:
        text: '10 UFOs'
        size_hint: 0.1, None
        size: 100, 25 
        pos_hint: {'x':0.2, 'y':0}
        on_press: root.spawn_ufo(10)
        
    Label:
        text: 'Continuous'
        size_hint: 0.1, 1
        pos_hint: {'right': 1.0, 'y':0.0}
        text_size: self.size
        halign: 'right'
        valign: 'middle'
        
    Switch:
        id: _switch_continuous_enemies
        active: False
        size_hint: None, None
        pos_hint: {'right': 1.0, 'y':0.0}
        on_active: root.continuous_enemies(self.active)
        
""")


class EnemySpawnerSettings(Hoverlayout.HoverLayout):
    switch_continuous_enemies = ObjectProperty(None)

    def __init__(self, game_screen, enemies, **kwargs):
        super(EnemySpawnerSettings, self).__init__(**kwargs)
        self.game_screen = game_screen
        self.enemies = enemies
        self.size_hint = 1, 0.1
        self.pos_hint = {'y': 0.99}
        with self.canvas:
            Color(0, 0.5, 0.5, 0.5)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

        self.in_animation = Animation(pos_hint={'y': 0.9}, duration=.10)  # , t='in_expo')
        self.out_animation = Animation(pos_hint={'y': 0.99}, duration=.10)  # , t='in_expo')

    def spawn_ufo(self, val):
        self.game_screen.spawn_ufo(val)

    def continuous_enemies(self, active):
        if active:
            self.game_screen.continuous_generation = True
        else:
            self.game_screen.continuous_generation = False

    def left_click(self):
        pass

    def right_click(self):
        pass

    def double_click(self):
        pass

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


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


class ShipSettings(Hoverlayout.HoverLayout):
    ship_speed = ObjectProperty(None)
    ship_pos = ObjectProperty(None)
    switch_momentum = ObjectProperty(None)

    def __init__(self, game_screen, ship, **kwargs):
        super(ShipSettings, self).__init__(**kwargs)
        self.game_screen = game_screen
        self.ship = ship
        self.size_hint = 1, None
        self.size = 100, 25
        self.pos_hint = {'y': 0.0}
        with self.canvas:
            Color(0, 0.5, 0.5, 0.5)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

        self.in_animation = Animation(pos_hint={'y': 0}, duration=.10)  # , t='in_expo')
        self.out_animation = Animation(pos_hint={'y': 0.0}, duration=.10)  # , t='in_expo')

        Clock.schedule_interval(self.obtain_ship_var, 60 ** -1)

    def obtain_ship_var(self, game_speed):
        # self.ship_speed.text = 'Velocity: %s, %s' % (self.ship.x_vel, self.ship.y_vel)
        # self.ship_pos.text = 'Position: %s, %s' % (self.ship.x, self.ship.y)
        self.ship_speed.text = 'Ship Velocity: (%s, %s)' % (int(self.game_screen.player_x_velocity), int(self.game_screen.player_y_velocity))
        self.ship_pos.text = 'Ship Position: (%s, %s)' % (int(self.ship.x), int(self.ship.y))

    def switch_player_momentum(self, active):
        # print(active)
        if active:
            self.game_screen.player_momentum = True
        else:
            self.game_screen.player_momentum = False

    def left_click(self):
        pass

    def right_click(self):
        pass

    def double_click(self):
        pass

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
