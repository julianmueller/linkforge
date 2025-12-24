# Getting Started

This guide will help you get started with LinkForge.

## Installation

See the [main page](index.md#installation) for installation instructions.

## Creating Your First Robot

### 1. Create Links

Links are the rigid bodies of your robot.

1. Create or select a mesh in Blender
2. Open the **LinkForge** panel (3D Viewport sidebar)
3. Click **Create Link**
4. Configure:
   - **Mass**: Total mass in kg
   - **Inertia**: Automatically calculated or custom
   - **Collision**: Simplified geometry for physics

### 2. Connect with Joints

Joints connect links and define how they move.

1. Select the **child link**
2. Click **Create Joint**
3. Choose joint type:
   - **Fixed**: No movement
   - **Revolute**: Rotation with limits
   - **Continuous**: Unlimited rotation
   - **Prismatic**: Linear sliding
   - **Planar**: 2D movement
   - **Floating**: 6-DOF movement
4. Set parent link and configure limits

### 3. Add Sensors (Optional)

Add sensors for simulation.

1. Select the link to attach sensor to
2. Go to **Sensors** tab
3. Click **Add Sensor**
4. Choose type: Camera, LiDAR, IMU, GPS, etc.
5. Configure sensor parameters

### 4. Configure ROS2 Control (Optional)

For actuated joints:

1. Go to **Robot** tab
2. Enable **Generate ROS2 Control**
3. Select joints to control
4. Choose hardware interfaces (position, velocity, effort)

### 5. Export

1. Go to **Export** tab
2. Choose format:
   - **URDF**: Standard format
   - **XACRO**: Parameterized format with macros
3. Configure export options:
   - **Validate Before Export**: Check for errors
   - **Export Meshes**: Include mesh files
   - **Mesh Format**: OBJ, STL, DAE, etc.
4. Click **Export URDF** or **Export XACRO**

## Importing Existing URDF

1. **File > Import > URDF (.urdf)**
2. Select your URDF file
3. Robot appears in viewport with:
   - Links as Blender objects
   - Joints as parent-child relationships
   - Properties preserved

## Example Workflow

### Mobile Robot

```python
# 1. Create base link
base = create_box(size=(0.6, 0.4, 0.1), mass=10.0)
create_link(base, name="base_link")

# 2. Create wheels
wheel_fl = create_cylinder(radius=0.1, length=0.05, mass=0.8)
create_link(wheel_fl, name="front_left_wheel")

# 3. Connect with joint
create_joint(
    child="front_left_wheel",
    parent="base_link",
    type="continuous",
    axis=(0, 1, 0)
)

# 4. Add LiDAR sensor
add_sensor(
    link="base_link",
    type="lidar",
    position=(0, 0, 0.15)
)

# 5. Export
export_urdf("mobile_robot.urdf")
```

## Tips and Best Practices

### Modeling

- **Use primitives** (box, cylinder, sphere) when possible for better physics performance
- **Keep link origins** at the center of mass for accurate physics
- **Name links clearly** (e.g., `left_wheel`, `arm_link_2`)
- **Use collections** to organize complex robots

### Physics

- **Set realistic masses**: Use real-world values
- **Check inertia**: Auto-calculation works for primitives
- **Simplify collision**: Use simple shapes for collision geometry
- **Validate before export**: Catch errors early

### Joints

- **Set proper limits**: Prevent unrealistic motion
- **Use continuous** for wheels (unlimited rotation)
- **Add dynamics**: Damping and friction for realistic behavior
- **Visualize axes**: Enable joint visualization to verify directions

### Export

- **Validate first**: Always enable validation
- **Export meshes**: Include mesh files for portability
- **Use XACRO** for complex robots with repeated elements
- **Test in simulator**: Verify exported URDF works

## Common Issues

### "Link has no inertia"

**Solution**: Set mass and inertia in link properties. Use auto-calculation for primitives.

### "Joint axis is zero"

**Solution**: Ensure joint axis is set correctly (e.g., (0, 0, 1) for Z-axis rotation).

### "Disconnected links detected"

**Solution**: All links except root must be connected via joints. Check joint parent-child relationships.

### "Mesh file not found"

**Solution**: Enable "Export Meshes" and ensure mesh export path is correct.

## Next Steps

- Read the [Architecture Guide](ARCHITECTURE.md) to understand LinkForge's design
- Check the [API Reference](api/index.md) for programmatic usage
- See [Contributing Guide](CONTRIBUTING.md) to contribute

## Support

- [GitHub Issues](https://github.com/arounamounchili/linkforge/issues) - Bug reports and feature requests
- [Discussions](https://github.com/arounamounchili/linkforge/discussions) - Questions and community support
- [Examples](https://github.com/arounamounchili/linkforge/tree/main/examples) - Sample URDF files
