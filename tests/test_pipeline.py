from pipeline import process_tags

def test_pipeline_basic():
    tags = ["long hair", "hair", "white hair", "commentary request"]
    processed = process_tags(tags)
    assert "commentary request" not in processed
    assert any("hair" in t for t in processed)