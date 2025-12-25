# How-to: Configure Transmissions & Control

This guide explains how to set up transmissions and `ros2_control` interfaces for your actuated joints.

## 1. Enable Control
Before adding transmissions, ensure the global control setting is enabled:
1. Go to the **Robot** tab in the LinkForge panel.
2. Check **Enable ros2_control**.
3. (Optional) Set the hardware system name (default: `GazeboSimSystem`).

## 2. Add a Transmission
1. Select the **Joint** you want to actuate (either in the viewport or via the Outliner).
2. Go to the **Transmissions** tab in LinkForge.
3. Click **Add Transmission**.

## 3. Configure Hardware Interfaces
A transmission can support multiple hardware interfaces. For most ROS 2 controllers, you should select at least one:
- **Position**: For standard servo-like control.
- **Velocity**: For wheels or continuous rotation.
- **Effort**: For torque-based control.

## 4. Mechanical Reduction
You can set a **Mechanical Reduction** factor (default is 1.0). This generates the `<mechanicalReduction>` tag in the URDF, which is used by some physics engines to simulate gearboxes.

## 5. Multiple Actuators
If your joint is driven by multiple motors (rare but supported by URDF), you can add multiple actuators to a single transmission by clicking the **+** button in the list.
