# https://docs.microsoft.com/en-us/azure/sql-database/sql-database-develop-python-simple
import pyodbc
import os
from sanic import Sanic
from sanic.response import json, html, redirect
from jinja2 import Environment, FileSystemLoader

from aoiklivereload import LiveReloader
reloader = LiveReloader()
reloader.start_watcher_thread()

template_envirnoment = Environment(loader=FileSystemLoader(os.getcwd() + '/html'))
get_template = template_envirnoment.get_template

app = Sanic()

app.static('/css', './css')

########################
# Connect to database
########################

server = 'IS-HAY04.ischool.uw.edu'
database = 'Consulting'
username = 'INFO445'
password = 'GoHuskies!'
driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

########################
# Routing
########################

@app.route("/")
async def index(request):
	cursor.execute("SELECT * FROM SKILL")
	rows = cursor.fetchall()
	# for row in rows:
	# return json({"hello": "world"})
	template = get_template('list.html')
	return html( template.render(rows=rows) ) 

@app.route("/create_form")
async def create_form(request):
	template = get_template('create-form.html')
	return html( template.render() ) 

@app.route("/<skill_id:int>/edit_form")
async def edit_form(request, skill_id):
	cursor.execute("SELECT * FROM SKILL WHERE SkillID = " +  str(skill_id))
	template = get_template('edit-form.html')
	return html( template.render(row=cursor.fetchone(), skill_id=skill_id)	  ) 

@app.route("/create")
async def create(request):
	print(request.args)
	skill_name = request.args.get('skill')
	skill_description = request.args.get('description')
	skill_type_id = request.args.get('selectbasic')
	statement = """ 
		INSERT INTO SKILL
		(SkillName, SkillDescription, SkillTypeID)
		VALUES
		('%(sn)s', '%(sd)s', %(sti)s )
	""" % {
		"sn": skill_name,
		"sd": skill_description,
		"sti": skill_type_id
	}
	cursor.execute(statement)
	cnxn.commit()

	return redirect('/')

@app.route("/<skill_id:int>/edit")
async def edit(request, skill_id):
	print(request.args)
	skill_name = request.args.get('skill')
	skill_description = request.args.get('description')
	skill_type_id = request.args.get('selectbasic')
	statement = """ 
		UPDATE SKILL
		SET SkillName = '%(sn)s', 
		SkillDescription = '%(sd)s', 
		SkillTypeID = %(sti)s
		WHERE SkillID = %(skill_id)s;
	""" % {
		"sn": skill_name,
		"sd": skill_description,
		"sti": skill_type_id,
		"skill_id": skill_id
	}
	cursor.execute(statement)
	cnxn.commit()

	return redirect('/')

@app.route('/<skill_id:int>/delete')
async def integer_handler(request, skill_id):
	cursor.execute("DELETE FROM SKILL WHERE SkillID = " + str(skill_id))
	cnxn.commit()
	return redirect('/')

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8000)
