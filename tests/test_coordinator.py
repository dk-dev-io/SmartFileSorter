import pytest
from unittest.mock import MagicMock
from pathlib import Path
from queue import Queue
from coordinator import FileEventHandler

@pytest.fixture
def setup_handler():
    mock_sorter = MagicMock()
    queue = Queue()
    ignore_set = {"ignored.txt"}
    handler = FileEventHandler(mock_sorter, queue, ignore_set)
    return handler, mock_sorter, queue

def test_on_created_adds_to_queue(setup_handler):
    handler, mock_sorter, queue = setup_handler
    mock_sorter.get_path.return_value = ["/target"]
    

    event = MagicMock()
    event.is_directory = False
    event.src_path = "downloads/new_file.png"
    
    handler.on_created(event)
    

    assert queue.qsize() == 1
    src, targets, name = queue.get()
    assert name == "new_file.png"

def test_on_created_ignores_file(setup_handler):
    handler, _, queue = setup_handler
    
    event = MagicMock()
    event.is_directory = False
    event.src_path = "downloads/ignored.txt"
    
    handler.on_created(event)
    
    assert queue.empty()