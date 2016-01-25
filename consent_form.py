from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.storage.jsonstore import JsonStore

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
            print(key, value)
            dict[key].text = value[::-1]

    def contin(self):
        if self.checkbox_agree.active:
            self.the_app.sm.current = self.the_app.sm.next()
        else:
            print("pls mark checkbox")

    def mark_checkbox(self):
        if self.checkbox_agree.active:
            self.button.background_color = self.get_color_from_hex("#FFFFFF")
        else:
            self.button.background_color = self.get_color_from_hex("#FFC0CB")

    def get_color_from_hex(self, color):
        return get_color_from_hex(color)

