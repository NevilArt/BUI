import bpy
from bui import Dialog,Button,Slider

# Sample test -------------------------------------------------------------
class BUI_OT_Test(Dialog):
	bl_idname = "bui.test"
	bl_label = "BUI Test"
	
	def setup(self):
				""" dialog box parameters """
		self.escape = True
		self.pos.set(30,30)
		self.size.set(300,300)
		#self.size.lock = True
		self.border.set(10,10,10,10)
		self.scale.enabled = True
		self.scale.sensitive = 10
		self.caption.text = "Dialog"

		self.btn1 = Button(self,text="11",column=1,row=1)
		self.btn1.scale.enabled = True
		self.btn1.scale.sensitive = 10
		self.controllers.append(self.btn1)

		self.btn2 = Button(self,text="21",column=2,row=1)
		self.btn2.scale.enabled = True
		self.btn2.scale.sensitive = 10
		self.controllers.append(self.btn2)

		self.btn3 = Button(self,text="31",column=3,row=1)
		self.btn3.scale.enabled = True
		self.btn3.scale.sensitive = 10
		self.controllers.append(self.btn3)

		self.btn4 = Button(self,text="12",column=1,row=2)
		self.btn4.scale.enabled = True
		self.btn4.scale.sensitive = 10
		self.controllers.append(self.btn4)

		self.btn5 = Button(self,text="22",column=2,row=2)
		self.btn5.scale.enabled = True
		self.btn5.scale.sensitive = 10
		self.controllers.append(self.btn5)

		self.btn6 = Button(self,text="32",column=3,row=2)
		self.btn6.scale.enabled = True
		self.btn6.scale.sensitive = 10
		self.controllers.append(self.btn6)

		self.btn7 = Button(self,text="13",column=1,row=3)
		self.btn7.scale.enabled = True
		self.btn7.scale.sensitive = 10
		self.controllers.append(self.btn7)

		self.btn8 = Button(self,text="23",column=2,row=3)
		self.btn8.scale.enabled = True
		self.btn8.scale.sensitive = 10
		self.controllers.append(self.btn8)

		self.btn9 = Button(self,text="33",column=3,row=3)
		self.btn9.scale.enabled = True
		self.btn9.scale.sensitive = 10
		self.controllers.append(self.btn9)

def register(reg):
	classes = [BUI_OT_Test]
	if reg:
		[bpy.utils.register_class(c) for c in classes]
	else:
		[bpy.utils.unregister_class(c) for c in classes]

if __name__ == '__main__':
	register(True)