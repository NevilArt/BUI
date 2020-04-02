############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################
# import itertools
from .classes import Vector2,Edge,Align,Dimension,Scale,VectorRange2,Caption,Border
from .input import Mouse,Keyboard
from .table import Table

class BUI:
	def __init__(self):
		""" Aperiance """
		self.caption = Caption(self)
		self.icon = None
		self.graphics = []
		""" Control data """
		self.mouse = Mouse()
		self.kb = Keyboard()
		self.pos = VectorRange2(0,0)
		self.size = VectorRange2(0,0)
		self.column = 0
		self.row = 0
		self.location = Vector2(0,0)
		self.offset = Vector2(0,0)
		self.owner = None
		self.controllers = []
		self.fit = Edge(False,False,False,False)
		self.align = Align(False,False,False,False,False)
		self.border = Border(0,0,0,0)
		self.scale = Scale(False,True,True,True,True,10)
		self.table = Table(self)
		""" Flags """
		self.active = None
		self.focus = None
		self.hover = False
		self.grab = False
		self.state = 0
		self.enabled = True
		self.moveable = False
		self.destroy = False
		""" Reserved for user funcions """
		self.onmove = None
		self.onclick = None
		self.ondoubleclick = None
		self.onpush = None
		self.onrelease = None
		self.ondrag = None
		self.onrightpush = None
		self.onrightrelease = None
		self.onrightclick = None
		self.onmiddlepush = None
		self.onmiddlerelease = None
		self.onmiddleclick = None

	def reset(self):
		pass

	def state_fix(self):
		if self.size.auto:
			self.scale.enabled = False
		if self.table.ignore:
			self.pos.auto = False
		if self.pos.auto:
			self.moveable = False

	def arrange(self):
		##########################################################################
		# if self.owner != None:
		# 	size,pos,owner = self.size,self.pos,self.owner
		# 	border = Edge(0,0,0,0) if owner.border.ignore else self.border
		# 	dim = Dimension(Vector2(0,0),owner.size)
		# 	start,end,length = dim.get_start_end_length(border)
		# 	if self.fit.left:
		# 		size.x += pos.x-start.x
		# 		pos.x = start.x
		# 	if self.fit.right:
		# 		size.x = length.x
		# 	if self.fit.bottom:
		# 		size.y += pos.y-start.y
		# 		pos.y = start.y
		# 	if self.fit.top:
		# 		size.y = length.y
		##########################################################################

		x,y = (self.owner.location.get() if self.owner != None else (0,0))
		self.location = Vector2(x,y) + self.pos + self.offset
		return self.location, self.size

	def get_graphics(self):
		graphics = []
		if self.enabled:
			pos,size = self.arrange()
			for graphic in self.graphics:
				graphic.create_shape(pos, size, self.state)
				graphics.append(graphic)
			for controller in self.controllers:
				graphics += controller.get_graphics()
		return graphics

	def get_captions(self):
		captions = []
		if self.enabled:
			for c in self.controllers:
				captions += c.get_captions()
			captions.append(self.caption)
		return captions

	def _append(self,controller):
		controller.state_fix()
		self.controllers.append(controller)
		self.table.create()
	def append(self,controller):
		self._append(controller)

	# reserved functions #
	def focus_on(self,me):
		if self.owner != None:
			self.owner.focus_on(me)
		else:
			self.focus = me

	def setup(self):
		pass
	def update(self):
		if self.enabled:
			for c in self.controllers:
				c.update()
	def _update(self):
		self.update()

	def push(self):
		if self.onpush != None:
			self.onpush()
	def release(self):
		if self.onrelease != None:
			self.onrelease()
	def click(self):
		if self.onclick != None:
			self.onclick()
	def doubleclick(self):
		if self.ondoubleclick != None:
			self.ondoubleclick()
	def rightpush(self):
		if self.onrightpush != None:
			self.onrightpush()
	def rightrelease(self):
		if self.onrightrelease != None:
			self.onrightrelease()
	def rightclick(self):
		if self.onrightclick != None:
			self.onrightclick()
	def middlepush(self):
		if self.onmiddlepush != None:
			self.onmiddlepush()
	def middlerelease(self):
		if self.onmiddlerelease != None:
			self.onmiddlerelease()
	def middleclick(self):
		if self.onmiddleclick != None:
			self.onmiddleclick()

	def drag(self,x,y):
		if self.moveable:
			self.pos.x += x
			self.pos.y += y
		if self.ondrag != None:
			self.ondrag(x,y)
	def move(self,x,y):
		if self.onmove != None:
			self.onmove(x,y)
	def resize(self,edges,value):
		if edges.left:
			self.size.x -= value.x
			self.pos.x += value.x
		if edges.right:
			self.size.x += value.x
		if edges.top:
			self.size.y += value.y
		if edges.bottom:
			self.size.y -= value.y
			self.pos.y += value.y

__all__ = ["BUI"]