import os
import random

from main import read_tags_from_file


def test_read_tags_from_file():
    test_file_name = 'test'+str(random.random())+'.txt'
    with open(test_file_name, "w", encoding="utf-8") as f:
      f.write(' CAPS , Shift,no_spa_ce  ,etc,,')

    tags = read_tags_from_file(test_file_name)
    os.remove(test_file_name)
    assert 'caps, etc, no spa ce, shift' == ', '.join(tags)
