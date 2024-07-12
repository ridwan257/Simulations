from tkinter import font
from traceback import print_tb
from turtle import pos
import pygame
from setuptools import Command
from lib import utils as utl

class InputBox():
	"""docstring for InputBox"""
	# border = (color, border_width)
	# font = (name, size)
	def __init__(self, surface, font, font_color, box_bg_color, box_info, border):
		"""
		Parameters:
		box_info : tuple(x, y, w, h) of box position ans size
		"""
		self.surface = surface
		self.font_color = font_color
		self.box_info = box_info
		self.border = border
		self.box_bg_color = box_bg_color
		
		self.font = font
		self.font_width = font.size('a')[0]
		self.font_height = font.size('a')[1]
		self.font_y_margin = box_info[1] + (box_info[3] - font.get_height())//2
		self.font_x_margin = box_info[0] + 10

		self.buffer = ''
		self.buffer_length = 0
		self.holder = { "text" : "Type here...", "color": (51,51,51)}
		self.focused = False
		self.triggered = False
		self.text = ''
		self.cursor = {"color": (0,0,0), "w": 5, "h":3, "blink": 20}
		self.__counter = 0
		self.__onfocus_using_colon = False
		

	def font_size(self, size):
		pass

	def is_focused(self, event):
		mx, my = utl.mouse() - self.surface.pos
		x1, y1, w, h = self.box_info
		x2, y2 = w + x1, h + y1
		if event.type == pygame.MOUSEBUTTONDOWN:
			if mx > x1 and mx < x2 and my > y1 and my < y2:
				self.focused = True
				self.triggered = False
			else:
				self.focused = False
		if event.type == pygame.KEYDOWN and not self.focused:
			if event.key == pygame.K_SEMICOLON and pygame.key.get_mods() & pygame.KMOD_SHIFT:
				self.focused = True
				self.triggered = False
				self.__onfocus_using_colon = True
			

	def update(self, event):
		if self.focused and not self.__onfocus_using_colon:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.focused = False
				elif event.key == pygame.K_RETURN:
					self.triggered = True
					self.focused = False
				elif event.key == pygame.K_BACKSPACE:
					self.buffer = self.buffer[:-1]
				else:
					self.buffer += event.unicode
		
		else:
			self.__onfocus_using_colon = False
			

	def show(self):
		command = False
		if not self.focused and self.triggered:
			command = self.buffer
			self.triggered = False
		
		pygame.draw.rect(self.surface.surface, self.box_bg_color, self.box_info)
		if len(self.buffer) == 0:
			txt = self.holder["text"]
		else:
			txt = ''.join(self.buffer)
		text = self.font.render(txt, True, self.font_color)
		
		if self.focused:
			if self.__counter < self.cursor['blink']//2:
				buffer_len = len(self.buffer)
				x = self.font_x_margin + buffer_len * self.font_width
				# print(self.font.size(self.buffer)[0])
				start_pos = (x, self.font_y_margin)
				end_pos = (x, self.font_y_margin + self.font_height)
				pygame.draw.line(self.surface.surface, self.cursor['color'], start_pos, end_pos)
			elif self.__counter > self.cursor['blink']:
				self.__counter = 0
			self.__counter += 1

		self.surface.surface.blit(text, (self.font_x_margin, self.font_y_margin))
		
		return command

		
FONT = {
	"name" : "Consolas",
	"size" : 14,
	"color" : (0, 0, 0)
}		


def println(surface, txt, pos = (100,100), **font_info):
	name = font_info.get("name", "Consolas")
	size = font_info.get("size", 14)
	color = font_info.get("color", (0,0,0))
	pygame.font.init()
	font = pygame.font.SysFont(name, size)
	txt = font.render(txt, True, color)
	surface.surface.blit(txt, pos)
	# pygame.font.quit()

