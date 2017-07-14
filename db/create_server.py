import sqlite3
import sys

import time
import subprocess
import os
import requests
import threading

import ParticleCloud
import scheduler

# from flask import Flask, render_template, request
import cherrypy
import json


conf = {
    '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
         },
    '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static',
            'tools.staticdir.index': 'html/index.html'
         }
}

def schedule_daemon():
	while True:
		print "Checking events"
		event = tasklist.check_event()
		if event != None:
			print "Theres an event!"
			growerapp.relay_set(event[0],event[1])

		time.sleep(10)

class CherryServer():

	@cherrypy.expose
	def index(self):
		raise cherrypy.HTTPRedirect("/static")

	@cherrypy.expose
	@cherrypy.tools.json_out() 
	def SetRelay(self,relay,val):
		# relay_target = request.form['relay']
		# relay_state = request.form['sor']
		print relay
		print val

		print "Inside setrelay"
		growerapp.relay_set(int(relay),int(val) )
		return json.dumps({"response" : "1"})

	@cherrypy.expose
	@cherrypy.tools.json_out() 
	def AddTask(self,relay,val,hour,minute):
		
		print relay
		print val
		print hour
		print minute


		tasklist.add_to_table(int(hour),int(minute),int(relay),int(val) )

	@cherrypy.expose
	@cherrypy.tools.json_out() 
	def PrintSchedule(self):
		responseData = tasklist.print_table()
		responseJSON = {}

		for i in xrange(0,len(responseData)):
			responseJSON.update({i:responseData[i]})

		return responseJSON

#Start flask webservice
# app = Flask(__name__,static_url_path='/static')


# @app.route('/')
# def webhook():
# 	return render_template('index.html')

# @app.route('/v1/relays/set',methods=['POST'])
# def SetRelay():
# 	if request.method == "POST":
# 		relay_target = request.form['relay']
# 		relay_state = request.form['sor']
# 		print relay_target
# 		print relay_state
# 		growerapp.relay_set(int(relay_target),int(relay_state) )
# 		return render_template("index.html")

# @app.route('/v1/scheduler/<task>',methods=['POST'])


if __name__ == '__main__':
	tasklist = scheduler.Scheduler()
	growerapp = ParticleCloud.Controller()
	growerapp.login()
	
	t = threading.Thread(target=schedule_daemon)
	t.daemon = True
	t.start()
	cherrypy.quickstart(CherryServer(),'/',conf)


	growerapp.logout()

