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
import itertools
from .classes import Vector2,Mouse,Keyboard,Edge,Align,Dimension,\
						Scale,VectorRange2,Caption,Border
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
		self.hover = False
		self.grab = False
		self.state = 0
		self.enabled = True
		self.moveable = False
		self.destroy = False
		# self.ignorechildren = False
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
	# 	self._setup()

	# def _setup(self):
	# 	self.table = 

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
			#captions += [c.caption for c in self.controllers]
			captions.append(self.caption)
		return captions

	def mouse_hover(self, event, deep=True):
		if self.enabled:
			mx,my = event.mouse_region_x, event.mouse_region_y
			x,y = self.location.x, self.location.y
			w,h = self.size.x, self.size.y
			if deep:
				self.active = self
				for c in self.controllers:
					if c.mouse_hover(event):
						self.active = c if c.active == c else c.active
						break
			if self.scale.enabled:
				s, scale = self.scale.sensitive, self.scale
				if scale.top:
					scale.touched.top = y+h-s < my < y+h
				if scale.bottom:
					scale.touched.bottom = y < my < y+s
				if scale.left:
					scale.touched.left = x < mx < x+s
				if scale.right:
					scale.touched.right = x+w-s < mx < x+w
			return (x < mx < x+w and y < my < y+h)
		return False

	def mouse_action(self, event):
		if self.enabled:
			""" read mouse """
			x,y = event.mouse_region_x, event.mouse_region_y

			""" get keys state """
			if event.type in {'LEFT_SHIFT','RIGHT_SHIFT'}:
				if event.value == 'PRESS':
					self.kb.shift = True
				if event.value == 'RELEASE':
					self.kb.shift = False

			if event.type in {'LEFT_CTRL','RIGHT_CTRL'}:
				if event.value == 'PRESS':
					self.kb.ctrl = True
				if event.value == 'RELEASE':
					self.kb.ctrl = False

			if event.type in {'LEFT_ALT','RIGHT_ALT'}:
				if event.value == 'PRESS':
					self.kb.alt = True
				if event.value == 'RELEASE':
					self.kb.alt = False

			if event.type == 'LEFTMOUSE' and self.hover:
				if event.value == 'PRESS':
					self.grab = True
					self.mouse.lmb.pressed = True
					self.mouse.lmb.pos = Vector2(x,y)
					self.active.push()
					self.active.mouse.lmb.grab = True
				if event.value =='RELEASE':
					self.grab = False
					self.mouse.lmb.pressed = False
					self.active.mouse.lmb.grab = False
					self.active.release()
					if self.active.mouse_hover(event,deep=False):
						self.active.click()

			if event.type == 'MIDDLEMOUSE':
				if event.value == 'PRESS':
					self.mouse.mmb.pressed = True
					self.mouse.mmb.pos = Vector2(x,y)
					self.active.middlepush()
				if event.value =='RELEASE':
					self.mouse.mmb.pressed = False
					self.active.middlerelease()
					if self.active.mouse_hover(event,deep=False):
						self.active.middleclick()

			if event.type == 'RIGHTMOUSE':
				if event.value == 'PRESS':
					self.mouse.rmb.pressed = True
					self.mouse.rmb.pos = Vector2(x,y)
					self.active.rightpush()
				if event.value =='RELEASE':
					self.mouse.rmb.pressed = False
					self.active.rightrelease()
					if self.active.mouse_hover(event,deep=False):
						self.active.rightclick()

			if event.type == 'MOUSEMOVE':
				dx,dy = self.mouse.delta(x,y)
				if dx != 0 or dy != 0:
					if self.mouse.lmb.pressed:
						if self.active.scale.enabled and self.active.scale.touched.any():
							self.active.resize(self.active.scale.touched,Vector2(dx,dy))
						else:
							self.active.drag(dx,dy)
					elif self.hover:
						self.active.move(dx,dy)
				self.mouse.pos = Vector2(x,y)

			self.active.state = 2 if self.mouse.lmb.pressed else 1 if self.hover else 0

	def _append(self,controller):
		controller.state_fix()
		self.controllers.append(controller)
		self.table.create()
	def append(self,controller):
		self._append(controller)

	# reserved functions #
	def setup(self):
		pass
	def update(self):
		pass # self._update()
	def _update(self):
		#if not self.ignorechildren:
		if self.enabled:
			for c in self.controllers:
				c.update()

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
			self.ondrag()
	def move(self,x,y):
		if self.onmove != None:
			self.onmove()
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