# https://docs.microsoft.com/en-us/azure/sql-database/sql-database-develop-python-simple
import pyodbc
import os
from sanic import Sanic
from sanic.response import json, html
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

@app.route("/create")
async def create(request):
	print(request.args)
	return json({'msg':'ok'})


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8000)

# cursor.execute("INSERT INTO INDUSTRY (IndustryName) VAlUES ('BLAH BLAH')")
# cnxn.commit()
