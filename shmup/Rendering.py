from kivy.graphics import Color, Rectangle, Mesh, RenderContext
from kivy.uix.widget import Widget

import Helpers


class PSWidget(Widget):
    indices = []
    vertices = []
    particles = []

    """
    • vCenter: This is the location of the sprite on the screen. It should be the same
               value for all vertices of a given sprite
    • vPosition: This is the vertex position relative to the center of the sprite,
                 unaffected by the previous value
    • vTexCoords0: This is the texture coordinates (UV) for each vertex.
                   It determines which part of the large texture will be rendered.
    """

    def __init__(self, **kwargs):
        super(PSWidget, self).__init__(**kwargs)
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.source = self.glsl

        # self.red, self.green, self.blue, self.hue = 1, 1, 0, 1

        self.vfmt = (
            (b'vCenter', 2, 'float'),
            (b'vScale', 1, 'float'),
            (b'vPosition', 2, 'float'),
            (b'vTexCoords0', 2, 'float'),
            # (b'opacity', 1, 'float'),
        )

        self.vsize = sum(attr[1] for attr in self.vfmt)

        self.texture, self.uvmap = Helpers.load_atlas(self.atlas)

    def make_particles(self, Cls, num):
        # num = requested number of partcles
        count = len(self.particles)
        uv = self.uvmap[Cls.tex_name]
        particles = []
        print('%s Size: (%s, %s)' % (Cls, uv.su * 2, uv.sv * 2))

        for i in range(count, count + num):
            j = 4 * i
            self.indices.extend((
                j, j + 1, j + 2, j + 2, j + 3, j))

            self.vertices.extend((
                0, 0, 1,  -uv.su,  -uv.sv,  uv.u0,  uv.v1,
                0, 0, 1,   uv.su,  -uv.sv,  uv.u1,  uv.v1,
                0, 0, 1,   uv.su,   uv.sv,  uv.u1,  uv.v0,
                0, 0, 1,  -uv.su,   uv.sv,  uv.u0,  uv.v0,
            ))

            p = Cls(self, i)
            p.texture_size = (uv.su * 2, uv.sv * 2)
            p.width = uv.su * 2
            p.height = uv.sv * 2
            self.particles.append(p)
            particles.append(p)

        return particles

    def update_glsl(self, game_speed):
        """
        • This loop can and should be parallelized, in full or partially
        • This code can also run on another thread completely, and
          not update every frame (again, this optimization may
          apply to selected classes of particles, for example, stuff in
          background that doesn't affect main program flow)
        """
        for p in self.particles:
            p.advance(game_speed)  # update state of particle
            p.update()  # keep necessary data in array of vertices in sync with internal state

        self.canvas.clear()

        # print('texture:', self.texture)
        with self.canvas:
            # Color(self.red, self.green, self.blue, self.hue)
            Mesh(fmt=self.vfmt, mode='triangles',
                 indices=self.indices, vertices=self.vertices,
                 texture=self.texture)
