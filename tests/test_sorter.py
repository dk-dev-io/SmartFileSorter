import pytest
from sorter import FileSorter


@pytest.fixture
def sorter():
    test_rules = {
        ".jpg": ["/images"],
        ".png": ["/images"]
    }
    return FileSorter(test_rules)

@pytest.mark.parametrize("filename, expected", [
    ("cat.jpg", ["/images"]),
    ("DOG.PNG", ["/images"]),
    ("file.exe", []),
    ("README", []) 
])
def test_logic(sorter, filename, expected):
    assert sorter.get_path(filename) == expected