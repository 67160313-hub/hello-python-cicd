import csv
import html
import shutil
from pathlib import Path

from grades import average, grade

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "_site"


def load_scores(csv_path):
    """Read a CSV file and return a list of (name, score) tuples."""
    with open(csv_path, encoding="utf-8", newline="") as file:
        return [(row["name"], int(row["score"])) for row in csv.DictReader(file)]


def render_html(rows, title):
    """Render a styled HTML results page."""
    if not rows:
        raise ValueError("At least one score is required")

    table_rows = "\n".join(
        f"<tr>"
        f"<td>{idx:02d}</td>"
        f"<td>{html.escape(name)}</td>"
        f"<td>{score}</td>"
        f"<td><span class=\"grade-tag\">{grade(score)}</span></td>"
        f"</tr>"
        for idx, (name, score) in enumerate(rows, 1)
    )

    scores = [score for _, score in rows]
    total_students = len(scores)
    avg_score = average(scores)
    max_score = max(scores)
    passed_students = sum(1 for s in scores if s >= 50)
    safe_title = html.escape(title)

    return f"""<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{safe_title}</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>

  <header>
    <div class="nav-container">
      <a href="#" class="logo">67160313 <span>/ SCORE LAB &#10035;</span></a>
      <nav>
        <a href="#results">ผลคะแนน</a>
        <a href="https://github.com/67160313-hub/hello-python-cicd" target="_blank">GitHub &#8599;</a>
      </nav>
    </div>
  </header>

  <main>
    <section class="hero">
      <span class="badge">PYTHON · CI/CD · GITHUB PAGES</span>
      <h1>รายงานผลคะแนน <span>ที่อ่านสนุกขึ้น &#10035;</span></h1>
      <p>ไฟล์ CSV หนึ่งไฟล์ กลายเป็นหน้ารายงานที่ดูง่าย พร้อมการตรวจโค้ดและเผยแพร่อัตโนมัติผ่าน GitHub Actions</p>
    </section>

    <section class="stats-grid">
      <div class="stat-card">
        <span class="icon">&#10035;</span>
        <p>ผู้เรียนในตัวอย่าง</p>
        <h3>{total_students} <small style="font-size: 1rem;">คน</small></h3>
      </div>
      <div class="stat-card">
        <span class="icon">&#8599;</span>
        <p>คะแนนเฉลี่ย</p>
        <h3>{avg_score:.2f}</h3>
      </div>
      <div class="stat-card">
        <span class="icon">&#9733;</span>
        <p>คะแนนสูงสุด</p>
        <h3>{max_score}</h3>
      </div>
      <div class="stat-card">
        <span class="icon">&#10003;</span>
        <p>ผ่านเกณฑ์</p>
        <h3>{passed_students} <small style="font-size: 1rem;">คน</small></h3>
      </div>
    </section>

    <section class="table-section" id="results">
      <div class="section-title">
        <h2>ตารางผลคะแนนตัวอย่าง</h2>
      </div>
      <table>
        <thead>
          <tr>
            <th>ลำดับ</th>
            <th>ชื่อ</th>
            <th>คะแนน</th>
            <th>เกรด</th>
          </tr>
        </thead>
        <tbody>
          {table_rows}
        </tbody>
      </table>
    </section>
  </main>

  <footer>
    <p>© 67160313 · PYTHON CI/CD LAB &#10035;</p>
  </footer>

</body>
</html>
"""


def main():
    csv_path = BASE_DIR / "data" / "scores.csv"
    if not csv_path.exists():
        csv_path = BASE_DIR / "scores.csv"

    rows = load_scores(csv_path)
    html_output = render_html(rows, "Python CI/CD - Score Report")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "index.html").write_text(html_output, encoding="utf-8")

    css_src = BASE_DIR / "style.css"
    if css_src.exists():
        shutil.copy(css_src, OUTPUT_DIR / "style.css")

    print("Site generated successfully in _site/index.html")


if __name__ == "__main__":
    main()
