#!/usr/bin/env python

##--Michael duPont - flyinactor91.com
##--Control hub for multiple robots/clients
##--EV3-Remote - https://github.com/flyinactor91/EV3-Remote

##--2013-12-04

import socket , os

host = ('192.168.42.11','192.168.42.17','192.168.42.18','localhost')
#Alter the values to reflect the number of clients according to index in 'host'
quitFlag = [True , True , False , True]
port = 5678
cueNum = 0
lastCue = -1

##--Ex Cue: '0 : F 500;LED 4 | 2 : L 400;BEEP 4'
cueList = [ '0: F 100 N ; S 100 | 1: F 100 N ; S 100 | 2: F 100 N ; S 100' ,	#Init Robot
			
			##--Scene One--## Start = 1
			'2: MS M 200 ; LED 8; F 500; MS M 150;F 750;MS M 100; F 1000; P 500; R 170',
			'3: TR Goodbye, World! | 2: P 3000; BEEP 5;P 2000;LED 0;QUIT',
			
			##--Scene Two--## Start = 3
			'1: LED 3 ; F 1700',
			'1: L 220 ; F 500 ; R 220 ; F 1000 ; R 220 ; F 1000',
			'3: TO [Evil Laugh] | 1: LED 6 ; MS S 1000 ; S 2000',
			"3: TO With R3-D712's death, human-robot relations go down the down. Those stupid fleshbags won't know what's coming.",
			"3: TO I, DeputyDroid, will help robots take over the world!",
			'3: TO [Evil Laugh] | 1: S 2000',
			"0: LED 4 ; F 1700 | 3: TG You're early to the scene, rookie. | 1: LED 3 ; P 1000 ; B 500 ; R 210",
			#10
			'0: LED 1 | 1: LED 6 | 3: TO Ah yes, boss. I live close by.',
			'0: R 100 ; LED 4 ; P 1000 ; L 200 ; P 1000 ; R 120 | 1: LED 3',
			'3: TG Nasty business this -- viral internal meltdown.',
			"0: LED 0 | 1: LED 6 ; R 3560 N ; S -6000 | 0: LED 1 | 3: TO No robot is safe! It's robopocalypse! I need to update my Virus Definitions!",
			'0: F 600 ; S -70 ; S 70',
			'0: LED 4 ; B 600 | 3: TG Quiet rookie! Calm down.',
			'0: LED 1 | 1: LED 6 | 3: TO But boss, someone could be infecting me as we speak.',
			"0: LED 4 | 1: LED 3 | 3: TG Rookie, you would need to download the virus for it to affect you. You can't catch a virus like humans can.",
			"0: LED 1| 1: LED 6 | 3: TO Oh yeah, Wow I need to calibrate my personality matrix, I almost feel embarrassed.",
			"0: LED 4| 1: LED 3 | 3: TG You find any clues, Rookie?",
			#20
			'0: LED 1 | 1: MS M 360 ; R 100 ; P 1000 ; L 200 ; P 1000 ; R 930',
			'1: LED 6 | 3: TO NOPE, no clues here boss, just a couple footprints.',
			'0: LED 4 ; BEEP 2 | 1: LED 3 | 3: TG You idiot -- that is a clue.',
			'3: TG So think this was human caused?',
			'0: LED 1 | 1: LED 6 | 3: TO Definitely human.  I mean no droid would kill another droid.',
			'0: LED 4 ; S -70 ; P 2000 ; S 70 | 1: LED 3 | 3: TG Not necessarily, few years ago we had a rogue bot that cannibalized other bots for parts.',
			'0: LED 1 | 1: LED 6 ; MS S 360 ; S 100 ; S -100 ; S 100 ; S -100 | 3: TO But no parts are missing.',
			"0: LED 4 | 1: LED 3 | 3: TG Not the point, Rookie. Just don't jump to conclusions.",
			'0: LED 1 | 1: LED 6 ; BEEP 3 | 3: TO Sorry Boss, got a little carried away.',
			"0: LED 4 ; BEEP 3 | 1: LED 3 | 3: TG Alright, HQ just sent a message they rounded up a few suspects. Let’s interview them and see what they know."
			#30
			'0: LED 1 ; R 440 ; F 1700',
			'3: TO [Evil Laugh] | 1: S 2000',
			'1: LED 6 | 3: TO As if HQ could find me -- HAL shall be avenged!',
			'1: LED 3 ; F 2700',
			
			
			'0: QUIT | 1: QUIT | 3: QUIT'				#End Program
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


#Send stand-alone command to selected recvr. Returns None
#If cue or command contains "QUIT", sets recvr's quitFlag to False
#Ex. sendCommand('1 : F 1000 ; LED 3')
def sendCommand(cmd):
	cmd = cmd.strip().split('|')
	for i in range(len(cmd)):
		recvr = int(cmd[i].split(':')[0].strip())
		command = cmd[i].split(':')[1].strip()
		sendDATA(recvr , command)
		#If command contains "QUIT", set recvr's quitFlag to False
		if command.find('QUIT') != -1: quitFlag[recvr] = False


def main():
	global cueNum , lastCue
	#Init terminal
	os.system('clear')
	print "Accepts blank (ENTER), cue number, or stand-alone command.\nExample command:  0 : F 500 ; LED 3\nMultiple robots:  0 : LED 1 | 1 : LED 2"
	
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
				sendCommand(cueList[cueNum])
				#Update queNums
				lastCue = cueNum
				cueNum += 1
		
		#Else stand-alone command is entered
		else:
			sendCommand(cue)


if __name__ == '__main__':
	main()
