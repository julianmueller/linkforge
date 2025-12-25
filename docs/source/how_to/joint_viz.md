# How-to: Customize Joint Visualization

LinkForge provides semantic visual feedback in the viewport to help you verify robot kinematics instantly.

## 1. The XYZ Frame
When a joint is created, LinkForge renders a small coordinate frame at the joint origin:
- **Red**: X-Axis
- **Green**: Y-Axis
- **Blue**: Z-Axis

## 2. Changing Visualization Size
If your robot is very large or very small, the default coordinate frames might be hard to see.
1. Open Blender **Preferences** (`Edit > Preferences`).
2. Go to the **Add-ons** (or **Extensions**) tab.
3. Find **LinkForge** and expand its settings.
4. Locate the **Joint Visualization Size** slider.
5. Adjust it to your preference. This change is saved across Blender sessions.

## 3. Toggling Visuals
You can toggle the entire kinematic visualization on or off:
1. In the **LinkForge** panel, go to the **Robot** (or **Display**) tab.
2. Toggle the **Show Joint Frames** checkbox.
3. This is useful when you want a clean view of your meshes for rendering.
