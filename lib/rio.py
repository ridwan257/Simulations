from typing import Union
import pygame
import numpy as np
from lib import frame, rmath
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
def setBold(state):
	global RIOFONT
	RIOFONT.set_bold(state)
	
def fontColor(color):
	global FONT_OPT, RIOFONT
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
		border_color = (0, 0, 0),
		border_width=1, holder = 'Type here...',
		colon_focus = True
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
		self.border_color = border_color
		
		self.font_name = font_name
		self.font_height = font_size
		self.font = load_font(self.font_name, self.font_height)
		self.font_width = self.font.size('a')[0]
		self.font_y_margin = box_info[1] + (box_info[3] - self.font_height)//2
		self.font_x_margin = box_info[0] + 10

		self.buffer = ''
		self.buffer_length = 0
		self.holder = { "text" : holder, "color": (51,51,51)}
		self.focused = False
		self.triggered = False
		self.text = ''
		self.cursor = {"color": (0,0,0), "w": 5, "h":3, "blink": 20}
		self.__counter = 0
		self.__onfocus_using_colon = True
		self.__colon_focus = colon_focus
		
	@staticmethod
	def process_cmd(text, delim='='):
		text = text.split(delim)
		return [s.strip() for s in text]

	def changeFont(self, font_name, size): ...


	def _is_focused(self, event):
		mx, my = utl.mouse() - self.surface.pos
		x1, y1, w, h = self.box_info
		x2, y2 = w + x1, h + y1
		if event.type == pygame.MOUSEBUTTONDOWN:
			if mx > x1 and mx < x2 and my > y1 and my < y2:
				self.focused = True
				self.triggered = False
			else:
				self.focused = False
		

		if event.type == pygame.KEYDOWN and not self.focused and self.__colon_focus:
			if event.key == pygame.K_SEMICOLON and pygame.key.get_mods() & pygame.KMOD_SHIFT:
				self.focused = True
				self.triggered = False
				self.__onfocus_using_colon = True
			

	def update(self, event):
		self._is_focused(event)
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

	def getInput(self):
		command = False
		if not self.focused and self.triggered:
			command = self.buffer
			self.triggered = False
		
		return command

	def setValue(self, text):
		self.buffer = str(text)
	
	def getValue(self):
		return self.buffer

	def show(self):
		pygame.draw.rect(self.surface.surface, self.box_bg_color, self.box_info)
		pygame.draw.rect(self.surface.surface, self.border_color, self.box_info, self.border_width)
		
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
		self.is_triggered = False

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

	def triggered(self):
		if self.is_triggered:
			self.is_triggered = False
			return True

		return False

	def focused(self):
		return self.is_focused

	
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
			if self.is_focused:
				self.is_triggered = True
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

		# print(self.is_focused, self.is_triggered)


# *******************************************************************
# ----------------------------- Button Class -------------------------
# *******************************************************************

class Button:
	def __init__(
		self, screen, button_info, value, /, *,
		bg_color = (105, 206, 235, 100), border_color = (0, 0, 0),
		border_width = 1, border_radius = 8,
		font_color = (0, 0, 0), size = 14, bold = False
		
	) -> None:
		self.screen = screen
		self.x, self.y, self.w, self.h = button_info
		self._button_surface = frame.createSurface(self.w, self.h)

		self._properties = {
			'value' : value,
			'bg_color' : bg_color, 
			'border_color' : border_color,
			'border_width' : border_width, 
			'border_radius' : border_radius,
			'font_color' : font_color, 
			'size' : size,
			'bold' : bold,
			'show_border' : True
		}

		self.__default_properties = self._properties.copy()
		self._hover_properties = self._properties.copy()

		self.focused = False
		self.triggered = False
		self.hover_effect_done = False

		self._font = load_font(size=size)
		self._font.set_bold(bold)
		
		self.setValue(value)
		self._decorate_button_surface()


	def _change_property(self, name, value):
		self._properties[name] = value
		self.__default_properties[name] = value
		self._hover_properties[name] = value

	def showBorder(self) : 
		self._properties['show_border'] = True
		self._properties['show_border'] = True
		self._decorate_button_surface()
	def hideBorder(self) : 
		self._properties['show_border'] = False
		self._decorate_button_surface()

	def setBoldText(self, bold : Union[bool, None] = None):
		if bold is None:
			bold = self._properties['bold']
		self._font.set_bold(bold)
		self.setValue()
		self._decorate_button_surface()

	def setFontSize(self, size : Union[int, None] = None):
		if size is None:
			size = self._properties['size']
		else:
			self._change_property('size', size)

		self._font = load_font(size=size)
		self.setValue()
		self._decorate_button_surface()


	def setValue(self, text : Union[str, None] = None):
		if text is None:
			text = self._properties['value']
		else:
			self._change_property('value', text)

		self._text_surface = self._font.render(text, True,  self._properties['font_color'])
		self._font_info = self._font.size(text)
		self._font_xy = (
			(self.w - self._font_info[0]) / 2,
			(self.h - self._font_info[1]) / 2 
		)
		self._decorate_button_surface()

	def getValue(self):
		return self._properties['value']
	
	def setHoverProperties(self, properties):
		self._hover_properties |= properties

	def clicked(self):
		if self.triggered:
			self.triggered = False
			return True
		else:
			return False	

	def update(self, event):
		x0, y0 = utl.mouse() - (self.x, self.y)
		if x0 > 0 and x0 < self.w and y0 > 0 and y0 < self.h:
			self.focused = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.triggered = True
		else:
			self.focused = False

	def _on_hover_function(self):
		if self.focused and not self.hover_effect_done:
			self._properties |= self._hover_properties
			self.setFontSize()
			self.setBoldText()
			self.setValue()
			self._decorate_button_surface()
			self.hover_effect_done = True
			# print('doing hover - ', np.random.randint(0, 999))

		elif not self.focused and self.hover_effect_done:
			self.hover_effect_done = False
			self._properties |= self.__default_properties
			self.setFontSize()
			self.setBoldText()
			self.setValue()
			self._decorate_button_surface()
			# print('no hover - ', np.random.randint(0, 999))
		

	def _decorate_button_surface(self):
		pygame.draw.rect(self._button_surface, self._properties['bg_color'], (0, 0, self.w, self.h), 
				   border_bottom_left_radius=self._properties['border_radius'], 
				   border_top_left_radius= self._properties['border_radius'],
				   border_top_right_radius= self._properties['border_radius'],
				   border_bottom_right_radius = self._properties['border_radius'])

		if self._properties['show_border']:
			pygame.draw.rect(self._button_surface, self._properties['border_color'], (0, 0, self.w, self.h), 
					width=self._properties['border_width'],
					border_bottom_left_radius=self._properties['border_radius'], 
					border_top_left_radius= self._properties['border_radius'],
					border_top_right_radius= self._properties['border_radius'],
					border_bottom_right_radius = self._properties['border_radius'])
		
		self._button_surface.blit(self._text_surface, self._font_xy)
	

	def show(self):
		self._on_hover_function()
		self.screen.blit(self._button_surface, (self.x, self.y))
		