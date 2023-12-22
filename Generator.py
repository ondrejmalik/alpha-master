import random
import time

from Permutator import HeapPermutationGenerator


class Generator:
    def __init__(self, rozvrh, shared_count, shared_queue, shared_queue_generated):
        self.multiple_hour = []
        self.rozvrh = self.convert_to_ids(rozvrh)
        self.shared_count = shared_count
        self.unique = set()
        self.queue = shared_queue
        self.batch_size = 1_00_000
        self.shared_queue_generated = shared_queue_generated

    def generate(self):
        permutations_instance = HeapPermutationGenerator(self.rozvrh)
        while True:
            start = time.time()
            while len(self.unique) < self.batch_size:
                self.unique.add(tuple(next(permutations_instance)))
                self.shared_count.value = len(self.unique)
            self.queue.put(self.unique)
            self.shared_queue_generated.value += 1
            end = time.time()
            print(f"generated in {end - start} seconds")
            time.sleep(5)
            self.unique = set()

    def generate_random_schedule(self):
        schedule = self.rozvrh[:]
        random.shuffle(schedule)
        return schedule

    def generateRandomly(self):
        while True:
            start = time.time()
            while len(self.unique) < self.batch_size:
                self.unique.add(tuple(self.generate_random_schedule()))
                self.shared_count.value = len(self.unique)
            self.queue.put(self.unique)
            self.shared_queue_generated.value += 1
            end = time.time()
            print(f"generated in {end - start} seconds")
            # time.sleep(5)
            self.unique = set()

    def convert_to_ids(self, rozvrh):
        id_dict = {}
        id_list = []
        current_id = 0
        for item in rozvrh:
            if item is not None:
                if item not in id_dict:
                    id_dict[item] = bytes([current_id])
                    if item.getis_multiple_hour():
                        self.multiple_hour.append(bytes([current_id]))
                current_id += 1
                id_list.append(id_dict[item])
            else:
                id_list.append(None)
        self.subjects = id_dict
        return id_list
