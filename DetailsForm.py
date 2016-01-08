from kivy.graphics import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.storage.jsonstore import JsonStore
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner


class DetailsForm(BoxLayout):
    details = {}

    def __init__(self):
        super(DetailsForm, self).__init__()
        with self.canvas.before:
            self.rect = Rectangle(source='back2.png')
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
                        dict[key][kqa]={}
                        for k,v in value[kqa].items():
                           dict[key][kqa][k]= v
                    else:
                        dict[key][kqa]=[]
                        age=10
                        while age<100:
                            dict[key][kqa].append(str(age))
                            age+=1



        layout = GridLayout(cols=5, rows=7)
        layoutup = BoxLayout(orientation='vertical')
        layoutup.add_widget(
             Label(text=dict['details_title'], font_size=50, font_name="DejaVuSans.ttf", halign='right', size_hint_y=0.2,
                   color=[1, 0, 1, 1]))
        layoutup.add_widget(BoxLayout(size_hint_y=0.2))
        layout.add_widget(BoxLayout(size_hint_y=0.2))
        layout.add_widget(TextInput(size_hint_x=0.5))
        layout.add_widget(
            Label(text=dict['LastName'], font_size=20, font_name="DejaVuSans.ttf", halign='right', size_hint_y=0.2,
                   color=[1, 0, 1, 1]))
        layout.add_widget(TextInput(size_hint_x=0.5))
        layout.add_widget(
            Label(text=dict['FirstName'], font_size=20, font_name="DejaVuSans.ttf", halign='right', size_hint_y=0.2,
                   color=[1, 0, 1, 1]))
        layout.add_widget(BoxLayout())
        spinner = Spinner(
        text="Choose Gender",
        values=dict['Gender']['Genders'],
        size=(50, 50) )
        layout.add_widget(spinner)
        layout.add_widget(
            Label(text=dict['Gender']['text'], font_size=20, font_name="DejaVuSans.ttf", halign='right', size_hint_y=0.2,
                   color=[1, 0, 1, 1]))
        spinner = Spinner(
        text="Choose Age",
        values=dict['Age']['ages'])
        layout.add_widget(spinner)
        layout.add_widget(
            Label(text=dict['Age']['text'], font_size=20, font_name="DejaVuSans.ttf", halign='right', size_hint_y=0.2,
                   color=[1, 0, 1, 1]))
        layout.add_widget(BoxLayout(size_hint_x=0.2))
        layout.add_widget(TextInput(size_hint_x=2))
        layout.add_widget(
            Label(text=dict['Email'], font_size=20, font_name="DejaVuSans.ttf", halign='right',
                   color=[1, 0, 1, 1]))
        layout.add_widget(BoxLayout(size_hint_x=0.2))
        layout.add_widget(BoxLayout(size_hint_x=0.2))
        layout.add_widget(BoxLayout())
        spinner = Spinner(
        text="Choose Faculty",
        values=dict['Faculty']['Faculties'],
        size=(50, 50) )
        layout.add_widget(spinner)
        layout.add_widget(
            Label(text=dict['Faculty']['text'], font_size=20, font_name="DejaVuSans.ttf", halign='right', size_hint_x=1.5,
                   color=[1, 0, 1, 1]))
        layout.add_widget(BoxLayout())
        layout.add_widget(BoxLayout())
        layout.add_widget(Button(background_color=[1, 0, 1, 1],
                                 text=dict['end_button'], font_size=20, font_name="DejaVuSans.ttf",
                                 halign='right'))
        layout.add_widget(BoxLayout())
        layout.add_widget(BoxLayout())
        layout.add_widget(
            Label(text="Thanks from participating!", font_size=20, font_name="DejaVuSans.ttf", halign='right', size_hint_x=1.5))
        layoutup.add_widget(layout)

        self.add_widget(layoutup)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size