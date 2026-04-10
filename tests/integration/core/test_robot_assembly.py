from pathlib import Path

import pytest
from linkforge_core.composer import RobotAssembly
from linkforge_core.parsers import SRDFParser, URDFParser, XACROParser


def test_robot_assembly(examples_dir: Path) -> None:
    """Build an assembly from separately resolved URDF-XACRO and SRDF-XACRO files."""
    package_root = examples_dir / "robot_assembly"

    xacro_parser = XACROParser()
    urdf_parser = URDFParser()
    srdf_parser = SRDFParser()

    robot_urdf = urdf_parser.parse_xacro(
        package_root / "urdf" / "robot.urdf.xacro",
        tool_offset="0.24",
        include_alignment_pin="true",
    )

    adapter_urdf = urdf_parser.parse_xacro(
        package_root / "urdf" / "adapter.urdf.xacro",
        flange_offset="0.09",
        include_support_block="true",
    )

    endeffector_urdf = urdf_parser.parse_xacro(
        package_root / "urdf" / "endeffector.urdf.xacro",
        finger_length="0.14",
        include_tip_pad="true",
    )

    robot_srdf = srdf_parser.parse_xacro(
        package_root / "srdf" / "robot.srdf.xacro",
        include_world_joint="true",
        include_alignment_pin_joint="true",
    )

    adapter_srdf = srdf_parser.parse_xacro(
        package_root / "srdf" / "adapter.srdf.xacro",
        include_support_block="true",
        collision_reason="Mounted",
    )

    endeffector_srdf = srdf_parser.parse_xacro(
        package_root / "srdf" / "endeffector.srdf.xacro",
        include_tip_pad="true",
    )

    robot_assembly = RobotAssembly(urdf=robot_urdf, srdf=robot_srdf)
    adapter_assembly = RobotAssembly(urdf=adapter_urdf, srdf=adapter_srdf)
    endeffector_assembly = RobotAssembly(urdf=endeffector_urdf, srdf=endeffector_srdf)

    robot_assembly.attach(
        adapter_assembly,
        at_link="tool_flange",
        joint_name="adapter_attachment_link",
    )
    robot_assembly.attach(
        endeffector_assembly,
        at_link="adapter_flange",
        joint_name="endeffector_attachment_link",
    )

    assert robot_assembly.urdf.get_link("base_link") is not None
    assert robot_assembly.urdf.get_link("alignment_pin") is not None
    assert robot_assembly.urdf.get_link("adapter_flange") is not None
    assert robot_assembly.urdf.get_link("finger_link") is not None
    assert robot_assembly.urdf.get_link("support_block") is not None
    assert robot_assembly.urdf.get_link("compact_cap") is None
    assert robot_assembly.urdf.get_link("finger_pad") is not None

    assert robot_assembly.urdf.get_joint("tool_mount_joint") is not None
    assert robot_assembly.urdf.get_joint("alignment_pin_joint") is not None
    assert robot_assembly.urdf.get_joint("adapter_attachment_link") is not None
    assert robot_assembly.urdf.get_joint("adapter_support_joint") is not None
    assert robot_assembly.urdf.get_joint("endeffector_attachment_link") is not None
    assert robot_assembly.urdf.get_joint("finger_joint") is not None
    assert robot_assembly.urdf.get_joint("finger_pad_joint") is not None

    assert robot_urdf.get_joint("tool_mount_joint").origin.xyz.x == pytest.approx(0.24)
    assert adapter_urdf.get_joint("adapter_body_joint").origin.xyz.x == pytest.approx(0.09)
    assert endeffector_urdf.get_joint("finger_joint").origin.xyz.x == pytest.approx(0.07)
    assert endeffector_urdf.get_link("finger_link").visuals[0].geometry.size.x == pytest.approx(
        0.14
    )

    passive_joint_names = {joint.name for joint in robot_assembly.srdf.passive_joints}
    assert passive_joint_names == {
        "tool_mount_joint",
        "alignment_pin_joint",
        "adapter_body_joint",
        "finger_joint",
    }

    disabled_collision_pairs = {
        (collision.link1, collision.link2) for collision in robot_assembly.srdf.disabled_collisions
    }
    assert ("adapter_base", "adapter_flange") in disabled_collision_pairs
    assert ("adapter_base", "support_block") in disabled_collision_pairs
    assert ("endeffector_base", "finger_link") in disabled_collision_pairs
    assert ("finger_link", "finger_pad") in disabled_collision_pairs
    assert ("adapter_base", "compact_cap") not in disabled_collision_pairs

    adapter_collision_reasons = {
        (collision.link1, collision.link2): collision.reason
        for collision in robot_assembly.srdf.disabled_collisions
    }
    assert adapter_collision_reasons[("adapter_base", "adapter_flange")] == "Mounted"
    assert adapter_collision_reasons[("adapter_base", "support_block")] == "Mounted"

    virtual_joint_names = {joint.name for joint in robot_assembly.srdf.virtual_joints}
    assert virtual_joint_names == {"world_joint"}

    urdf_xml = robot_assembly.export_urdf()
    srdf_xml = robot_assembly.export_srdf()

    assert 'name="simple_robot"' in urdf_xml
    assert 'link name="alignment_pin"' in urdf_xml
    assert 'link name="adapter_flange"' in urdf_xml
    assert 'joint name="endeffector_attachment_link"' in urdf_xml

    assert 'name="simple_robot"' in srdf_xml
    assert 'passive_joint name="alignment_pin_joint"' in srdf_xml
    assert 'passive_joint name="adapter_body_joint"' in srdf_xml
    assert (
        'disable_collisions link1="adapter_base" link2="support_block" reason="Mounted"' in srdf_xml
    )
    assert 'disable_collisions link1="endeffector_base" link2="finger_link"' in srdf_xml
