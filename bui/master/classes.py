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

class Vector2:
	def __init__(self,x,y):
		self.set(x,y)
	def set(self,x,y):
		self.x = x
		self.y = y
	def copy(self):
		return(Vector2(self.x,self.y))
	def add(self,x,y):
		self.x += x
		self.y += y
	def __add__(self, vec):
		return Vector2(self.x+vec.x,self.y+vec.y)
	def __iadd__(self, vec):
		return Vector2(self.x+vec.x,self.y+vec.y)

class VectorRange2:
	def __init__(self,x,y):
		self.limit = Vector2(False,False)
		self.min = Vector2(0,0)
		self.max = Vector2(0,0)
		self.default = Vector2(x,y)
		self.set(x,y)
	def set(self,x,y):
		self._x = x
		self._y = y
	def copy(self):
		return(Vector2(self._x,self._y))
	def reset(self):
		self.set(self.default.x,self.default.y)
	def add(self,x,y):
		self._x += x
		self._y += y
	def __add__(self, vec):
		return VectorRange2(self.x+vec.x,self.y+vec.y)
	@property
	def x(self):
		return self._x
	@x.setter
	def x(self, x):
		if self.limit.x:
			self._x = self.min.x if x < self.min.x else self.max.x if x > self.max.x else x
		else:
			self._x = x
	@property
	def y(self):
		return self._y
	@y.setter
	def y(self, y):
		if self.limit.y:
			self._y = self.min.y if y < self.min.y else self.max.y if y > self.max.y else y
		else:
			self._y = y 

class Edge:
	def __init__(self,left,right,top,bottom):
		self.set(left,right,top,bottom)
	def set(self,left,right,top,bottom):
		self.left = left
		self.right = right
		self.top = top
		self.bottom = bottom
	def any(self):
		return self.left or self.right or self.top or self.bottom

class Border:
	def __init__(self,left,right,top,bottom):
		self.set(left,right,top,bottom)
	def set(self,left,right,top,bottom):
		self.left = left
		self.right = right
		self.top = top
		self.bottom = bottom

class Corner:
	def __init__(self,top_left,top_right,bottom_left,bottom_right):
		self.set(top_left,top_right,bottom_left,bottom_right)
	def set(self,top_left,top_right,bottom_left,bottom_right):
		self.top_left = top_left
		self.top_right = top_right
		self.bottom_left = bottom_left
		self.bottom_right = bottom_right

class Range:
	def __init__(self, minval, maxval, default):
		self.set(minval, maxval, default)
	def set(self, minval, maxval, default):
		self.min = minval
		self.max = maxval
		self.default = default
		self.value = default
		self.check()
	def check(self):
		if self.max < self.min:
			self.max == self.min
		if self.min < self.default > self.max:
			self.default = self.min
	def reset(self):
		self.value = self.default
	def get_lenght(self):
		return self.max - self.min
	def get_negative_lenght(self):
		s = self.min if self.min < 0 else 0
		e = self.max if self.max < 0 else 0
		return e - s
	def get_posetive_length(self):
		s = self.min if self.min > 0 else 0
		e = self.max if self.max > 0 else 0
		return e - s
	def get_position_percet(self):
		length = self.get_lenght()
		val = self.value - self.min
		return val / length if length > 0 else 0

class Align:
	def __init__(self,left,right,top,bottom,center):
		self.set(left,right,top,bottom,center)
	def set(self,left,right,top,bottom,center):
		self.left = left
		self.right = right
		self.top = top
		self.bottom = bottom
		self.center = center
	def location(self,pos,size1,size2):
		if self.center:
			if not self.left and not self.right:
				pos.x = size1.x/2-size2.x/2
			if not self.top and not self.bottom:
				pos.y = size1.y/2-size2.y/2
		if self.left and not self.right:
			pos.x = 0
		if self.right and not self.left:
			pos.x = size1.x-size2.x
		if self.top and not self.bottom:
			pos.y = size1.y-size2.y
		if self.bottom and not self.top:
			pos.y = 0
		return pos

class Scale:
	def __init__(self,enabled,left,right,top,bottom,sensitive):
		self.set(enabled,left,right,top,bottom,sensitive)
	def set(self,enabled,left,right,top,bottom,sensitive):
		self.enabled = enabled
		self.left = left
		self.right = right
		self.top = top
		self.bottom = bottom
		self.sensitive = sensitive
		self.touched = Edge(False,False,False,False)

class Dimension:
	def __init__(self,pos,size):
		self.set(pos,size)
	def set(self,pos,size):
		self.pos = pos
		self.size = size
	def get_start_end_length(self,border):
		x = self.pos.x+border.left
		y = self.pos.y+border.bottom
		w = self.size.x-border.left-border.right
		h = self.size.y-border.bottom-border.top
		return Vector2(x,y),Vector2(x+w,y+h),Vector2(w,h)

class Colors:
	def __init__(self):
		self.a = (0.4,0.4,0.4,1) # default
		self.b = (0.5,0.5,0.5,1) # hover
		self.c = (0.6,0.6,0.6,1) # click
	def set(self,a,b,c):
		self.a,self.b,self.c = a,b,c
	def get(self, state):
		if state == 1:
			return self.b
		elif state == 2:
			return self.c
		else:
			return self.a

class MouseButton:
	def __init__(self):
		self.pressed = False
		self.grab = False
		self.pos = Vector2(0,0)
	def delta(self,x,y):
		return x-self.pos.x, y-self.pos.y

class Mouse:
	def __init__(self):
		self.rmb = MouseButton()
		self.mmb = MouseButton()
		self.lmb = MouseButton()
		self.pos = Vector2(0,0)
	def delta(self,x,y):
		return x-self.pos.x,y-self.pos.y

class Keyboard:
	def __init__(self):
		self.ctrl = False
		self.shift = False
		self.alt = False

class Caption:
	def __init__(self):
		self.owner = None
		self.text = ""
		self.font = ""
		self.size = 12
		self.pos = Vector2(0,0)
		self.offset = Vector2(0,0)
		self.color = Colors()
		self.align = Align(False,False,False,False,True)
		self.hide = False
	def __iadd__(self, targ):
		self.text = targ.text
		self.font = targ.font
		self.size = targ.size
		self.pos = targ.pos.copy()
		# self.color = targ.color.copy()
		# self.align = targ.align.copy()
		return self
	def location(self,size):
		if self.owner != None:
			return self.owner.location+self.align.location(self.pos,self.owner.size,size)+self.offset
		else:
			return self.pos

__all__ = ["Vector2", "Edge", "Corner", "Scale", "VectorRange2", "Border",
			"Range", "Align", "Dimension", "Colors", "Caption",
			"MouseButton", "Mouse", "Keyboard"]