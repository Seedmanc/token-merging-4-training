import os
import pathlib
import random

from utils import dicts, load_yaml_config, is_solo, get_series_candidates, part_of


def test_load_yaml_config():
    test_file_name = 'test'+str(random.random())
    ROOT = pathlib.Path(__file__).resolve().parent.parent
    with open(str(ROOT)+'/config/' +test_file_name+'.yaml', "w", encoding="utf-8") as f:
        f.write('- elem1\n'
                '- elem2')
    load_yaml_config(test_file_name)
    assert 'elem1' in dicts[test_file_name]
    assert dicts[test_file_name][1] == 'elem2'
    os.remove(str(ROOT)+'/config/' +test_file_name+'.yaml')

def test_is_solo():
    assert is_solo(['solo']) == True
    assert is_solo(['1girl']) == True
    assert is_solo(['2girls']) == False
    assert is_solo(['1girl','1other']) == False
    assert is_solo(['serval (kemono friends)', 'kemono friends', 'kaban (kemono friends)']) == False

def test_series_candidates():
    processed = get_series_candidates(['serval (kemono friends)', 'kemono friends', 'character (missing series)'])
    assert 'kemono friends' in processed
    assert 'missing series' not in processed

def test_part_of():
    assert part_of('word', 'and word') == True
    assert part_of('word', 'more,words') == True
    assert part_of('word', 'subword') == False