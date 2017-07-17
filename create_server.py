import sqlite3
import sys

import time
import subprocess
import os
import requests
import threading

import ParticleCloud
import scheduler

import logging

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
		# return "Hello world"
		raise cherrypy.HTTPRedirect("/static")

	@cherrypy.expose
	@cherrypy.tools.json_out() 
	def SetRelay(self,relay,val):
		logging.debug('SetRelay Call: Relay: %d, Val: %d' % (int(relay), int(val) ) )

		growerapp.relay_set(int(relay),int(val) )
		return json.dumps({"response" : "1"})

	@cherrypy.expose
	@cherrypy.tools.json_out() 
	def AddTask(self,relay,val,hour,minute):
		logging.debug('AddTask Call: Relay: %d, Val: %d, Hour: %d, Minute: %d' % (int(relay), int(val), int(hour), int(minute) ) )

		tasklist.add_to_table(int(hour),int(minute),int(relay),int(val) )

	@cherrypy.expose
	@cherrypy.tools.json_out() 
	def PrintSchedule(self):
		responseData = tasklist.print_table()
		responseJSON = {}

		for i in xrange(0,len(responseData)):
			responseJSON.update({i:responseData[i]})

		return responseJSON

	@cherrypy.expose
	@cherrypy.tools.json_out() 
	def GetRelayStatus(self):
		data = growerapp.relay_status()
		logging.debug('GetRelayStatus Call: Data: %s' % str(data) )
		return data
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
	logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

	tasklist = scheduler.Scheduler()
	growerapp = ParticleCloud.Controller()
	growerapp.login()
	
	t = threading.Thread(target=schedule_daemon)
	t.daemon = True
	t.start()
	cherrypy.config.update({'server.socket_host': '0.0.0.0','server.socket_port': 80})      
	cherrypy.quickstart(CherryServer(),'/',conf)


	growerapp.logout()

