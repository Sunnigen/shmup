from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


Builder.load_string("""
<TitleScreen>:
    Label:
        # text: 'shmup'
        text: 'Test'
        font_size: 30
        pos_hint: {'center_x': 0.5, 'center_y': 0.8}
        
    Label:
        text: 'Test'
        font_size: 20
        pos_hint: {'center_x': 0.5, 'center_y': 0.25}
""")


class TitleScreen(Screen):
    user_touch = True

    def on_touch_down(self, touch):
        if self.user_touch:
            self.manager.current = 'menu'
            self.user_touch = False
