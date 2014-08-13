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
screen = pygame.display.set_mode((WIDTH,HEIGHT))
BLACK = (0,0,0)
ORANGE = (255,102,0)
pygame.mixer.pre_init(44100, -16, 2, 2048) 
pygame.mixer.music.load('mindhest.ogg')
monospace6 = pygame.font.SysFont("monospace", 6)
monospace10 = pygame.font.SysFont("monospace", 10)
monospace20 = pygame.font.SysFont("monospace", 20)


def get_picsize_from_asciipic(asciipic, font=monospace6):
	size = font.size(''.join(asciipic[0]))
	height = len(asciipic) * size[1]
	return (size[0], height)


def delete_random_letter(l, count):
	if count == 0:
		return
	#Don't pop from empty lists
	indices = [l.index(i) for i in l if len(i) != 0]
	l[indices[randint(0,len(indices) - 1)]].pop()
	delete_random_letter(l, count - 1)

def print_asciipic(asciipic, (x,y), font=monospace6):
	for i in asciipic:
		screen.blit(font.render("".join(i),1, ORANGE),(x,y))
		y += font.get_height()


def fade_in(pic,pos):
	for t in range(255):
		pic.set_alpha(t)
		screen.blit(pic,pos)
		pygame.display.flip()
	sleep(1)

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

def from_asciipic_to_realtext(pic,asciipic, text, (textx, texty), asciipos):
	total_letters_in_ascii = len(asciipic[0]) * len(asciipic)
	total_letters_in_text = sum([len(a) for a in text])
	ratio = total_letters_in_ascii/total_letters_in_text #integer-ratio is good enough
	blackground = pygame.Surface(pic.get_size())

	i = 0
	while (i < len(text)):
		for j in range(len(text[i])):
			#Clear asciipic every frame, but leave the text visible
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

	fade_in(pic,asciipos)
	fade_to_black()
	
	
	

def main():
	logo = pics.logo
	mort = pics.mort
	skurk = pics.skurk
	ninja = pics.ninja
	hagge = pics.hagge

	dHack = pygame.transform.scale(pygame.image.load('dhack.png'), (get_picsize_from_asciipic(logo))).convert()
	mortpic = pygame.transform.scale(pygame.image.load('mort.jpg'), (get_picsize_from_asciipic(mort))).convert()
	ninjapic = pygame.transform.scale(pygame.image.load('ninja.jpg'), (get_picsize_from_asciipic(ninja))).convert()
	skurkpic = pygame.transform.scale(pygame.image.load('booby.jpg'), (get_picsize_from_asciipic(skurk))).convert()
	haggepic = pygame.transform.scale(pygame.image.load('ingencd.png'), (get_picsize_from_asciipic(hagge))).convert()

	pygame.mixer.music.play(-1)

	print get_picsize_from_asciipic(logo)
	fade_pic_to_ascii(dHack, logo, (318, 106))
	from_asciipic_to_realtext(dHack,logo, intro_text, (2, 100), (318,106))

	fade_pic_to_ascii(haggepic, hagge, (443,0))
	from_asciipic_to_realtext(haggepic, hagge, hagge_text, (234, 650), (443,0))

	fade_pic_to_ascii(ninjapic, ninja, (234,40))
	from_asciipic_to_realtext(ninjapic,ninja, ninja_text, (234, 650), (234,40))

	fade_pic_to_ascii(skurkpic, skurk, (234,40))
	from_asciipic_to_realtext(skurkpic, skurk, skurk_text, (234, 650), (234,40))

	fade_pic_to_ascii(mortpic, mort, (277, 40))
	from_asciipic_to_realtext(mortpic, mort, mort_text, (277,650), (277,40))


if __name__=="__main__":
	main()
