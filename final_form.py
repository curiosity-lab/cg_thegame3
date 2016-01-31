#!/usr/bin/python
# -*- coding: utf-8 -*-
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty
from kivy.uix.button import Button


class FinalForm(BoxLayout):
    the_app = None
    statements = None
    statement_label = None
    title=ObjectProperty()
    curiosity_lbl=ObjectProperty()
    end_button=ObjectProperty()

    def __init__(self, the_app):
        super(FinalForm, self).__init__()
        self.the_app = the_app

        self.statements = {}
        store = JsonStore('final_statements.json').get('final_statements')
        for key, value in store.items():
            self.statements[key] = {}
            for k,v in value.items():
                self.statements[key][k] = v

        title_txt = "כל הכבוד!"
        self.title.text = title_txt[::-1]

        curiosity_txt = "מדד סקרנות"
        self.curiosity_lbl.text = curiosity_txt[::-1]

        self.statement_label = Label(text="test", font_size=40,
                                     font_name="fonts/the_font.ttf",
                                     halign='center', size_hint_y=0.4,
                                     color=[0,0,0, 1])


        # self.add_widget(title_label)
        self.add_widget(self.statement_label)
        self.add_widget(BoxLayout())
        end_text = "סיום"
        self.end_button.text = end_text[::-1]
        self.end_button.bind(on_press=self.next)

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
                Color(0, 0.71, 1., 1)
                Ellipse(pos=(400,400), size=(200,200),angle_start=0,
                        angle_end=score_angle)

        statement = self.statements[final_score]["s1"][::-1]
        print(statement)
        self.statement_label.text = statement

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def next(self, pars):
        self.the_app.start()
