# LinkForge Documentation

Welcome to LinkForge's documentation!

**LinkForge** is a professional Blender extension for roboticists.

**In robotics, creativity starts in your head — but getting that idea into a simulator usually means hours of writing XML, fixing joint limits, and fighting coordinate systems.**

LinkForge removes that friction. Model your robot in Blender as naturally as sculpting a 3D scene, then let LinkForge handle the engineering.

**From idea → robot → ready for simulation.** All inside Blender.

```{toctree}
:maxdepth: 2
:caption: Contents:

getting_started
ARCHITECTURE
api/index
CONTRIBUTING
CHANGELOG
README
LICENSE
```

## Quick Links

- [GitHub Repository](https://github.com/arounamounchili/linkforge)
- [Issue Tracker](https://github.com/arounamounchili/linkforge/issues)
- [Discussions](https://github.com/arounamounchili/linkforge/discussions)

## Features

- **Bidirectional Workflow**: Seamlessly import existing URDF/XACRO files for editing or build complex robot models from scratch using Blender's native tools.
- **Production-Ready Export**: Generates strictly compliant URDF/XACRO files optimized for ROS, ROS 2, and Gazebo. Output is clean, validated, and requires no manual post-processing.
- **Smart Validation**: Built-in integrity checker inspects robot topology, physics data, and joint limits to prevent common simulation crashes before they happen.
- **ROS2 Control Support**: Automatically generates hardware interface configurations for `ros2_control`, compatible with Gazebo, Webots, Isaac Sim, and physical hardware.
- **Complete Sensor Suite**: Integrated support for Camera, Depth Camera, LiDAR, IMU, GPS, and Force/Torque sensors with configurable noise models.
- **Automatic Physics**: Scientifically accurate calculation of mass properties and inertia tensors for both primitive shapes and complex arbitrary meshes.
- **Advanced XACRO Support**: Intelligent extraction of repeated geometry into macros and shared materials, producing maintainable and modular code.
- **Round-Trip Fidelity**: Import → Edit → Export cycle preserves all data absolute precision, including sensor origins, transmission interfaces, and custom user properties.
- **Interactive Kinematic Visualization**: Real-time rendering of joint coordinate frames (`RGB=XYZ`) in the viewport, enabling instant visual verification of kinematic chain orientations.


## 🛠️ Workflow

LinkForge follows a structured **Forge → Perceive → Control → Export** workflow:

### 1. Forge Links
- Convert meshes to robot links with automatic naming
- Generate optimized collision geometry
- Calculate physics properties (mass, inertia)
- Reversible actions (safely remove links)

### 2. Forge Joints
- Connect links with precise joint configuration
- Visual feedback for joint axes in viewport
- Full CRUD operations (Create, Read, Update, Delete)
- Support for all URDF joint types

### 3. Perceive (Sensors)
- Attach sensors to links
- Configure update rates, resolutions, noise models
- Gazebo plugin integration

### 4. Control (Transmissions)
- Configure hardware interfaces (Position, Velocity, Effort)
- Set up mechanical reductions and joint limits
- Auto-generate `ros2_control` tags

### 5. Validate & Export
- Built-in validator catches common errors
- Export to URDF or XACRO with mesh handling

## Installation

### Requirements
- Blender 4.2 or later
- Python 3.11+

### Installation

1. **Download**: Get `linkforge-1.0.0.zip` from [Releases](https://github.com/arounamounchili/linkforge/releases).
2. **Open Blender**: Go to **Edit > Preferences > Get Extensions**.
3. **Install**: Click the dropdown (⌄) in top-right → **Install from Disk**.
4. **Select**: Choose the downloaded `.zip` file.


## Indices and tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
