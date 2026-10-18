import tempfile
from pathlib import Path

from build_site import load_scores, main, render_html


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


def test_render_html_empty():
    try:
        render_html([], "Empty Page")
    except ValueError:
        pass


def test_main_execution(monkeypatch, tmp_path):
    # ทดสอบฟังก์ชัน main() เพื่อให้ Coverage ผ่านเกณฑ์ 80%
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    csv_file = data_dir / "scores.csv"
    csv_file.write_text("name,score\nAlice,85\n", encoding="utf-8")

    import build_site
    monkeypatch.setattr(build_site, "BASE_DIR", tmp_path)
    monkeypatch.setattr(build_site, "OUTPUT_DIR", tmp_path / "_site")

    main()
    assert (tmp_path / "_site" / "index.html").exists()
