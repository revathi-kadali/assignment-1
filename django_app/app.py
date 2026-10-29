import sys
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import connection
from django.http import HttpResponse
from django.urls import path

settings.configure(
    DEBUG=True,
    SECRET_KEY="assignment",
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=["*"],
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "students.db"}},
)

def init_db():
    cur = connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS students (roll_no INTEGER PRIMARY KEY, name TEXT, branch TEXT, cgpa REAL)")
    cur.execute("SELECT COUNT(*) FROM students")
    if cur.fetchone()[0] == 0:
        data = [
            (201, "Anjali Verma", "CSE", 8.7),
            (202, "Rahul Nair", "IT", 7.9),
            (203, "Meena Das", "ECE", 9.0),
            (204, "Vikram Singh", "CIVIL", 7.4),
            (205, "Pooja Patel", "CSE", 8.2),
        ]
        cur.executemany("INSERT INTO students VALUES (%s, %s, %s, %s)", data)

def home(request):
    cur = connection.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    html = "<h2>Student Details - Django + SQLite</h2><table border='1' cellpadding='8'>"
    html += "<tr><th>Roll No</th><th>Name</th><th>Branch</th><th>CGPA</th></tr>"
    for r in rows:
        html += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    html += "</table>"
    return HttpResponse(html)

urlpatterns = [path("", home)]

if __name__ == "__main__":
    import django
    django.setup()
    init_db()
    execute_from_command_line(sys.argv)
