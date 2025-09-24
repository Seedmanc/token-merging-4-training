from transforms.filters import remove_blacklisted, clip_after_series, remove_series, alternate_costume
from utils import dicts

def test_remove_blacklisted():
    dicts['blacklist'] = ['blacklisted tag', 'startswith*', '*endswith' ]
    processed = remove_blacklisted(['normal tag','blacklisted tag', 'startswith smth', 'another normal', 'smth endswith'])
    assert "normal tag" in processed
    assert "another normal" in processed
    assert "blacklisted tag" not in processed
    assert "starts with smth" not in processed
    assert "smth endswith" not in processed

def test_clip_after_series():
    processed = clip_after_series(['normal tag','tag with (series)', 'tag with (two) (brackets)'])
    assert 'normal tag' in processed
    assert 'tag with (series)' in processed
    assert 'tag with (two)' in processed
    assert 'tag with (two) (brackets)' not in processed

def test_remove_series():
    processed = remove_series(['normal tag', 'tag with (series)', 'series', 'series 2'])
    assert 'normal tag' in processed
    assert 'tag with (series)' in processed
    assert 'series' not in processed
    assert 'series 2' not in processed

def test_alternate_costume():
    processed = alternate_costume(['official alternate costume'])
    assert processed[0] == 'alternate costume'