#!/usr/bin/env python

##--Michael duPont - flyinactor91.com
##--Control hub for multiple robots/clients
##--EV3-Remote - https://github.com/flyinactor91/EV3-Remote

##--2013-12-31
##--Ex Cue: '0 : F 500;LED 4 | 2 : L 400;BEEP 4'

import socket , os , sys

port = 5678
defaultTimeout = 5

class host:
	def __init__(self , IP):
		self.IP = IP
		self.isOn = True
	def turnOff(self):
		self.isOn = False

def sendDATA(IP , command):
	"""Creates socket and send/recieve a single string of data
	Returns the recieved string or error message"""
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create socket
		sock.settimeout(defaultTimeout)
		sock.connect((IP, port))
		sock.send(command+'\n') #Send command
		ret = sock.recv(1024) #Recv confirmation
		sock.close() #Close socket
		if ret.find('\n') != -1: return ret[:ret.find('\n')]
		return ret
	#Catch communication errors
	except Exception , e:
		return 'Connection error\nError: ' + str(e)[str(e).find(']')+1:]

def sendCommand(cmd , hosts , cueNum):
	"""Send stand-alone command to selected recvr. If cue or command contains "QUIT", call host.turnOff(). Returns hosts
	Ex. sendCommand('1 : F 1000 ; LED 3' , hosts , cueNum)"""
	cmd = cmd.strip().split('|')
	for i in range(len(cmd)):
		try:
			hostNum = int(cmd[i].split(':')[0].strip())
			command = cmd[i].split(':')[1].strip()
			if cueNum == -1: print 'Command'+' to '+str(hostNum)+': '+command
			else: print 'Cue '+str(cueNum)+' to '+str(hostNum)+': '+command
			print sendDATA(hosts[hostNum].IP , command)
			if command.find('QUIT') != -1: hosts[hostNum].turnOff()
		except Exception , e:
			print 'Command text error\nError: ' + str(e)[str(e).find(']')+1:]
	return hosts

def anyOn(hosts):
	"""Returns true if any hosts are on"""
	for obj in hosts:
		if obj.isOn: return True
	return False

def setup():
	"""Returns hosts, cueList, and cueNum vars. Value contents based on how program is called
	Ex.  ./Controller.py cues.txt  or  ./Controller.py 192.168.42.1 192.168.42.2"""
	hosts , cueList = [] , []
	cueNum = -1
	#If loading show from a file--##
	#Ex. ./Controller.py cues.txt
	if len(sys.argv) == 2 and sys.argv[1].find('.txt') != -1:
		try:
			fin = open(sys.argv[1] , 'rb')
			rawLines = fin.readlines()
			#Add non-empty and non-comment lines to cueList
			for line in rawLines:
				if line != '\n' and line != '' and line[0] != '#': cueList.append(line[:line.find('\n')])
			#Make list of IPs and associated quitFlags, then remove first (IP) line
			for IP in cueList[0].split(','): hosts.append(host(IP.strip()))
			cueList.pop(0)
			cueNum = 0
		except Exception , e:
			sys.exit('Error loading show. Check your txt file for errors.\nError: ' + str(e)[str(e).find(']')+1:])
	#If loading IPs (not loading show)--##
	#Ex. ./Controller.py 192.168.42.1 192.168.42.2
	elif len(sys.argv) > 1:
		for i in range(1 , len(sys.argv)): hosts.append(host(sys.argv[i].strip()))
		cueList = ['']
	#Exit if incorrectly called
	else: sys.exit("Usage:\n./Controller.py (file.txt)\t\t- loading show from a file\n./Controller.py (IP address, ...)\t- loading IP(s) from terminal")
	return hosts , cueList , cueNum
	
def main():
	hosts , cueList , cueNum = setup() #If cueNum = -1, the program knows a show has not been loaded
	lastCue = -1
	
	#Init terminal
	os.system('clear')
	print "Accepts blank (ENTER), cue number, or stand-alone command.\nExample command:  0 : F 500 ; LED 3\nMultiple robots:  0 : LED 1 | 1 : LED 2"
	
	while anyOn(hosts): #Exits once all clients have QUIT
		#Get command
		if cueNum != -1:
			if cueNum != len(cueList): print '\nNext cue #' + str(cueNum) + '\t' + str(cueList[cueNum])
			cue = raw_input('Last: '+str(lastCue)+'  Next: ')
		else: cue = raw_input('\nCommand: ')
		#If continue or cue entered
		if (cue == '') or (cue.isdigit()):
			if cueNum != -1: #Only do cue lookup if a show has been loaded
				if cue.isdigit(): cueNum = int(cue) #Set cueNum if new cue is entered
				if not (-1 < cueNum < len(cueList)): #Check cueNum is within bounds. Else reset to previous cueNum
					print 'Cue is out of bounds. Reverting to last cue'
					cueNum = lastCue+1
				else:
					hosts = sendCommand(cueList[cueNum] , hosts , cueNum)
					#Update queNums
					lastCue = cueNum
					cueNum += 1
			else: print 'No show has been loaded'
		#Else stand-alone command is entered
		else:
			hosts = sendCommand(cue , hosts , cueNum)
	print 'End Program'

if __name__ == '__main__':
	main()
