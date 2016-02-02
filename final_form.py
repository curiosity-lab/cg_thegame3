#!/usr/bin/python
# -*- coding: utf-8 -*-
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty
from hebrew_management import HebrewManagement


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

        title_txt = u"כל הכבוד!"
        self.title.text = title_txt[::-1]

        curiosity_txt = u"        חובק אפשרויות                 סקרנות                   חיפוש הלא נודע                      "
        self.curiosity_lbl.text = curiosity_txt[::-1]

        statement_layout = BoxLayout(orientation="vertical")
        self.statement_label = []
        statement_layout.add_widget(BoxLayout(size_hint_y=0.3))

        for k in range(0,4):
            self.statement_label.append(Label(font_size=40,
                                              font_name="fonts/the_font.ttf",
                                              halign='center', size_hint_y=0.4,
                                              color=[0,0,0, 1]))
            statement_layout.add_widget(self.statement_label[-1])
        self.add_widget(statement_layout)
        end_text = u"סיום"
        self.end_button.text = end_text[::-1]
        self.end_button.bind(on_press=self.next)

    def start(self, pars):
        final_score = 'high'
        score_angle = []
        print(self.the_app.score.score)

        # stretching in percentage
        if 'stretching' in self.the_app.score.score:
            score = self.the_app.score.score['stretching'] / float(25)
            if score < 0:
                score = 0.75
            score_angle.append(score * 360)

        # total_info in percentage
        if 'total_info' in self.the_app.score.score:
            score = self.the_app.score.score['total_info']
            if score < 0:
                score = 0.75
            score_angle.append(score * 360)

            if score < 0.25:
                final_score = 'low'
            else:
                if score < 0.5:
                    final_score = 'medium'

        # embracing in percentage
        if 'embracing' in self.the_app.score.score:
            score = self.the_app.score.score['embracing'] / float(25)
            if score < 0:
                score = 0.75
            score_angle.append(score * 360)

        new_lines = HebrewManagement.multiline(self.statements[final_score]["s1"][::-1], 75)
        for nl in range(0, len(new_lines)):
            self.statement_label[nl].text = new_lines[nl]

        self.canvas.remove(Ellipse())
        self.canvas.add(Color(0, 0.71, 1., 1))
        for k in range(0, len(score_angle)):
            self.canvas.add(Ellipse(pos=(400 + 450 * k,350),size=(300,300),angle_start=0,
                        angle_end=score_angle[k]))


    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def next(self, pars):
        self.the_app.start()
