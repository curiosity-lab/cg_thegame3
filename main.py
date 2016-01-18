#!/usr/bin/kivy
import kivy
kivy.require('1.0.6')
from cg_graphics_audio import *
from cei2 import *
from DetailsForm import *
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy_logger import *
from curiosity_score import *



class CuriosityApp(App):
    sm = None
    cg = None
    qf = None
    df = None
    score = None
    float_layout = None

    def build(self):
        # initialize logger
        KL.start([DataMode.file, DataMode.encrypted], self.user_data_dir)

        self.cg = CuriosityGame(self)
        self.qf = QuestionsForm(self)
        self.df = DetailsForm()

        self.score = CuriosityScore(self.cg.game_duration, len(self.cg.items), self.user_data_dir)

        self.sm = ScreenManager()

        screen = Screen(name='thegame')
        screen.add_widget(self.cg.the_widget)
        # self.sm.add_widget(screen)

        screen = Screen(name="question")
        screen.add_widget(self.qf)
        # self.sm.add_widget(screen)

        screen = Screen(name="details")
        screen.add_widget(self.df)
        self.sm.add_widget(screen)

        self.cg.start()

        return self.sm


    def on_pause(self):
        return True

if __name__ == '__main__':
    CuriosityApp().run()

