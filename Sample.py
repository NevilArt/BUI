import bpy
from bui import Dialog,Button,Slider

# Sample test -------------------------------------------------------------
class BUI_OT_Test(Dialog):
	bl_idname = "bui.test"
	bl_label = "BUI Test"
	
	def setup(self):
		self.btn1 = Button(self,text="B11",column=1,row=1)
		self.btn2 = Button(self,text="B21",column=2,row=1)
		self.btn3 = Button(self,text="B31",column=3,row=1)
		self.btn4 = Button(self,text="B12",column=1,row=2)
		self.btn5 = Button(self,text="B22",column=2,row=2)
		self.btn6 = Button(self,text="B32",column=3,row=2)
		self.btn7 = Button(self,text="B13",column=1,row=3)
		self.btn8 = Button(self,text="B23",column=2,row=3)
		self.btn9 = Button(self,text="B33",column=3,row=3)

def register(reg):
	classes = [BUI_OT_Test]
	if reg:
		[bpy.utils.register_class(c) for c in classes]
	else:
		[bpy.utils.unregister_class(c) for c in classes]

if __name__ == '__main__':
	register(True)