#!/usr/bin/python
# -*- coding: utf-8 -*-
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.storage.jsonstore import JsonStore


class FinalForm(BoxLayout):
    the_app = None
    statements = None
    statement_label = None

    def __init__(self, the_app):
        super(FinalForm, self).__init__()
        self.the_app = the_app

        self.statements = {}
        store = JsonStore('final_statements.json').get('final_statements')
        for key, value in store.items():
            self.statements[key] = {}
            for k,v in value.items():
                self.statements[key][k] = v

        title = "כל הכבוד!"
        title_label = Label(text=title[::-1], font_size=50,
                            font_name="DejaVuSans.ttf", halign='center', size_hint_y=1.2,
                            color=[0.235294, 0.701961, 0.443137, 1])

        self.statement_label = Label(text="test", font_size=40,
                            font_name="DejaVuSans.ttf", halign='center', size_hint_y=0.4,
                            color=[0.235294, 0.701961, 0.443137, 1])

        self.add_widget(title_label)
        self.add_widget(self.statement_label)

    def start(self, pars):
        final_score = 'high'
        print(self.the_app.score.score)
        # total_info in percentage
        if 'total_info' in self.the_app.score.score:
            score = self.the_app.score.score['total_info']
            if score < 0:
                score = 0.75
            score_angle = score * 360

            if score < 0.5:
                final_score = 'low'
            else:
                if score < 0.75:
                    final_score = 'medium'

            with self.canvas:
                Ellipse(pos=(400,400), size=(200,200),angle_start=0, angle_end=score_angle)

        statement = self.statements[final_score]["s1"][::-1]
        print(statement)
        self.statement_label.text = statement