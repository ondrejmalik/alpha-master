import copy
import multiprocessing
import time


class Watchdog:
    def __init__(self,sharedcounts,shared_queue_generated_count,shared_queue_completed_count,shared_best_queue):
        self.shared_counts = sharedcounts
        self.shared_queue_generated_count = shared_queue_generated_count
        self.shared_queue_completed_count = shared_queue_completed_count
        self.shared_best_queue = shared_best_queue
    def run(self):
        for i in range(1, 5):  # 3 min timer
            time.sleep(5)
            total = 0
            print()
            for shared_count in self.shared_counts:
                print(f'shared counts {shared_count.value}', end=" ")
                total += shared_count.value
            print()
            print(f'Batches generated {self.shared_queue_generated_count.value}', end=", ")
            print(f'batches evaluated {self.shared_queue_completed_count.value}')
            if self.shared_queue_completed_count.value + 5 < self.shared_queue_generated_count.value:
                print(f'Recommendation: increase the number of evaluator processes {int(self.shared_queue_generated_count.value / self.shared_queue_completed_count.value + 0.01)} times')
            elif self.shared_queue_completed_count.value + 3 >= self.shared_queue_generated_count.value:
                print(f'Recommendation: increase the number of generator processes')
            print(f"unique schedules in {str(i * 5)} seconds")
        # ----------------get best from queue----------------
        print('-----------------------------Results-----------------------------')
        print()
        self.shared_best_queue.put(None)
        best = None
        while True:
            tmp = self.shared_best_queue.get()
            if tmp is None:
                break
            elif best is None:
                best = tmp
            elif tmp[1] > best[1]:
                best = tmp
        for i, item in enumerate(best[0]):
            print(item, end=f"; {i} ")
            if i != 0 and i % 10 == 0:
                print()
        print()
        print(f'with {best[1]} points')

