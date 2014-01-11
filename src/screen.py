#!/usr/bin/env python

##-- Zachary Trette & Michael duPont
##-- Accepts commands for screen responses
##-- EV3- Remote - https://github.com/flyinactor91/EV3-Remote

## 2014-01-11

# Available Commands:
#     Text:    T(R/O/Y/G/B/P/def=W) text
#     Image:   I fileName
#     Clear:   C
#     Quit:    QUIT

# Example Command: TG Hello World!
# Text color determined by letter following T (default is white)

import os , pygame
from pygame.locals import *
from PIL import Image

class screen:
	
	#Default colors match those available as EV3 LED choices
	#Add custom RGB colors here
	colorLib = { 'N' : (0,0,0) , 'W' : (255,255,255) , 'R' : (255,0,0) , 'O' : (255,115,0) , 'Y' : (255,255,0) , 'G' : (0,255,0) , 'B' : (0,0,255) , 'P' : (139,0,204)}
	
	def __init__(self , width , height , font_size = 128):
		"""Init window: screen(width , height [, font_size])
		"""
		pygame.init()
		self.size = (width , height)
		self.fontSize = font_size
		self.resize = 0.9 #Alter this value to adjust text width relative to window width
		self.win = pygame.display.set_mode(self.size,HWSURFACE|DOUBLEBUF|RESIZABLE)

	def clearWin(self):
		"""Clear text or image from screen
		"""
		self.win.fill(self.colorLib['N'])
		pygame.display.flip()

	def showText(self , txt , txtColor = 'W'):
		"""Display text in window
		"""
		self.clearWin()
		basicfont = pygame.font.SysFont(None, self.fontSize)
		w, h = basicfont.size(txt) #get dimensions of font
		lines = self.__wrapline(txt,basicfont,self.size[0]*self.resize) #gets lines of text that will be put up with text wraping engaged
		for x in range(0,len(lines)): #places all lines on screen with text wrapping
			text = basicfont.render(lines[x] , True , self.colorLib[txtColor], (0,0,0))
			textRect = text.get_rect()
			textRect.centerx = self.size[0]/2
			#Determine line height: (center of line) = (middle of window) - (distance to center of first line) + (distance to center of current line from first line)
			textRect.centery = (self.size[1]/2) - ((len(lines)-1)*h/2) + (h * x)
			self.win.blit(text , textRect)
		pygame.display.update() #updates window all at once
		##--Un-comment the next three lines to enable text-to-speach----##
		#if txtColor == 'R': os.system('espeak -ven-us+m1 """'+txt+'"""')
		#elif txtColor == 'G': os.system('espeak -ven-us+f3 """'+txt+'"""')
		#elif txtColor == 'O': os.system('espeak -ven-sc+m7 """'+txt+'"""')
		##--------------------------------------------------------------##

	def showImg(self , fName):
		"""Display image in window
		Supported formats: JPG, PNG, GIF (non animated), BMP, PCX,
		TGA (uncompressed), TIF, LBM (and PBM), PBM (and PGM, PPM), XPM
		Images that are 24-bit or 32-bit are smooth-scaled
		"""
		if os.path.isfile(fName):
			self.clearWin()
			img = pygame.image.load(fName)
			imgPIL = Image.open(fName)
			scnW , scnH = self.size
			imgW , imgH = imgPIL.size
			scnRatio = 1.0*scnW/scnH
			imgRatio = 1.0*imgW/imgH
			#32 and 24 bit file formats for smoothscale
			if imgPIL.mode in ['RGB' , 'RGBA' , 'CMYK' , 'YCbCr' , 'I' , 'F']:
				#Bounded by screen height
				if scnRatio >= imgRatio: self.win.blit(pygame.transform.smoothscale(img, (int(scnH*imgRatio),scnH)) , (int(scnW/2-scnH*imgRatio/2),0))
				#Bounded by screen width
				else: self.win.blit(pygame.transform.smoothscale(img, (scnW,int(scnW/imgRatio))) , (0,int(scnH/2-(scnW/imgRatio)/2)))
			#Else use scale, likely to cause pixelation
			else:
				if scnRatio > imgRatio: self.win.blit(pygame.transform.scale(img, (int(scnH*imgRatio),scnH)) , (int(scnW/2-scnH*imgRatio/2),0))
				else: self.win.blit(pygame.transform.scale(img, (scnW,int(scnW/imgRatio))) , (0,int(scnH/2-(scnW/imgRatio)/2)))
			pygame.display.flip()
		else: print 'File not found: ' + fName
	
	def setFontSize(self , newSize):
		"""Change font size for next line of text written to the window
		"""
		self.fontSize = newSize
	
	def setTextBuffer(size_multiplier = 0.9):
		"""Change font width multiplier for text in the window
		Should be used if window is resized after created
		"""
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
	import sys
	from socket import *
	port = 5678
	defaultTimeout = 5
	screenWidth = 800 #1920 (16:9 1080p)
	screenHeight = 500 #1080
	
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
			if msg[0] == 'T':
				if msg[1] == ' ': disp.showText(msg[2:].strip())
				else: disp.showText(msg[2:].strip(),msg[1].upper())
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
