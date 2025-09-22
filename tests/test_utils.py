import os
import pathlib
import random

from utils import dicts, load_yaml_config, is_solo


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
