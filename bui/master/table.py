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
import itertools
from .classes import Vector2,Border

class Cell:
	def __init__(self):
		self.controllers = []
		self.size = Vector2(0,0)
		self.pos = Vector2(0,0)

class Table:
	def __init__(self):
		self.cells = []
		self._size = Vector2(0,0)
		self.gap = Vector2(0,0)
		self.border = Border(0,0,0,0)

	def create(self,controllers):
		self._size.set(0,0)

		""" get biget number in each direction """
		rows = [c.row for c in controllers if not c.ignoretable and not c.moveable]
		lastrow = max(rows) if len(rows) > 0 else 0
		cols = [c.column for c in controllers if not c.ignoretable and not c.moveable]
		lastcol = max(cols) if len(cols) > 0 else 0

		""" create a 2d variable sheet """
		self.cells = [[Cell() for x in range(lastcol+1)] for y in range(lastrow+1)]
		
		""" put controlers inside the sheet """
		for c in controllers:
			if not c.ignoretable and not c.moveable:
				self.cells[c.row][c.column].controllers.append(c)

	def get_column(self,index):
		column = []
		if len(self.cells) > 0:
			if index < len(self.cells[0]):
				for row in self.cells:
					column.append(row[index])
		return column

	def get_row(self,index):
		row = []
		if index < len(self.cells):
			for r in self.cells[index]:
				row.append(r)
		return row

	def get_cell(self,column,row):
		if row < len(self.cells) > 0:
			if column < len(self.cells[0]) > 0:
				return self.cells[row][column]
		return Cell()

	def get_table_dimension(self):
		rows = len(self.cells)
		columns = len(self.cells[0]) if rows > 0 else 0
		return columns,rows

	def arrange_sizes(self):
		cols,rows = self.get_table_dimension()
		for i in range(cols):
			maxwidth,column = 0,self.get_column(i)
			for cell in column:
				width = 0
				for c in cell.controllers:
					width += c.size.x
				maxwidth = max(width, maxwidth)
			for cell in column:
				cell.size.x = maxwidth
		for i in range(rows):
			maxheight,row = 0,self.get_row(i)
			for cell in row:
				height = 0
				for c in cell.controllers:
					height += c.size.y
				maxheight = max(height, maxheight)
			for cell in row:
				cell.size.y = maxheight

	def update(self):
		self.arrange_sizes()
		cols,rows = self.get_table_dimension()
		x,y = 0,0
		for i in range(cols):
			y = self.border.bottom+self.gap.y
			for cell in self.get_column(i):
				cell.pos.y = y
				y += cell.size.y+self.gap.y
			y += self.border.top
		self._size.y = y
		for i in range(rows):
			x = self.border.left+self.gap.x
			for cell in self.get_row(i):
				cell.pos.x = x
				x += cell.size.x+self.gap.x
			x += self.border.right
		self._size.x = x

	@property
	def size(self):
		self.update()
		return self._size

	@size.setter
	def size(self, newsize):
		""" set cells size by new sizes """
		pass

__all__ = ["Table"]