class Vector2:
	def __init__(self, x,y):
		self.set(x,y)
	def set(self,x,y):
		self.x = x
		self.y = y

class Vector4:
	def __init__(self,a,b,c,d):
		self.set(a,b,c,d)
	def set(self,a,b,c,d):
		self.a = a
		self.b = b
		self.c = c
		self.d = d

class Edge:
	def __init__(self,up,down,left,right):
		self.set(up,down,left,right)
	def set(self,up,down,left,right):
		self.up = up
		self.down = down
		self.left = left
		self.right = right

class Corner:
	def __init__(self,up_left,up_right,down_left,down_right):
		self.set(up_left,up_right,down_left,down_right)
	def set(self,up_left,up_right,down_left,down_right):
		self.up_left = up_left
		self.up_right = up_right
		self.down_left = down_left
		self.down_right = down_right

class Range:
	def __init__(self, minval, maxval, default):
		self.min = minval
		self.max = maxval
		self.default = default
		self.value = default

class Align:
	def __init__(self,left,right,up,down,center):
		self.set(left,right,up,down,center)
	def set(self,left,right,up,down,center):
		self.left = left
		self.right = right
		self.up = up
		self.down = down
		self.center = center

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
		y = self.y+border.down
		w = self.width-border.left-border.right
		h = self.height-border.down-border.up
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

__all__ = ["Vector2", "Vector4", "Edge", "Corner",
			"Range", "Align", "Dimantion", "Colors",
			"MouseButton", "Mouse", "Keyboard"]