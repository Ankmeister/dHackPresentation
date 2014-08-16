# -*- coding: utf-8 -*-
import pygame
import argparse
from pygame.locals import FULLSCREEN
import pics
from time import sleep,time
from random import randint
from texts import *

parser = argparse.ArgumentParser(description='dHackpresentation')
parser.add_argument('--fullscreen', action='store_const', const=pygame.FULLSCREEN, default=0, help='Start in fullscreen')
args = parser.parse_args()

start_time = time()
pygame.init()
WIDTH = 1280
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH,HEIGHT), args.fullscreen)
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

def center_pic(pic, xoffset = 0, yoffset = 0):
	x = (WIDTH - pic.get_width() + xoffset) / 2
	y = (HEIGHT - pic.get_height() + yoffset) / 2
	return (x,y)

def delete_random_letter(l, count):
	if count == 0:
		return
	#Don't pop from empty lists
	indices = [l.index(i) for i in l if len(i) != 0]
	l[indices[randint(0,len(indices) - 1)]].pop()
	delete_random_letter(l, count - 1)
	
def draw_ascii_pictures(text, (x, y), font=monospace6):
	"""Draws asciipicture one letter at a time"""
	dickbutt = [0]*len(text)
	rowIndices = range(len(text))
	while rowIndices:
		index = randint(0, len(rowIndices)-1)
		letterToRender = "".join(text[index][dickbutt[index]])
		screen.blit(font.render(letterToRender ,1, ORANGE),(x+font.size(text[0][0])[0]*dickbutt[index],y+font.get_height()*rowIndices[index]))
		screen.blit(font.render(letterToRender ,1, ORANGE),(x+font.size(text[0][0])[0]*dickbutt[index],y+font.get_height()*rowIndices[index]))
		screen.blit(font.render(letterToRender ,1, ORANGE),(x+font.size(text[0][0])[0]*dickbutt[index],y+font.get_height()*rowIndices[index]))
		dickbutt[index] += 1
		if dickbutt[index] == len(text[0])-1:
			rowIndices.pop(index)
			dickbutt.pop(index)
		pygame.display.flip()
	
		

def blit_asciipic(asciipic, (x,y),font=monospace6):
	for i in asciipic:
		screen.blit(font.render("".join(i),1, ORANGE),(x,y))
		y += font.get_height()


def fade_in(pic,pos):
	for t in range(100):
		pic.set_alpha(t)
		screen.blit(pic,pos)
		pygame.display.flip()
	sleep(1)

def fade_to_black():
	blackground = pygame.Surface(screen.get_size())
	for i in range(100): #apparantly, 100 is enough.
		blackground.set_alpha(i)
		screen.blit(blackground,(0,0))
		pygame.display.flip()

def fade_pic_to_ascii(pic,asciipic,pos):
	fade_in(pic,pos)
	for t in range(255,0,-2):
		screen.fill(BLACK)
		blit_asciipic(asciipic,pos)
		pic.set_alpha(t)
		screen.blit(pic, pos)
		pygame.display.flip()

def from_asciipic_to_realtext(pic,asciipic, text, (textx, texty), asciipos, font=monospace20):
	"""For a printed asciipicture, this function animates the asciipicture into text (by deleting letters from asciipic),
	and then fades back the given picture (pic) at the position of the old asciipic"""
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
			
			screen.blit(monospace20.render(text[i][:j+1], 1, ORANGE), (textx,texty + font.get_height()*i))
			delete_random_letter(asciipic, ratio)
			blit_asciipic(asciipic, asciipos)
			pygame.display.flip()
			sleep(0.01)
		i+=1

	#clear asciipic completely when text is done (because of integer-ratio)
	screen.blit(blackground, asciipos)
	pygame.display.flip()

	fade_in(pic,asciipos)
	fade_to_black()
	
	
def asciipic_to_real_pic(pic,asciipic, picpos):
	"""Animates an asciipic by writing one letter at a time, and then fades the finished asciipicture into pic"""
	draw_ascii_pictures(asciipic,picpos)
	fade_in(pic, picpos)
	fade_to_black()

def fade_pic_to_real_text(pic, asciipic, picpos, text, textpos):
	fade_pic_to_ascii(pic,asciipic, picpos)
	from_asciipic_to_realtext(pic, asciipic, text, textpos, picpos)

	

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

	fade_pic_to_real_text(haggepic, hagge, center_pic(haggepic), hagge_text, (234, 700))

	fade_pic_to_real_text(ninjapic, ninja, center_pic(ninjapic, 0, -150), ninja_text, (100,650))

	fade_pic_to_real_text(skurkpic, skurk, center_pic(skurkpic), skurk_text, (234, 650))

	fade_pic_to_real_text(mortpic, mort, center_pic(mortpic), mort_text, (277,700))

	asciipic_to_real_pic(dHack, logo, center_pic(dHack))

	print time() - start_time


if __name__=="__main__":
	main()
