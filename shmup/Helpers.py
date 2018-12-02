import json
from kivy.core.image import Image as CoreImage


def load_atlas(atlas_name):
    # print('\nload_atlas')
    with open(atlas_name, 'rb') as f:
        atlas = json.loads(f.read().decode('utf-8'))

        tex_name, mapping = atlas.popitem()
        # print(tex_name, mapping)
        tex = CoreImage(tex_name).texture
        tex_width, tex_height = tex.size

        uvmap = {}
        for name, val in mapping.items():
            x0, y0, w, h = val
            x1, y1 = x0 + w, y0 + h
            uvmap[name] = UVMapping(
                x0 / tex_width, 1 - y1 / tex_height,
                x1 / tex_width, 1 - y0 / tex_height,
                0.5 * w, 0.5 * h
            )
        return tex, uvmap


class UVMapping:
    """
    UVMapping is essentially a tuple, an immutable and memory-efficient
    data structure with all fields still accessible by index.

    Field(s) Description
    u0, v0   UV coordinates of the sprite's top-left corner
    u1, v1   UV coordinates of the sprite's bottom-right corner
    su       Sprite width divided by 2; this value is useful when building
    an       array of vertices
    sv       Sprite height divided by 2; this is similar to the previous field

    """
    def __init__(self, u0, v0, u1, v1, su, sv):
        self.u0 = u0  # top left corner
        self.v0 = v0  # ---
        self.u1 = u1  # bottom right corner
        self.v1 = v1  # ---
        self.su = su  # equals to 0.5 * width
        self.sv = sv  # equals to 0.5 * height