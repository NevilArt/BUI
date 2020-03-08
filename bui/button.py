from .master.bui import BUI
from .master.graphic import Rectangle

# custom controller -------------------------------------------
class Button(BUI):
	def __init__(self,x,y,width,height,owner):
		super().__init__()
		self.pos.set(x,y)
		self.size.set(width,height)
		self.owner = owner
		self.body = Rectangle()
		self.body.fillet.set(9,9,9,9)
		self.body.color.set((0.345,0.345,0.345,1),(0.415,0.415,0.415,1),(0.474,0.620,0.843,1))
		self.graphics = [self.body]
		self.setup()
	def update(self):
		if self.owner != None:
			self.body.pos = self.pos
			self.body.size = self.size

__all__ = ["Button"]