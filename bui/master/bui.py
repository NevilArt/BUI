import bpy, gpu, bgl, blf
from gpu_extras.batch import batch_for_shader
from bpy.types import Operator
from .classes import Vector2,Mouse,Keyboard,Edge,Align,Dimantion

class BUI:
	def __init__(self):
		""" Aperiance """
		self.caption = None
		self.icon = None
		self.graphics = []

		""" Control data """
		self.mouse = Mouse()
		self.kb = Keyboard()
		self.pos = Vector2(0,0)
		self.location = Vector2(0,0)
		self.size = Vector2(0,0)
		self.offset = Vector2(0,0)
		self.owner = None
		self.controllers = []
		self.fit = Edge(False,False,False,False)
		self.align = Align(False,False,False,False,False)
		self.border = Edge(0,0,0,0)
		
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
			position.x = owner.location.x
			position.y = owner.location.y

			""" get allowd area """
			border = Edge(0,0,0,0) if self.ignorborder else owner.border
			dim = Dimantion(0,0,owner.size.x,owner.size.y)
			start,end,length = dim.get_start_end_length(border)

			""" limit location inside of parent """
			if pos.x > end.x-size.x:
				pos.x = end.x-size.x
			if pos.x < start.x:
				pos.x = start.x
			if pos.y > end.y-size.y:
				pos.y = end.y-size.y
			if pos.y < start.y:
				pos.y = start.y

			""" apply fit """
			if self.fit.left:
				size.x += pos.x-start.x
				pos.x = start.x
			if self.fit.right:
				size.x = length.x
			if self.fit.down:
				size.y += pos.y-start.y
				pos.y = start.y
			if self.fit.up:
				size.y = length.y

			""" apply alignment """
			align = self.align
			if align.center:
				if not align.left and not align.right:
					pos.x = owner.size.x/2-size.x/2
				if not align.up and not align.down:
					pos.y = owner.size.y/2-size.y/2
			
			if align.left and not align.right:
				pos.x = 0
			if align.right and not align.left:
				pos.x = owner.size.x-size.x

			if align.up and not align.down:
				pos.y = owner.size.y-size.y
			if align.down and not align.up:
				pos.y = 0

		x = position.x+pos.x+self.offset.x
		y = position.y+pos.y+self.offset.y
		w = size.x
		h = size.y

		self.location.x = x
		self.location.y = y
		return Vector2(x,y),Vector2(w,h)

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
				m_dx,m_dy = self.mouse.delta(x,y)
				if m_dx != 0 or m_dy != 0:
					if self.mouse.lmb.pressed:
						self.active.drag(m_dx,m_dy)
					elif self.hover:
						self.active.move(m_dx,m_dy)
				self.mouse.pos = Vector2(x,y)

			self.active.state = 2 if self.mouse.lmb.pressed else 1 if self.hover else 0

	# reserved functions #
	def setup(self):
		pass
	def update(self):
		# self._update()
		pass
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

__all__ = ["BUI"]