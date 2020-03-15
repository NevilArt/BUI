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
			self.body.size = self.size.copy()

__all__ = ["Button"]