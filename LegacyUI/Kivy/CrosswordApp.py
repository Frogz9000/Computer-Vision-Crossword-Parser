from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen

class IntroScreen(Screen):
    pass
class LoadScreen(Screen):
    pass

class CrosswordApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(IntroScreen(name="intro"))
        sm.add_widget(LoadScreen(name="load"))
        return sm

if __name__ == '__main__':
    CrosswordApp().run()