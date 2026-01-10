"""UI Panel for managing robot transmissions."""

from __future__ import annotations

import bpy
from bpy.types import Context, Panel


class LINKFORGE_PT_control(Panel):
    """Panel for configuring motor control and transmissions."""

    bl_label = "Control"
    bl_description = "Step 3: Configure actuators and transmissions for ROS2 Control"
    bl_idname = "LINKFORGE_PT_control"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LinkForge"
    bl_order = 2
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context: Context):
        """Draw the panel."""
        layout = self.layout
        obj = context.active_object

        # Check if selected object is a transmission (edit mode vs create mode)
        is_transmission = (
            obj
            and obj.select_get()
            and obj.type == "EMPTY"
            and obj.linkforge_transmission.is_robot_transmission
        )

        # Only show Create button when NOT editing a transmission
        if not is_transmission:
            # Detect if a joint is selected
            target_joint = None
            if (
                obj
                and obj.select_get()
                and obj.type == "EMPTY"
                and obj.linkforge_joint.is_robot_joint
            ):
                target_joint = obj

            # Create Transmission button (creation mode)
            box = layout.box()
            row = box.row()
            row.enabled = target_joint is not None
            row.operator("linkforge.create_transmission", icon="ADD", text="Create Transmission")

        # Show transmission properties only if a transmission is selected (edit mode)
        if not is_transmission:
            return

        props = obj.linkforge_transmission

        # === TRANSMISSION IDENTIFICATION ===
        box = layout.box()
        box.label(text=f"Transmission: {obj.name}", icon="CON_TRANSLIKE")
        box.prop(props, "transmission_name")
        box.prop(props, "transmission_type")

        # Custom type field (if CUSTOM is selected)
        if props.transmission_type == "CUSTOM":
            box.prop(props, "custom_type")

        # === JOINT SELECTION ===
        box.separator()
        box.label(text="Joints", icon="LINKED")

        if props.transmission_type == "SIMPLE" or props.transmission_type == "CUSTOM":
            box.prop(props, "joint_name", text="Joint", icon="OUTLINER_OB_EMPTY")

        elif (
            props.transmission_type == "DIFFERENTIAL"
            or props.transmission_type == "FOUR_BAR_LINKAGE"
        ):
            box.prop(props, "joint1_name", text="Joint 1", icon="OUTLINER_OB_EMPTY")
            box.prop(props, "joint2_name", text="Joint 2", icon="OUTLINER_OB_EMPTY")

        # === HARDWARE INTERFACE ===
        box.separator()
        box.label(text="Hardware Interface", icon="SETTINGS")
        box.prop(props, "hardware_interface")

        # === MECHANICAL PROPERTIES ===
        box.separator()
        box.label(text="Mechanical Properties", icon="TOOL_SETTINGS")
        box.prop(props, "mechanical_reduction")
        box.prop(props, "offset")

        # === ACTUATOR NAMING ===
        box.separator()
        box.label(text="Actuator Naming", icon="DRIVER")
        box.prop(props, "use_custom_actuator_name")

        if props.use_custom_actuator_name:
            if props.transmission_type == "SIMPLE":
                box.prop(props, "actuator_name", text="Name")
            elif (
                props.transmission_type == "DIFFERENTIAL"
                or props.transmission_type == "FOUR_BAR_LINKAGE"
            ):
                box.prop(props, "actuator1_name", text="Actuator 1")
                box.prop(props, "actuator2_name", text="Actuator 2")

        # Remove Transmission button (Danger Zone)
        box.separator()
        box.separator()
        row = box.row()
        row.scale_y = 1.2  # Make it slightly bigger
        row.operator("linkforge.delete_transmission", icon="TRASH", text="Remove Transmission")


# Registration
classes = [
    LINKFORGE_PT_control,
]


def register():
    """Register panel."""
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            bpy.utils.unregister_class(cls)
            bpy.utils.register_class(cls)


def unregister():
    """Unregister panel."""
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass


if __name__ == "__main__":
    register()
