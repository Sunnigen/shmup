from kivy.animation import Animation
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout


class HoverBehavior(object):
    """Hover behavior.

    :Events:
        `on_enter`
            Fired when mouse enter the bbox of the widget.
        `on_leave`
            Fired when the mouse exit the widget
    """

    hovered = BooleanProperty(False)
    border_point = ObjectProperty(None)
    '''Contains the last relevant point received by the Hoverable. This can
    be used in `on_enter` or `on_leave` in order to know where was dispatched the event.
    '''

    def __init__(self, **kwargs):
        self.register_event_type('on_mouse_enter')
        self.register_event_type('on_mouse_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        # Window.bind(mouse_pos=self.on_mouse_leave)
        super(HoverBehavior, self).__init__(**kwargs)

    def on_mouse_pos(self, *args):
        if not self.parent:
            Window.unbind(mouse_pos=self.on_mouse_pos)

        if not self.get_root_window():
            return  # do proceed if I'm not displayed <=> If have no parent
        pos = args[1]
        # Next line to_widget allow to compensate for relative layout
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            # We have already done what was needed
            return
        self.border_point = pos
        self.hovered = inside
        if inside:
            self.dispatch('on_mouse_enter')
        else:
            self.dispatch('on_mouse_leave')

    def on_mouse_enter(self):
        pass

    def on_mouse_leave(self):
        pass


Factory.register('HoverBehavior', HoverBehavior)


class HoverLayout(FloatLayout, HoverBehavior):

    def __init__(self, **kwargs):
        super(HoverLayout, self).__init__(**kwargs)
        self.in_animation = Animation(pos_hint={'x': .75}, duration=.10)  #, t='in_expo')
        self.out_animation = Animation(pos_hint={'x': .995}, duration=.10)  #, t='in_expo')
        # print('HoverLayout loaded')

    def on_opacity(self, *args, **kwargs):
        # print('hover gui opacity: %d' % self.opacity)
        if self.opacity < 1:
            # print('hiding h9overlayout')
            self.out_animation.start(self)

    def on_mouse_enter(self, *args):
        if not self.disabled and self.parent.opacity == 1 and self.in_animation:
            # print("You are in, through this point", self.border_point)
            self.in_animation.start(self)

    def on_mouse_leave(self, *args):
        if not self.disabled and self.parent.opacity == 1:
            # print("You left through this point", self.border_point)
            self.out_animation.start(self)

    def on_touch_down(self, touch):
        if not self.disabled and self.collide_point(*touch.pos):

            if touch.is_double_tap and touch.button == 'left':
                # print('double click on hover layout')
                self.double_click()
                return super(HoverLayout, self).on_touch_down(touch)

            if touch.button == 'right':
                # print('right click on hover layout')
                self.right_click()
                return super(HoverLayout, self).on_touch_down(touch)

            if touch.button == 'left':
                # print('left click on hover layout')
                self.left_click()
                return super(HoverLayout, self).on_touch_down(touch)


    def double_click(self):
        raise NotImplementedError()

    def left_click(self):
        raise NotImplementedError()

    def right_click(self):
        raise NotImplementedError()
