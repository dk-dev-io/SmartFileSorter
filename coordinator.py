from pathlib import Path
from watchdog.observers import Observer as WatchdogLib
from watchdog.events import FileSystemEventHandler

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, sorter, queue, ignore_set):
        self.sorter = sorter
        self.queue = queue
        self.ignore_set = ignore_set

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path)
        file_name = file_path.name

        if file_name in self.ignore_set:
            return
            
        target_paths = self.sorter.get_path(file_name)

        if target_paths:
            self.queue.put((file_path, target_paths, file_name))
        else:
            self.ignore_set.add(file_name)


class Coordinator:
    def __init__(self, sources, sorter, queue, ignore_set):
        self.observer = WatchdogLib()
        self.sources = sources
        self.handler = FileEventHandler(sorter, queue, ignore_set)

    def start(self):
        for folder in self.sources:
            path = Path(folder)
            if not path.exists():
                try:
                    path.mkdir(parents=True, exist_ok=True)
                except OSError:
                    continue
            

            self.observer.schedule(self.handler, str(path), recursive=False)
        
        self.observer.start()

    def stop(self):
        self.observer.stop()

    def join(self):
        self.observer.join()