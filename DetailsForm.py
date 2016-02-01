#!/usr/bin/python
# -*- coding: utf-8 -*-

from kivy.graphics import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.storage.jsonstore import JsonStore
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy_logger import *

class MySpinnerOption(SpinnerOption):
    pass


class MySpinner(WidgetLogger, Spinner):
    pass

class HebrewText(WidgetLogger, TextInput):
    the_text = ''


class DetailsForm(BoxLayout):
    details = {}
    the_app = None
    age_spinner = None
    faculty_spinner = None
    gender_spinner = None
    last_name_text = None
    first_name_text = None
    email_text = None

    def __init__(self, the_app):
        super(DetailsForm, self).__init__()
        self.the_app = the_app

        with self.canvas.before:
            self.rect = Rectangle(source='back3.png')
            self.bind(size=self._update_rect, pos=self._update_rect)

        dict = {}
        self.answers = {}
        store = JsonStore('details.json').get('details')

        for key, value in store.items():
            if key in ['FirstName', 'LastName', 'Email', 'end_button','details_title']:
                dict[key] = value[::-1]
            if key in ['Gender','Faculty','Age']:
                dict[key] = {}
                for kqa, qa in value.items():
                    if kqa=='text':
                        dict[key][kqa] = qa[::-1]
                    elif kqa != 'ages':
                        dict[key][kqa]=[]
                        for k,v in value[kqa].items():
                           dict[key][kqa].append(v[::-1])
                    else:
                        dict[key][kqa]=[]
                        age=10
                        while age<100:
                            dict[key][kqa].append(str(age))
                            age += 1

        layout = GridLayout(cols=5, rows=7)
        layoutup = BoxLayout(orientation='vertical')
        layoutup.add_widget(BoxLayout(size_hint_y=0.3))
        layoutup.add_widget(
             Label(text=dict['details_title'], 
                   font_size=50, font_name="fonts/the_font.ttf",
                   halign='right', size_hint_y=0.2,
                   color=[0,0,0,1]))
        layout.add_widget(BoxLayout(size_hint_y=0.2))

        self.last_name_text = HebrewText(size_hint_x=0.5,
                                    multiline=False,
                                    font_name="fonts/the_font.ttf",
                                    font_size=30)
        self.last_name_text.name = 'last_name'
        self.last_name_text.bind(text=self.justify_hebrew)
        layout.add_widget(self.last_name_text)

        layout.add_widget(
            Label(text=dict['LastName'], font_size=30,
                  font_name="fonts/the_font.ttf",
                  halign='right', size_hint_y=0.2,
                  color=[0,0,0,1]))

        self.first_name_text = HebrewText(size_hint_x=0.5,
                                     multiline=False,
                                     font_name="fonts/the_font.ttf",
                                     font_size=30)
        self.first_name_text.name = 'first_name'
        self.first_name_text.bind(text=self.justify_hebrew)
        layout.add_widget(self.first_name_text)

        layout.add_widget(
            Label(text=dict['FirstName'], font_size=30,
                  font_name="fonts/the_font.ttf", halign='right',
                  size_hint_y=0.2,
                  color=[0,0,0,1]))
        layout.add_widget(BoxLayout())

        # gender spinner
        self.gender_spinner = MySpinner(text="רכז",
                                        values=dict['Gender']['Genders'],
                                        size=(50, 50), font_name="fonts/the_font.ttf",
                                        font_size=30,
                                        option_cls = MySpinnerOption)
        self.gender_spinner.name = 'gender'
        self.gender_spinner.bind(text=self.gender_spinner.on_spinner_text)
        layout.add_widget(self.gender_spinner)

        layout.add_widget(
            Label(text=dict['Gender']['text'], font_size=30,
                  font_name="fonts/the_font.ttf", halign='right',
                  size_hint_y=0.2,
                  color=[0,0,0,1]))

        # age spinner
        self.age_spinner = MySpinner(
            text="20",
            values=dict['Age']['ages'],
            font_name="fonts/the_font.ttf",
            font_size=30,
            option_cls = MySpinnerOption)
        self.age_spinner.name = 'age'
        self.age_spinner.bind(text=self.age_spinner.on_spinner_text)
        layout.add_widget(self.age_spinner)

        layout.add_widget(
            Label(text=dict['Age']['text'],
                  font_size=30, font_name="fonts/the_font.ttf",
                  halign='right', size_hint_y=0.2,
                  color=[0,0,0,1]))
        layout.add_widget(BoxLayout(size_hint_x=0.2))
        self.email_text = TextInput(size_hint_x=2)
        layout.add_widget(self.email_text)
        layout.add_widget(
            Label(text=dict['Email'], font_size=30,
                  font_name="fonts/the_font.ttf", halign='right',
                  color=[0,0,0,1]))
        layout.add_widget(BoxLayout(size_hint_x=0.2))
        layout.add_widget(BoxLayout(size_hint_x=0.2))
        layout.add_widget(BoxLayout())

        # faculty spinner
        self.faculty_spinner = MySpinner(text="הסדנה",
                                         values=dict['Faculty']['Faculties'],
                                         size=(50, 50),
                                         font_name="fonts/the_font.ttf",
                                         font_size=30,
                                         option_cls = MySpinnerOption)
        self.faculty_spinner.name = 'faculty'
        self.faculty_spinner.bind(text=self.faculty_spinner.on_spinner_text)
        layout.add_widget(self.faculty_spinner)

        layout.add_widget(
            Label(text=dict['Faculty']['text'],
                  font_size=30, font_name="fonts/the_font.ttf",
                  halign='right', size_hint_x=1.5,
                  color=[0,0,0,1]))
        layout.add_widget(BoxLayout())
        layout.add_widget(BoxLayout())

        end_button = Button(background_color=[0,0.71,1,1],
                            background_normal="",
                            text=dict['end_button'], font_size=30,
                            font_name="fonts/the_font.ttf",
                            halign='right',on_press=self.next)
        end_button.bind(on_press=self.save)
        layout.add_widget(end_button)
        layout.add_widget(BoxLayout())
        layout.add_widget(BoxLayout())
        layout.add_widget(
            Label(text="ךתופתתשה לע הדות", font_size=40,
                  color=[0,0,0,1],
                  font_name="fonts/the_font.ttf", halign='right', size_hint_x=1.5))
        layoutup.add_widget(layout)

        self.add_widget(layoutup)
        self.start()

    def start(self):
        self.first_name_text.text = ""
        self.last_name_text.text = ""
        self.email_text.text = ""
        self.faculty_spinner.text = self.faculty_spinner.values[0]
        self.gender_spinner.text = self.gender_spinner.values[0]
        self.age_spinner.text = "20"

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def justify_hebrew(self, instance, value):
        print("justify hebrew", instance, value)
        if len(value) > 0:
            if len(instance.the_text) != len(value):
                instance.the_text = value
                instance.text = value[-1] + instance.the_text[:-1]

    def save(self, instance):
        details = {'age': self.age_spinner.text,
                   'gender': self.gender_spinner.text,
                   'faculty': self.faculty_spinner.text}
        self.the_app.score.add_details(details)

    def next(self, pars):
        self.the_app.sm.current = self.the_app.sm.next()