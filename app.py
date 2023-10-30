import sqlite3

from flask import Flask, render_template, abort, redirect, request, url_for

DB_PATH = '../test.s3db'

app = Flask(__name__)

def db_query(query_text):
	with sqlite3.connect(DB_PATH) as conn:
		cur = conn.cursor()
		cur.execute(query_text)
		column_names = [descr[0] for descr in cur.description]
		return column_names, cur.fetchall()

def db_modify(query_text, args):
	with sqlite3.connect(DB_PATH) as conn:
		cur = conn.cursor()
		cur.execute(query_text, args)
		conn.commit()

@app.route('/')
def main_page():
	column_names, data = db_query('SELECT * FROM t1')
	return render_template('main_page.html', rows=data, column_names=column_names)

@app.route('/add', methods=['POST'])
def add_entry():
	try:
		a = int(request.form['a'])
		b = request.form['b']
	except (KeyError, ValueError):
		abort(400)

	db_modify('INSERT INTO t1(a, b) VALUES (?, ?)', (a, b))
	return redirect(url_for('main_page'))

@app.route('/del/<int:entry_id>', methods=['POST'])
def del_entry(entry_id):
	db_modify('DELETE FROM t1 WHERE id = ?', [entry_id])
	return 'OK'
	
if __name__ == '__main__':
	app.run(debug=True)
