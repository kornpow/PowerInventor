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

class SQL_DB:

    def __init__(self):
        create_table()

    def create_table():
        print "creating"
        conn = sqlite3.connect('GrowerApp.db')

        c = conn.cursor()
        #Create table
        c.execute('''CREATE TABLE schedule 
            (hour integer, minute integer ,outlet integer, onoff integer)''')
        conn.commit()

    def add_to_table(hour,min,outlet,onoff):
        conn = sqlite3.connect('GrowerApp.db')

        c = conn.cursor()
        pack = (hour,min,outlet,onoff)
        c.execute("INSERT INTO schedule VALUES (?, ?, ?, ?)", pack )
        conn.commit()

    def print_table():
        conn = sqlite3.connect('GrowerApp.db')
        c = conn.cursor()
        for row in c.execute('SELECT * FROM schedule ORDER BY hour'):
                print row

    def check_event():
        conn = sqlite3.connect('GrowerApp.db')
        c = conn.cursor()
        t = time.localtime()
        chour = t[3]
        cmin = t[4]
        print "Current hour is: " + str(chour)
        print "Current minute is: " + str(cmin)
        # for row in c.execute('SELECT * FROM schedule WHERE hour=?',(chour,) ):
      #         print row   
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

     #      device_id = '3f003b000447343337373739'
        # access_token = 'fda31bbba7b0a1130f428cb3d87a2155e91e5b43'
        # args = str(outlet + onoff)
        # subprocess.call(["particle", "call", "DadSwitch", "set", str(outlet + onoff)])

    def remove_event(hour,mins):
        conn = sqlite3.connect('GrowerApp.db')
        c = conn.cursor()
        c.execute('DELETE FROM schedule WHERE hour=? AND minute=?',(hour,mins))
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

if __name__ == "__main__":
    # if run directly we'll just create an instance of the class and output
    # the current readings
    pca9555 = PCA9555()
    sql = SQL_DB()
    sql.add_to_table(22,22,1,1)
    while True:
        # print "INPUT:"
        # pca9555.readIN()
        # adxl345.writeOUT(0,0x01)
        pca9555.writeOUT(1,0x11)
        sleep(0.3)
        # adxl345.writeOUT(0,0x03)
        pca9555.writeOUT(1,0x33)
        sleep(0.2)
        # adxl345.writeOUT(0,0x07)
        pca9555.writeOUT(1,0x77)
        sleep(0.1)
        # adxl345.writeOUT(0,0x0F)
        pca9555.writeOUT(1,0xFF)
        sleep(1)
        # adxl345.writeOUT(0,0x00)
        pca9555.writeOUT(1,0x00)
        sleep(1.5)

