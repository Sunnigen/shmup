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

    def advance(self, nap):
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

    def advance(self, nap):
        self.size -= nap
        if self.size <= 0.1:
            self.reset()
        else:
            self.x -= self.drift_distance * nap


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

    def advance(self, nap):
        if self.active:  # If bullet is already live
            self.x += self.speed * nap

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

    def reset(self, created=False):
        self.active = False
        self.x = -100
        self.y = -100
        self.v = 0

    def advance(self, nap):
        # print('nap:', nap)
        if self.active:
            if self.check_hit():  # Step 1
                self.reset()
                return

            self.x -= 200 * nap  # Step 2
            if self.x < 50:
                self.reset()
                return

            self.y += self.v * nap  # Step 3
            if self.y <= 0:
                self.v = abs(self.v)
            elif self.y >= self.parent.height:
                self.v = -abs(self.v)

        elif self.parent.spawn_delay <= 0:  # Step 4
            self.active = True



            self.x = self.parent.width + 50
            self.y = self.parent.height * random()
            self.v = randint(-100, 100)
            self.parent.spawn_delay += 1

    def check_hit(self):
        if math.hypot(self.parent.player_x - self.x,
                      self.parent.player_y - self.y) < 60:
            return True

        for b in self.parent.bullets:
            if not b.active:
                continue

            if math.hypot(b.x - self.x, b.y - self.y) < 30:
                b.reset()
                return True


class Player(Particle):
    tex_name = 'player'

    def reset(self, created=False):
        self.x = self.parent.player_x
        self.y = self.parent.player_y

    def advance(self, nap):
        self.x = self.parent.player_x
        self.y = self.parent.player_y

class Star(Particle):
    plane = 1
    tex_name = 'star'
    # default_speed = 40
    speed = 40
    default_size = 0.1

    def reset(self, created=False):
        # Randomizes star's plane and position
        self.plane = randint(1, 3)

        if created:
            self.x = random() * self.parent.width + self.size
            # print('self.parent:', self.parent)
            # print('self.parent.width:', self.parent.width)
            # print('not created', self.x)

        else:
            self.x = self.parent.width + self.size
            # self.default_speed = self.speed
            # print('self.parent:', self.parent)
            # print('self.parent.width:', self.parent.width)
            # print('not created', self.x)

        self.y = random() * self.parent.height
        self.size = self.default_size * self.plane
        # self.speed = randint(self.default_speed - 10, self.default_speed + 10)

    def advance(self, nap):
        # Move sprite to the left until out of screen then reset
        self.x -= self.speed * self.plane * nap
        self.size = self.default_size * self.plane
        if self.x < 0:
            self.reset()
