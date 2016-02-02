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


class Learning():
    the_app = None

    def __init__(self, the_app):
        self.the_app = the_app


class LearningForm(BoxLayout):
    answers = {}

    def __init__(self, app, questions):
        super(LearningForm, self).__init__()
        self.the_app = app
        with self.canvas.before:
            self.rect = Rectangle(source='back4.png')
            self.bind(size=self._update_rect, pos=self._update_rect)

        layoutup = BoxLayout(orientation='vertical')
        layoutup.add_widget(BoxLayout(size_hint_y=0.7))
        layoutup.add_widget(
            Label(text=u"מה למדת?",
                  font_size=50, font_name="fonts/the_font.ttf",
                  halign='right', size_hint_y=0.4,size_hint_x=1.5,
                  color=[0,0,0,1]))
        layoutup.add_widget(BoxLayout(size_hint_y=0.1))
        layoutup.add_widget(
            Label(text=u"ענה על השאלות הבאות לפי מה ששמעת.",
                  font_name="fonts/the_font.ttf", font_size=36, halign='right',
                  size_hint_y=0.15,
                  color=[0,0,0,1]))
        layoutup.add_widget(BoxLayout(size_hint_y=0.2))

        for q in questions:
            q_layout = BoxLayout()
            q_layout.add_widget(Label(text=q['question']['text'],
                  font_size=40, font_name="fonts/the_font.ttf",
                  halign='right', size_hint_y=0.4,size_hint_x=1.5,
                  color=[0,0,0,1]))
            q_layout.add_widget(BoxLayout(size_hint_x=0.2))
            layoutup.add_widget(q_layout)

            for a in q['answers']:
                q_layout = BoxLayout()
                q_layout.add_widget(Label(text=a['text'],
                      font_size=32, font_name="fonts/the_font.ttf",
                      halign='right', size_hint_y=0.4,size_hint_x=1.5,
                      color=[0,0,0,1]))
                self.answers = AnswerButton()
                q_layout.add_widget(BoxLayout(size_hint_x=0.2))
                layoutup.add_widget(q_layout)
