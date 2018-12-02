from kivy.app import App
from kivy.base import EventLoop
from kivy.uix.screenmanager import FallOutTransition, ScreenManager

import GameScreen
import MenuScreen
import TitleScreen


class GameApp(App):
    def build(self):
        sm = ScreenManager(transition=FallOutTransition())
        sm.add_widget(TitleScreen.TitleScreen(name='title'))
        sm.add_widget(GameScreen.GameScreen(name='game'))
        sm.add_widget(MenuScreen.MenuScreen(name='menu'))
        sm.current = 'title'
        EventLoop.ensure_window()
        return sm


if __name__ == '__main__':
    GameApp().run()
