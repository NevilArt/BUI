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
class Box(BUI):
	def __init__(self,owner,pos=[0,0],size=[0,0],text="",column=0,row=0,onclick=None):
		super().__init__()
		self.owner = owner
		self.pos.set(pos[0],pos[1])
		self.pos.auto = True
		self.size.set(size[0],size[1])
		self.size.auto = size == [0,0]
		self.caption.text = text
		self.caption.align.center = True
		self.column = column
		self.row = row
		self.onclick = onclick
		owner.append(self)

__all__ = ["Box"]