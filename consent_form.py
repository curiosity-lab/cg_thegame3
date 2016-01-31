from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.storage.jsonstore import JsonStore
from hebrew_management import HebrewManagement

class ConsentForm(BoxLayout):
    title=ObjectProperty()
    body=ObjectProperty()
    checkbox_agree=ObjectProperty()
    checkbox_txt=ObjectProperty()
    button=ObjectProperty()
    the_app = None

    def __init__(self, the_app):
        super(ConsentForm, self).__init__()
        self.the_app = the_app

        dict = {'title':self.title,
                'body':self.body,
                'checkbox_txt':self.checkbox_txt,
                'button':self.button}
        store = JsonStore('consent_form.json').get('agreement')
        for key, value in store.items():
            dict[key].text = value[::-1]
        txt = dict['body'].text
        new_lines = HebrewManagement.multiline(txt, 50)
        for nl in new_lines[::-1]:
            l = Label(text=nl,
                      font_name="fonts/the_font",
                      font_size=30,
                      orientation='vertical',
                      halign='right',
                      color=[0,0,0,1], size_hint_y=0.5)
            #l.bind(texture_size=l.setter('size'))
            dict['body'].add_widget(l)
            dict['body'].add_widget(BoxLayout(size_hint_y=0.2))
        self.start(the_app)

    def start(self, the_app):
        self.checkbox_agree.active = False
        self.button.background_color = (0, 0.71, 1, 1)

    def contin(self):
        if self.checkbox_agree.active:
            self.the_app.sm.current = self.the_app.sm.next()
        else:
            print("pls mark checkbox")

    def mark_checkbox(self):
        if self.checkbox_agree.active:
            self.button.background_color = (0.71, 0, 1., 1)
        else:
            self.button.background_color = (0, 0, 0.5, 1)

    def get_color_from_hex(self, color):
        return get_color_from_hex(color)

