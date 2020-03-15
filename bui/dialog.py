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

import bpy, gpu, bgl, blf
from gpu_extras.batch import batch_for_shader
from bpy.types import Operator
from .master.bui import BUI
from .master.graphic import Rectangle
from .button import Button

class TitleBar(BUI):
	def __init__(self, owner):
		super().__init__()
		""" public values """
		self.moveable = True
		self.owner = owner
		self.size.y = 30
		self.fit.left = True
		self.fit.right = True
		self.align.top = True
		self.ignorborder = True
		""" graphics """
		self.body = Rectangle()
		self.body.size.y = self.size.y
		self.body.fillet.top_left = 9
		self.body.fillet.top_right = 9
		self.body.color.set((0.300,0.300,0.300,1),(0.300,0.300,0.300,1),(0.320,0.320,0.340,1))
		self.graphics.append(self.body)
		""" special """
		self.collased = False
		self.owner_size_y = 0
		self.owner_controllers = []
		self.setup()

	def close_btn_pressed(self):
		if self.owner != None:
			self.owner.destroy= True

	def fit_btn_pressed(self):
		pass

	def collaps_btn_pressed(self):
		self.collased = not self.collased
		if self.collased:
			self.owner.pos.y += self.owner.size.y-self.size.y
			self.owner_size_y = self.owner.size.y
			self.owner.size.y = self.size.y
			self.body.fillet.bottom_left = 9
			self.body.fillet.bottom_right = 9
			""" store controllers bu titlebar """
			for c in self.owner.controllers:
				if c != self:
					self.owner_controllers.append(c)
			self.owner.controllers.clear()
			self.owner.controllers.append(self)
		else:
			self.owner.size.y = self.owner_size_y
			self.owner.pos.y -= self.owner.size.y-self.size.y
			self.body.fillet.bottom_left = 0
			self.body.fillet.bottom_right = 0
			""" restore controllers first titlebar """
			self.owner.controllers.clear()
			self.owner.controllers.append(self)
			self.owner.controllers += self.owner_controllers
			self.owner_controllers.clear()
	
	def setup(self):
		self.owner.size.y += self.size.y
		self.owner.border.top += self.size.y
		self.border.right = 3

		self.close_btn = Button(0,0,26,26,self)
		self.close_btn.align.center = True
		self.close_btn.align.right = True
		self.close_btn.onclick = self.close_btn_pressed
		self.controllers.append(self.close_btn)

		self.fit_btn = Button(0,0,26,26,self)
		self.fit_btn.align.center = True
		self.fit_btn.align.right = True
		self.fit_btn.offset.x = -30
		self.fit_btn.onclick = self.fit_btn_pressed
		self.controllers.append(self.fit_btn)

		self.collaps_btn = Button(0,0,26,26,self)
		self.collaps_btn.align.center = True
		self.collaps_btn.align.right = True
		self.collaps_btn.offset.x = -60
		self.collaps_btn.onclick = self.collaps_btn_pressed
		self.controllers.append(self.collaps_btn)

	def drag(self,x,y):
		self.owner.pos.add(x,y)

class Dialog(Operator,BUI):
	def __init__(self):
		super().__init__()
		self.handler = None
		self.active_space = None
		self.shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
		self.escape = False
		self.body = Rectangle()
		self.body.fillet.set(9,9,9,9)
		self.body.color.set((0.13,0.13,0.13,1),(0.13,0.13,0.13,1),(0.13,0.13,0.13,1))
		self.graphics.append(self.body)

	def update(self):
		self.body.size = self.size.copy()
		self._update()

	def redraw(self):
		""" re draw the graphic """
		self.update()
		for g in self.get_graphics():
			self.shader.bind()
			vertices, indices, color = g.get_shape()
			batch = batch_for_shader(self.shader,'TRIS',{"pos":vertices},indices=indices)
			self.shader.uniform_float("color", color)
			batch.draw(self.shader)

	def modal(self, ctx, event):
		if ctx.area:
			ctx.area.tag_redraw()

		if self.destroy or (event.type in {'ESC'} and self.escape):
			self.unregister()
			return {'CANCELLED'}

		if event.type == 'MOUSEMOVE':
			self.hover = True if self.grab else self.mouse_hover(event)

		self.mouse_action(event)

		if not self.hover and not self.grab:
			self.reset()
			return {'PASS_THROUGH'}
		return {'RUNNING_MODAL'}

	def unregister(self):
		if self.handler != None:
			self.active_space.draw_handler_remove(self.handler, "WINDOW")

	def invoke(self, ctx, event):
		ctx.window_manager.modal_handler_add(self)
		self.active_space = ctx.area.spaces.active
		self.handler = self.active_space.draw_handler_add(self.redraw,(),'WINDOW','POST_PIXEL')
		self.setup()
		self.controllers.append(TitleBar(self))
		return {'RUNNING_MODAL'}

__all__ = ["Dialog"]