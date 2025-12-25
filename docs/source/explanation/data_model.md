# Explanation: The LinkForge Data Model

To understand how LinkForge converts a Blender scene into a URDF, it's important to understand the underlying data model.

## Why not just use Blender groups?
Standard Blender parent-child relationships don't store enough information for robotics simulation (like joint types, axis orientations, or mass properties).

## The Three Layers
LinkForge maintains a parallel data structure that maps Blender objects to URDF elements:

1. **Blender Object Layer**: The visual mesh and collision geometry you see in the viewport.
2. **LinkForge Property Layer**: Hidden custom properties attached to Blender objects that store mass, inertia, and joint settings.
3. **Core URDF Model**: An immutable Python object created only during validation/export that ensures the robot tree is mathematically sound.

## Coordinate Frames
Blender uses a **Right-Handed Z-Up** coordinate system. LinkForge ensures that when you export to URDF (which is also Right-Handed), all offsets and rotations are correctly converted so your robot "stands up" correctly in Gazebo.
