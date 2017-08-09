import sqlite3
import sys

import time
import subprocess
import os
# import requests
import threading

import ParticleCloud
import scheduler
import PCA9555

import logging
# import logging_tree

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
            'tools.staticdir.dir': '../static',
            'tools.staticdir.index': 'html/index.html'
         }
}


log = logging.getLogger('')

def schedule_daemon():
	while True:
		print "Checking events"
		event = tasklist.check_event()
		if event != None:
			print "Theres an event!"
			growerapp.relay_set(event[0],event[1],event[2])

		time.sleep(10)

class CherryServer():

	@cherrypy.expose
	def index(self):
		# return "Hello world"

		raise cherrypy.HTTPRedirect("/static")

	def _cp_dispatch(self, vpath):
		logging.warning('Value of vpath is %s, and number of elements is: %d, and request type is: %s' % (vpath,len(vpath),str(cherrypy.request.method.upper()) ) )
		# logging.warning(cherrypy.request.method.upper() )
		# if len(vpath) > 1:
			# if vpath[1] == "javascripts":
			# 	# logging.warning("Trying to load a javascript file")
			# 	cherrypy.request.params['name'] = vpath.pop()
	  #      		return self

			# if vpath[1] == "users":
			# 	logging.warning("Trying to load list of users %d" % (1,))
			# 	cherrypy.request.params['userId'] = vpath.pop()
			# 	return self.users

	# 	if len(vpath) == 3:
	# 		cherrypy.request.params['artist'] = vpath.pop(0)  # /band name/
 #        	vpath.pop(0) # /albums/
 #        	cherrypy.request.params['title'] = vpath.pop(0) # /album title/
 #        	return self.users

	# 	return vpath
		# return vpath


	@cherrypy.expose
	def users(self,userId=None):
		# logging_tree.printout()
		return "UserId =" + str(userId)

	@cherrypy.expose
	@cherrypy.tools.json_out() 
	def SetRelay(self,devname,relay,val):
		logging.debug('SetRelay Call: Devname: %s Relay: %d, Val: %d' % (devname,int(relay), int(val) ) )


		growerapp.relay_set(int(relay),int(val),devname )
		# io.relay_set(int(relay),int(val) )
		return json.dumps({"response" : "1"})

	@cherrypy.expose
	@cherrypy.tools.json_out() 
	def AddTask(self,devname,relay,val,hour,minute):
		logging.debug('AddTask Call: Relay: %d, Val: %d, Hour: %d, Minute: %d' % (int(relay), int(val), int(hour), int(minute) ) )

		tasklist.add_to_table(devname,int(hour),int(minute),int(relay),int(val) )

	@cherrypy.expose
	@cherrypy.tools.json_out() 
	def RemoveTask(self,devname,hour,minute):
		logging.debug('RemoveTask Call:  Hour: %d, Minute: %d' % (int(hour), int(minute) ) )

		tasklist.remove_event(devname,int(hour),int(minute) )

	@cherrypy.expose
	@cherrypy.tools.json_out() 
	def PrintSchedule(self,devname):
		responseData = tasklist.print_dev_table(devname)
		
		print "length of response data + " + str(len(responseData))
		if len(responseData) == 0:
			return "<p>No Events Schedule for Device: " + str(devname) + "</p>"
		html = "<tr> <th> Hour </th> <th> Min </th> <th> Relay </th> <th> Val </th> </tr>"

		for i in xrange(0,len(responseData)):
			html = html + "<tr> <th>" + str(responseData[i][0]) + "</th> <th>" + str(responseData[i][1]) + "</th> <th>" + str(responseData[i][2]) + "</th> <th>" + str(responseData[i][3])

		html = html + "</tr>"
		return html

	@cherrypy.expose
	@cherrypy.tools.json_out() 
	def GetRelayStatus(self):
		data = growerapp.relay_status()
		# data = io.relay_status()
		logging.debug('GetRelayStatus Call: Data: %s' % str(data) )
		return data
		

	@cherrypy.expose
	@cherrypy.tools.json_out() 
	def ShowDevices(self):
		responseData = growerapp.getDeviceList()
		responseJSON = {}

		# for i in xrange(0,len(responseData)):
		# 	responseJSON.update({i:responseData[i]})

		return responseData

	@cherrypy.expose
	@cherrypy.tools.json_out() 
	def SelectDevice(self,name):
		rname = growerapp.setCurrentDevice(name)
		logging.debug('SelectDevice Call: Data: %s' % str(rname) )



if __name__ == '__main__':
	logging.basicConfig(filename='../example.log', level=logging.WARN, format='%(asctime)s - %(levelname)s - %(message)s')
	logging.getLogger('cherrypy').propagate = False
	# logging_tree.printout()
	

	tasklist = scheduler.Scheduler()
	growerapp = ParticleCloud.Controller()
	growerapp.login()
	# io = PCA9555.PCA9555()
	
	t = threading.Thread(target=schedule_daemon)
	t.daemon = True
	t.start()
	cherrypy.config.update({'server.socket_host': '0.0.0.0','server.socket_port': 80})      
	cherrypy.quickstart(CherryServer(),'/',conf)


	growerapp.logout()

