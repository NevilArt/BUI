############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################
from .master.bui import BUI
from .master.graphic import Rectangle
# from .box import Box

class TextBox(BUI):
	def __init__(self,owner,pos=[0,0],size=[80,30],text="",column=0,row=0,onclick=None):
		super().__init__()
		self.owner = owner
		self.pos.set(pos[0],pos[1])
		self.pos.auto = True
		self.size.set(size[0],size[1])
		self.column = column
		self.row = row

		self.typeon = False

		self.body = Rectangle(self)
		self.body.color.set((0.219,0.219,0.219,1),(0.219,0.219,0.219,1),(0.219,0.219,0.219,1))

		self.text = ""
		self.setup()
		owner.append(self)

	def setup(self):
		self.caption.align.set(False,False,False,False,True)

	def click(self):
		self.owner.focus_on(self)

	def update(self):
		self.caption.text = self.kb.str

__all__ = ["Numeric"]