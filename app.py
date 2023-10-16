import sqlite3

from flask import Flask, render_template

DB_PATH = '../test.s3db'

app = Flask(__name__)

def db_query(query_text):
	with sqlite3.connect(DB_PATH) as conn:
		cur = conn.cursor()
		cur.execute(query_text)
		return cur.fetchall()

@app.route('/')
def root():
	data = db_query('SELECT * FROM t1')
	return render_template('root.html', rows=data)

if __name__ == '__main__':
	app.run(debug=True)
