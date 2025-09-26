import utils
from pipeline import process_tags


def test_pipeline():
    for name in ['blacklist', 'replace', 'colors', 'animals']:
        utils.load_yaml_config(name)
    tags = ["long hair", "hair", "white hair", "commentary request", "red shirt", "sleeveless shirt",'official alternate costume',
      "multicolored shirt", "dog tail", "dog girl", "animal tail", "serval (kemono friends) (derp)", "kemono friends", 'solo', 'adjusting eyewear', 'glasses']
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
    assert "official alternate costume" not in processed
    assert "alternate costume" in processed
    assert "kemono friends" not in processed
    assert "serval (kemono friends)" in processed
    assert "adjusting eyewear" not in processed