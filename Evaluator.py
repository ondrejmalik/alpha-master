import time

from Lesson import Lesson
from collections import Counter


class Evaluator:
    def __init__(self, shared_queue, subjects, multiple_hour, shared_queue_completed_count,shared_best_queue):
        self.shared_queue = shared_queue
        self.subjects = subjects
        self.subjects_reverse_mapping = self.build_reverse_mapping(subjects)
        self.best = None
        self.best_points = -1000000
        self.worst_points = 0
        self.allowed_duplicates = multiple_hour
        self.shared_queue_completed_count = shared_queue_completed_count
        self.shared_best_queue = shared_best_queue
    def build_reverse_mapping(self,dict):  # Chat-GPT prompt - how do you get key from value python dictionary
        return {value: key for key, value in dict.items()}

    def convert_subjects_to_ids(self, subjects):
        id_list = []
        for i, item in enumerate(subjects):
            if item is not None:
                id_list.append(i)

    def evaluate(self):
        while True:
            data_list = self.shared_queue.get()
            start = time.time()
            for data in data_list:
                break_outer_loop = False
                if self.best is None:
                    self.best = data
                    continue
                week = [list(data[i:i + 10]) for i in range(0, 50, 10)]
                points = 0
                pocetHodinDene = 0
                for i, day in enumerate(week):
                    wasObed = False
                    lastSubject = None
                    if self.check_duplicity(day) == True:
                        points -= 100
                        break_outer_loop = True
                        break
                    else:
                        points += 10
                    for j, subject in enumerate(day):
                        # ----------------check room----------------------
                        if lastSubject is not None and subject is not None:
                            self.check_room(subject,lastSubject)
                            pocetHodinDene += 1
                        # ------------check prvni hodina-----------------
                        if j == 0:
                            points -= self.check_profile_lesson(subject)
                        # ----------------check oběd---------------------
                        if j == 5 or j == 6 or j == 7:  # 5.-6.-7.-8. hodina je oběd
                            if subject is None:
                                wasObed = True
                        if j == 8 and subject is not None and wasObed is False:
                            points -= 100
                            break_outer_loop = True
                            break
                        if j == 6 or j == 7 or j == 8 or j == 9:  # hodina po obědě nesmí být profilová
                            if lastSubject is None:
                                points -= self.check_profile_lesson(subject)
                        lastSubject = subject
                    # ----------------check pocet hodin----------------
                    if break_outer_loop:
                        break
                    if pocetHodinDene == 8:
                        points -= 5
                    elif pocetHodinDene == 9:
                        points -= 10
                    elif pocetHodinDene == 10:
                        points -= 100
                        break_outer_loop = True
                        break
                    pocetHodinDene = 0
                # -----------------set best set worst-----------------
                if points > self.best_points:
                    self.best = data
                    self.best_points = points
                if points < self.worst_points:
                    self.worst_points = points
            end = time.time()
            self.shared_queue_completed_count.value += 1
            self.evaluate_best()
            print()
            print('------------------------------------------')
            print(f"evaluated in {end - start} seconds", )
            print(f"best {self.best_points} points", end=" ")
            print(f"worst {self.worst_points} points")
            print('------------------------------------------')
            print()
    def evaluate_best(self):
        temp = [[],]
        for sub in self.best:
            if sub is None:
                temp[0].append(None)
            else:
                temp[0].append(self.subjects_reverse_mapping[sub])
        temp.append(self.best_points)
        self.shared_best_queue.put(temp)
    def check_duplicity(self, day):
        # kontrola duplicitních hodin kromě vícehodinovek
        points = 0
        is_duplicate = False
        count = Counter(day)
        unique_set = set()
        for sub in day:
            if sub not in unique_set:
                unique_set.add(sub)
                pass
            elif sub in self.allowed_duplicates:
                if day.count(sub) < 2:  # vícehodinovka musí být alespoň 2x
                    is_duplicate = True
            else:
                is_duplicate = True
        return is_duplicate

    def check_profile_lesson(self, subject):
        points = 0
        if subject is None:  #hodina je volna
            points += 20
        elif subject == self.subjects[Lesson("M", "Ng", 24, False)]:  # je matika
            points -= 10
        elif subject == self.subjects[Lesson("WA", "Pv", 17, True)]:  # je wap
            points -= 10
        elif subject == self.subjects[Lesson("WA", "Pv", 24, False)]:  # je wa
            points -= 10
        elif subject == self.subjects[Lesson("DS", "Ka", 24, False)]:  # je ds
            points -= 10
        elif subject == self.subjects[Lesson("DS", "Ka", 18, True)]:  # je dsp
            points -= 10
        elif subject == self.subjects[Lesson("PV", "Re", 24, False)]:  # je pv
            points -= 10
        elif subject == self.subjects[Lesson("PV", "Ma", 18, True)]:  # je pvp
            points -= 10
        return points
    def check_room(self,subject,last_subject):
        points = 0
        s = self.subjects_reverse_mapping[subject].room
        l = self.subjects_reverse_mapping[last_subject].room
        
        if s == l:# stejna trida
            points += 10
        #stejne patro
        elif s in range(1, 10) and l in range(1, 10):
            points += 10
        elif s in range(10, 20) and l in range(10, 20):
            points += 10
        elif s in range(20, 30) and l in range(20, 30):
            points += 10

        return self.subjects_reverse_mapping[subject]