import pygame

class InputBox():
	"""docstring for InputBox"""
	# border = (color, border_width)
	# font = (name, size)
	def __init__(self, surface, txt_color, box_info, box_color, border, font = ("dejavusan", 14)):
		self.surface = surface
		self.txt_color = txt_color
		self.box_info = box_info
		self.border = border
		self.box_color = box_color
		self.font = font
		self.value = ""
		self.holder = { "text" : "Type here...", "color": (51,51,51)}
		self.focused = False
		self.cursor = {"color": (0,0,0), "w": 5, "h":3, "blink": 8}
		self.__counter = 0

	def font_size(self, size):
		self.font = (self.font[0], size)

	def update(self, event):
		if self.focused:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_BACKSPACE:
					self.value = self.value[:-1]
				else:
					self.value += event.unicode

	def show(self):
		txt = ""
		pygame.draw.rect(self.surface, self.box_color, self.box_info)
		pygame.draw.rect(self.surface, self.border[0], self.box_info, self.border[1])
		if self.value == "":
			txt = self.holder["text"]
		else:
			txt = self.value
		
		pygame.font.init()
		font = pygame.font.SysFont(self.font[0], self.font[1])
		text = font.render(txt, True, self.txt_color)
		x, y, th, h = self.box_info
		th = font.size(txt)[1]
		p = round((h - th) / 2) if h > th else 0
		self.surface.blit(text, (x + 4, y + p))
		if self.focused:
			tw = font.size(self.value)[0]
			if self.__counter > 6:
				pygame.draw.rect(self.surface, self.cursor["color"], (x + tw + 4, y + p + th - self.cursor["h"], self.cursor["w"], self.cursor["h"]))
		
			self.__counter += 1
			if self.__counter > self.cursor["blink"]:
				self.__counter = 0

		pygame.font.quit()
		
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

