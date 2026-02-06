import time
import threading
import yaml
from queue import Queue
from sorter import FileSorter, config_parsing
from mover import Mover
from coordinator import Coordinator

def load_ignore_config(path='ignore.yaml'):
    ign_set = set()
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if data and 'ignore' in data:
                for item in data['ignore']:
                    ign_set.add(item)
    except Exception:
        pass
    return ign_set

def worker(queue, mover):
    while True:
        src, targets, fname = queue.get()
        try:
            mover.move(src, targets, fname)
        except Exception:
            pass
        queue.task_done()

if __name__ == "__main__":
    try:
        rules, sources = config_parsing()
    except Exception:
        exit()

    if not sources:
        exit()

    initial_ignore = load_ignore_config()
    task_queue = Queue()
    
    my_sorter = FileSorter(rules)
    my_mover = Mover()
    

    my_coordinator = Coordinator(sources, my_sorter, task_queue, initial_ignore)

    worker_thread = threading.Thread(target=worker, args=(task_queue, my_mover), daemon=True)
    worker_thread.start()

    my_coordinator.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_coordinator.stop()
    
    my_coordinator.join()