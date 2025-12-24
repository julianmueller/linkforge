"""Blender addon preferences for LinkForge.

User preferences for controlling visualization and behavior.
"""

from __future__ import annotations

import bpy
from bpy.props import BoolProperty, FloatProperty
from bpy.types import AddonPreferences


def update_joint_axes_visibility(self, context):
    """Callback when show_joint_axes changes - force viewport redraw."""
    # Force all 3D viewports to redraw
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == "VIEW_3D":
                area.tag_redraw()


def update_joint_axis_length(self, context):
    """Callback when joint_axis_length changes - force viewport redraw."""
    # Force all 3D viewports to redraw
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == "VIEW_3D":
                area.tag_redraw()


def update_joint_empty_size(self, context):
    """Callback when joint_empty_size changes - update all joint empties."""

    # Get new size
    new_size = self.joint_empty_size

    # Update all existing joint empties in the scene
    for obj in context.scene.objects:
        if (
            obj.type == "EMPTY"
            and hasattr(obj, "linkforge_joint")
            and obj.linkforge_joint.is_robot_joint
        ):
            obj.empty_display_size = new_size

    # Force viewport redraw
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == "VIEW_3D":
                area.tag_redraw()


def update_sensor_empty_size(self, context):
    """Callback when sensor_empty_size changes - update all sensor empties."""

    # Get new size
    new_size = self.sensor_empty_size

    # Update all existing sensor empties in the scene
    for obj in context.scene.objects:
        if (
            obj.type == "EMPTY"
            and hasattr(obj, "linkforge_sensor")
            and obj.linkforge_sensor.is_robot_sensor
        ):
            obj.empty_display_size = new_size

    # Force viewport redraw
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == "VIEW_3D":
                area.tag_redraw()


def update_transmission_empty_size(self, context):
    """Callback when transmission_empty_size changes - update all transmission empties."""

    # Get new size
    new_size = self.transmission_empty_size

    # Update all existing transmission empties in the scene
    for obj in context.scene.objects:
        if (
            obj.type == "EMPTY"
            and hasattr(obj, "linkforge_transmission")
            and obj.linkforge_transmission.is_robot_transmission
        ):
            obj.empty_display_size = new_size

    # Force viewport redraw
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == "VIEW_3D":
                area.tag_redraw()


def update_link_empty_size(self, context):
    """Callback when link_empty_size changes - update all link empties."""

    # Get new size
    new_size = self.link_empty_size

    # Update all existing link empties in the scene
    for obj in context.scene.objects:
        if obj.type == "EMPTY" and hasattr(obj, "linkforge") and obj.linkforge.is_robot_link:
            obj.empty_display_size = new_size

    # Force viewport redraw
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == "VIEW_3D":
                area.tag_redraw()


class LinkForgePreferences(AddonPreferences):
    """User preferences for LinkForge extension."""

    bl_idname = "bl_ext.user_default.linkforge"

    # Joint axis visualization (GPU overlay - optional enhancement)
    show_joint_axes: BoolProperty(  # type: ignore
        name="Show GPU Overlay Axes",
        description="Show thick RGB arrows at each joint (Red=X, Green=Y, Blue=Z) like RViz visualization",
        default=False,
        update=update_joint_axes_visibility,
    )

    joint_axis_length: FloatProperty(  # type: ignore
        name="Axis Length",
        description="How long the RGB arrows should be (adjust based on your robot size)",
        default=0.2,
        min=0.01,
        max=100.0,
        soft_min=0.05,
        soft_max=5.0,
        step=5,
        precision=2,
        unit="LENGTH",
        update=update_joint_axis_length,
    )

    joint_empty_size: FloatProperty(  # type: ignore
        name="Empty Size",
        description="Size of the joint markers in viewport (bigger = easier to select, smaller = cleaner view)",
        default=0.2,
        min=0.01,
        max=100.0,
        soft_min=0.05,
        soft_max=5.0,
        step=1,
        precision=2,
        unit="LENGTH",
        update=update_joint_empty_size,  # Update all joint empties when changed
    )

    sensor_empty_size: FloatProperty(  # type: ignore
        name="Sensor Empty Size",
        description="Size of the sensor markers in viewport (bigger = easier to select, smaller = cleaner view)",
        default=0.1,
        min=0.01,
        max=100.0,
        soft_min=0.05,
        soft_max=5.0,
        step=1,
        precision=2,
        unit="LENGTH",
        update=update_sensor_empty_size,  # Update all sensor empties when changed
    )

    transmission_empty_size: FloatProperty(  # type: ignore
        name="Transmission Empty Size",
        description="Size of the transmission markers in viewport (bigger = easier to select, smaller = cleaner view)",
        default=0.05,
        min=0.01,
        max=100.0,
        soft_min=0.05,
        soft_max=5.0,
        step=1,
        precision=2,
        unit="LENGTH",
        update=update_transmission_empty_size,  # Update all transmission empties when changed
    )

    link_empty_size: FloatProperty(  # type: ignore
        name="Link Empty Size",
        description="Size of the link markers in viewport (bigger = easier to select, smaller = cleaner view)",
        default=0.1,
        min=0.01,
        max=100.0,
        soft_min=0.05,
        soft_max=5.0,
        step=1,
        precision=2,
        unit="LENGTH",
        update=update_link_empty_size,  # Update all link empties when changed
    )

    def draw(self, context):
        """Draw the preferences UI."""
        layout = self.layout

        # Joint visualization
        box = layout.box()
        box.label(text="Joint Visualization", icon="EMPTY_ARROWS")

        # Empty display settings (always visible)
        row = box.row()
        row.label(text="Empty Display:", icon="EMPTY_AXIS")
        row = box.row()
        row.prop(self, "joint_empty_size", text="Size", slider=True)

        col = box.column(align=True)
        col.scale_y = 0.7
        col.label(text="Joint empties show RGB colored axes (Red=X, Green=Y, Blue=Z)")

        # GPU overlay (optional enhancement)
        box.separator()
        row = box.row()
        row.prop(self, "show_joint_axes", text="Enhanced GPU Overlay (RViz-style)")

        row = box.row()
        row.prop(self, "joint_axis_length", text="Overlay Length", slider=True)
        row.enabled = self.show_joint_axes

        if self.show_joint_axes:
            col = box.column(align=True)
            col.scale_y = 0.7
            col.label(text="Adds thicker, more prominent axes with arrow cones", icon="INFO")

        # Sensor visualization
        layout.separator()
        box = layout.box()
        box.label(text="Sensor Visualization", icon="LIGHT_SUN")
        row = box.row()
        row.prop(self, "sensor_empty_size", text="Sensor Empty Size", slider=True)

        # Transmission visualization
        layout.separator()
        box = layout.box()
        box.label(text="Transmission Visualization", icon="DRIVER")
        row = box.row()
        row.prop(self, "transmission_empty_size", text="Transmission Empty Size", slider=True)

        # Link visualization
        layout.separator()
        box = layout.box()
        box.label(text="Link Visualization", icon="LINKED")
        row = box.row()
        row.prop(self, "link_empty_size", text="Link Empty Size", slider=True)

        # General help text
        layout.separator()
        col = layout.column(align=True)
        col.scale_y = 0.7
        col.label(text="Tip: Larger empties are easier to click in viewport", icon="HAND")
        col.label(text="Use Outliner to select components if empties are too small")


def register():
    """Register preferences."""
    bpy.utils.register_class(LinkForgePreferences)


def unregister():
    """Unregister preferences."""
    bpy.utils.unregister_class(LinkForgePreferences)


if __name__ == "__main__":
    register()
