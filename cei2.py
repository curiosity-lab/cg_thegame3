#!/usr/bin/python
# -*- coding: utf-8 -*-

from kivy.graphics import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from kivy_logger import *


class AnswerButton(CheckBox, WidgetLogger):
    question = ""
    answer = ""
    form = None

    def on_press(self, *args):
        super(AnswerButton, self).on_press(*args)
        self.form.answers[self.question] = self.answer


class QuestionsForm(BoxLayout):
    answers = {}
    the_app = None

    def __init__(self, app):
        super(QuestionsForm, self).__init__()
        self.the_app = app
        with self.canvas.before:
            self.rect = Rectangle(source='back2.png')
            self.bind(size=self._update_rect, pos=self._update_rect)
        dict = {'q_in_page': [], 'qu_title': "", 'qu_description': "", 'ques': {},
                'ans': {}, 'next_button': "", 'prev_button': ""}
        self.answers = {}
        store = JsonStore('questions.json').get('questionnaire')

        for key, value in store.items():
            if key in ['qu_title', 'next_button', 'prev_button', 'questions']:
                dict[key] = value[::-1]
            if key in ['qu_description', 'ques', 'ans']:
                dict[key] = {}
                for kqa, qa in value.items():
                    dict[key][kqa] = qa[::-1]

        layout = GridLayout(cols=len(dict['ans']) + 2, rows=len(dict['ques']) + 1, row_default_height=40)
        layoutup = BoxLayout(orientation='vertical')
        layoutup.add_widget(
            Label(text=dict['qu_title'], font_size=50, font_name="DejaVuSans.ttf", halign='right', size_hint_y=0.2,
                  color=[1, 0, 1, 1]))
        layoutup.add_widget(BoxLayout(size_hint_y=0.5))
        layoutup.add_widget(
            Label(text=dict['qu_description']['d1'], font_name="DejaVuSans.ttf", font_size=40, halign='right',
                  size_hint_y=0.1))
        layoutup.add_widget(
            Label(text=dict['qu_description']['d2'], font_name="DejaVuSans.ttf", font_size=40, halign='right',
                  size_hint_y=0.1))
        layoutup.add_widget(
            Label(text=dict['qu_description']['d3'], font_name="DejaVuSans.ttf", font_size=40, halign='right',
                  size_hint_y=0.1))
        layoutup.add_widget(BoxLayout(size_hint_y=0.2))

        q_counter = 0
        for ques in dict['ques']:
            layout.add_widget(BoxLayout(size_hint_x=0.05))
            q_counter += 1
            if q_counter == 1:
                for ans in dict['ans']:
                    print(ans)
                    layout.add_widget(
                        Label(size_hint_x=0.1, text=dict['ans'][ans], font_name="DejaVuSans.ttf", halign='right'))
                layout.add_widget(
                    Label(text="תולאש", font_name="DejaVuSans.ttf", halign='right', orientation='vertical'))
                layout.add_widget(BoxLayout(size_hint_x=0.1))

            for ans in dict['ans']:
                ab = AnswerButton(size_hint_x=0.15, text="", group=str(q_counter), )
                ab.name = str(ques) + "," + str(ans)
                ab.question = ques
                ab.answer = ans
                ab.form = self
                layout.add_widget(ab)

            # CHECK ID AND KEEP THE CLICK VALUE
            layout.add_widget(
                Label(halign='right', text=dict['ques'][ques], font_name="DejaVuSans.ttf", orientation='vertical',
                      font_size=30))

        layoutup.add_widget(layout)
        layoutup.add_widget(BoxLayout())
        layoutbuttons = BoxLayout(size_hint_y=0.2)

        layoutbuttons.add_widget(Button(background_color=[1, 0, 1, 1],
                                        text=dict['next_button'], font_size=20, font_name="DejaVuSans.ttf",
                                        halign='right', on_press=self.next))
        layoutbuttons.add_widget(BoxLayout(size_hint_x=0.2))
        layoutbuttons.add_widget(Button(background_color=[1, 0, 1, 1],
                                        text=dict['prev_button'], font_size=20, font_name="DejaVuSans.ttf",
                                        halign='right'))

        layoutup.add_widget(layoutbuttons)
        self.add_widget(layoutup)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def next(self, pars):
        self.the_app.sm.current = self.the_app.sm.next()
