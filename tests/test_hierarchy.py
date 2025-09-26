from transforms.hierarchy import subsume, specify_animal, replace
from utils import dicts

def test_subsume():
    processed = subsume(['noun', 'adjective noun', 'word postfix', 'word', 'series', 'series 2'])
    assert "adjective noun" in processed
    assert "word postfix" in processed
    assert "noun" not in processed
    assert "word" not in processed
    assert "series" in processed

def test_specify_animal():
    dicts['animals'] = ['cat','dog']
    processed = specify_animal(['animal ears', 'cat ears', 'animal tail', 'long tail', 'animal paws'])
    assert "cat ears" in processed
    assert "animal tail" in processed
    assert "long tail" in processed
    assert "animal paws" in processed
    assert "animal ears" not in processed


def test_replace():
    dicts['replace'] = {'footwear': ['boots']}
    proc = replace(['brown footwear', 'boots', 'a long sentence about footwear'])
    assert 'brown boots' in proc
    assert 'a long sentence about footwear' in proc
