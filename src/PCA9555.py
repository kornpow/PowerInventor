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

class PCA9555:

    address = None
    status = [0,0,0,0]

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

    def Cycle_Relays(self):
        bus.write_byte_data(self.address, 2, 0xFF)
        bus.write_byte_data(self.address, 3, 0xFF)
        time.sleep(2)
        bus.write_byte_data(self.address, 2, 0x0)
        bus.write_byte_data(self.address, 3, 0x0)
        time.sleep(2)

    def relay_set(self,relay,val):
        self.status[relay-1] = val
        mask = self.status[0] | self.status[1] << 1 | self.status[2] << 2 | self.status[3] << 3
        print mask
        bus.write_byte_data(self.address, 2, mask)

    def relay_status(self):
        status_dict = {"relay1":0,"relay2":0,"relay3":0,"relay4":0}
        status_dict["relay1"] = self.status[0]
        status_dict["relay2"] = self.status[1]
        status_dict["relay3"] = self.status[2]
        status_dict["relay4"] = self.status[3]
        return status_dict



if __name__ == "__main__":
    # if run directly we'll just create an instance of the class and output
    # the current readings
    #Start the web server
    
    #Start the GPIO expander 
    pca9555 = PCA9555()
    #Connect and create database
    # sql = SQL_DB()
    # #print database
    # sql.print_table()


    # threading.Thread(target=sql.check_event()).start()

    # threading.Thread(target=pca9555.LED_Pattern()).start()


    # PORT = 8000

    # Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

    # httpd = SocketServer.TCPServer(("", PORT), Handler)

    # print "serving at port", PORT
    # httpd.serve_forever()
    pca9555.LED_Pattern()
    
    while True:
        pca9555.Cycle_Relays()
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

