from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import Screen

import DebugPanel
import KeyboardInputs
import Rendering
import ParticleSystem
import PlayerGUI


class GameScreen(Screen):

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.game_update = None
        self.pressed_keys = KeyboardInputs.KeyboardInputs.pressed_keys
        # print('self.pressed_keys:', self.pressed_keys.items())
        self.user_press_clock = None

        self.game_screen = Game(size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.star_field_debug = DebugPanel.StarfieldSettings(game_screen=self.game_screen)
        self.player_gui = PlayerGUI.PlayerGUI(game_screen=self.game_screen)
        self.add_widget(self.game_screen)
        self.add_widget(self.player_gui)
        self.add_widget(self.star_field_debug)

    def on_enter(self, *args):
        # print('GameScreen.on_enter')
        self.game_screen.initialize()
        self.ship_debug = DebugPanel.ShipSettings(game_screen=self.game_screen, ship=self.game_screen.player_ship)
        self.enemy_debug = DebugPanel.EnemySpawnerSettings(game_screen=self.game_screen, enemies=self.game_screen.enemies)
        self.add_widget(self.enemy_debug)
        self.add_widget(self.ship_debug)
        self.game_update = Clock.schedule_interval(self.game_screen.update_glsl, 60 ** -1)
        Clock.schedule_once(self.start_game, 0.5)

    def start_game(self, dt):
        game_screen = self.game_screen
        # game_screen.player_x = Window.width/5
        # game_screen.player_y = Window.height/2
        game_screen.player_x, game_screen.player_y = 100, 100

        game_screen.player_ship.move_ship(100, 100)
        self.user_press_clock = Clock.schedule_interval(self.check_for_keys, 60 ** -1)  # start checking for inputs

        Window.bind(on_key_down=self.on_keyboard_down)
        Window.bind(on_key_up=self.on_keyboard_up)

    def fly_in(self, dt):
        # spiral: r = ae^(theta*math.cot(b))
        # x,
        pass

    def check_for_keys(self, game_speed):
        game_screen = self.game_screen
        ship_speed = 8

        # if self.pressed_keys['275']:  # 'A Button'
        #     game_screen.on_touch_down(touch=None)
        # else:
        #     game_screen.on_touch_up(touch=None)

        if self.pressed_keys['115']:  # 'Down Arrow Pad'
            if game_screen.player_momentum:
                game_screen.change_speed(y_vel=-ship_speed*2)
            else:
                game_screen.change_ship_pos(y=-ship_speed/2)

        if self.pressed_keys['100']:  # 'Right Arrow Pad'
            if game_screen.player_momentum:
                game_screen.change_speed(x_vel=ship_speed*2)
            else:
                game_screen.change_ship_pos(x=ship_speed / 2)

        if self.pressed_keys['97']:  # 'Left Arrow Pad'
            if game_screen.player_momentum:
                game_screen.change_speed(x_vel=-ship_speed*2)
            else:
                game_screen.change_ship_pos(x=-ship_speed / 2)

        if self.pressed_keys['119']:  # 'Up Arrow Pad'
            if game_screen.player_momentum:
                game_screen.change_speed(y_vel=ship_speed*2)
            else:
                game_screen.change_ship_pos(y=ship_speed / 2)

        if self.pressed_keys['274']:  # 'B Button'
            pass

    def on_keyboard_down(self, keyboard, keycode, text, modifiers, *args):
        keycode = str(keycode)
        self.pressed_keys[keycode] = True

        if keycode == '275':  # start firing
            self.game_screen.firing = True
            return

    def on_keyboard_up(self, keyboard, keycode, *args):
        keycode = str(keycode)
        self.pressed_keys[str(keycode)] = False

        if keycode == '275':  # stop firing
            self.game_screen.firing = False
            return


class Game(Rendering.PSWidget):
    firing = False
    fire_delay = 0
    glsl = 'starfield.glsl'
    atlas = 'shmup.atlas'
    spawn_delay = 1
    spawn_counter = 0
    max_spawn = 100
    continuous_generation = BooleanProperty(False)

    player_momentum = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.fire_delay = 0
        self.player_x, self.player_y = -100, -100
        self.player_x_velocity, self.player_y_velocity = 0, 0

    def initialize(self):
        # print('Game.initialize')
        star_count = 200
        trail_count = 100
        player_count = 1
        enemy_count = self.max_spawn
        bullet_count = 100

        self.stars = self.make_particles(ParticleSystem.Star, star_count)
        self.trail = self.make_particles(ParticleSystem.Trail, trail_count)
        self.player_ship = self.make_particles(ParticleSystem.Player, player_count)[0]
        self.enemies = self.make_particles(ParticleSystem.Enemy, enemy_count)
        self.bullets = self.make_particles(ParticleSystem.Bullet, bullet_count)

    def on_touch_down(self, touch):

        self.firing = True
        # self.fire_delay = 0

    def on_touch_up(self, touch):

        self.firing = False

    def update_glsl(self, game_speed):
        # self.player_x, self.player_y = Window.mouse_pos

        # ---Player Fire Delay---
        if self.fire_delay > 0:
            self.fire_delay -= game_speed

        # ---Player Ship Movement---
        if self.player_momentum:  # momentum-based movement
            # TODO: Add acceleration
            new_x = self.player_x + self.player_x_velocity * game_speed
            if self.check_within_screen(x=new_x):
                self.player_x = new_x

            new_y = self.player_y + self.player_y_velocity * game_speed
            if self.check_within_screen(y=new_y):
                self.player_y = new_y

            # self.player_x += self.player_x_velocity * game_speed
            # self.player_y += self.player_y_velocity * game_speed
            self.velocity_degradation(game_speed)  # degrade velocity

        # ---Enemy Ship Generation---
        if self.continuous_generation:
            self.spawn_ufo(0.05)
        # self.spawn_delay -= game_speed

        # Rendering.PSWidget.update_glsl(self, game_speed)
        return super(Game, self).update_glsl(game_speed)

    def spawn_ufo(self, count):
        if self.spawn_counter > self.max_spawn:
            return
        else:
            self.spawn_counter += count

    def change_ship_pos(self, x=-100.0, y=-100.0):
        if x > -100:
            if self.check_within_screen(x=x + self.player_x):
                self.player_x += x

        if y > -100:
            if self.check_within_screen(y=y + self.player_y):
                self.player_y += y

    def change_speed(self, x_vel=0, y_vel=0):
        max_velocity = self.player_ship.max_velocity

        if x_vel != 0:
            if x_vel + self.player_x_velocity < -max_velocity:
                self.player_x_velocity = -max_velocity
            elif x_vel + self.player_x_velocity > max_velocity:
                self.player_x_velocity = max_velocity
            else:
                self.player_x_velocity += x_vel
            # print('x_vel:', self.player_x_velocity)
            return

        if y_vel != 0:
            if y_vel + self.player_y_velocity < -max_velocity:
                self.player_y_velocity = -max_velocity
            elif y_vel + self.player_y_velocity > max_velocity:
                self.player_y_velocity = max_velocity
            else:
                self.player_y_velocity += y_vel
            # print('y_vel:', self.player_y_velocity)
            return
        # elif y_vel != 0 and not self.player_momentum:

    def velocity_degradation(self, game_speed):
        max_velocity = self.player_ship.max_velocity
        degradation_factor = max_velocity * game_speed * 0.75
        # ship_speed = 8

        if self.player_x_velocity < 0:
            self.player_x_velocity += degradation_factor
            # print('positive degradation')
        elif self.player_x_velocity > 0:
            self.player_x_velocity -= degradation_factor
            # print('negative degradation')

        if self.player_y_velocity < 0:
            self.player_y_velocity += degradation_factor
            # print('positive degradation')
        elif self.player_y_velocity > 0:
            self.player_y_velocity -= degradation_factor
            # print('negative degradation')

    def check_within_screen(self, x=-100.0, y=-100.0):
        ship_width = self.player_ship.texture_size[0]
        ship_height = self.player_ship.texture_size[1]
        if x > -100 and y > -100:
            # print('both x and y movement')
            if ship_width/2 < x <= self.width - (ship_width/2) and ship_height/2 < y <= self.height - (ship_height/2):
                return True
            return False

        if x > -100:
            # print('x movement')
            if ship_width/2 < x <= self.width - (ship_width/2):
                return True
            return False

        if y > -100:
            # print('y movement')
            if ship_height/2 < y <= self.height - (ship_height/2):
                return True
            return False

    def on_player_momentum(self, instance, val):
        if not val:
            self.player_x_velocity = 0
            self.player_y_velocity = 0


