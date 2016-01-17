from datetime import datetime
from kivy.storage.jsonstore import JsonStore
from math import log

class CuriosityScore:
    id = ''
    game_sequence = []
    cei2 = {}
    max_duration = 0
    num_options = 0
    score = {}
    pathname = ''

    def __init__(self, max_duration, num_options, pathname):
        self.max_duration = max_duration
        self.num_options = num_options
        self.pathname = pathname + '/'
        self.id = datetime.now()
        self.game_sequence = []
        self.cei2 = {}

    def add_game_item_begin(self, item):
        self.game_sequence.append([item, datetime.now()])

    def add_game_item_end(self, item):
        for i in self.game_sequence:
            if i[0] == item and len(i) == 2:
                i.append(datetime.now())
                i.append((i[2]-i[1]).seconds)
                i.append(i[3] / self.max_duration)
        self.calculate_score()

    def set_cei2(self, ans):
        self.cei2 = {}
        for k,v in ans.items():
            self.cei2[k] = v
        self.calculate_score()

    def print(self):
        for i in self.game_sequence:
            print(i[0], i[3], i[4])
        print(self.cei2)


    def calculate_score(self):
        # total listening time
        total_info = 0
        for i in self.game_sequence:
            total_info += i[4]
        self.score['total_info'] = total_info

        # multi-disciplinary, entropy
        multidisciplinary = 0
        if total_info > 0:
            prob = {}
            for i in self.game_sequence:
                if i[0] not in prob:
                    prob[i[0]] = i[4]
                else:
                    prob[i[0]] += i[4]
            for pk, pv in prob.items():
                p = pv / total_info
                multidisciplinary += p * log(p,2)
        self.score['multi'] = -multidisciplinary / log(self.num_options, 2)

        # cei2
        stretching = 0
        embracing = 0
        for ck, cv in self.cei2.items():
            if ck in ['q01', 'q03', 'q05', 'q07', 'q09']:
                stretching += int(cv[3])
            else:
                embracing += int(cv[3])
        self.score['stretching'] = stretching
        self.score['embracing'] = embracing

        self.save()

    def save(self):
        print(self.pathname)
        store = JsonStore(self.pathname + 'CuriosityScore.txt')
        store.put(self.id.strftime('%Y_%m_%d_%H_%M_%S_%f'),
                  total=self.score['total_info'],
                  multi=self.score['multi'],
                  stretching=self.score['stretching'],
                  embracing=self.score['embracing'])





