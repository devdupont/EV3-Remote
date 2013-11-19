#!/usr/bin/env python++
 
import socket

def main():
	host = '192.168.42.11'
	port = 5678
	cueNum = 0
	lastCue = -1
	
	cueList = [ 'F 100',				#Init Robot
				'F 500;LED 1',			#First Cue
				'R 220 Y;LED 2',		
				'L 220;LED 3',
				'B 500;LED 0',			#Final Que
				'QUIT' ]				#End Program
	
	quitFlag = True
	while quitFlag:
		
		##--Get command--##
		if cueNum != len(cueList): print '\nNext cue #' + str(cueNum) + '\t' + cueList[cueNum]
		command = raw_input('Last: '+str(lastCue)+'  Next: ')
		
		if command.isdigit(): cueNum = int(command)
		
		if not (-1 < cueNum < len(cueList)):
			print 'Cue is out of bounds. Reverting to last cue'
			cueNum = lastCue+1
		else:
			if (command.find('QUIT') != -1) or (cueList[cueNum].find('QUIT') != -1): quitFlag = False
			
			##--Create socket--##
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((host, port))
			
			##--Send and Recieve--##		
			if (command == '') or (command.isdigit()):				
				sock.send(cueList[cueNum]+'\n')
				print str(cueNum)+': '+cueList[cueNum]
			else:
				sock.send(command+'\n')
				print command
			ret = sock.recv(1024)
			print ret
			
			##--Close Socket--##
			sock.close()
			
			##--Update queNums--##
			if (command == '') or (command.isdigit()):
				lastCue = cueNum
				cueNum += 1


if __name__ == '__main__':
	main()
