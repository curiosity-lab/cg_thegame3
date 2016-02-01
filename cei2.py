#!/usr/bin/python
# -*- coding: utf-8 -*-

from kivy.graphics import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import collections
from kivy_logger import *


class AnswerButton(WidgetLogger, CheckBox):
    question = ""
    answer = ""
    form = None

    def on_press(self, *args):
        super(AnswerButton, self).on_press(*args)
        self.form.set_answer(self.question, self.answer)


class QuestionsForm(BoxLayout):
    answers = {}
    ans_button = []
    the_app = None
    questions = {}
    next_button = None

    def __init__(self, app):
        super(QuestionsForm, self).__init__()
        self.the_app = app
        with self.canvas.before:
            self.rect = Rectangle(source='back4.png')
            self.bind(size=self._update_rect, pos=self._update_rect)

        dict = {'q_in_page': [], 'qu_title': "", 'qu_description': "", 'ques': {},
                'ans': {}, 'next_button': "", 'prev_button': ""}
        self.answers = {}
        store = JsonStore('questions.json', encoding='utf-8').get('questionnaire')

        for key, value in store.items():
            if key in ['qu_title', 'next_button', 'prev_button', 'questions']:
                dict[key] = value[::-1]
            if key in ['qu_description', 'ques', 'ans']:
                dict[key] = {}
                for kqa, qa in value.items():
                    dict[key][kqa] = qa[::-1]
        dict['ques'] = collections.OrderedDict(sorted(dict['ques'].items()))
        dict['ans'] = collections.OrderedDict(sorted(dict['ans'].items()))

        self.questions = dict['ques']

        layout = GridLayout(cols=len(dict['ans']) + 2,
                            rows=len(dict['ques']) + 1,
                            row_default_height=40)
        layoutup = BoxLayout(orientation='vertical')
        layoutup.add_widget(BoxLayout(size_hint_y=0.7))
        layoutup.add_widget(
            Label(text=dict['qu_title'],
                  font_size=50, font_name="fonts/the_font.ttf",
                  halign='right', size_hint_y=0.4,size_hint_x=1.5,
                  color=[0,0,0,1]))
        layoutup.add_widget(BoxLayout(size_hint_y=0.1))
        layoutup.add_widget(
            Label(text=dict['qu_description']['d1'],
                  font_name="fonts/the_font.ttf", font_size=30, halign='right',
                  size_hint_y=0.15,
                  color=[0,0,0,1]))
        layoutup.add_widget(
            Label(text=dict['qu_description']['d2'],
                  font_name="fonts/the_font.ttf", font_size=30, halign='right',
                  size_hint_y=0.15,
                  color=[0,0,0,1]))
        layoutup.add_widget(
            Label(text=dict['qu_description']['d3'],
                  font_name="fonts/the_font.ttf", font_size=30, halign='right',
                  size_hint_y=0.15,
                  color=[0,0,0,1]))
        layoutup.add_widget(BoxLayout(size_hint_y=0.2))

        q_counter = 0
        ans_button = []
        for ques in dict['ques']:
            layout.add_widget(BoxLayout(size_hint_x=0.05))
            q_counter += 1
            if q_counter == 1:
                for ans in dict['ans']:
                    layout.add_widget(
                        Label(size_hint_x=0.1,
                              text=dict['ans'][ans],
                              font_name="fonts/the_font.ttf",
                              font_size=25,
                              halign='right',
                              color=[0,0,0,1]))
                layout.add_widget(
                    Label(text="תולאש",
                          font_name="fonts/the_font.ttf",
                          font_size=30,
                          halign='right', orientation='vertical',
                          color=[0,0,0,1]))
                layout.add_widget(BoxLayout(size_hint_x=0.1))

            for ans in dict['ans']:
                ab = AnswerButton(size_hint_x=0.15,
                                  text="", group=str(q_counter))
                ab.name = str(ques) + "," + str(ans)
                ab.question = ques
                ab.answer = ans
                ab.form = self
                self.ans_button.append(ab)
                layout.add_widget(ab)

            # CHECK ID AND KEEP THE CLICK VALUE
            layout.add_widget(
                Label(halign='right', text=dict['ques'][ques],
                      font_name="fonts/the_font.ttf", orientation='vertical',
                      font_size=25,
                      color=[0,0,0,1]))

        layoutup.add_widget(layout)
        layoutup.add_widget(BoxLayout())
        layoutbuttons = BoxLayout(size_hint_y=0.2)
        self.next_button = Button(on_press=self.next,
                                  background_color=(0, 0.71, 1., 1),
                                  background_normal="",
                                  size_hint_x=0.3,
                                  text=dict['next_button'],
                                  font_name="fonts/the_font",
                                  font_size=20,
                                  disabled=True)

        layoutbuttons.add_widget(BoxLayout(size_hint_x=0.2))
        layoutbuttons.add_widget(self.next_button)
        layoutbuttons.add_widget(BoxLayout())
        layoutbuttons.add_widget(BoxLayout(size_hint_x=0.7))

        layoutup.add_widget(layoutbuttons)
        layoutup.add_widget(BoxLayout(size_hint_y=0.1))
        self.add_widget(layoutup)

    def start(self):
        print("qf start")
        print(self.ans_button)
        for b in self.ans_button:
            b.active = False
        self.next_button.disabled = True

    def set_answer(self, question, answer):
        self.answers[question] = answer
        print(self.answers)
        all_answered = True
        for qk,qv in self.questions.items():
            if qk not in self.answers:
                all_answered = False
        if all_answered:
            self.next_button.disabled = False

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def next(self, pars):
        self.the_app.score.set_cei2(self.answers)
        self.the_app.sm.current = self.the_app.sm.next()
