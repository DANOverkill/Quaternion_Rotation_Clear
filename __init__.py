import bpy

class OBJECT_OT_convert_rotation(bpy.types.Operator):
    """Convert Quaternion Rotation to Euler and Clean Keyframes"""
    bl_idname = "object.convert_rotation"
    bl_label = "Convert Quaternion to Euler"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'ARMATURE'

    def execute(self, context):
        ob = context.active_object
        quaternion_channels = set()

        # Convert rotation modes
        for bone in ob.pose.bones:
            if bone.rotation_mode == 'QUATERNION':
                bone.rotation_mode = 'XYZ'

        # Process animation data if exists
        if ob.animation_data and ob.animation_data.action:
            action = ob.animation_data.action
            fcurves_to_remove = []

            # Collect fcurves to remove and quaternion channels
            for fcurve in action.fcurves:
                if "rotation_mode" in fcurve.data_path:
                    fcurves_to_remove.append(fcurve)
                elif "quaternion" in fcurve.data_path and fcurve.group:
                    quaternion_channels.add(fcurve.group.name)

            # Remove collected fcurves
            for fcurve in fcurves_to_remove:
                action.fcurves.remove(fcurve)

        # Report results
        if quaternion_channels:
            self.report({'INFO'}, f"Quaternion keys found on bones: {', '.join(quaternion_channels)}")
        else:
            self.report({'INFO'}, "Rotation modes converted and keyframes cleaned")
        
        return {'FINISHED'}

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