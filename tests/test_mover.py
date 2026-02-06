import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from mover import Mover

@pytest.fixture
def mover():
    return Mover()

def test_move_file_success(mover):

    with patch('shutil.copy2') as mock_copy, \
         patch.object(Path, 'unlink') as mock_unlink, \
         patch.object(Path, 'exists') as mock_exists:

        mock_exists.side_effect = [False, True]
        
        src = Path("downloads/test.txt")
        targets = ["/documents"]
        
        mover.move(src, targets, "test.txt")
        
        mock_copy.assert_called_once()
        mock_unlink.assert_called_once() 

def test_move_with_duplicate_name(mover):

    with patch.object(Path, 'exists') as mock_exists, \
         patch('shutil.copy2') as mock_copy, \
         patch.object(Path, 'unlink'):
        

        mock_exists.side_effect = [True, False, True]
        
        mover.move(Path("src.txt"), ["/dest"], "test.txt")
        

        args, _ = mock_copy.call_args
        assert "test_1.txt" in str(args[1])