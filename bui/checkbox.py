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
from .box import Box

class CheckBox(BUI):
	def __init__(self,owner,pos=[0,0],size=[80,30],text="",column=0,row=0,onclick=None):
		super().__init__()
		self.owner = owner
		self.pos.set(pos[0],pos[1])
		self.pos.auto = True
		self.size.set(size[0],size[1])
		self.column = column
		self.row = row
		self.text = text
		self.checked = False
		self.setup()
		owner.append(self)

	def setup(self):
		w1,w2,h = self.size.y,self.size.x-self.size.y,self.size.y
		self.check = Box(self,size=[w1,h],column=1,row=1,onclick=self.check_clicked)
		self.check.body = Rectangle(self.check)
		self.check.body.fillet.set(3,3,3,3)
		self.check.body.color.set((0.345,0.345,0.345,1),(0.415,0.415,0.415,1),(0.474,0.620,0.843,1))
		self.mark = Box(self.check,size=[w1-6,h-6],column=1,row=1,onclick=self.check_clicked)
		self.mark.body = Rectangle(self.mark)
		self.mark.body.fillet.set(3,3,3,3)
		self.mark.body.color.set((0,0,0,1),(0,0,0,1),(0,0,0,1))
		self.mark.align.set(False,False,False,False,True)
		self.label = Box(self,text=self.text,size=[w2,h],column=2,row=1,onclick=self.check_clicked)
		self.label.caption.align.set(True,False,False,False,True)
		self.label.caption.offset.set(3,0)

	def check_clicked(self):
		self.owner.focus_on(self)
		self.checked = not self.checked
		self.mark.enabled = self.checked

	def update(self):
		pass

__all__ = ["CheckBox"]