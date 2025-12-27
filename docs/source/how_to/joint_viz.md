# How-to: Customize Joint Visualization

LinkForge provides semantic visual feedback in the viewport to help you verify robot kinematics instantly.

## 1. The XYZ Frame
When a joint is created, LinkForge renders a small coordinate frame at the joint origin:
- **Red**: X-Axis
- **Green**: Y-Axis
- **Blue**: Z-Axis

## 2. Visualization Styles
LinkForge offers two ways to visualize joint axes, both configurable in Blender Preferences:

### Empty Display (Standard)
This is the default visualization using standard Blender Empty arrows.
1. Open Blender **Preferences** (`Edit > Preferences`).
2. Go to the **Add-ons** (or **Extensions**) tab and find **LinkForge**.
3. Under the **Joint Visualization** section, locate **Empty Display**.
4. Adjust the **Size** slider. This changes the physical size of the joint markers in the viewport.

### Enhanced GPU Overlay (RViz-style)
For a more professional look similar to ROS tools, you can enable a thick, arrowed overlay.
1. In the same LinkForge Preferences, check **Enhanced GPU Overlay (RViz-style)**.
2. Adjust the **Overlay Length** to match your robot's scale.
3. This adds thicker red/green/blue arrows with cone tips that remain visible even when the robot is obscured.

## 3. Cleaning the View
To hide all LinkForge markers for a final render or clean view:
- Use the standard Blender **Hide Extras** toggle in the Viewport Overlays menu (top right of the 3D View).
- Since LinkForge joints are standard Empty objects, hiding "Extras" will hide all joint, link, and sensor markers instantly.
