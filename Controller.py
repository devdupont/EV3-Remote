#!/usr/bin/env python

##--Michael duPont - flyinactor91.com
##--Control hub for multiple robots/clients
##--EV3-Remote - https://github.com/flyinactor91/EV3-Remote

##--2013-11-26

import socket , os

host = ('192.168.42.11','192.168.42.12','192.168.42.13','localhost')

#Alter the values to reflect the number of clients according to index in 'host'
quitFlag = [True , False , False , False]

port = 5678

cueNum = 0
lastCue = -1

##--Ex Cue: [ (0 , 'F 500;LED 4') , (2 , 'L 400;BEEP 4') ]
cueList = [ [ (0 , 'F 100 N;S 100') ] ,								#Init Robot
			[ (0 , 'F 500;LED 1') ],								#First Cue
			[ (0 , 'R 220 N;LED 2') ],
			[ (0 , 'BEEP 4;S 500;P 2000;S -500;BEEP 5') ],
			[ (0 , 'L 220;LED 3') ],
			[ (0 , 'B 500;LED 0') ],								#Final Que
			[ (0 , 'QUIT') ]											#End Program
		  ]

showCues = [[ (0 , 'F 100 N;S 100') ],
			[ (0 , 'LED 8;MS M 100;F 1000;P 1000; BEEP 5;P 1000;LED 0') ],
			[ (0 , 'QUIT') ]
		   ]


def sendDATA(recvr , command):
	global cueNum
	try:
		#Create socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

#Send cue from cueList to selected recvr. Returns None.
#If cue contains "QUIT", sets recvr's quitFlag to False
#Ex. sendCue(5)
def sendCue(cueNum):
	for tup in cueList[cueNum]:
		recvr = int(tup[0])
		command = tup[1]
		sendDATA(recvr , command)
		#If command contains "QUIT", set recvr's quitFlag to False
		if command.find('QUIT') != -1: quitFlag[recvr] = False


#Send stand-alone command to selected recvr. Returns None
#If cue or command contains "QUIT", sets recvr's quitFlag to False
#Ex. sendCommand("1:F 1000;LED 3")
def sendCommand(cmd):
	recvr = int(cmd.split(':')[0])
	command = cmd.split(':')[1]
	sendDATA(recvr , command)
	#If command contains "QUIT", set recvr's quitFlag to False
	if command.find('QUIT') != -1: quitFlag[recvr] = False


def main():
	global cueNum , lastCue
	#Init terminal
	os.system('clear')
	print "Accepts blank (ENTER), cue number, or stand-alone command.\nExample command:  0:F 500;LED 3"
	
	while quitFlag[0] or quitFlag[1] or quitFlag[2] or quitFlag[3]:		#Exits once all clients have QUIT
		
		#Get command
		if cueNum != len(cueList): print '\nNext cue #' + str(cueNum) + '\t' + str(cueList[cueNum])
		cue = raw_input('Last: '+str(lastCue)+'  Next: ')
		
		#If continue or cue entered
		if (cue == '') or (cue.isdigit()):
			if cue.isdigit(): cueNum = int(cue)			#Set cueNum if new cue is entered
			if not (-1 < cueNum < len(cueList)):		#Check cueNum is within bounds. Else reset to previous cueNum
				print 'Cue is out of bounds. Reverting to last cue'
				cueNum = lastCue+1
			else:
				sendCue(cueNum)
				#Update queNums
				lastCue = cueNum
				cueNum += 1
		
		#Else stand-alone command is entered
		else:
			sendCommand(cue)


if __name__ == '__main__':
	main()
