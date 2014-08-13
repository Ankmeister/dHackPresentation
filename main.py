# -*- coding: utf-8 -*-
import pygame
from pygame.locals import FULLSCREEN
import pics
from time import sleep
from random import randint
from texts import *

pygame.init()
WIDTH = 1280
HEIGHT = 800
BLACK = (0,0,0)
ORANGE = (255,102,0)
pygame.mixer.pre_init(44100, -16, 2, 2048) 
pygame.mixer.music.load('mindhest.ogg')
screen = pygame.display.set_mode((WIDTH,HEIGHT))
monospace10 = pygame.font.SysFont("monospace", 10)
monospace20 = pygame.font.SysFont("monospace", 20)
dHack = pygame.transform.scale(pygame.image.load('dhack.png'), (432,432)).convert()
mortpic = pygame.transform.scale(pygame.image.load('mort.jpg'), (726,586)).convert()
ninjapic = pygame.transform.scale(pygame.image.load('ninja.jpg'), (812,540)).convert()
skurkpic = pygame.transform.scale(pygame.image.load('booby.jpg'), (812,612)).convert()
haggepic = pygame.transform.scale(pygame.image.load('ingencd.png'), (394,635)).convert()

logo = pics.logo
mort = pics.mort
skurk = pics.skurk
ninja = pics.ninja
hagge = pics.hagge


def delete_random_letter(l, count):
	if count == 0:
		return
	#Don't pop from empty lists
	indices = [l.index(i) for i in l if len(i) != 0]
	l[indices[randint(0,len(indices) - 1)]].pop()
	delete_random_letter(l, count - 1)

def print_asciipic(asciipic, (x,y)):
	for i in asciipic:
		screen.blit(monospace10.render("".join(i),1, ORANGE),(x,y))
		y += 12



def fade_in(pic,pos):
	for t in range(255):
		pic.set_alpha(t)
		screen.blit(pic,pos)
		pygame.display.flip()
	sleep(2)

def fade_to_black():
	blackground = pygame.Surface(screen.get_size())
	for i in range(255):
		blackground.set_alpha(i)
		screen.blit(blackground,(0,0))
		pygame.display.flip()

def fade_pic_to_ascii(pic,asciipic,pos, initdelay = 0):
	fade_in(pic,pos)
	for t in range(255,0,-1):
		screen.fill(BLACK)
		print_asciipic(asciipic,pos)
		pic.set_alpha(t)
		screen.blit(pic, pos)
		pygame.display.flip()
		sleep(initdelay)
		initdelay = 0
	sleep(0.5)

def from_asciipic_to_realtext(pic, asciipic, text, (textx, texty), asciipos, fade_back = False):
	#unfortinately, there's no (straight-forward) way of finding out how big the asciipic is,
	#therefore, the real picture is needed as an argument as well, to determine 
	#what size of the sceen to clear
	total_letters_in_ascii = len(asciipic[0]) * len(asciipic)
	total_letters_in_text = sum([len(a) for a in text])
	ratio = total_letters_in_ascii/total_letters_in_text #integerratio is good enough

	i = 0
	while (i < len(text)):
		for j in range(len(text[i])):
			#Clear asciipic every frame, but leave the text visible
			blackground = pygame.Surface(pic.get_size())
			blackground.fill(BLACK)
			screen.blit(blackground, asciipos)
			
			screen.blit(monospace20.render(text[i][:j+1], 1, ORANGE), (textx,texty + 20*i))
			delete_random_letter(asciipic, ratio)
			print_asciipic(asciipic, asciipos)
			pygame.display.flip()
			sleep(0.06)
		i+=1
	#clear asciipic completely when text is done (because of integer-ratio)
	screen.blit(blackground, asciipos)
	pygame.display.flip()

	if fade_back:
		fade_in(pic,asciipos)
	fade_to_black()
	
	
	

def main():
	pygame.mixer.music.play(-1)
	test = pygame.image.load('gruppfoto.png')

	fade_pic_to_ascii(dHack, logo, (450,200), 4)
	from_asciipic_to_realtext(dHack, logo, intro_text, (2, 100), (450,200))

	fade_pic_to_ascii(haggepic, hagge, (443,0),0.5)
	from_asciipic_to_realtext(haggepic, hagge, hagge_text, (234, 650), (443,0), True)

	fade_pic_to_ascii(ninjapic, ninja, (234,40),0.5)
	from_asciipic_to_realtext(ninjapic, ninja, ninja_text, (234, 650), (234,40), True)

	fade_pic_to_ascii(skurkpic, skurk, (234,40),0.5)
	from_asciipic_to_realtext(skurkpic, skurk, skurk_text, (234, 650), (234,40), True)

	fade_pic_to_ascii(mortpic, mort, (277, 40),0.5)
	from_asciipic_to_realtext(mortpic, mort, mort_text, (277,650), (277,40), True)


if __name__=="__main__":
	main()
