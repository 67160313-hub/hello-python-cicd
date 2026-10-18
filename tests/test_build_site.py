import tempfile
from pathlib import Path

from build_site import load_scores, render_html


def test_load_scores():
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv", encoding="utf-8") as tmp:
        tmp.write("name,score\nAlice,85\nBob,40\n")
        tmp_path = Path(tmp.name)

    rows = load_scores(tmp_path)
    assert len(rows) == 2
    assert rows[0] == ("Alice", 85)
    assert rows[1] == ("Bob", 40)


def test_render_html():
    rows = [("Alice", 85), ("Bob", 40)]
    html_out = render_html(rows, "Test Page")
    assert "Alice" in html_out
    assert "Bob" in html_out
