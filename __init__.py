bl_info = {
    "name": "Quaternion Rotation Clear",
    "author": "DANOverkill",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
from .operators import (  # Import from operators.py
    OBJECT_OT_convert_rotation,
    OBJECT_OT_confirm_delete_quaternions
)

class TOPBAR_MT_scripts_menu(bpy.types.Menu):
    bl_label = "Scripts"
    bl_idname = "TOPBAR_MT_scripts_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator(OBJECT_OT_convert_rotation.bl_idname)

# Registration
def menu_func(self, context):
    self.layout.menu(TOPBAR_MT_scripts_menu.bl_idname)

classes = (
    OBJECT_OT_convert_rotation,
    OBJECT_OT_confirm_delete_quaternions,
    TOPBAR_MT_scripts_menu,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.append(menu_func)
    bpy.types.WindowManager.quaternion_channels = bpy.props.StringProperty()

def unregister():
    del bpy.types.WindowManager.quaternion_channels
    bpy.types.TOPBAR_MT_editor_menus.remove(menu_func)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()