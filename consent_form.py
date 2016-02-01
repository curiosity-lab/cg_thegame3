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
    dict = None
    body_labels = None

    def __init__(self, the_app):
        super(ConsentForm, self).__init__()
        self.the_app = the_app
        self.dict = {'title':self.title,
                'body':self.body,
                'checkbox_txt':self.checkbox_txt,
                'button':self.button}
        store = JsonStore('consent_form.json').get('agreement')
        for key, value in store.items():
            self.dict[key].text = value[::-1]

        self.body_labels = []
        txt = self.dict['body'].text
        new_lines = HebrewManagement.multiline(txt, 50)
        for nl in new_lines[::-1]:
            self.body_labels.append(Label(text=nl,
                      font_name="fonts/the_font",
                      font_size=36,
                      color=[0,0,0,1]))
            self.dict['body'].add_widget(self.body_labels[-1])

    def start(self, the_app):
        self.checkbox_agree.active = False
        self.button.background_color = (0, 0.71, 1, 1)

    def contin(self):
        if self.checkbox_agree.active:
            # the next screen is the game
            # start the clock and then transition
            self.the_app.cg.start()
            self.the_app.sm.current = "thegame"
        else:
            print("pls mark checkbox")

    def mark_checkbox(self):
        if self.checkbox_agree.active:
            self.button.background_color = (0.71, 0, 1., 1)
        else:
            self.button.background_color = (0, 0, 0.5, 1)

    def get_color_from_hex(self, color):
        return get_color_from_hex(color)

