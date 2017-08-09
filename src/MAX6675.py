# import PCA9555
import serial



if __name__ == "__main__":    
	# pca9555 = PCA9555.PCA9555()
	ser = serial.Serial('/dev/ttyACM1')
	while 1:
		temp = ser.readline().rstrip('\r\n')

		if temp == "ERROR":
			print "Turn off the engine!"
			continue
		tempint = float(temp)
		print tempint

