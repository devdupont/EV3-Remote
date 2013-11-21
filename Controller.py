#!/usr/bin/env python

##--Michael duPont - flyinactor91.com
##--Control hub for multiple robots/clients
##--EV3-Remote - https://github.com/flyinactor91/EV3-Remote

##--2013-11-21
 
import socket

def main():
	host = ('192.168.42.11','192.168.42.12','192.168.42.13','localhost')
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
				[ (0,'QUIT') ]											#End Program
			  ]
	
	#Alter the values to reflect the number of clients according to index in 'host'
	quitFlag = [True , False , False , False]
	while quitFlag[0] or quitFlag[1] or quitFlag[2] or quitFlag[3]:		#Exits once all clients have QUIT
		
		##--Get command--##
		if cueNum != len(cueList): print '\nNext cue #' + str(cueNum) + '\t' + str(cueList[cueNum])
		cue = raw_input('Last: '+str(lastCue)+'  Next: ')
		
		if cue.isdigit(): cueNum = int(cue)
		
		if not (-1 < cueNum < len(cueList)):
			print 'Cue is out of bounds. Reverting to last cue'
			cueNum = lastCue+1
		else:
			for tup in cueList[cueNum]:
				recvr = int(tup[0])
				command = tup[1]
				if ((type(cue) == type("")) and (cue.find('QUIT') != -1)) or (command.find('QUIT') != -1): quitFlag[recvr] = False
				
				##--Create socket--##
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.connect((host[recvr], port))
				
				##--Send and Recieve--##		
				if (cue == '') or (cue.isdigit()):				
					sock.send(command+'\n')
					print str(cueNum)+' to '+str(recvr)+': '+command
				else:
					sock.send(cue+'\n')
					print cue
				ret = sock.recv(1024)
				print ret
				
				##--Close Socket--##
				sock.close()
			
			##--Update queNums--##
			if (cue == '') or (cue.isdigit()):
				lastCue = cueNum
				cueNum += 1


if __name__ == '__main__':
	main()
