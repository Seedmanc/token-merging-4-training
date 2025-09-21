from transforms.redundancy import merge, multicolor, omit_parts, andjoin
from utils import  dicts

def test_merge():
    processed = merge(['long hair', 'white hair', 'very short hair'])
    assert "long white hair" in processed
    assert "long hair" not in processed
    assert "white hair" not in processed
    assert "very short hair" in processed

def test_multicolor():
    dicts['colors'] = ['white','red']
    processed = multicolor(['red hair', 'white hair','multicolored hair', 'black skirt', 'other skirt'])
    assert 'red hair' not in processed
    assert 'white hair' not in processed
    assert 'multicolored hair' in processed
    assert 'black skirt' in processed
    assert 'other skirt' in processed

def test_omit_parts():
    dicts['animals'] = ['cat','dog']
    processed = omit_parts(['cat girl', 'cat tail', 'dog ears', 'other girl', 'other part'])
    assert 'cat tail' not in processed
    assert 'dog ears' in processed
    assert 'other part' in processed

def test_andjoin():
    processed = andjoin(['yellow boots', 'yellow hair', 'shirt'])
    assert 'yellow boots' not in processed
    assert 'yellow hair' not in processed
    assert 'shirt' in processed
    assert 'yellow boots and hair' in processed