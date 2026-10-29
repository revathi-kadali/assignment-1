from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

def init_db():
    con = sqlite3.connect("students.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS students (roll_no INTEGER PRIMARY KEY, name TEXT, branch TEXT, cgpa REAL)")
    cur.execute("SELECT COUNT(*) FROM students")
    if cur.fetchone()[0] == 0:
        data = [
            (101, "Ravi Kumar", "CSE", 8.4),
            (102, "Priya Sharma", "ECE", 9.1),
            (103, "Arjun Reddy", "MECH", 7.6),
            (104, "Sneha Iyer", "CSE", 8.9),
            (105, "Kiran Rao", "EEE", 7.2),
        ]
        cur.executemany("INSERT INTO students VALUES (?, ?, ?, ?)", data)
    con.commit()
    con.close()

page = """
<h2>Student Details - Flask + SQLite</h2>
<table border="1" cellpadding="8">
<tr><th>Roll No</th><th>Name</th><th>Branch</th><th>CGPA</th></tr>
{% for s in students %}
<tr><td>{{ s[0] }}</td><td>{{ s[1] }}</td><td>{{ s[2] }}</td><td>{{ s[3] }}</td></tr>
{% endfor %}
</table>
"""

@app.route("/")
def home():
    con = sqlite3.connect("students.db")
    students = con.execute("SELECT * FROM students").fetchall()
    con.close()
    return render_template_string(page, students=students)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
