from flask import Flask, render_template, redirect, request
import sqlite3
from flask import g

from datetime import date
today = date.today()

app = Flask(__name__)
app.config["DEBUG"] = True

conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute('''DROP TABLE IF EXISTS table_e''')
cursor.execute('''CREATE TABLE table_e (id INTEGER PRIMARY KEY, title TEXT, details TEXT, date TEXT, time TEXT);''')
cursor.execute('''DROP TABLE IF EXISTS table_r''')
cursor.execute('''CREATE TABLE table_r (id INTEGER PRIMARY KEY, title TEXT, details TEXT, time TEXT);''')

@app.before_request
def before_request():
    g.db = sqlite3.connect("database.db")

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route("/")
def index():
    return render_template("log_in.html")



@app.route("/main_page")
def main_page():
    return render_template("main_page.html")

@app.route("/events")
def events():
    events = g.db.execute('''SELECT * FROM table_e''').fetchall()
    return render_template("events.html", events=events)

@app.route("/routines")
def routines():
    routines = g.db.execute('''SELECT * FROM table_r''').fetchall()
    return render_template("routines.html", routines=routines)


@app.route('/add_event', methods = ['POST'])
def add_event():
    title = request.form['title']
    details = request.form['details']
    date = request.form['date']
    time = request.form['time']
    g.db.execute('''INSERT INTO table_e (title, details, date, time) VALUES (?,?,?,?)''', [title, details, date, time])
    g.db.commit()
    return redirect("/events")

@app.route('/add_routine', methods = ['POST'])
def add_routine():
    title = request.form['title']
    details = request.form['details']
    time = request.form['time']
    g.db.execute('''INSERT INTO table_r (title, details, time) VALUES (?,?,?)''', [title, details, time])
    g.db.commit()
    return redirect("/routines")

@app.route('/viewdetails_e', methods = ['POST'])
def viewdetails_e():
    e_id = request.form['e_id']
    details = g.db.execute('''SELECT * FROM table_e where rowid = ?;''',[e_id])
    return render_template("/details_e.html", details=details)


@app.route('/viewdetails_r', methods = ['POST'])
def viewdetails_r():
    r_id = request.form['r_id']
    details = g.db.execute('''SELECT * FROM table_r where rowid = ?;''',[r_id])
    return render_template("/details_r.html", details=details)

@app.route('/delete_event', methods = ['POST'])
def delete_event():
    e_id = request.form['e_id']
    g.db.execute('''DELETE FROM table_e where rowid = ?;''',[e_id])
    g.db.commit()
    return redirect("/events")

@app.route('/delete_routine', methods = ['POST'])
def delete_routine():
    r_id = request.form['r_id']
    g.db.execute('''DELETE FROM table_r where rowid = ?;''',[r_id])
    g.db.commit()
    return redirect("/routines")

@app.route('/update_event', methods = ['POST'])
def update_event():
    title = request.form['title']
    details = request.form['details']
    e_id = request.form['e_id']
    date = request.form['date']
    time = request.form['time']
    g.db.execute('''UPDATE table_e SET title = ?, details = ?, date = ?, time = ?  where rowid = ?;''', [title, details, date, time, e_id])
    g.db.commit()
    return redirect("/events")

@app.route('/update_routine', methods = ['POST'])
def update_routine():
    title = request.form['title']
    details = request.form['details']
    r_id = request.form['r_id']
    time = request.form['time']
    g.db.execute('''UPDATE table_r SET title = ?, details = ?, date = ?, time = ? where rowid = ?;'''[title, details, time, r_id])
    g.db.commit()
    return redirect("/routines")


@app.route('/edit_event', methods = ['POST'])
def edit_event():
    e_id = request.form['e_id']
    details = g.db.execute('''SELECT * FROM table_e where rowid = ?;''',[e_id])
    return render_template('/edit_e.html', details=details)

@app.route('/edit_routine', methods = ['POST'])
def edit_routine():
    r_id = request.form['r_id']
    details = g.db.execute('''SELECT * FROM table_r where rowid = ?;''',[r_id])
    return render_template('/edit_r.html', details=details)


@app.route("/test")
def test():
    return render_template("test.html")

if __name__ == "__main__":
    app.run(debug=True)
