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
		self.scale.sensitive = 10
		self.caption.text = "Dialog"

		self.joy = Slider(20,100,150,150,self)
		self.joy.caption.text = "Joystic"
		self.joy.caption.align.set(True,False,True,False,False)
		self.joy.caption.offset.set(5,-5)
		self.joy.moveable = True
		self.joy.scale.enabled = True
		self.joy.scale.sensitive = 10
		self.joy.x.set(-65,85,0)
		self.joy.y.set(-65,85,0)
		self.joy.ondrag = self.joy_draged
		self.controllers.append(self.joy)

		self.btn1 = Button(20,20,80,20,self)
		self.btn1.caption.text = "Botton 01"
		self.btn1.onclick = self.btn1_clicked
		self.controllers.append(self.btn1)

		self.btn2 = Button(20,20,80,20,self)
		self.btn2.caption.text = "Center"
		self.btn2.align.left = True
		self.btn2.offset.set(100,0)
		self.controllers.append(self.btn2)

		self.btn3 = Button(20,20,80,20,self)
		self.btn3.caption.text = "Right"
		self.btn3.align.right = True
		self.btn3.offset.set(-10,0)
		self.controllers.append(self.btn3)

	def joy_draged(self):
		print("val :",self.joy.x.value,self.joy.y.value)

	def btn1_clicked(self):
		self.joy.x.value = 20
		self.joy.y.value = 20

def register(reg):
	classes = [BUI_OT_Test]
	if reg:
		[bpy.utils.register_class(c) for c in classes]
	else:
		[bpy.utils.unregister_class(c) for c in classes]

if __name__ == '__main__':
	register(True)