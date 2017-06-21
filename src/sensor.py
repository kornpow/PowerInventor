# ADXL345 Python library for Raspberry Pi
#
# author:  Jonathan Williamson
# license: BSD, see LICENSE.txt included in this package
#
# This is a Raspberry Pi Python implementation to help you get started with
# the Adafruit Triple Axis ADXL345 breakout board:
# http://shop.pimoroni.com/products/adafruit-triple-axis-accelerometer

import smbus, os

import sqlite3
import sys


import time
import subprocess
import requests


from flask import Flask


import SimpleHTTPServer
import SocketServer


busNumber =  1 #int(os.getenv("I2C_BUS"))

bus = smbus.SMBus(busNumber)

# ADXL345 constants
ADDRESS            = 34

in0                 = 0
in1                 = 1
out0                = 2
out1                = 3
inv0                = 4
inv1                = 5
config0             = 6
config1             = 7

class WebServer():
    def __init__(self):
        self.app = Flask(__name__)
        self.app.run(host='0.0.0.0', port=80)
        # @self.app.route('/')
    
    def hello_world():
        return 'Hello World!'

class SQL_DB():

    def __init__(self):
        self.create_table()
        self.add_to_table(22,22,1,1)

    def create_table(self):
        
        conn = sqlite3.connect('GrowerApp.db')

        c = conn.cursor()
        #Create table
        print "creating"
        c.execute('''CREATE TABLE IF NOT EXISTS schedule 
            (hour integer, min integer, outlet integer, onoff integer)''')
        conn.commit()
        

    def add_to_table(self,hour,min,outlet,onoff):
        conn = sqlite3.connect('GrowerApp.db')

        c = conn.cursor()
        pack = (hour,min, outlet,onoff)
        # c.execute("SELECT * FROM schedule WHERE EXISTS",(chour,cmin) )
        c.execute("INSERT INTO schedule VALUES (?, ?, ?, ?)", pack )
        conn.commit()

    def print_table(self):
        conn = sqlite3.connect('GrowerApp.db')
        c = conn.cursor()
        for row in c.execute('SELECT * FROM schedule ORDER BY hour'):
                print row

    def check_event(self):
        while True:
            conn = sqlite3.connect('GrowerApp.db')
            c = conn.cursor()
            t = time.localtime()
            chour = t[3]
            cmin = t[4]

            # print "Current hour is: " + str(chour)
            # print "Current minute is: " + str(cmin)
            # print "Current second is: " + str(csec)
            # for row in c.execute('SELECT * FROM schedule WHERE hour=?',(chour,) ):
          #         print row   
            c.execute('SELECT outlet,onoff FROM schedule WHERE hour=? AND min=?',(chour,cmin) )
            event_list = c.fetchall()
            if(len(event_list) == 0):
                print "There is no event occuring this minute!"
                continue

            print "Event List ----->"
            print event_list
            outlet = event_list[0:][0][0]
            onoff = event_list[0:][0][1]
            print "Outlet to be toggled: " + str(outlet)
            print "Parameter value sending to set function: " + str(outlet + onoff)


     #      device_id = '3f003b000447343337373739'
        # access_token = 'fda31bbba7b0a1130f428cb3d87a2155e91e5b43'
        # args = str(outlet + onoff)
        # subprocess.call(["particle", "call", "DadSwitch", "set", str(outlet + onoff)])

    def remove_event(self,hour,mins):
        conn = sqlite3.connect('GrowerApp.db')
        c = conn.cursor()
        c.execute('DELETE FROM schedule WHERE hour=? AND min=?',(hour,mins))
        conn.commit()

class PCA9555:

    address = None

    def __init__(self, address = 34):
        self.address = address
        self.setCONFIG(0,0xF0)
        self.setCONFIG(0,0x00)

    def ToggleRelay(self,relay,onoff):
        mask = onoff << (relay-1)
        writeOUT(0,mask)

    def setCONFIG(self,port,config):
        if port == 0:
            port = config0
        elif port == 1:
            port = config1

        print "\nCurrent Config:\n"
        current = bus.read_byte_data(self.address, port)
        print current
        print "\nDesired new config" + str(config) + "\n"
        bus.write_byte_data(self.address, port, config)
        print "\nNew Config: \n"
        current = bus.read_byte_data(self.address, port)
        print current

    def writeOUT(self,port,out):
        if port == 0:
            port = config0
        elif port == 1:
            port = config1

        # print "Current Output:\n"
        current = bus.read_byte_data(self.address, port)
        # print current
        # print "Desired new output" + str(out) + "\n"
        bus.write_byte_data(self.address, port, out)
        # print "New Output: \n"
        current = bus.read_byte_data(self.address, port)
        # print current

    def readIN(self):
        portvals = 69
        portvals = bus.read_byte_data(self.address, in0)

        print portvals & 0xF0

    def LED_Pattern(self):
        self.writeOUT(1,0x11)
        time.sleep(0.3)
        # adxl345.writeOUT(0,0x03)
        self.writeOUT(1,0x33)
        time.sleep(0.2)
        # adxl345.writeOUT(0,0x07)
        self.writeOUT(1,0x77)
        time.sleep(0.1)
        # adxl345.writeOUT(0,0x0F)
        self.writeOUT(1,0xFF)
        time.sleep(1)
        # adxl345.writeOUT(0,0x00)
        self.writeOUT(1,0x00)
        time.sleep(1.5)

if __name__ == "__main__":
    # if run directly we'll just create an instance of the class and output
    # the current readings
    #Start the web server
    
    #Start the GPIO expander 
    pca9555 = PCA9555()
    #Connect and create database
    sql = SQL_DB()
    #print database
    sql.print_table()


    # threading.Thread(target=sql.check_event()).start()

    # threading.Thread(target=pca9555.LED_Pattern()).start()


    PORT = 8000

    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

    httpd = SocketServer.TCPServer(("", PORT), Handler)

    print "serving at port", PORT
    httpd.serve_forever()
    
    while True:
        pca9555.LED_Pattern()
        print "Time is elapsing"
        time.sleep(2)
        # print "INPUT:"
        # pca9555.readIN()
        # adxl345.writeOUT(0,0x01)
        # pca9555.writeOUT(1,0x11)
        # sleep(0.3)
        # # adxl345.writeOUT(0,0x03)
        # pca9555.writeOUT(1,0x33)
        # sleep(0.2)
        # # adxl345.writeOUT(0,0x07)
        # pca9555.writeOUT(1,0x77)
        # sleep(0.1)
        # # adxl345.writeOUT(0,0x0F)
        # pca9555.writeOUT(1,0xFF)
        # sleep(1)
        # # adxl345.writeOUT(0,0x00)
        # pca9555.writeOUT(1,0x00)
        # sleep(1.5)

