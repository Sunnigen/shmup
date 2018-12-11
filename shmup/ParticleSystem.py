import math
from random import choice, randint, random


class Particle:
    x = 0
    y = 0
    size = 1

    def __init__(self, parent, i):
        self.parent = parent  # store reference PSWidget
        self.vsize = parent.vsize
        self.base_i = 4 * i * self.vsize
        self.reset(created=True)
        self.texture_size = (1, 1)

    def update(self):
        # Update all (4) vertices of a polygon to keep in sync with particle's
        # desired location and scale. Specifically the x, y and size properties
        for i in range(self.base_i,
                       self.base_i + 4 * self.vsize,
                       self.vsize):
            self.parent.vertices[i:i + 3] = (
                self.x, self.y, self.size)

    def reset(self, created=False):
        """
        Raising NotImplementedError from a virtual method is a
        way to inform the developer that it would be nice to define
        this method on a derived class. We could have omitted the last
        two methods altogether, but that would lead to a less relevant
        error, AttributeError. Preserving method signatures, even
        in the absence of a default implementation, is also nice and
        reduces guesswork for your peers (or your future self, should
        you revisit the same code after a long delay).
        """
        raise NotImplementedError()

    def advance(self, game_speed):
        raise NotImplementedError()


class Trail(Particle):
    tex_name = 'trail'
    default_size = 0.6
    drift_distance = 120

    def reset(self, created=False):
        self.x = self.parent.player_x + randint(-30, -20)
        self.y = self.parent.player_y + randint(-10, 10)

        if created:
            self.size = 0
        else:
            self.size = random() + self.default_size

    def advance(self, game_speed):
        self.size -= game_speed
        if self.size <= 0.1:
            self.reset()
        else:
            self.x -= self.drift_distance * game_speed


class Bullet(Particle):
    active = False
    tex_name = 'bullet'
    speed = 500
    delay = 0.5
    angle = 0

    def reset(self, created=False):
        self.active = False
        self.x = -100
        self.y = -100

    def advance(self, game_speed):
        if self.active:  # If bullet is already live
            self.x += self.speed * game_speed

            # ---"Deactive" Bullet If Off-screen---
            if 0 > self.x or self.x > self.parent.width:
                self.reset()

        elif self.parent.firing and self.parent.fire_delay <= 0:  # Check if bullet can be created
            self.active = True
            self.x = self.parent.player_x + 40
            self.y = self.parent.player_y
            self.parent.fire_delay += self.delay


class Enemy(Particle):
    active = False
    tex_name = 'ufo'
    v = 0
    movement_patterns = ['right_parabola', 'across', 'up_diagonal', 'down_diagonal']
    current_pattern = 'across'
    ship_speed = 4

    def reset(self, created=False):
        self.active = False
        self.x = -100
        self.y = -100
        self.v = 0
        self.current_pattern = None

    def advance(self, game_speed):
        # print('game_speed:', game_speed)
        if self.active:
            if self.check_collision():  # Step 1
                self.reset()
                return

            # Horizontal Movement
            if self.current_pattern == 'across':
                self.x -= self.width * self.ship_speed * game_speed
            elif self.current_pattern == 'right_parabola':
                pass
            elif self.current_pattern == 'up_diagonal':
                pass
            elif self.current_pattern == 'down_diagonal':
                pass

            if self.x < -self.width:  # Check if ship is completely out of sight
                self.reset()
                return

            # Vertical Movement
            if self.current_pattern == 'across':
                # self.y += self.v * game_speed *
                pass
            elif self.current_pattern == 'right_parabola':
                pass
            elif self.current_pattern == 'up_diagonal':
                self.y += self.v * game_speed * 2
            elif self.current_pattern == 'down_diagonal':
                self.y -= self.v * game_speed * 2

            if self.y <= 0:
                self.v = abs(self.v)
            elif self.y >= self.parent.height:
                self.v = -abs(self.v)

        # elif self.parent.spawn_delay <= 0:  # Step 4
        elif self.parent.spawn_counter > 0:  # Step 4
            self.active = True
            # self.current_pattern = choice(self.movement_patterns)
            self.current_pattern = 'across'

            if self.current_pattern == 'across':
                self.x = self.parent.width + self.width
                self.y = self.parent.height * random()
            elif self.current_pattern == 'right_parabola':
                pass
            elif self.current_pattern == 'up_diagonal':
                self.y += self.v * game_speed * 2
            elif self.current_pattern == 'down_diagonal':
                self.y -= self.v * game_speed * 2

            self.v = randint(-100, 100)
            # self.parent.spawn_delay += 1
            self.parent.spawn_counter -= 1
        # if self.active:
        #     print('Enemy Ship pos: (%s, %s)' % (self.x, self.y))
        #     print('Current Pattern: %s' % self.current_pattern)

    def check_collision(self):
        if math.hypot(self.parent.player_x - self.x,
                      self.parent.player_y - self.y) < 60:
            return True

        for bullet in self.parent.bullets:
            if not bullet.active:
                continue

            if math.hypot(bullet.x - self.x, bullet.y - self.y) < 30:
                bullet.reset()
                return True


class Player(Particle):
    tex_name = 'player'
    control_mode = 'keyboard'
    max_velocity = 600
    x_vel = 0
    y_vel = 0

    def move_ship(self, x, y):
        self.x = x
        self.y = y

    def reset(self, created=False):
        # pass
        self.x = self.parent.player_x
        self.y = self.parent.player_y

    # advance = reset

    def advance(self, game_speed):
        self.x = self.parent.player_x
        self.y = self.parent.player_y
    #     self.x_vel = self.parent.player_x_velocity
    #     self.y_vel = self.parent.player_y_velocity
    #     self.x += self.x_vel * game_speed
    #     self.y += self.y_vel * game_speed


class Star(Particle):
    plane = 1
    tex_name = 'star'
    speed = 40
    default_size = 0.1

    def reset(self, created=False):
        # Randomizes star's plane and position
        self.plane = randint(1, 3)

        if created:
            if self.speed > 0:
                self.x = random() * self.parent.width + self.size
            # print('self.parent:', self.parent)
            # print('self.parent.width:', self.parent.width)
            # print('not created', self.x)

        else:
            if self.speed > 0:
                self.x = self.parent.width + self.size
            else:
                self.x = -self.width*2
            # self.default_speed = self.speed
            # print('self.parent:', self.parent)
            # print('self.parent.width:', self.parent.width)
            # print('not created', self.x)

        self.y = random() * self.parent.height
        self.size = self.default_size * self.plane
        # self.speed = randint(self.default_speed - 10, self.default_speed + 10)

    def advance(self, game_speed):
        # Move sprite to the left until out of screen then reset
        self.x -= self.speed * self.plane * game_speed
        self.size = self.default_size * self.plane
        # ---Going Right to Left---
        if self.x < 0 - (self.width * 2) and self.speed > 0:
            self.reset()
        # ---Going Left to Right---
        if self.x > self.parent.width + (self.width * 2) and self.speed < 0:
            self.reset()
