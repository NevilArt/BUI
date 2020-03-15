############################################################################
#    BsMax, 3D apps inteface simulator and tools pack for Blender
#    Copyright (C) 2020  Naser Merati (Nevil)
#
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

import bpy, gpu, bgl, blf
from gpu_extras.batch import batch_for_shader
from bpy.types import Operator
from .classes import Vector2,Mouse,Keyboard,Edge,Align,Dimantion,Scale,VectorRange2

class BUI:
	def __init__(self):
		""" Aperiance """
		self.caption = None
		self.icon = None
		self.graphics = []

		""" Control data """
		self.mouse = Mouse()
		self.kb = Keyboard()
		self.pos = VectorRange2(0,0)
		self.pos.limit.set(True,True)
		self.size = VectorRange2(0,0)
		self.size.limit.set(True,True)
		self.location = Vector2(0,0)
		self.offset = Vector2(0,0)
		self.owner = None
		# self.master = []
		self.controllers = []
		self.fit = Edge(False,False,False,False)
		self.align = Align(False,False,False,False,False)
		self.border = Edge(0,0,0,0)
		self.scale = Scale(False,True,True,True,True,5)
		
		""" Flags """
		self.active = None
		self.hover = False
		self.grab = False
		self.state = 0
		self.enabled = True
		self.moveable = False
		self.destroy = False
		self.ignorborder = False
		self.ignorechildren = False

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

	def arrange(self):
		pos,size,owner = self.pos,self.size,self.owner

		#TODO if owner is None set space as owner

		""" change size and position of controllers by avalible data """
		position = Vector2(0,0)
		if owner != None:
			""" get offset by parent location """
			position.set(owner.location.x,owner.location.y)

			""" get allowd area """
			border = Edge(0,0,0,0) if self.ignorborder else owner.border
			dim = Dimantion(0,0,owner.size.x,owner.size.y)
			start,end,length = dim.get_start_end_length(border)

			""" limit size fit to parent """
			size.min.set(0,0)
			size.max.set(owner.size.x-border.right-pos.x,owner.size.y-border.top-pos.y)
			# size.max.set(length.x-pos.x,length.y-pos.y)

			""" limit location inside of parent """
			pos.limit.set(True,True)
			pos.min.set(start.x,start.y)
			pos.max.set(end.x-size.x,end.y-size.y)

			""" apply fit """
			if self.fit.left:
				size.x += pos.x-start.x
				pos.x = start.x
			if self.fit.right:
				size.x = length.x
			if self.fit.bottom:
				size.y += pos.y-start.y
				pos.y = start.y
			if self.fit.top:
				size.y = length.y

			""" apply alignment """
			align = self.align
			if align.center:
				if not align.left and not align.right:
					pos.x = owner.size.x/2-size.x/2
				if not align.top and not align.bottom:
					pos.y = owner.size.y/2-size.y/2
			
			if align.left and not align.right:
				pos.x = 0
			if align.right and not align.left:
				pos.x = owner.size.x-size.x

			if align.top and not align.bottom:
				pos.y = owner.size.y-size.y
			if align.bottom and not align.top:
				pos.y = 0

		x = position.x+pos.x+self.offset.x
		y = position.y+pos.y+self.offset.y
		w = size.x
		h = size.y

		self.location.x = x
		self.location.y = y
		return VectorRange2(x,y),VectorRange2(w,h)

	def get_graphics(self):
		pos,size = self.arrange()
		graphics = []
		for g in self.graphics:
			g.create_shape(pos, size, self.state)
			graphics.append(g)
		for c in self.controllers:
			graphics += c.get_graphics()
		return graphics

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
					self.kb,ctrl = False

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

	# reserved functions #
	def setup(self):
		pass
	def update(self):
		pass # self._update()
	def _update(self):
		if not self.ignorechildren:
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
		if edges.top:
			self.size.y += value.y
		if edges.bottom:
			self.size.y -= value.y
			self.pos.y += value.y
		if edges.left:
			self.size.x -= value.x
			self.pos.x += value.x
		if edges.right:
			self.size.x += value.x

__all__ = ["BUI"]