import math
from random import random


class Star:
    angle = 0
    distance = 0
    size = 0.1

    def __init__(self, sf, i):
        self.sf = sf  # Starfield
        self.j = 4 * i * sf.vsize  # index of star's 1st vertex in vertices array
        self.reset()

    def iterate(self):
        return range(self.j,
                     self.j + 4 * self.sf.vsize,
                     self.sf.vsize)

    def update(self, x0, y0):
        # ---Refreshes (4) Vertices belonging to a star, writing new coordinates(Vertices)---
        x = x0 + self.distance * math.cos(self.angle)
        y = y0 + self.distance * math.sin(self.angle)

        for i in self.iterate():
            self.sf.vertices[i:i + 3] = (x, y, self.size)

    def reset(self):
        # ---Reverts Attributes to Default/Slightly Randomized---
        self.angle = 2 * math.pi * random()  # Angle at which star will fly
        self.distance = 90 * random() + 10  # How fast specific star will fly
        self.size = 0.05 * random() + 0.1  # Randomized Size, although random range is quite small
