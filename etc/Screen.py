#!/usr/bin/env python

##-- Zachary Trette & Michael duPont
##-- Accepts commands for screen responses
##-- EV3- Remote - https://github.com/flyinactor91/EV3-Remote

## 2014-01-01

# Available Commands:
#     Text:    T[R/G/O] text
#     Image:   I fileName
#     Clear:   C
#     Quit:    QUIT

# Example Command: TG Hello World!
# Text color determined by letter following T (red, green, orange)

import os , pygame , sys
from socket import *
from pygame.locals import *

port = 5678
defaultTimeout = 5
screenWidth = 1920
screenHeight = 1080

class screen:
	
	#Default colors match those available as EV3 LED choices
	#Add custom RGB colors here
	colorLib = { 'B' : (0,0,0) , 'W' : (255,255,255) , 'R' : (255,0,0) , 'G' : (0,255,0) , 'O' : (255,115,0) }
	
	def __init__(self , width , height , font_size = 128):
		"""Init window: screen(width , height [, font_size])"""
		pygame.init()
		self.size = (width , height)
		self.fontSize = font_size
		self.resize = 1 #Alter this value to adjust text width relative to window width
		self.win = pygame.display.set_mode(self.size,HWSURFACE|DOUBLEBUF|RESIZABLE)

	def clearWin(self):
		"""Clear text or image from screen"""
		self.win.fill(self.colorLib['B'])
		pygame.display.flip()

	def showText(self , txt , txtColor = 'W'):
		"""Display text in window"""
		self.clearWin()
		basicfont = pygame.font.SysFont(None, self.fontSize)
		w, h = basicfont.size(txt) #get dimensions of font
		lines = self.__wrapline(txt,basicfont,self.size[1]*self.resize) #gets lines of text that will be put up with text wraping engaged
		for x in range(0,len(lines)): #places all lines on screen with text wrapping
			text = basicfont.render(lines[x] , True , self.colorLib[txtColor], (0,0,0))
			textRect = text.get_rect()
			textRect.centerx = self.win.get_rect().centerx
			textRect.centery = self.size[1]/3 + h * x # used to determine where to place the letters so that they aren't on top of each other, also starts text 1/3 down screen.
			self.win.blit(text , textRect)
		pygame.display.update() #updates window all at once
		##--Un-comment the next three lines to enable text-to-speach----##
		#if txtColor == 'R': os.system('espeak -ven-us+m1 """'+txt+'"""')
		#elif txtColor == 'G': os.system('espeak -ven-us+f3 """'+txt+'"""')
		#elif txtColor == 'O': os.system('espeak -ven-sc+m7 """'+txt+'"""')
		##--------------------------------------------------------------##

	def showImg(self , fName):
		"""Display vertical 4x3 image in window
		Supported formats: JPG, PNG, GIF (non animated), BMP, PCX, TGA (uncompressed),
		TIF, LBM (and PBM), PBM (and PGM, PPM), XPM"""
		self.clearWin()
		if os.path.isfile(fName):
			img = pygame.image.load(fName)
			w , h = self.size
			imgW = h*3/4
			self.win.blit(pygame.transform.scale(img, (imgW,h)) , (w/2-imgW/2,0))
			pygame.display.flip()
		else: print 'File not found: ' + fName
	
	def setFontSize(self , newSize):
		"""Change font size for next line of text written to the window"""
		self.fontSize = newSize
	
	def setTextResize(size_multiplier = 1):
		"""Change font width multiplier for text in the window
		Should be used if window is resized after created"""
		self.resize = size_multiplier

	def __truncline(self , text , font , maxwidth):
		real=len(text)
		stext=text
		l=font.size(text)[0]
		cut=0
		a=0
		done=1
		while l > maxwidth:
			a += 1
			n=text.rsplit(None, a)[0]
			if stext == n:
				cut += 1
				stext= n[:-cut]
			else: stext = n
			l=font.size(stext)[0]
			real=len(stext)
			done=0
		return real, done, stext

	def __wrapline(self , text , font , maxwidth):
		done=0
		wrapped=[]
		while not done:
			nl, done, stext=self.__truncline(text, font, maxwidth)
			wrapped.append(stext.strip())
			text=text[nl:]
		return wrapped

def main():
	fromClient = True
	#If recieving commands from the terminal
	if len(sys.argv) > 1 and sys.argv[1] == '-t':
		fromClient = False
	#If recieving commands from the controller
	else:
		#Init socket
		screenSocket = socket(AF_INET, SOCK_STREAM)
		screenSocket.bind(('' , port))
		screenSocket.listen(1)

	#Create screen
	disp = screen(screenWidth , screenHeight) #Set window dimentions here
	quitFlag = False
	while not quitFlag:
		#Recieve connection / command
		if fromClient:
			connectionSocket , addr = screenSocket.accept()
			connectionSocket.settimeout(defaultTimeout)
			msg = connectionSocket.recv(1024).strip()
		else:
			msg = raw_input('Command: ').strip()
		#Command ident
		try:
			#Text
			if msg[0] == 'T': disp.showText(msg[2:].strip(),msg[1].upper())
			#Image
			elif msg[0] == 'I': disp.showImg(msg[1:].strip())
			#Clear
			elif msg[0] == 'C': disp.clearWin()
			#Quit
			elif msg == 'QUIT': quitFlag = True
			#Catch
			else: print 'Not a valid command'
		except:
			print 'Command error'
		if fromClient:
			#Close connection
			connectionSocket.close()
	if fromClient:
		#Close socket
		screenSocket.close()


if __name__ == '__main__':
        main()
