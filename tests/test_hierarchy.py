from transforms.hierarchy import subsume, specify_animal

def test_subsume():
    processed = subsume(['noun', 'adjective noun', 'word postfix', 'word'])
    assert "adjective noun" in processed
    assert "word postfix" in processed
    assert "noun" not in processed
    assert "word" not in processed

def test_specify_animal():
    processed = specify_animal(['animal ears', 'cat ears', 'animal tail', 'long tail', 'animal paws'], ['cat','dog'])
    assert "cat ears" in processed
    assert "animal tail" in processed
    assert "long tail" in processed
    assert "animal paws" in processed
    assert "animal ears" not in processed
