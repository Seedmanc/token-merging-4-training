from transforms.filters import remove_blacklisted, clip_after_series, remove_series

def test_remove_blacklisted():
    processed = remove_blacklisted(['normal tag','blacklisted tag', 'another blacklisted', 'another normal'],
                                   ['blacklisted tag', 'another blacklisted'])
    assert "normal tag" in processed
    assert "another normal" in processed
    assert "blacklisted tag" not in processed
    assert "another another blacklisted" not in processed

def test_clip_after_series():
    processed = clip_after_series(['normal tag','tag with (series)', 'tag with (two) (brackets)'])
    assert 'normal tag' in processed
    assert 'tag with (series)' in processed
    assert 'tag with (two)' in processed
    assert 'tag with (two) (brackets)' not in processed

def test_remove_series():
    processed = remove_series(['normal tag', 'tag with (series)', 'series'])
    assert 'normal tag' in processed
    assert 'tag with (series)' in processed
    assert 'series' not in processed