#!/usr/bin/kivy
import kivy
kivy.require('1.0.6')
from cg_graphics_audio import *
from cei2 import *
from DetailsForm import *
from consent_form import ConsentForm
from final_form import FinalForm
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy_logger import *
from curiosity_score import *



class CuriosityApp(App):
    sm = None
    cg = None
    cf = None
    qf = None
    df = None
    ff = None
    score = None
    float_layout = None

    cei2 = None

    def build(self):
        # initialize logger
        KL.start([DataMode.file], "/sdcard/Android/curiosity/")# self.user_data_dir)

        self.cg = CuriosityGame(self)
        self.cf = ConsentForm(self)
        self.cei2 = CEI2()
        self.qf = []
        for p in range(0, len(self.cei2.page_dict)):
            self.qf.append(QuestionsForm(self, self.cei2.page_dict[p]))
        self.df = DetailsForm(self)
        self.ff = FinalForm(self)

        self.score = CuriosityScore(self.cg.game_duration,
                                    len(self.cg.items),
                                    self.user_data_dir)

        self.sm = ScreenManager()

        screen = Screen(name='consent')
        screen.add_widget(self.cf)
        self.sm.add_widget(screen)

        screen = Screen(name='thegame')
        screen.add_widget(self.cg.the_widget)
        # self.sm.add_widget(screen)

        for kqf in range(0, len(self.qf)):
            screen = Screen(name="question"+str(kqf))
            screen.add_widget(self.qf[kqf])
            # self.sm.add_widget(screen)

        screen = Screen(name="details")
        screen.add_widget(self.df)
        # self.sm.add_widget(screen)

        screen = Screen(name="final")
        screen.bind(on_enter=self.ff.start)
        screen.add_widget(self.ff)
        self.sm.add_widget(screen)

        self.start()
        return self.sm

    def start(self):
        KL.start([DataMode.file], self.user_data_dir)
        self.cf.start(self)
        for qf in self.qf:
            qf.start()
        self.df.start()
        self.sm.current = "consent"

    def on_pause(self):
        return True

if __name__ == '__main__':
    CuriosityApp().run()

