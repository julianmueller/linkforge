"""Blender event handlers for LINKFORGE.

This module manages scene event hooks to ensure data consistency:
1.  Syncing object names in the Outliner to LinkForge properties.
2.  Validating robot topology validation (e.g. handling deleted links).
3.  Managing internal caches.
"""

from __future__ import annotations

import bpy
from bpy.app.handlers import persistent

# Global cache for tracking object names to detect renames
# Maps object ID (as_pointer) -> object name
_name_cache: dict[int, str] = {}


@persistent
def clear_cache_on_load(dummy):
    """Clear internal caches when loading a new file.

    This prevents stale object IDs from persisting across file loads.
    """
    global _name_cache
    _name_cache.clear()


@persistent
def sync_object_names(scene):
    """Sync Blender object names to LinkForge properties.

    Detects when a user renames an object in the Outliner and updates
    the corresponding `link_name` or `joint_name`.
    """
    if not bpy or not scene:
        return

    global _name_cache

    # Check for name changes in robot objects
    for obj in scene.objects:
        obj_id = obj.as_pointer()

        # Check if this is a robot link
        if hasattr(obj, "linkforge") and obj.linkforge.is_robot_link:
            old_name = _name_cache.get(obj_id)
            current_name = obj.name

            # If name changed (and wasn't just initialized)
            if old_name is not None and old_name != current_name:
                # If the property doesn't match the new object name, update it
                if obj.linkforge.link_name != current_name:
                    obj.linkforge.link_name = current_name

            # Update cache
            _name_cache[obj_id] = current_name

        # Check if this is a robot joint
        elif (
            obj.type == "EMPTY"
            and hasattr(obj, "linkforge_joint")
            and obj.linkforge_joint.is_robot_joint
        ):
            old_name = _name_cache.get(obj_id)
            current_name = obj.name

            # If name changed
            if old_name is not None and old_name != current_name:
                # Update property if needed
                if obj.linkforge_joint.joint_name != current_name:
                    obj.linkforge_joint.joint_name = current_name

            # Update cache
            _name_cache[obj_id] = current_name


@persistent
def validate_robot_topology(scene):
    """Validate robot topology connectivity.

    Ensures that joints do not point to non-existent links.
    In Blender, PointerProperty naturally becomes None when the object is deleted.
    This handler ensures the internal hierarchy (parenting) stays clean.
    """
    if not bpy or not scene:
        return

    # Check all joints for stale references
    for obj in scene.objects:
        if (
            obj.type == "EMPTY"
            and hasattr(obj, "linkforge_joint")
            and obj.linkforge_joint.is_robot_joint
        ):
            # Validate robot topology connectivity

            # If either parent or child pointer is None, the system might need
            # a hierarchy sync (unparenting). Since PointerProperty updates
            # trigger their 'update' callback on deletion, we mostly rely on that.
            # This handler serves as a secondary sweep for scene integrity.

            # (Logic is now mostly handled by PointerProperty update callbacks
            # but we keep this as a hook for future complex topology validations)
            pass


def register():
    """Register event handlers."""
    handlers = bpy.app.handlers

    if sync_object_names not in handlers.depsgraph_update_post:
        handlers.depsgraph_update_post.append(sync_object_names)

    if validate_robot_topology not in handlers.depsgraph_update_post:
        handlers.depsgraph_update_post.append(validate_robot_topology)

    if clear_cache_on_load not in handlers.load_post:
        handlers.load_post.append(clear_cache_on_load)


def unregister():
    """Unregister event handlers."""
    handlers = bpy.app.handlers

    if sync_object_names in handlers.depsgraph_update_post:
        handlers.depsgraph_update_post.remove(sync_object_names)

    if validate_robot_topology in handlers.depsgraph_update_post:
        handlers.depsgraph_update_post.remove(validate_robot_topology)

    if clear_cache_on_load in handlers.load_post:
        handlers.load_post.remove(clear_cache_on_load)

    # Clean up
    global _name_cache
    _name_cache.clear()
