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
from .master.classes import Vector2,Range
from .master.graphic import Rectangle
from .button import Button
from .box import Box

class Numeric(BUI):
	def __init__(self,owner,pos=[0,0],size=[80,30],text="",column=0,row=0,onclick=None):
		super().__init__()
		self.owner = owner
		self.pos.set(pos[0],pos[1])
		self.pos.auto = True
		self.size.set(size[0],size[1])
		self.column = column
		self.row = row

		self.body = Rectangle(self)
		self.body.color.set((0.219,0.219,0.219,1),(0.219,0.219,0.219,1),(0.219,0.219,0.219,1))

		self.value = Range(0,100,20)
		self.setup()
		owner.append(self)

	def setup(self):
		w,h = self.size.x-(self.size.y*2),self.size.y
		self.btn_left = Button(self,size=[h,h],column=1,row=1,text="<",onclick=self.btn_left_clicked)
		self.text_box = Box(self,size=[w,h],column=2,row=1,text="20")
		self.text_box.caption.align.center = True
		self.btn_right = Button(self,size=[h,h],column=3,row=1,text=">",onclick=self.btn_right_clicked)

	def btn_left_clicked(self):
		self.value.value -= 1
		self.text_box.caption.text = str(self.value.value)

	def btn_right_clicked(self):
		self.value.value += 1
		self.text_box.caption.text = str(self.value.value)

	def update(self):
		self.text_box.caption.text = str(self.value.value)
		print(self.value.value)
		self._update()

__all__ = ["Numeric"]