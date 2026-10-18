# Python CI/CD: เว็บประกาศผลคะแนน

โปรเจกต์ตัวอย่างสำหรับฝึก GitHub, GitHub Actions (CI) และ GitHub Pages (CD)

## โปรเจกต์ทำอะไร
- อ่านชื่อและคะแนนจาก `data/scores.csv`
- คำนวณเกรด A, B, C, D, F และค่าเฉลี่ย
- สร้างเว็บ HTML ที่ `_site/index.html`
- ทุกครั้งที่ push เข้า `main` GitHub Actions จะตรวจโค้ดและรัน test ก่อน
- เมื่อ test ผ่าน ระบบจะ deploy เว็บไปยัง GitHub Pages โดยอัตโนมัติ

## เกณฑ์เกรด
- 80–100: A
- 70–79: B
- 60–69: C
- 50–59: D
- 0–49: F

## ใช้บน Windows
เปิดโฟลเดอร์นี้ด้วย VS Code แล้วเปิด Terminal:

```powershell
python --version
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements-dev.txt
ruff check .
pytest
python build_site.py
```

เปิดไฟล์ `_site/index.html` ในเว็บเบราว์เซอร์เพื่อดูผล

## แก้คะแนน
แก้ `data/scores.csv` โดยใช้รูปแบบ `name,score` และคะแนนต้องอยู่ระหว่าง 0 ถึง 100 เช่น:

```csv
name,score
Somchai,85
Somying,72
Manee,64
Piti,48
```

## อัปโหลดขึ้น GitHub
1. สร้าง repository ใหม่บน GitHub ชื่อ `hello-python-cicd` และเลือก Public
2. อย่าเลือกสร้าง README เพิ่ม เพราะมี README ในโฟลเดอร์นี้แล้ว
3. เปิด Terminal ในโฟลเดอร์โปรเจกต์ แล้วรัน:

```bash
git init
git branch -M main
git add .
git commit -m "Initial Python CI/CD project"
git remote add origin https://github.com/YOUR-USERNAME/hello-python-cicd.git
git push -u origin main
```

แทน `YOUR-USERNAME` ด้วยชื่อบัญชี GitHub ของตัวเอง

## เปิดเว็บ GitHub Pages
1. เข้า repository → Settings → Pages
2. ใน Build and deployment เลือก Source เป็น **GitHub Actions**
3. เข้าแท็บ Actions แล้วรอ workflow `CI/CD` ให้ทั้ง `test` และ `deploy` ผ่าน
4. ลิงก์เว็บจะปรากฏในงาน deploy หรือใช้รูปแบบ `https://YOUR-USERNAME.github.io/hello-python-cicd/`

## อัปเดตเว็บภายหลัง
แก้ไฟล์ CSV แล้วรัน:

```bash
git add .
git commit -m "Update scores"
git push
```

ถ้า test ผ่าน เว็บจะอัปเดตเอง หากข้อมูลผิด เช่น คะแนน 850, test จะไม่ผ่านและ deploy จะไม่ทำงาน

## โครงสร้างไฟล์
```text
hello-python-cicd/
├── .github/workflows/ci.yml
├── data/scores.csv
├── tests/
│   ├── test_build_site.py
│   └── test_grades.py
├── .gitignore
├── build_site.py
├── grades.py
├── pyproject.toml
├── requirements-dev.txt
└── README.md
```
