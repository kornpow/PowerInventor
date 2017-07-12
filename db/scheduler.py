import sys


import sqlite3


import time
import subprocess
import os
import requests



class Scheduler:

	def __init__(self,filename="GrowerApp.db"):
		self.create_table(filename)

	def create_table(self,dbname):
		print "creating"
		conn = sqlite3.connect('/home/skorn/Documents/GrowerApp/db/' + str(dbname) )

		c = conn.cursor()
		#Create table
		c.execute('''CREATE TABLE IF NOT EXISTS schedule 
			(hour integer, minute integer ,outlet integer, onoff integer)''')
		conn.commit()

	def add_to_table(self,hour,min,outlet,onoff):
		conn = sqlite3.connect('GrowerApp.db')

		c = conn.cursor()
		pack = (hour,min,outlet,onoff)
		c.execute("INSERT INTO schedule VALUES (?, ?, ?, ?)", pack )
		conn.commit()

	def print_table(self):
		conn = sqlite3.connect('GrowerApp.db')
		c = conn.cursor()
		for row in c.execute('SELECT * FROM schedule ORDER BY hour'):
	        	print row

	def check_event(self):
		conn = sqlite3.connect('/home/skorn/Documents/GrowerApp/db/GrowerApp.db')
		c = conn.cursor()
		t = time.localtime()
		chour = t[3]
		cmin = t[4]
	 	print "Current hour is: " + str(chour)
	 	print "Current minute is: " + str(cmin)
	 	# for row in c.execute('SELECT * FROM schedule WHERE hour=?',(chour,) ):
	  #       	print row	
	  	c.execute('SELECT outlet,onoff FROM schedule WHERE hour=? AND minute=?',(chour,cmin) )
	  	event_list = c.fetchall()
	  	if(len(event_list) == 0):
	  		print "There is no event occuring this minute!"
	  		return

	  	print "Event List ----->"
	  	print event_list
	  	outlet = event_list[0:][0][0]
	  	onoff = event_list[0:][0][1]
	  	print "Outlet to be toggled: " + str(outlet)
	  	print "Parameter value sending to set function: " + str(outlet + onoff)
	  	payload = outlet+onoff

	  	return tuple((outlet,onoff) )

	 #  	device_id = '3f003b000447343337373739'
		# access_token = 'fda31bbba7b0a1130f428cb3d87a2155e91e5b43'
		# args = str(outlet + onoff)
	  	# subprocess.call(["particle", "call", "GrowerApp", "set", str(outlet + onoff)])
		# subprocess.call(["curl", "https://api.particle.io/v1/devices/3f003b000447343337373739/set", "-d", "arg=\"4\"", "-d", "access_token=ef123bf1c94947efc8523b7d16eda5a3a2ef6eff"])
		# subprocess.call(["curl", "https://api.particle.io/v1/devices/3f003b000447343337373739/set","-d", "arg=\"2\"","-d", "access_token=ef123bf1c94947efc8523b7d16eda5a3a2ef6eff"])

	def remove_event(self,hour,mins):
		conn = sqlite3.connect('GrowerApp.db')
		c = conn.cursor()
		c.execute('DELETE FROM schedule WHERE hour=? AND minute=?',(hour,mins))
		conn.commit()

# 

if __name__ == "__main__":
	schedule = Scheduler()

	print sys.argv[1]

	if(sys.argv[1] == "add"): 
		schedule.add_to_table( int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]) )

	if(sys.argv[1] == "print"): 
		schedule.print_table()

	if(sys.argv[1] == "check"): 
		event = schedule.check_event()
		print event

	if(sys.argv[1] == "remove"): 
		schedule.remove_event(int(sys.argv[2]),int(sys.argv[3]))