from functools import partial

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen

import DebugPanel
import KeyboardInputs
import Rendering
import ParticleSystem


class GameScreen(Screen):

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.game_update = None
        self.pressed_keys = KeyboardInputs.KeyboardInputs.pressed_keys
        # print('self.pressed_keys:', self.pressed_keys.items())
        self.user_press_clock = None

        self.game_screen = Game(size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.debug = DebugPanel.StarfieldSettings(game_screen=self.game_screen)

        self.add_widget(self.game_screen)
        self.add_widget(self.debug)

    def on_enter(self, *args):
        # print('GameScreen.on_enter')
        self.game_screen.initialize()
        self.game_update = Clock.schedule_interval(self.game_screen.update_glsl, 60 ** -1)
        Clock.schedule_once(self.start_game, 0.5)

    def start_game(self, dt):
        game_screen = self.game_screen
        game_screen.player_x = Window.width/5
        game_screen.player_y = Window.height/2
        game_screen.player_x = 100
        game_screen.player_y = 100
        self.user_press_clock = Clock.schedule_interval(self.check_for_keys, 60 ** -1)  # start checking for inputs

        Window.bind(on_key_down=self.on_keyboard_down)
        Window.bind(on_key_up=self.on_keyboard_up)

    def fly_in(self, dt):
        # spiral: r = ae^(theta*math.cot(b))
        # x,
        pass

    def check_for_keys(self, dt):
        game_screen = self.game_screen

        if self.pressed_keys['275']:  # 'A Button'
            game_screen.on_touch_down(touch=None)
        else:
            game_screen.on_touch_up(touch=None)

        if self.pressed_keys['115']:  # 'Down Arrow Pad'

            game_screen.player_y -= 2

        if self.pressed_keys['100']:  # 'Right Arrow Pad'
            game_screen.player_x += 2

        if self.pressed_keys['97']:  # 'Left Arrow Pad'
            game_screen.player_x -= 2

        if self.pressed_keys['119']:  # 'Up Arrow Pad'
            game_screen.player_y += 2

        if self.pressed_keys['274']:  # 'B Button'
            pass

    def on_keyboard_down(self, keyboard, keycode, text, modifiers, *args):
        self.pressed_keys[str(keycode)] = True
        print('')

    def on_keyboard_up(self, keyboard, keycode, *args):
        self.pressed_keys[str(keycode)] = False


class Game(Rendering.PSWidget):
    firing = False
    fire_delay = 0
    glsl = 'starfield.glsl'
    atlas = 'shmup.atlas'
    spawn_delay = 1

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.fire_delay = 0
        self.player_x, self.player_y = -100, -100

    def initialize(self):
        # print('Game.initialize')
        star_count = 200
        trail_count = 100
        player_count = 1
        enemy_count = 25
        bullet_count = 100

        self.stars = self.make_particles(ParticleSystem.Star, star_count)
        self.trail = self.make_particles(ParticleSystem.Trail, trail_count)
        self.players = self.make_particles(ParticleSystem.Player, player_count)
        self.enemies = self.make_particles(ParticleSystem.Enemy, enemy_count)
        self.bullets = self.make_particles(ParticleSystem.Bullet, bullet_count)

    def on_touch_down(self, touch):
        # if not self.user_control:
        #     return

        self.firing = True
        # self.fire_delay = 0

    def on_touch_up(self, touch):
        # if not self.user_control:
        #     return

        self.firing = False

    def update_glsl(self, nap):
        # if self.user_control:
        #     self.player_x, self.player_y = Window.mouse_pos

        # if self.firing:
        if self.fire_delay > 0:
            self.fire_delay -= nap
        # print('fire_delay:', self.fire_delay)

        self.spawn_delay -= nap

        # Rendering.PSWidget.update_glsl(self, nap)
        return super(Game, self).update_glsl(nap)
