import bpy

class OBJECT_OT_confirm_delete_quaternions(bpy.types.Operator):
    """Delete remaining quaternion keyframes"""
    bl_idname = "object.confirm_delete_quaternions"
    bl_label = "Delete Quaternion Keys?"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        wm = context.window_manager
        self.bone_list = wm.quaternion_channels.split(',') if wm.quaternion_channels else []
        return context.window_manager.invoke_props_dialog(self, width=400)

    def execute(self, context):
        ob = context.active_object
        quaternion_channels = set()

        # --- ALWAYS RUN THESE STEPS ---
        # Convert rotation modes (this always happens)
        for bone in ob.pose.bones:
            if bone.rotation_mode == 'QUATERNION':
                bone.rotation_mode = 'XYZ'

        # Always remove rotation mode keyframes
        if ob.animation_data and ob.animation_data.action:
            action = ob.animation_data.action
            fcurves_to_remove = [
                fcurve for fcurve in action.fcurves
                if "rotation_mode" in fcurve.data_path
            ]
            
            for fcurve in fcurves_to_remove:
                action.fcurves.remove(fcurve)

        # --- CONDITIONAL QUATERNION HANDLING ---
        # Only check for quaternion keys after core operations
        if ob.animation_data and ob.animation_data.action:
            action = ob.animation_data.action
            quaternion_channels = {
                fcurve.group.name for fcurve in action.fcurves
                if "quaternion" in fcurve.data_path and fcurve.group
            }

        if quaternion_channels:
            wm = context.window_manager
            wm.quaternion_channels = ','.join(quaternion_channels)
            # Show dialog but CORE OPERATIONS ARE ALREADY DONE
            bpy.ops.object.confirm_delete_quaternions('INVOKE_DEFAULT')
            self.report({'INFO'}, "Core conversion done - check popup for quaternions")
        else:
            self.report({'INFO'}, "Rotation converted with no quaternion keys")
        
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.label(text=f"Found quaternion keys on {len(self.bone_list)} bones:")
        col = layout.column(align=True)
        for bone in self.bone_list:
            col.label(text=f"- {bone}")
        layout.separator()
        layout.label(text="Delete these quaternion keys?")

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

        # Process animation data
        if ob.animation_data and ob.animation_data.action:
            action = ob.animation_data.action
            fcurves_to_remove = []

            for fcurve in action.fcurves:
                if "rotation_mode" in fcurve.data_path:
                    fcurves_to_remove.append(fcurve)
                elif "quaternion" in fcurve.data_path and fcurve.group:
                    quaternion_channels.add(fcurve.group.name)

            # Remove rotation mode curves
            for fcurve in fcurves_to_remove:
                action.fcurves.remove(fcurve)

        # Handle quaternion channels
        if quaternion_channels:
            wm = context.window_manager
            wm.quaternion_channels = ','.join(quaternion_channels)
            bpy.ops.object.confirm_delete_quaternions('INVOKE_DEFAULT')
            self.report({'INFO'}, "Found quaternion keys - check popup dialog")
        else:
            self.report({'INFO'}, "Rotation modes converted, no quaternion keys found")
        
        return {'FINISHED'}