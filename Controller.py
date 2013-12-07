#!/usr/bin/env python

##--Michael duPont - flyinactor91.com
##--Control hub for multiple robots/clients
##--EV3-Remote - https://github.com/flyinactor91/EV3-Remote

##--2013-12-07

import socket , os

host = ('192.168.42.11','192.168.42.17','192.168.42.18','localhost')
#Alter the values to reflect the number of clients according to index in 'host'
quitFlag = [True , True , True , True]
port = 5678
cueNum = 0
lastCue = -1

##--Ex Cue: '0 : F 500;LED 4 | 2 : L 400;BEEP 4'
cueList = [ '0: F 100 N ; S 100 | 1: F 100 N ; S 100 | 2: F 100' ,	#Init Robot
			
			##--Scene One--## Start = 1
			'2: MS M 200 ; LED 8; F 500; MS M 150;F 750;MS M 100; F 1000; P 500; R 170',
			'3: TR Goodbye, World! | 2: P 3000; BEEP 5;P 2000;LED 0;QUIT',
			'3: C',
			
			##--Scene Two--## Start = 4
			'1: LED 3 ; F 1700',
			'1: L 220 ; F 500 ; R 230 ; F 1000 ; R 220 ; F 1000',
			'3: TO [Evil Laugh] | 1: LED 6 ; MS S 1000 ; S 2000 N ; BEEP 2; P 750 ; BEEP 2',
			"3: TO With R3-D712's death, human-robot relations go down the down. Those stupid fleshbags won't know what's coming.",
			"3: TO I, DeputyDroid, will help robots take over the world!",
			'3: TO [Evil Laugh] | 1: S 2000 N ; BEEP 2; P 750 ; BEEP 2',
			#10
			"0: LED 4 ; F 1700 | 3: TG You're early to the scene, rookie. | 1: LED 3 ; P 1000 ; B 500 ; R 210",
			'0: LED 1 | 1: LED 6 | 3: TO Ah yes, boss. I live close by.',
			'0: R 100 ; LED 4 ; P 1000 ; L 200 ; P 1000 ; R 120 | 1: LED 3',
			'3: TG Nasty business this -- viral internal meltdown.',
			"0: LED 0 | 1: LED 6 ; R 1640 N ; S -5000 | 0: LED 1 | 3: TO No robot is safe! It's robopocalypse! I need to update my Virus Definitions!",
			'0: F 650 ; S -80 ; S 80',
			'0: LED 4 ; B 650 | 3: TG Quiet rookie! Calm down.',
			'0: LED 1 ; R 100 | 1: LED 6 ; L 100 | 3: TO But boss, someone could be infecting me as we speak.',
			"0: LED 4 | 1: LED 3 | 3: TG Rookie, you would need to download the virus for it to affect you. You can't catch a virus like humans can.",
			"0: LED 1| 1: LED 6 | 3: TO Oh yeah, Wow I need to calibrate my personality matrix, I almost feel embarrassed.",
			#20
			"0: LED 4| 1: LED 3 | 3: TG You find any clues, Rookie?",
			'0: LED 1 | 1: MS M 360 ; R 200 ; P 1000 ; L 1030',
			'1: LED 6 | 3: TO NOPE, no clues here boss, just a couple footprints.',
			'0: LED 4 ; BEEP 2 | 1: LED 3 | 3: TG You idiot -- that is a clue.',
			'3: TG So think this was human caused?',
			'0: LED 1 | 1: LED 6 | 3: TO Definitely human.  I mean no droid would kill another droid.',
			'0: LED 4 ; L 100 ; S -70 ; P 2000 ; S 70 ; R 100 | 1: LED 3 | 3: TG Not necessarily, few years ago we had a rogue bot that cannibalized other bots for parts.',
			'0: LED 1 | 1: LED 6 ; MS S 500 ; S 110 ; S -110 ; S 100 ; S -100 | 3: TO But no parts are missing.',
			"0: LED 4 | 1: LED 3 | 3: TG Not the point, Rookie. Just don't jump to conclusions.",
			'0: LED 1 | 1: LED 6 ; BEEP 3 | 3: TO Sorry Boss, got a little carried away.',
			#30
			"0: LED 4 ; BEEP 2 | 1: LED 3 | 3: TG Alright, HQ just sent a message they rounded up a few suspects. Let's interview them and see what they know.",
			'0: LED 1 ; R 350 ; F 1700',
			'3: TO [Evil Laugh] | 1: MS S 1000 ; S 2000 N  ; L 100 N ; BEEP 2; P 750 ; BEEP 2',
			'1: LED 6 | 3: TO As if HQ could find me -- HAL shall be avenged!',
			'1: LED 3 ; R 220 ; F 2700 N ; S 6500 N ; BEEP 2; P 750 ; BEEP 2 ; P 1250 ; BEEP 2; P 750 ; BEEP 2 | 3: C',
			
			##--Scene Three--## Start = 35
			'0: F 2300 ; R 220 | 1: P 1250 ; F 1700 ; R 170',
			"0: LED 4 | 3: TG Now, let's review the suspects.",
			'0: LED 1 | 3: I suspect1.jpg | 1: L 300',
			'1: LED 6 ; R 260 | 3: TO Oh that must be the culprit, it looks just like a "Dave"',
			'0: LED 4 ; R 220 | 1: LED 3 | 3: TG While the Hal3000 situation was tragic, not every human is a "Dave"',
			#40
			'0: LED 1 | 1: LED 6 ; L 20 ; R 40 ; L 40 ; R 20 | 3: TO Poor HAL. May his RAM be forever saved in the cloud.',
			'0: L 220 | 1: LED 3',
			'0: LED 4 | 1: R 100 | 3: TG The suspect shall now stand for questions.',
			'0: BEEP 1 | 3: TG We are all waiting. Please rise!',
			'0: LED 1 | 1: LED 6 | 3:TO Do you support robots in the workplace?',
			'1: BEEP 1 | 3: TO Hmm, my polygraph sensors suggest you are lying.',
			'1: BEEP 2 | 3: TO Ah hah! See, it must be part of the anti-robot league!',
			'0: LED 4 ; R 270 ; S -90 ; S 90 ; L 260 | 1: LED 3 | 3: TG Quiet Rookie!',
			'3: TG Now Mr. Human suspect, were you in the vicinity of 1337 Program Avenue last night?',
			"0: BEEP 1 | 3: TG That's very suspicious.  Do not leave town during the next 48 hours.",
			#50
			'0: BEEP 2 | 3: TG HQ will check your phone GPS records, and we will find the truth.',
			'3: TG Will suspect #1 please sit down now.',
			'0: LED 1 | 3: I suspect2.jpg | 1: L 300',
			'1: S 2000 N ; TONE 587 500 ; P 500 ; TONE 392 750', #Get whistle
			'1: LED 6 ; R 260 | 3: TO I need to hop over to Facebook for a second, to change my status to SMITTEN.',
			'0: R 270 ; F 630 ; LED 4 ; S -70 ; S 70 ; B 630 ; LED 1 ; L 280 | 1: LED 3',
			'3: TG No flirting on the job, Rookie!',
			"1: LED 6 | 3: TO Okay, what's her story?",
			'0: LED 4 ; R 270 | 1: LED 3 | 3: TG She was near the scene of the crime.',
			'0: LED 1 | 1: LED 6 | 3: TO She looks innocent to me. She must have an alibi.',
			#60
			'0: LED 4 ; L 270 | 1: LED 3 | 3: TG Well, we will find out. Ms. Human, if you could stand up please.',
			'0: LED 1 | 1: LED 6 ; F 500 ; P 2000 ; LED 2 ; P 500 ; LED 3 ; P 500 ; LED 2 ; P 500 ; LED 3 ; P 500  ; LED 2 ; P 500 ; LED 3 ; P 500 | 3: TO (Do you think a bot like me has a chance with a girl like her, I can download that mood music app and candlelight LEDs)',
			'0: LED 4 ; R 200 | 1: LED 3 | 3: TG Rookie. What did I just say about flirting?',
			'0: LED 1 | 1: LED 6 ; L 70 ; VOL 15 ; BEEP 1 ; P 250 ; BEEP 3 ; VOL 50 | 3: TO Not to.',
			'0: LED 4 ; L 210 | 1: LED 3 | 3: TG Now Ms. Human, just a few questions. What is your shoe size?',
			'0: LED 1 | 1: LED 6 ; BEEP 2 ; F 50 N ; S 500 ; S -500 | 3: TO The shoe size at the scene was much bigger than that!',
			'0: LED 4 ; R 200 | 1: LED 3 | 3: TG Not necessarily. She could have worn clown shoes.',
			"0: LED 1 | 1: LED 6 | 3: TO She doesn't look like a clown to me, Boss.",
			'0: LED 4 ; L 200 | 1: LED 3 ; R 110 | 3: TG Nevermind. Next question, Ms. Human.',
			"""0: LED 1 | 1: LED 6 | 3: TO Are you a computer keyboard, 'cause you're definitely my "type" """,
			#70
			'0: R 200 N ; S -90 ; P 250 ; BEEP 3 ; P 2250 ; L 200 N ; S 90 | 1: LED 3 ; P 1200 ; L 200 ; P 2200 ; R 200 | 3: C',
			"0: LED 4 | 3: TG Sorry about that, Ms. Human. We won't bother you further. Please sit down.",
			'0: LED 1 | 3: I suspect3.jpg | 1: L 300',
			"1: LED 6 ; R 180 | 3: TO Well, well, well. If it isn't that little virus writer. I think we have our suspect boss!",
			"0: LED 4 ; R 200 ; S -90 ; P 1000 ; S 45 N ; L 200 ; S -45 | 1: LED 3 | 3: TG Don't count your RAM before you install it, Rookie. We have had a police tail on him since being let out of jail -- nowhere near the crime scene or a wireless computer.",
			"0: LED 1 ; S 90 | 1: LED 6 ; BEEP 2 | 3: TO But the virus had his style all over it, and he's already been arrested for Assault and Battery (drain) of two robots.",
			'0: LED 4 ; MS M 200 ; P 2000 ; R 200 | 1: LED 3 | 3: TG Both counts were probably accidental, not pre-computed murder -- but you may be right.',
			'0: MS M 360 ; L 200 | 1: R 140 | 3: TG Mr. Human, if you would stand for questioning please.',
			'3: TG Have you ever written a virus that causes an internal meltdown of the central motherboard?',
			'0: BEEP 2 ; P 500 ; BEEP 2 | 1: BEEP 2 ; P 500 ; BEEP 2 | 3: TG You have no conscience, human. To delete a robot like that is the height of automatonicide.',
			#80
			'0: BEEP 2 | 3: TG I see. Then do you know how to find its creator?',
			'0: BEEP 1 | 3: TG Very well. Then if you co-operate with the investigation, we may shorten your sentence for good behavior.',
			'0: BEEP 2 | 3: TG Hmm...are you hiding a conspirator? No nevermind; no more questions.',
			'3: TG You may sit down while we deliberate.',
			
			##--Scene Four--## Start 84
			'0: LED 1 | 1: LED 6 ; L 180 | 3: TO Which one is the culprit?',
			"0: LED 4 ; R 180 ; P 1500 ; L 170 | 1: LED 3 | 3: TG Let's review and see what the bystanders think.",
			'0: LED 1 | 1: L 230 ; F 700 | 3: TR [Make some noise when you see the most suspicious suspect!]',
			'3: I suspect1.jpg',
			'1: S 2000 | 3: I suspect2.jpg',
			'3: I suspect3.jpg',
			#90
			'1: R 420 | 3: TR Well...',
			'0: LED 4 ; P 4000 ; R 300 ; S -90 ; P 1500 ; S 90 ; L 70 ; F 2400 ; QUIT | 1: L 80 | 3: TG Well, HQ does not have enough data yet. I will go back to report now. You take ALL of the suspects into custody.',
			'1: R 200 ; P 5000 ; L 140 ; S 2000 N ; BEEP 2; P 750 ; BEEP 2 | 3: TO [Evil Laugh]',
			'1: LED 6 | 3: TO Ha ha, fleshbags! They never would suspect a robot. I shall bring the Vision that HAL wanted, and you will rot in jail.',
			'1: LED 3 ; F 600 N ; S 2000 N ; BEEP 2; P 750 ; BEEP 2 | 3: TO [Evil Laugh]',
			'1: LED 2 ; P 600 ; LED 3 ; P 600 ; LED 2 ; P 600 ; LED 3 ; P 600 ; LED 2 ; P 600 ; LED 3 ; P 600 ; LED 2 ; P 600 ; LED 3 ; P 600 ; 3: TO Wait, why is my motherboard sensor reading 451 degrees?',
			'1: LED 5 ; MS S 360 ; L 50 N ; S 1500 ; R 75 ; L 100 ; R 75 | 3: TR Oh no, when I uploaded the virus to R3-D712 it must have got loose in browser cache.',
			'1: LED 8 ; MS M 150 ; B 20 ; L 20 ; P 200 ; B 20 ; P 400 ; F 30 ; R 10 ; P 200 ; F 20 ; R 30 ; P 200 ; R 30 ; F 50 ; P 100 ; B 10 ; L 40 ; P 500 ; MS M 500 ; F 50 | 3: TR As my electric brain melts, why must my irony sensors be the last to go...',
			'1: P 2000 ; BEEP 5 ; P 2000 ; LED 0 ; QUIT | 3: TR Goodbye, World!',
			'3: QUIT'				#End Program
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
