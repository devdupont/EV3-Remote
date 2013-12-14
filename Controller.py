#!/usr/bin/env python

##--Michael duPont - flyinactor91.com
##--Control hub for multiple robots/clients
##--EV3-Remote - https://github.com/flyinactor91/EV3-Remote

##--2013-12-13
##--Ex Cue: '0 : F 500;LED 4 | 2 : L 400;BEEP 4'

import socket , os , sys

port = 5678
defaultTimeout = 5
cueNum = 0
lastCue = -1
cueList , host , quitFlag = [] , [] , []

#Creates socket and send/recieve a single string of data
def sendDATA(recvr , command):
	global cueNum
	try:
		#Create socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(defaultTimeout)
		sock.connect((host[recvr], port))
		#Send command
		sock.send(command+'\n')
		print "Cue "+str(cueNum)+' to '+str(recvr)+': '+command
		#Recv confirmation
		ret = sock.recv(1024)
		if ret.find("\n") != -1: print ret[:ret.find("\n")]
		else: print ret
		#Close socket
		sock.close()
	#Catch communication errors
	except Exception , e:
		print 'Error: ' + str(e)[str(e).find(']')+1:]


#Send stand-alone command to selected recvr. Returns None
#If cue or command contains "QUIT", sets recvr's quitFlag to False
#Ex. sendCommand('1 : F 1000 ; LED 3')
def sendCommand(cmd):
	cmd = cmd.strip().split('|')
	for i in range(len(cmd)):
		try:
			recvr = int(cmd[i].split(':')[0].strip())
			command = cmd[i].split(':')[1].strip()
			sendDATA(recvr , command)
			#If command contains "QUIT", set recvr's quitFlag to False
			if command.find('QUIT') != -1: quitFlag[recvr] = False
		except Exception , e:
			print 'Error: ' + str(e)[str(e).find(']')+1:]


#Returns True if any value in list is True. Else False
def checkTrue(lst):
	ret = False
	for itm in lst:
		if itm == True: ret = True
	return ret


def main():
	global cueNum , lastCue , cueList , host , quitFlag
	loadShow = False
	
	#If loading show from a file--##
	#Ex. ./Controller.py cues.txt
	if len(sys.argv) == 2 and sys.argv[1].find('.txt') != -1:
		fin = open(sys.argv[1] , 'rb')
		cueList = fin.readlines()
		#Iterate through file and remove empty and comment lines
		remv = []
		for i in range(len(cueList)):
			if cueList[i] == '\n' or cueList[i] == '' or cueList[i][0] == '#': remv.append(i)
		remv.reverse()
		for i in range(len(remv)):
			cueList.pop(remv[i])
		#Make list of IPs and associated quitFlags, then remove first (IP) line
		for IP in cueList[0].split(','):
			host.append(IP.strip())
			quitFlag.append(True)
		cueList.pop(0)
		#Remove '\n' from the end of each line
		for line in range(len(cueList)): cueList[line] = cueList[line].strip('\n')
		loadShow = True
	#If loading IPs (not loading show)--##
	#Ex. ./Controller.py 192.168.42.1 192.168.42.2
	elif len(sys.argv) > 1:
		for i in range(1 , len(sys.argv)):
			host.append(sys.argv[i].strip())
			quitFlag.append(True)
		cueList = ['']
		print host , quitFlag
	#Exit if incorrectly called
	else: sys.exit("Usage:\n./Controller.py (file.txt)\t\t- loading show from a file\n./Controller.py (IP address, ...)\t- loading IP(s) from terminal")
	
	#Init terminal
	os.system('clear')
	print "Accepts blank (ENTER), cue number, or stand-alone command.\nExample command:  0 : F 500 ; LED 3\nMultiple robots:  0 : LED 1 | 1 : LED 2"
	
	while checkTrue(quitFlag):		#Exits once all clients have QUIT
		
		#Get command
		if loadShow:
			if cueNum != len(cueList): print '\nNext cue #' + str(cueNum) + '\t' + str(cueList[cueNum])
			cue = raw_input('Last: '+str(lastCue)+'  Next: ')
		else: cue = raw_input('\nCommand: ')
		
		#If continue or cue entered
		if (cue == '') or (cue.isdigit()):
			#Only do cue lookup if a show has been loaded
			if loadShow:
				if cue.isdigit(): cueNum = int(cue)			#Set cueNum if new cue is entered
				if not (-1 < cueNum < len(cueList)):		#Check cueNum is within bounds. Else reset to previous cueNum
					print 'Cue is out of bounds. Reverting to last cue'
					cueNum = lastCue+1
				else:
					sendCommand(cueList[cueNum])
					#Update queNums
					lastCue = cueNum
					cueNum += 1
			else: print 'No show has been loaded'
		
		#Else stand-alone command is entered
		else:
			sendCommand(cue)


if __name__ == '__main__':
	main()
