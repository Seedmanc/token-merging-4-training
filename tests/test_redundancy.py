from transforms.redundancy import merge, multicolor, omit_parts

def test_merge():
    processed = merge(['long hair', 'white hair', 'very short hair'])
    assert "long white hair" in processed
    assert "long hair" not in processed
    assert "white hair" not in processed
    assert "very short hair" in processed

def test_multicolor():
    processed = multicolor(['red hair', 'white hair','multicolored hair', 'black skirt', 'other skirt'],['white','red'])
    assert 'red hair' not in processed
    assert 'white hair' not in processed
    assert 'multicolored hair' in processed
    assert 'black skirt' in processed
    assert 'other skirt' in processed

def test_omit_parts():
    processed = omit_parts(['cat girl', 'cat tail', 'dog ears', 'other girl', 'other part'],['cat','dog'])
    assert 'cat tail' not in processed
    assert 'dog ears' in processed
    assert 'other part' in processed