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

from .master.bui import BUI
from .master.graphic import Rectangle

# custom controller -------------------------------------------
class Button(BUI):
	def __init__(self,owner,pos=[0,0],size=[80,30],text="",column=0,row=0,onclick=None):
		super().__init__()
		self.owner = owner
		self.pos.set(pos[0],pos[1])
		self.pos.limit.set(True,True)
		self.pos.max.set(7680,4320)
		self.pos.auto = True
		self.size.set(size[0],size[1])
		self.size.limit.set(True,True)
		self.size.min.set(size[0],size[1])
		self.size.default.set(size[0],size[1])
		self.size.max.set(7680,4320)
		self.caption.text = text
		self.caption.align.center = True
		self.column = column
		self.row = row
		self.onclick = onclick
		
		self.body = Rectangle(self)
		self.body.fillet.set(6,6,6,6)
		self.body.color.set((0.345,0.345,0.345,1),(0.415,0.415,0.415,1),(0.474,0.620,0.843,1))

		self.setup()
		owner.append(self)

	def click(self):
		self.owner.focus_on(self)
		if self.onclick != None:
			self.onclick()

	def update(self):
		if self.owner != None:
			self.body.size = self.size.copy()

__all__ = ["Button"]