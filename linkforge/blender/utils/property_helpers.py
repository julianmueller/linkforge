"""Helper utilities for Blender property groups.

This module provides optimized helper functions for property update callbacks.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass


def find_property_owner(context: Any, property_group: Any, property_attr: str) -> Any | None:
    """Find the Blender object that owns a given property group instance.

    This is an optimized helper for property update callbacks that need to find
    their owning object. It tries multiple strategies from fastest to slowest:
    1. Check context.object (active object) first
    2. Check context.selected_objects
    3. Fall back to full scene search as last resort

    Args:
        context: Blender context
        property_group: The property group instance (self in update callback)
        property_attr: The attribute name on objects (e.g., "linkforge_sensor")

    Returns:
        The object that owns this property group, or None if not found

    Example:
        >>> def update_sensor_name(self, context):
        >>>     obj = find_property_owner(context, self, "linkforge_sensor")
        >>>     if obj:
        >>>         obj.name = self.sensor_name
    """
    if not context:
        return None

    # Strategy 1: Check active object first (most common case)
    if hasattr(context, "object") and context.object:
        if hasattr(context.object, property_attr):
            if getattr(context.object, property_attr) == property_group:
                return context.object

    # Strategy 2: Check selected objects (faster than full scene search)
    if hasattr(context, "selected_objects"):
        for obj in context.selected_objects:
            if hasattr(obj, property_attr):
                if getattr(obj, property_attr) == property_group:
                    return obj

    # Strategy 3: Fall back to full scene search (slowest)
    if hasattr(context, "scene") and context.scene:
        for obj in context.scene.objects:
            if hasattr(obj, property_attr):
                if getattr(obj, property_attr) == property_group:
                    return obj

    return None
