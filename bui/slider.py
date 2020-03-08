from .master.bui import BUI
from .master.classes import Vector2,Range
from .master.graphic import Rectangle
from .button import Button

class Slider(BUI):
	def __init__(self,x,y,width,height,owner):
		super().__init__()
		self.pos.set(x,y)
		self.size.set(width,height)
		self.owner = owner

		self.body = Rectangle()
		self.body.color.set((0.219,0.219,0.219,1),(0.219,0.219,0.219,1),(0.219,0.219,0.219,1))
		self.graphics = [self.body]

		self.x = Range(0,100,20)
		self.y = Range(0,100,20)
		self.setup()

	#TODO has option to allow negative mode to
	def setup(self):
		self.handel = Button(0,0,30,30,self)
		self.handel.body.fillet.set(15,15,15,15)
		self.body.fillet.set(15,15,15,15)
		self.handel.moveable = True
		self.handel.ondrag = self.handel_draged
		self.controllers.append(self.handel)

	def handel_draged(self):
		start = Vector2(self.location.x, self.location.y)
		current = Vector2(self.handel.location.x, self.handel.location.y)
		end = Vector2(self.location.x+self.size.x-self.handel.size.x,
			self.location.y+self.size.y-self.handel.size.y)
		length = Vector2(self.x.max-self.x.min, self.y.max-self.y.min)
		if end.x-start.x != 0:
			self.x.value = self.x.min+length.x*((current.x-start.x)/(end.x-start.x))
		else:
			self.x.value = 0
		if end.y-start.y != 0:
			self.y.value = self.y.min+length.y*((current.y-start.y)/(end.y-start.y))
		else:
			self.y.value = 0
		if self.ondrag != None:
			self.ondrag()

	def drag(self,x,y):
		if self.moveable:
			self.pos.x += x
			self.pos.y += y

	def update(self):
		#TODO Update handel position by value if not in drag mode
		if self.owner != None:
			self.body.size = self.size
		self._update()

__all__ = ["Slider"]