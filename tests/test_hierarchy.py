from transforms.hierarchy import subsume, specify_animal, replace, _includes_or_plural
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
    dicts['replace'] = {'footwear': ['boots'], 'one eye closed': 'wink'}
    proc = replace(['brown footwear', 'boots', 'a long sentence about footwear', 'one eye closed'])
    assert 'brown boots' in proc
    assert 'a long sentence about footwear' in proc
    assert 'wink' in proc
    assert 'one eye closed' not in proc

def test_includes_or_plural():
    assert _includes_or_plural('starts', 'starts with') == True
    assert _includes_or_plural('with', 'ends with') == True
    assert _includes_or_plural('middle skipped', 'middle word skipped') == True