import csv
import html
import os
from pathlib import Path

from grades import average, grade

OUTPUT_DIR = Path("_site")


def load_scores(csv_path):
    """Read a CSV file and return a list of (name, score) tuples."""
    with open(csv_path, encoding="utf-8", newline="") as file:
        return [(row["name"], int(row["score"])) for row in csv.DictReader(file)]


def render_html(rows, title):
    """Render a simple HTML results page."""
    if not rows:
        raise ValueError("At least one score is required")
    table_rows = "\n".join(
        f"<tr><td>{html.escape(name)}</td><td>{score}</td>"
        f"<td>{grade(score)}</td></tr>"
        for name, score in rows
    )
    avg = average([score for _, score in rows])
    safe_title = html.escape(title)
    return f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{safe_title}</title>
<style>
body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 18px; color: #202938; }}
h1 {{ color: #174ea6; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
th, td {{ border: 1px solid #d7deea; padding: 12px; text-align: left; }}
th {{ background: #eaf1ff; }}
.summary {{ margin-top: 18px; padding: 14px; background: #f2f7f2; border-radius: 8px; }}
</style>
</head>
<body>
<h1>{safe_title}</h1>
<p>ตารางแสดงคะแนนและเกรดของนักเรียน</p>
<table>
<thead><tr><th>ชื่อ</th><th>คะแนน</th><th>เกรด</th></tr></thead>
<tbody>
{table_rows}
</tbody>
</table>
<p class="summary">ค่าเฉลี่ยคะแนน: {avg}</p>
</body>
</html>
"""


def main():
    """Build the static website from the CSV file."""
    title = os.environ.get("SITE_TITLE") or "ผลคะแนนวิชา CI/CD"
    rows = load_scores("data/scores.csv")
    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "index.html").write_text(
        render_html(rows, title),
        encoding="utf-8",
    )
    print(f"Built {OUTPUT_DIR / 'index.html'} ({len(rows)} students)")


if __name__ == "__main__":
    main()
