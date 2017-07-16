import requests

class Controller():
	def __init__(self,name="GrowerApp"):
		self.client_id = "powerinventor-2954"
		self.client_secret = "3e5e4bd2846a2109a171a5f7a5a23e81a95bbb09"
		self.target_name = name
		self.target_id = 0
		self.at = 0
	


	def login(self):
		#Login to Particle using OAuth
		payload = {'grant_type': 'password', 'username': 'korn94sam@gmail.com',
		'password':'sksk9494??','expires_in':'0'}

		r = requests.post('https://api.particle.io/oauth/token', \
			auth=(self.client_id, self.client_secret),data=payload)

		data = r.json()
		self.at = data["access_token"]
		print self.at

		#List devices
		header = {'Authorization':'Bearer %s'%self.at}
		r = requests.get('https://api.particle.io/v1/devices', \
			headers=header)
		data = r.json()
		print len(data)
		for w in xrange(0,len(data)):
			if(data[w]['connected'] == True and data[w]['name'] == self.target_name):
				print data[w]['name'] + " " + data[w]['id']
				self.target_id = data[w]['id']


	def relay_set(self,relay,onoff):
		#Set relay to a value
		print 
		print "setting relay " + str(relay) +  "with value " + str(onoff)
		if onoff == 0:
			print "Turning off relay "+ str(relay)
			relay = relay + 10

		payload = {'arg': str(relay)}
		header = {'Authorization':'Bearer %s'%self.at}
		r = requests.post('https://api.particle.io/v1/devices/%s/set' %self.target_id, \
			headers=header, data=payload)

		data = r.json()
		print data

	def logout(self):
		r = requests.delete('https://api.particle.io/v1/access_tokens/' + str(self.at) ,auth=('korn94sam@gmail.com','sksk9494??'))
		print r


# powerinventor = controller()
# powerinventor.login()
# powerinventor.relay_set(4,0)
# powerinventor.logout()
#Get list of access tokens
# r = requests.get('https://api.particle.io/v1/access_tokens',auth=('korn94sam@gmail.com','sksk9494??'))
# data = r.json()
# num_at = len(data)
# print num_at
# print data[0]['token']

# Delete all access tokens
# for i in xrange(0,num_at):
# 	payload = {'token': at}
# 	r = requests.delete('https://api.particle.io/v1/access_tokens/' + str(data[i]['token']),auth=('korn94sam@gmail.com','sksk9494??'))
# 	print r

# r = requests.get('https://api.particle.io/v1/access_tokens', \
# 	auth=('korn94sam@gmail.com','sksk9494??'))
# data = r.json()
# num_at = len(data)
# print num_at




#List device parameters
# payload = {'access_token': at, 'arg': '2'}
# header = {'Authorization':'Bearer %s'%at}
# r = requests.get('https://api.particle.io/v1/devices/%s' %target_id, \
# 	headers=header)

# data = r.json()
# print data



#Remove access token generated
# r = requests.delete('https://api.particle.io/v1/access_tokens/' + str(at) ,auth=('korn94sam@gmail.com','sksk9494??'))
# print r
