from pipeline import process_tags

def test_pipeline():
    tags = ["long hair", "hair", "white hair", "commentary request", "red shirt", "sleeveless shirt",
     "multicolored shirt", "dog tail", "dog girl", "animal tail", "serval (kemono friends) (derp)", "kemono friends"]
    processed = process_tags(tags)
    assert "commentary request" not in processed
    assert "long white hair" in processed
    assert "hair" not in processed
    assert "red shirt" not in processed
    assert "red sleeveless shirt" not in processed
    assert "multicolored sleeveless shirt" in processed
    assert "dog tail" not in processed
    assert "animal tail" not in processed
    assert "animal dog tail" not in processed
    assert "kemono friends" not in processed
    assert "serval (kemono friends)" in processed
