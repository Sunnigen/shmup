from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

Builder.load_string("""

<HealthBar>:
    size_hint: None, None
    size: 200, 50
        

<PlayerGUI>:
    player_health:_player_health
    size_hint: 1, 1
    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    
    HealthBar:
        id: _player_health
        pos_hint: {'x': 0.01, 'y':0.01}
        
""")


class HealthBar(Widget):

    curr_health = NumericProperty(-100)
    max_health = NumericProperty(-100)

    def __init__(self, max_health=100, curr_health=0, **kwargs):
        super(HealthBar, self).__init__(**kwargs)
        if curr_health == 0:
            self.curr_health = max_health
            self.max_health = max_health
        with self.canvas:
            Color(1, 0, 0, 0.5)
            self.health_bar_rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(pos=self.update_rect, size=self.update_rect)

        self.label = Label(text='%s/%s' % (self.curr_health, self.max_health))
        self.label.pos_hint = self.pos_hint
        self.label.size = self.size
        self.label.text_size = self.label.size
        self.label.halign = 'center'
        self.label.valign = 'middle'
        self.add_widget(self.label)

    def update_rect(self, *args):
        self.health_bar_rect.pos = self.pos
        self.health_bar_rect.size = self.size
        self.label.size = self.size
        self.label.pos = self.pos

    def take_damage(self, val):
        if val >= self.curr_health:
            new_health = 0
        else:
            new_health = self.curr_health - val
        health_anim = Animation(curr_health=new_health, duration=0.5)
        health_anim.start(self)

    def restore_life(self, val):
        if val > self.max_health:
            self.curr_health = self.max_health

    def on_curr_health(self, instance, val):
        self.health_bar_rect = val




class PlayerGUI(FloatLayout):
    player_health = ObjectProperty(None)

    def __init__(self, game_screen, **kwargs):
        super(PlayerGUI, self).__init__(**kwargs)
        self.game_screen = game_screen

    def hide_gui(self):
        hide_anim = Animation(opacity=0, duration=0.1)
        hide_anim.start(self)

    def show_gui(self):
        show_anim = Animation(opacity=1, duration=0.1)
        show_anim.start(self)
