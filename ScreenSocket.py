#!/usr/bin/env python

##--Zachary Trette
##-- accepts commands for screen responses
##-- EV3- Remote - https://github.com/flyinactor91/EV3-Remote

## 2013-12-1

from socket import *
import sys, os
import pygame
from pygame.locals import *

def setup():
    pygame.init()
    w = 640
    h = 480
    size=(w,h)
    screen = pygame.display.set_mode(size,HWSURFACE|DOUBLEBUF|RESIZABLE)
    return screen, size


def runCue(SorI, strOrImage):
    if SorI == "I":
        im = pygame.image.load(strOrImage)
        scrn.blit(pygame.transform.scale(im,size),(0,0))
	pygame.display.flip()	
    elif SorI == "T":
	basicfont = pygame.font.SysFont(None, 48)
	text = basicfont.render(strOrImage, True, (255, 0, 0), (0, 0, 0))
	textrect = text.get_rect()
	textrect.centerx = scrn.get_rect().centerx
	textrect.centery = scrn.get_rect().centery
	scrn.fill((0,0,0))
	scrn.blit(text, textrect)
	pygame.display.flip()
    elif SorI == "C":
	basicfont = pygame.font.SysFont(None, 48)
	text = basicfont.render("", True, (0, 0, 0), (0, 0, 0))
	textrect = text.get_rect()
	textrect.centerx = scrn.get_rect().centerx
	textrect.centery = scrn.get_rect().centery
	scrn.fill((0,0,0))
	scrn.blit(text, textrect)
	pygame.display.flip()


TCP_PORT = 5678
defaultTimeout = 5
if len(sys.argv) == 2:
	TCP_IP = sys.argv[1]

BUFFER_SIZE = 1024
screenSocket = socket(AF_INET, SOCK_STREAM)
screenSocket.bind(('' , TCP_PORT))
screenSocket.listen(1)
dne = False
scrn, size = setup()
while not dne:
	connectionSocket , addr = screenSocket.accept()
	connectionSocket.settimeout(defaultTimeout)
	msg = connectionSocket.recv(BUFFER_SIZE)
        msg = msg.strip()
	if msg == 'QUIT':
		print "DONE"
		dne = True
	else:	
		t = msg[0]
		s = msg[1:].strip()
		runCue(t,s)
	
	#connectionSocket.send()
	connectionSocket.close()

screenSocket.close()




    
