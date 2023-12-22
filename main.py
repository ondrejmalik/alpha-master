import json
import multiprocessing


from Evaluator import Evaluator
from Lesson import Lesson
from Generator import Generator
from Watchdog import Watchdog

if __name__ == "__main__":
    shared_batch_queue = multiprocessing.Queue()
    shared_best_queue = multiprocessing.Queue()
    shared_queue_completed_count = multiprocessing.Value('i', 0)
    shared_queue_generated_count = multiprocessing.Value('i', 0)
    try:
        rozvrh = json.loads(open("input.json", "r").read(), object_hook=lambda d: Lesson(**d))
    except:
        print("Error loading input the file")
        exit()
    mode = input("Method: Random(1) or Permutation(2)?")
    generator_processes = []
    evaluator_processes = []
    shared_counts = []
    subjects = {}
    multiple_hour = []
    if (mode == "1"):
        process_count = input("How many generator processes?")
        for p in range(int(process_count)):
            shared_counts.append(multiprocessing.Value('i', 0))
            generator = Generator(rozvrh, shared_counts[len(shared_counts) - 1], shared_batch_queue, shared_queue_generated_count)
            generator_processes.append(multiprocessing.Process(target=generator.generateRandomly))
        for p in generator_processes:
            p.start()
    elif (mode == "2"):
        shared_counts.append(multiprocessing.Value('i', 0))
        shared_counts.append(multiprocessing.Value('i', 0))
        generator = Generator(rozvrh, shared_counts[len(shared_counts) - 1], shared_batch_queue, shared_queue_generated_count)
        generator_processes.append(multiprocessing.Process(target=generator.generate))
        r2 = rozvrh[::-1]
        generator = Generator(r2, shared_counts[len(shared_counts) - 1], shared_batch_queue)
        generator_processes.append(multiprocessing.Process(target=generator.generate))
        for p in generator_processes:
            p.start()
    subjects = generator.subjects
    multiple_hour = generator.multiple_hour
    process_count = input("How many evaluator processes?")
    for p in range(int(process_count)):
        e = Evaluator(shared_batch_queue, subjects, multiple_hour, shared_queue_completed_count, shared_best_queue)
        evaluator_processes.append(multiprocessing.Process(target=e.evaluate))
    for p in evaluator_processes:
        p.start()
    print('Running...')
    active = multiprocessing.active_children()
    w = Watchdog(shared_counts,shared_queue_generated_count,shared_queue_completed_count,shared_best_queue)
    wp = multiprocessing.Process(target=w.run)
    wp.start()
    wp.join()
    for p in active:
        p.terminate()
