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
class CherryServer():

	def schedule_daemon():
		while True:
			print "Checking events"
			event = tasklist.check_event()
			if event != None:
				print "Theres an event!"
				growerapp.relay_set(event[0],event[1])

			time.sleep(10)

	@cherrypy.expose
	def index(self):
		raise cherrypy.HTTPRedirect("/static")

	@cherrypy.expose
	def SetRelay(self,relay):
		# relay_target = request.form['relay']
		# relay_state = request.form['sor']
		# print relay_target
		# print relay_state

		print "Inside setrelay"
		growerapp.relay_set(int(relay),1 )

	def EditSchedule(self,task):
		if request.method == "POST":

			relay_target = request.form['relay']
			relay_state = request.form['sor']
			hour = request.form['hour']
			minute = request.form['minute']

			print task
			print relay_target
			print relay_state
			print hour
			print minute

			if task == "add":
				print "adding "
				tasklist.add_to_table(hour,minute,relay_target,relay_state)
			if task == "remove":
				tasklist.remove_event(hour,minute)

			return render_template("index.html")

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
	

	# t = threading.Thread(target=schedule_daemon)
	# t.start()

	tasklist = scheduler.Scheduler()
	growerapp = ParticleCloud.Controller()
	growerapp.login()

	cherrypy.quickstart(CherryServer(),'/',conf)
	growerapp.logout()

