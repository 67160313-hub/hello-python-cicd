from build_site import load_scores, main, render_html


def test_load_scores(tmp_path):
    csv_file = tmp_path / "scores.csv"
    csv_file.write_text("name,score\nA,90\nB,40\n", encoding="utf-8")
    assert load_scores(csv_file) == [("A", 90), ("B", 40)]


def test_render_html_has_title_rows_and_average():
    page = render_html([("Somchai", 85), ("Piti", 48)], "Test Results")
    assert "<title>Test Results</title>" in page
    assert "<td>Somchai</td><td>85</td><td>A</td>" in page
    assert "<td>Piti</td><td>48</td><td>F</td>" in page
    assert "ค่าเฉลี่ยคะแนน: 66.5" in page


def test_render_html_escapes_names_and_title():
    page = render_html([("<script>", 50)], "<Demo>")
    assert "<script>" not in page
    assert "&lt;script&gt;" in page
    assert "&lt;Demo&gt;" in page


def test_render_html_rejects_empty_rows():
    import pytest

    with pytest.raises(ValueError, match="At least one score"):
        render_html([], "Empty")


def test_real_data_file_is_valid():
    rows = load_scores("data/scores.csv")
    assert len(rows) > 0
    assert all(0 <= score <= 100 for _, score in rows)


def test_main_builds_site(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "scores.csv").write_text(
        "name,score\nA,90\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SITE_TITLE", "Title from Variable")

    main()

    page = (tmp_path / "_site" / "index.html").read_text(encoding="utf-8")
    assert "<h1>Title from Variable</h1>" in page
