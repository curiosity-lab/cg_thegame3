#!/usr/bin/kivy
# -*- coding: utf-8 -*-

import kivy
kivy.require('1.0.6')

from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout
from functools import partial
from kivy.storage.jsonstore import JsonStore
from kivy.graphics import Rectangle
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy_logger import *
from hebrew_management import HebrewManagement


class Item(Scatter, WidgetLogger):
    item_lbl = ObjectProperty(None)
    source = StringProperty()
    img = {}
    info = {}
    current = 1
    cg = None
    base_pos = None
    question = {}

    def change_img(self, im = '1'):
        if im in self.img:
            self.source = self.img[im]

    def on_transform_with_touch(self, touch):
        if self.collide_point(*touch.pos):
            self.play()

    def play(self):
        # if still has something to play
        if self.current in self.info:
            if 'audio' in self.info[self.current]:
                # if not playing
                if not self.cg.is_playing:
                    self.info[self.current]['audio'].play()

    def on_play(self):
        super(Item, self).on_play_wl(self.info[self.current]['audio'].source)
        self.cg.is_playing = True
        self.change_img('2')

    def on_stop(self):
        super(Item, self).on_stop_wl(self.info[self.current]['audio'].source)
        self.cg.is_playing = False
        self.current += 1
        CuriosityGame.current += 1
        self.change_img('1')

    def get_text(self):
        # if still has text
        if self.current in self.info:
            if 'text' in self.info[self.current]:
                return self.info[self.current]['text'][::-1]
        return None


class CuriosityGame:
    items = {}
    current = 0
    the_app = None
    the_widget = None
    is_playing = False
    the_end = False
    game_duration = 15

    def __init__(self, parent_app):
        self.the_app = parent_app
        self.the_widget = CuriosityWidget()

        # initialize items
        items_path = 'items/'

        items_json = JsonStore(items_path + 'items.json')
        items_list = items_json.get('list')

        for name, value in items_list.items():
            self.items[name] = Item(do_rotation=False, do_scale=False)
            self.items[name].name = name
            self.items[name].cg = self

            if 'label' in value:
                self.items[name].item_lbl.text = value['label'][::-1]

            if 'pos' in value:
                self.items[name].base_pos = (int(value['pos']['x']), int(value['pos']['y']))

            self.items[name].img = {}
            if 'img' in value:
                for ki, i in value['img'].items():
                    self.items[name].img[ki] = items_path + i
                self.items[name].change_img('1')

            self.items[name].info = {}
            if 'text' in value:
                for kt, t in value['text'].items():
                    self.items[name].info[int(kt)] = {'text': t['text']}
                    try:
                        self.items[name].info[int(kt)]['audio'] = SoundLoader.load(items_path + t['audio'])
                        self.items[name].info[int(kt)]['audio'].bind(
                                on_play=partial(self.on_play, name))
                        self.items[name].info[int(kt)]['audio'].bind(
                                on_stop=partial(self.on_stop, name))
                    except:
                        if 'audio' in t:
                            Logger.info('audio: cant find ' + items_path + t['audio'])
                    if 'question' in t:
                        self.items[name].question = {}
                        self.items[name].question = t['question']

        # set widgets
        for key, value in self.items.items():
            self.the_widget.add_widget(value)

    def start(self):
        # set the timer of the game
        print('Starting clock...')
        Clock.schedule_once(self.end_game, self.game_duration)
        for k,v in self.items.items():
            v.current = 1
            v.pos = v.base_pos
        self.the_end = False
        self.is_playing = False
        self.the_app.score.start_game()


    def on_play(self, name, par):
        self.items[name].on_play()
        text = self.items[name].get_text()
        if text:
            self.show_text(text)
        self.the_app.score.add_game_item_begin(name)

    def on_stop(self, name, par):
        self.items[name].on_stop()
        self.show_text("")
        self.the_app.score.add_game_item_end(name)
        if self.the_end:
            self.end_game(0.5)

    def show_text(self, text):
        if len(text) > 0:
            new_lines = HebrewManagement.multiline(text, 75)
            for nl in range(0, len(new_lines)):
                self.the_widget.cg_lbl[nl].text = new_lines[nl]
        else:
            for l in self.the_widget.cg_lbl:
                l.text = ''

    def end_game(self, dt):
        self.the_end = True
        if not self.is_playing:
            self.the_app.sm.current = self.the_app.sm.next()


class CuriosityWidget(FloatLayout):
    cg_lbl = None

    def __init__(self):
        super(CuriosityWidget, self).__init__()
        with self.canvas.before:
            self.rect = Rectangle(source='cg_background_img.jpg')
            self.bind(size=self._update_rect, pos=self._update_rect)
        self.cg_lbl = []
        for k in range(0,3):
            self.cg_lbl.append(Label(font_name='fonts/the_font.ttf', halign='right', text='',
                            pos=(10, 10 + 30 * k), font_size='24sp', size_hint_y=0.1, color=[0,0.1,1.0,0.5]))
            self.add_widget(self.cg_lbl[-1])

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
