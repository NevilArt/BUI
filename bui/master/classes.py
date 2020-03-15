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
	def minus(self,x,y):
		self.x -= x
		self.y -= y

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
	def minus(self,x,y):
		self._x -= x
		self._y -= y
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
	def __init__(self,top,bottom,left,right):
		self.set(top,bottom,left,right)
	def set(self,top,bottom,left,right):
		self.top = top
		self.bottom = bottom
		self.left = left
		self.right = right
	def any(self):
		return self.top or self.bottom or self.left or self.right

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
	def __init__(self,top,bottom,left,right,center):
		self.set(top,bottom,left,right,center)
	def set(self,top,bottom,left,right,center):
		self.top = top
		self.bottom = bottom
		self.left = left
		self.right = right
		self.center = center

class Scale:
	def __init__(self,enabled,top,bottom,left,right,sensitive):
		self.set(enabled,top,bottom,left,right,sensitive)
	def set(self,enabled,top,bottom,left,right,sensitive):
		self.enabled = enabled
		self.top = top
		self.bottom = bottom
		self.left = left
		self.right = right
		self.sensitive = sensitive
		self.touched = Edge(False,False,False,False)

class Dimantion:
	def __init__(self,x,y,width,height):
		self.set(x,y,width,height)
	def set(self,x,y,width,height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
	def get_start_end_length(self,border):
		x = self.x+border.left
		y = self.y+border.bottom
		w = self.width-border.left-border.right
		h = self.height-border.bottom-border.top
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
		return x-self.pos.x, y-self.pos.y

class Keyboard:
	def __init__(self):
		self.ctrl = False
		self.shift = False
		self.alt = False

__all__ = ["Vector2", "Edge", "Corner", "Scale", "VectorRange2",
			"Range", "Align", "Dimantion", "Colors",
			"MouseButton", "Mouse", "Keyboard"]