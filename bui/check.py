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

class Check(BUI):
	def __init__(self,owner=None,pos=[0,0],size=[80,30],text="",column=0,row=0,
				onmove=None,ondrag=None,
				onpush=None,onrelease=None,
				onclick=None,ondoubleclick=None,
				onrightpush=None,onrightrelease=None,
				onrightclick=None,onmiddleclick=None,
				onmiddlepush=None,onmiddlerelease=None,
				# specila argumnets #
				checked=False,mode="check"):
		super().__init__(owner=owner,pos=pos,size=size,text=text,column=column,row=row,
				onmove=onmove,ondrag=ondrag,
				onpush=onpush,onrelease=onrelease,
				onclick=onclick,ondoubleclick=ondoubleclick,
				onrightpush=onrightpush,onrightrelease=onrightrelease,
				onrightclick=onrightclick,onmiddleclick=onmiddleclick,
				onmiddlepush=onmiddlepush,onmiddlerelease=onmiddlerelease)
		self.caption.hide = True
		self.pos.auto = True
		self._checked = checked
		self.mode = mode # check/radio
		self.touchable = False
		self.setup()
		owner.append(self)

	def setup(self):
		c1,c2 = 12,6
		w1,h1 = self.size.x-c1,self.size.y-c1
		w2,h2 = w1-c2,h1-c2

		if self.mode == 'check':
			r1,r2 = 3,3
		elif self.mode == 'radio':
			r1,r2 = min(w1,h1)/2, min(w2,h2)/2
		else:
			r1,r2 = 0,0

		self.check = Box(self,size=[w1,h1])
		self.check.body = Rectangle(self.check)
		self.check.body.fillet.set(r1,r1,r1,r1)
		self.check.body.color.set((0.345,0.345,0.345,1),(0.415,0.415,0.415,1),(0.474,0.620,0.843,1))
		self.offset.set(c1/2,c1/2)

		self.mark = Box(self.check,size=[w2,h2])
		self.mark.body = Rectangle(self.mark)
		self.mark.body.fillet.set(r2,r2,r2,r2)
		self.mark.body.color.set((0,0,0,1),(0,0,0,1),(0,0,0,1))
		self.mark.align.center = True

	@property
	def checked(self):
		return self._checked
	@checked.setter
	def checked(self, state):
		self.mark.enabled = self._checked = state

__all__ = ["Check"]