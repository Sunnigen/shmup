from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

Builder.load_string("""
#:import randint random

<CustomLabel@Label>:
    text_size: self.size
    halign: 'left'
    valign: 'top'

<MainMenuScreen>:

    BoxLayout:
        orientation: 'vertical'
        spacing: 10
        padding: 10
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint: 0.8, 0.8
        
        Button:
            text: 'New Game'
            size_hint: 1, 0.25
            on_press: root.start_game('new game')
            
        Button:
            text: 'Load Game'
            size_hint: 1, 0.25
            on_press: root.start_game('load game')
            
        Button:
            text: 'Options'
            size_hint: 1, 0.25
            on_press: root.switch_to_settings('options')
            
<SettingScreen>:
    Button:
        text: 'Back'
        size_hint: None, 0.1
        pos_hint: {'x': 0.01, 'top':0.99}
        size: 75, 50
        on_press: root.switch_back()

    BoxLayout:
        orientation: 'vertical'
        pos_hint: {'top': 0.9}
        size_hint_y: 0.9         
        Slider:
            min: 1
            max: 50
            # value: random.randint(1, 50)
            value: 2
            on_value: root.slider_1(self.value)
        Slider:
            min: 1
            max: 50
            # value: random.randint(1, 50)
            value: 25
            on_value: root.slider_2(self.value)
        
    BoxLayout:
        orientation: 'vertical'
        pos_hint: {'top': 0.9}
        size_hint_y: 0.9   
        
        CustomLabel:
            text: 'Option 1'
            
        CustomLabel:
            text: 'Option 2'
""")


class SettingScreen(Screen):

    def slider_1(self, val, *args):
        print('SettingScreen.slider_1:', val)

    def slider_2(self, val, *args):
        print('SettingScreen.slider_1:', val)

    def switch_back(self, *args):
        self.manager.current = 'main'

    def on_touch_down(self, touch):
        return super(SettingScreen, self).on_touch_down(touch)


class MainMenuScreen(Screen):
    def start_game(self, text):
        # print('MainMenuScreen.start_game:', text)
        self.manager.parent.start_game(text)

    def switch_to_settings(self, text):
        # print('MainMenuScreen.switch_to_settings', text)
        self.manager.parent.switch_to_settings(text)


class MenuScreen(Screen):

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.menu_sm = ScreenManager()
        self.menu_sm.add_widget(MainMenuScreen(name='main'))
        self.menu_sm.add_widget(SettingScreen(name='setting'))
        self.menu_sm.current = 'main'
        self.add_widget(self.menu_sm)

    def start_game(self, text, *args):
        # print('MenuScreen.start_game:', text)
        self.manager.current = 'game'

    def switch_to_settings(self, text, *args):
        # print('MenuScreen.switch_to_settings:', text)
        self.menu_sm.current = 'setting'

    def on_pre_enter(self, *args):
        print('MenuScreen.on_pre_enter')

    def on_enter(self, *args):
        print('MenuScreen.on_enter')
