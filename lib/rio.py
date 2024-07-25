import pygame
import numpy as np
from lib import rmath
from lib import utils as utl

pygame.font.init()


def load_font(name="Consolas", size=14, system_font=True):
	if system_font:
		return pygame.font.SysFont(name, size)
	else:
		return pygame.font.Font(name, size)


def genarate_pseudo_bold_text(font, text, color=(0, 255, 70), offset=1):
	width, height = font.render(text, True, color).get_size()
	
	bold_surface = pygame.Surface((width + offset, height + offset)).convert_alpha()
	bold_surface.fill((0, 0, 0, 0))
	
	# drawing the text multiple time
	for dx in range(-offset, offset):
		for dy in range(-offset,  offset + 1):
			bold_surface.blit(font.render(text, True, color), (dx, dy))
	
	return bold_surface

# *******************************************************************
# --------------------- Simple Printing Options ----------------------
# *******************************************************************

FONT_OPT = {
	"name" : "Consolas",
	"size" : 14,
	"color" : (0, 0, 0)
}

RIOFONT = pygame.font.SysFont(FONT_OPT['name'], FONT_OPT['size'])
def fontColor(color):
	global FONT_OPT
	FONT_OPT["color"] = color

def fontSize(size):
	global FONT_OPT, RIOFONT
	FONT_OPT["size"] = size
	RIOFONT = pygame.font.SysFont(FONT_OPT['name'], FONT_OPT['size'])
	
def println(surface, txt, pos = (100,100)):
	global RIOFONT
	txt = RIOFONT.render(txt, True, FONT_OPT["color"])
	surface.surface.blit(txt, pos)

# *******************************************************************
# ----------------------- input Box Class ------------------------
# *******************************************************************

class InputBox():
	"""docstring for InputBox"""
	# border = (color, border_width)
	# font = (name, size)
	def __init__(self, surface, box_info, /, *, 
		font_name='Consolas', font_size=14,	  
		font_color=(0, 0, 0), bg_color=(255, 255, 255), 
		border_width=1
	) -> None:
		"""
		Parameters:
		box_info : tuple(x, y, w, h) of box position ans size
		font : a font object of pygame
		"""
		self.surface = surface
		self.font_color = font_color
		self.box_info = box_info
		self.border_width = border_width
		self.box_bg_color = bg_color
		
		self.font_name = font_name
		self.font_height = font_size
		self.font = load_font(self.font_name, self.font_height)
		self.font_width = self.font.size('a')[0]
		self.font_y_margin = box_info[1] + (box_info[3] - self.font_height)//2
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
		
	@staticmethod
	def process_cmd(text, delim='='):
		text = text.split(delim)
		return [s.strip() for s in text]

	def changeFont(self, font_name, size): ...

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
		if self.focused:
			if not self.__onfocus_using_colon:
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
		else:
			self.is_focused(event)
			

	def getInput(self):
		command = False
		if not self.focused and self.triggered:
			command = self.buffer
			self.triggered = False
		
		return command

	def show(self):
		pygame.draw.rect(self.surface.surface, self.box_bg_color, self.box_info)
		if len(self.buffer) == 0:
			txt = self.holder["text"]
		else:
			txt = ''.join(self.buffer)
		text = self.font.render(txt, True, self.font_color)
		
		# blinking cursor
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




# *******************************************************************
# --------------------------- Slidder Class -------------------------
# *******************************************************************

class Slider:
	def __init__(self, surface, minValue, maxValue, currentValue, 
		x=0, y=0, w=100, h=2, r=8,
		bar_color = (255, 255, 255), 
		circle_color = (255, 0, 0)			  
	) -> None:
		self.surface = surface
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.r = r
		self.offset = x
		self.value = currentValue
		self.min_value = minValue
		self.max_value = maxValue
		self.is_focused = False

		self.bar_color = bar_color
		self.circle_color = circle_color

		self.setValue(currentValue)

	
	def getValue(self):
		value = rmath.linear_map(
			self.offset,
			self.x, self.x + self.w,
			self.min_value, self.max_value
		)
		return value
	
	def setValue(self, value):
		if value < self.min_value:
			value = self.min_value
		elif value > self.max_value:
			value = self.max_value
		
		offset = rmath.linear_map(
			value,
			self.min_value, self.max_value,
			self.x, self.x + self.w
		)

		self.offset = offset


	def update(self, event):
		mx, my = utl.mouse() - self.surface.pos
		x1 = self.offset
		y1 = self.y
		
		if event.type == pygame.MOUSEBUTTONUP:
			self.is_focused = False

		if not self.is_focused:
			dist = np.linalg.norm((mx-x1, my-y1))
			if dist < self.r:
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.is_focused = True

		else:
			val = mx - self.x
			if val > self.w:
				val = self.w
			elif val < 0:
				val = 0

			self.offset = val + self.x

			self.value = self.getValue()


	def show(self, x=None, y=None):
		self.x = x if x else self.x
		self.y = y if y else self.y
		self.setValue(self.value)

		pygame.draw.rect(
			self.surface.surface, self.bar_color, 
			(self.x, self.y, self.w, self.h)
		)
		pygame.draw.circle(
			self.surface.surface, self.circle_color, 
			(self.offset, self.y + self.h//2), self.r
		)
