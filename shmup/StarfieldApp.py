from kivy import utils
from kivy.app import App
from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout

from Starfield import Starfield, StarfieldControlPanel


class StarfieldApp(App):
    def build(self):
        EventLoop.ensure_window()
        sf = Starfield()
        sf_cp = StarfieldControlPanel(sf)
        l = FloatLayout(pos_hint={'center_x': 0.5, 'center_y': 0.5})
        l.sf = sf
        l.add_widget(sf)
        l.add_widget(sf_cp)
        return l

    def on_start(self):
        # print('self:', self)
        # print('self.root:', self.root)
        # print('self.root.children:', self.root.children)

        Clock.schedule_interval(self.root.sf.update_glsl, 60 ** -1)


if __name__ == '__main__':
    Config.set('graphics', 'width', '960')
    Config.set('graphics', 'height', '540')
    # Config.set('graphics', 'show_cursor', '0')
    # Config.set('input', 'mouse', 'mouse,disable_multitouch')

    from kivy.core.window import Window
    Window.clearcolor = utils.get_color_from_hex('111110')
    StarfieldApp().run()
