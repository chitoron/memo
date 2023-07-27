from flask import Flask,request, render_template, redirect
import sqlite3
from dotenv import load_dotenv
import os
load_dotenv('.env')
api_key = os.getenv('API_KEY')

app = Flask(__name__, static_folder='static', static_url_path='' )

if __name__=='__main__':
    app.run(port=3000)
    app.run(debug=True)

tasks = []

#データベースに繋ぐ
def get_db():
	db = sqlite3.connect("memo.db")
	db.row_factory = sqlite3.Row
	return db
def init_db():
	with app.app_context():
		try:
			db=get_db()

		finally:
			db.close()
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
	try:
		db = get_db()

		with db:
			days = db.execute('SELECT DISTINCT day FROM task').fetchall()
			tasks = db.execute('SELECT * FROM task').fetchall()
			categories = db.execute('SELECT * FROM category').fetchall()
			lives=db.execute('SELECT DISTINCT live FROM task').fetchall()

		if request.method == 'POST':
			task = request.form['task']
			category_id=request.form['category_id']
			live=request.form['live']
			lon=request.form['longitude']
			lat=request.form['latitude']
			day=request.form['day']
			with db:
				db.execute('INSERT INTO task (task_name, category_id, live, lon, lat, day) VALUES (?, ?, ?, ?, ?, ?)', (task, category_id, live, lon, lat, day,))
				return redirect('/')
		return render_template('index.html',tasks=tasks,categories=categories,lives=lives,days=days,api_key=api_key,)
	finally:
		db.close()
	

@app.route('/finish', methods=['POST'])
def finish():
	try:
		db=get_db()
		task_id=int(request.form['task_id'])
		with db:
			db.execute('DELETE FROM task WHERE id=?',(task_id,))
		return redirect('/')
	finally:
		db.close()
@app.route('/edit', methods=['POST'])
def edit():
	try:
		db=get_db()
		task_id=int(request.form['task_id'])
		a=request.form['task']
		category_id=int(request.form['category_id'])
		with db:
			db.execute('UPDATE task SET task_name=?,category_id=? WHERE id =? ',(a,category_id,task_id,))
		return redirect('/')
	finally:
		db.close()	
	return redirect('/')

@app.route('/map', methods=['GET', 'POST'])
def map():
	try:
		db = get_db()
		
		with db:
			tasks = db.execute('SELECT * FROM task').fetchall()

		return render_template('map.html', tasks=tasks,api_key=api_key)
	finally:
		db.close()
@app.route('/search',methods=['GET'])
def search():
	try:
		db = get_db()
		a = request.args.get('search')
		b = request.args.get('search1')
		if a=='null' and b=='null':
			with db:
				tasks = db.execute('SELECT * FROM task')
		elif a=='null':
			with db:
				tasks = db.execute('SELECT * FROM task WHERE day= ?',(b,)).fetchall()
		elif b=='null':
			with db:
				tasks = db.execute('SELECT * FROM task WHERE live = ?',(a,)).fetchall()
		else:
			with db:
				tasks = db.execute('SELECT * FROM task WHERE live = ? AND day = ?', (a,b,)).fetchall()
		return render_template('serch.html',tasks=tasks,)
	finally:
		db.close()
@app.route('/tuika',methods=['POST'])
def tuika():
	try:
		db = get_db()
		a = request.form['category']
		print(a)
		with db:
			db.execute('INSERT INTO category (category_name) VALUES (?)', (a,))
		return redirect('/')
	finally:
		db.close()	
	return redirect('/')