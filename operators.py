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
        deleted_quat = 0
        deleted_mode = 0

        # Step 1: Delete quaternion keys FIRST
        if ob.animation_data and ob.animation_data.action:
            action = ob.animation_data.action
            
            # Find quaternion curves
            quat_curves = [
                fcurve for fcurve in action.fcurves
                if "rotation_quaternion" in fcurve.data_path
            ]
            
            # Find rotation mode curves
            mode_curves = [
                fcurve for fcurve in action.fcurves
                if "rotation_mode" in fcurve.data_path
            ]

            # Remove quaternion curves
            deleted_quat = len(quat_curves)
            for fcurve in quat_curves:
                action.fcurves.remove(fcurve)

            # Remove rotation mode curves
            deleted_mode = len(mode_curves)
            for fcurve in mode_curves:
                action.fcurves.remove(fcurve)

        # Step 2: Convert rotation modes AFTER keyframe deletion
        for bone in ob.pose.bones:
            if bone.rotation_mode == 'QUATERNION':
                bone.rotation_mode = 'XYZ'

        # Report results
        msg_parts = []
        if deleted_quat:
            msg_parts.append(f"Deleted {deleted_quat} quaternion keys")
        if deleted_mode:
            msg_parts.append(f"Deleted {deleted_mode} rotation mode keys")
        if not msg_parts:
            msg_parts.append("Rotation modes converted - no keys to delete")
        
        self.report({'INFO'}, " | ".join(msg_parts))
        return {'FINISHED'}