import bpy
from bui import Dialog,Button,Slider

# Sample test -------------------------------------------------------------
class BUI_OT_Test(Dialog):
	bl_idname = "bui.test"
	bl_label = "BUI Test"
	
	def setup(self):
		""" dialog box parameters """
		self.escape = True
		self.pos.set(300,300)
		self.size.set(300,300)
		self.border.set(10,10,10,10)
		self.scale.enabled = True

		""" add more controllers """
		self.btn1 = Button(20,20,80,20,self)
		self.btn1.onclick = self.btn1_pressed
		self.controllers.append(self.btn1)

		self.btn2 = Button(150,20,80,20,self)
		self.btn2.moveable = True
		self.btn2.onclick = self.btn2_pressed
		self.controllers.append(self.btn2)

		self.slid = Slider(20,60,250,30,self)
		self.slid.moveable = True
		self.slid.ondrag = self.slide_draged
		self.controllers.append(self.slid)

		self.joy = Slider(20,100,150,150,self)
		self.joy.moveable = True
		self.joy.scale.enabled = True
		self.joy.x.set(-65,85,0)
		self.joy.y.set(-65,85,0)
		self.joy.ondrag = self.joy_draged
		self.controllers.append(self.joy)

	def btn1_pressed(self):
		x = self.joy.x.value / 10
		y = self.joy.y.value / 10
		bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, location=(x, y, 0))
		print("button one clicked")

	def btn2_pressed(self):
		bpy.ops.object.delete(use_global=False, confirm=False)
		print("button two clicked")

	def slide_draged(self):
		print(self.slid.x.value)
		print(self.slid.y.value)

	def joy_draged(self):
		print(self.joy.x.value)
		print(self.joy.y.value)

def register(reg):
	classes = [BUI_OT_Test]
	if reg:
		[bpy.utils.register_class(c) for c in classes]
	else:
		[bpy.utils.unregister_class(c) for c in classes]

if __name__ == '__main__':
	register(True)