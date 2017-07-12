import sqlite3
import sys

import time
import subprocess
import os
import requests
import threading

import ParticleCloud
import scheduler

from flask import Flask, render_template, request

def schedule_daemon():
	while True:
		print "Checking events"
		event = tasklist.check_event()
		if event != None:
			print "Theres an event!"
			growerapp.relay_set(event[0],event[1])

		time.sleep(10)


#Start flask webservice
app = Flask(__name__,static_url_path='/static')


@app.route('/')
def webhook():
	return render_template('index.html')

@app.route('/v1/relays/set',methods=['POST'])
def SetRelay():
	if request.method == "POST":
		relay_target = request.form['relay']
		relay_state = request.form['sor']
		print relay_target
		print relay_state
		growerapp.relay_set(int(relay_target),int(relay_state) )
		return render_template("index.html")

@app.route('/v1/scheduler/<task>',methods=['POST'])
def EditSchedule(task):
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


tasklist = scheduler.Scheduler()
growerapp = ParticleCloud.Controller()




growerapp.login()

t = threading.Thread(target=schedule_daemon)
t.start()

app.run()

growerapp.logout()




