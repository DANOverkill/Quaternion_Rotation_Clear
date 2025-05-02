bl_info = {
    "name": "Quaternion Rotation Clear",
    "author": "DANOverkill",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
from .operators import OBJECT_OT_convert_rotation

class TOPBAR_MT_scripts_menu(bpy.types.Menu):
    bl_label = "Scripts"
    bl_idname = "TOPBAR_MT_scripts_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator(OBJECT_OT_convert_rotation.bl_idname)

def menu_func(self, context):
    self.layout.menu(TOPBAR_MT_scripts_menu.bl_idname)

classes = (
    OBJECT_OT_convert_rotation,
    TOPBAR_MT_scripts_menu,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.append(menu_func)

def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(menu_func)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()