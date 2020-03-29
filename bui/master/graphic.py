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

from math import sin, cos, pi
from .classes import Colors, Vector2, Corner, Edge

class Rectangle:
	def __init__(self,owner):
		self.color = Colors()
		self.vertices = []
		self.indices = []
		self.state = 0
		self.size = Vector2(0,0)
		self.offset = Vector2(0,0)
		self.fillet = Corner(0,0,0,0)
		self.border = Edge(0,0,0,0)
		owner.graphics.append(self)

	def create_shape_(self,pos,size,state):
		self.state = state
		x,y = pos.x+self.offset.x, pos.y+self.offset.y
		w,h = self.size.x, self.size.y
		self.vertices = ((x,y),(x+w,y),(x+w,y+h),(x,y+h))
		self.indices = ((0,1,2),(2,3,0))

	def get_start_angle(self,dirx,diry):
		if dirx == 1 and diry == -1:
			return pi/2
		elif dirx == -1 and diry == -1:
			return pi
		elif dirx == -1 and diry == 1:
			return pi*1.5
		else:
			return 0

	def get_corner(self, orig, width, height, radius, dirx, diry):
		verts = []
		x1 = (width-radius)*dirx
		x2 = width*dirx
		y1 = (height-radius)*diry
		y2 = height*diry
		if radius > 0:
			s = self.get_start_angle(dirx,diry)
			div = 1 if radius < 10 else 3
			eges = radius/div
			steep = (pi/2)/eges
			for i in range(int(eges)):
				d = s+i*steep if i < int(eges)-1 else s+pi/2
				x = x1+sin(d)*radius
				y = y1+cos(d)*radius
				verts.append([x,y])
		else:
			verts.append([x2,y2])
		for i in range(len(verts)):
			verts[i][0] += orig.x
			verts[i][1] += orig.y
		return verts

	def create_shape(self,pos,size,state):
		self.state = state
		verts,inds = [],[]
		center = Vector2(pos.x+size.x/2,pos.y+size.y/2)
		verts.append((center.x,center.y))
		
		verts += self.get_corner(center,size.x/2,size.y/2,self.fillet.top_right,1,1)
		verts += self.get_corner(center,size.x/2,size.y/2,self.fillet.bottom_right,1,-1)
		verts += self.get_corner(center,size.x/2,size.y/2,self.fillet.bottom_left,-1,-1)
		verts += self.get_corner(center,size.x/2,size.y/2,self.fillet.top_left,-1,1)

		count = len(verts)
		for i in range(1,count):
			if i < count-1:
				inds.append((0,i,i+1))
			else:
				inds.append((0,i,1))
		self.vertices = verts
		self.indices = inds

	def get_shape(self):
		return self.vertices, self.indices, self.color.get(self.state)

class Gride:
	def __init__(self):
		self.count = Vector2(1,1)
		self.color = Colors()
		self.vertices = []
		self.indices = []
		self.state = 0
		self.size = Vector2(0,0)
		self.offset = Vector2(0,0)
		self.border = Edge(0,0,0,0)
		owner.graphics.append(self)

	def create_shape(self,pos,size,state):
		self.state = state
		x,y = pos.x+self.offset.x, pos.y+self.offset.y
		w,h = self.size.x, self.size.y
		self.vertices = ((x,y),(x+w,y),(x+w,y+h),(x,y+h))
		self.indices = ((0,1,2),(2,3,0))

	def get_shape(self):
		return self.vertices, self.indices, self.color.get(self.state)

__all__ = ["Rectangle", "Gride"]