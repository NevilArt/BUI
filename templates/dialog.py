import bpy
from bui import Dialog,Button

def btn2_clicked():
	print("btn2 clicked")

class BUI_OT_SimpleDialog(Dialog):
	bl_idname = "bui.simplediaog"
	bl_label = "BUI Dialog"
	
	def setup(self):
		self.btn1 = Button(self,text="Button 01",size=[100,30],column=1,row=1)
		self.btn1.onclick = self.btn1_clicked

		self.btn2 = Button(self,text="Button 02",size=[100,30],column=2,row=1)
		self.btn2.onclick = btn2_clicked

	def btn1_clicked(self):
		print("btn1 clicked")

def register():
	bpy.utils.register_class(BUI_OT_SimpleDialog)

def unregister():
	bpy.utils.unregister_class(BUI_OT_SimpleDialog)

if __name__ == '__main__':
	register()
	bpy.ops.bui.simplediaog('INVOKE_DEFAULT')