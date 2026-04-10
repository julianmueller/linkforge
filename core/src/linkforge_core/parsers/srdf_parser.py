"""SRDF XML parser for LinkForge.

This module implements a robust SRDF (Semantic Robot Description Format) parser
that supports MoveIt-style tags with optional XACRO preprocessing helpers.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Protocol, overload, runtime_checkable

from ..base import IResourceResolver
from ..exceptions import (
    RobotParserError,
    RobotParserIOError,
    RobotParserUnexpectedError,
    RobotParserXMLRootError,
    XacroDetectedError,
)
from ..logging_config import get_logger
from ..models import Robot
from ..models.srdf import (
    DisabledCollision,
    EndEffector,
    GroupState,
    PassiveJoint,
    PlanningGroup,
    SemanticRobotDescription,
    VirtualJoint,
)
from ..utils.xml_utils import parse_float
from .xacro_parser import ResolvedXacro, XACROParser
from .xml_base import MAX_FILE_SIZE, RobotXMLParser

logger = get_logger(__name__)
_SRDF_XACRO_DETECTED = "SRDF String contains XACRO"


@runtime_checkable
class ITemplateResolver(Protocol):
    """Protocol for resolving templated XML strings (e.g., XACRO, Jinja)."""

    def resolve_string(self, xml_string: str) -> str:
        """Resolve a templated string into plain XML."""
        ...


class SRDFParser(RobotXMLParser):
    """Refined SRDF parser with MoveIt support and explicit XACRO helpers."""

    def __init__(
        self,
        max_file_size: int = MAX_FILE_SIZE,
        sandbox_root: Path | None = None,
        resource_resolver: IResourceResolver | None = None,
        search_paths: list[Path] | None = None,
        template_resolver: ITemplateResolver | None = None,
    ) -> None:
        """Initialize SRDF parser.

        Args:
            max_file_size: Maximum allowed file size in bytes.
            sandbox_root: Optional root directory for security sandbox.
            resource_resolver: Optional resolver for URIs.
            search_paths: Optional search paths for XACRO includes.
            template_resolver: Optional template resolver for preprocessing the SRDF content.
        """
        super().__init__(
            max_file_size=max_file_size,
            sandbox_root=sandbox_root,
            resource_resolver=resource_resolver,
        )
        self.search_paths = search_paths or []
        self.template_resolver = template_resolver

    def _detect_xacro(self, xml_string: str) -> bool:
        """Detect if the string contains XACRO tags."""
        return "xmlns:xacro" in xml_string or "<xacro:" in xml_string

    def _parse_planning_group(self, group_elem: ET.Element) -> PlanningGroup:
        """Parse a planning group including its nested components."""
        name = group_elem.get("name", "unnamed_group")
        links: list[str] = []
        joints: list[str] = []
        chains: list[tuple[str, str]] = []
        subgroups: list[str] = []

        for child in group_elem:
            if child.tag == "link":
                link_name = child.get("name")
                if link_name:
                    links.append(link_name)
            elif child.tag == "joint":
                joint_name = child.get("name")
                if joint_name:
                    joints.append(joint_name)
            elif child.tag == "chain":
                base = child.get("base_link")
                tip = child.get("tip_link")
                if base and tip:
                    chains.append((base, tip))
            elif child.tag == "group":
                subgroup_name = child.get("name")
                if subgroup_name:
                    subgroups.append(subgroup_name)

        return PlanningGroup(
            name=name, links=links, joints=joints, chains=chains, subgroups=subgroups
        )

    def _parse_group_state(self, state_elem: ET.Element) -> GroupState:
        """Parse a named group state."""
        name = state_elem.get("name", "unnamed_state")
        group = state_elem.get("group", "")
        joint_values: dict[str, float] = {}

        for joint_elem in state_elem.findall("joint"):
            j_name = joint_elem.get("name")
            j_val = parse_float(joint_elem.get("value"), f"joint {j_name} value", default=0.0)
            if j_name:
                joint_values[j_name] = j_val

        return GroupState(name=name, group=group, joint_values=joint_values)

    @overload
    def parse_string(
        self,
        xml_string: str,
        robot: None = None,
        base_directory: Path | None = None,
        **kwargs: Any,
    ) -> SemanticRobotDescription: ...

    @overload
    def parse_string(
        self,
        xml_string: str,
        robot: Robot,
        base_directory: Path | None = None,
        **kwargs: Any,
    ) -> Robot: ...

    def parse_string(
        self,
        xml_string: str,
        robot: Robot | None = None,
        base_directory: Path | None = None,
        **kwargs: Any,
    ) -> SemanticRobotDescription | Robot:
        """Parse SRDF from string.

        When `robot` is provided, the parsed semantic description is attached
        to that robot and the robot is returned. Otherwise the standalone
        `SemanticRobotDescription` is returned.
        """
        if self.template_resolver is not None:
            xml_string = self.template_resolver.resolve_string(xml_string)
        elif self._detect_xacro(xml_string):
            raise XacroDetectedError(_SRDF_XACRO_DETECTED)

        try:
            root = ET.fromstring(xml_string)
        except ET.ParseError as e:
            raise RobotParserUnexpectedError(source_area="SRDF parse", original_error=e) from e
        except Exception as e:
            raise RobotParserUnexpectedError(
                source_area="Unexpected SRDF parse", original_error=e
            ) from e

        if root.tag != "robot":
            raise RobotParserXMLRootError(root.tag)

        semantic = self._parse_elements(root)

        if robot is None:
            return semantic

        robot.semantic = semantic

        unused_options = list(kwargs.keys())
        if base_directory is not None:
            unused_options.append("base_directory")
        if unused_options:
            logger.debug(f"SRDFParser received unused options: {unused_options}")

        return robot

    def _parse_elements(self, root: ET.Element) -> SemanticRobotDescription:
        """Internal helper to parse all SRDF elements from root."""
        virtual_joints: list[VirtualJoint] = []
        groups: list[PlanningGroup] = []
        group_states: list[GroupState] = []
        end_effectors: list[EndEffector] = []
        passive_joints: list[PassiveJoint] = []
        disabled_collisions: list[DisabledCollision] = []

        for child in root:
            if child.tag == "virtual_joint":
                virtual_joints.append(self._parse_virtual_joint_elem(child))
            elif child.tag == "group":
                groups.append(self._parse_planning_group(child))
            elif child.tag == "group_state":
                group_states.append(self._parse_group_state(child))
            elif child.tag == "end_effector":
                end_effectors.append(self._parse_end_effector_elem(child))
            elif child.tag == "passive_joint":
                passive_joints.append(PassiveJoint(name=child.get("name", "unnamed_pj")))
            elif child.tag == "disable_collisions":
                disabled_collisions.append(self._parse_disable_collisions_elem(child))

        return SemanticRobotDescription(
            virtual_joints=virtual_joints,
            groups=groups,
            group_states=group_states,
            end_effectors=end_effectors,
            passive_joints=passive_joints,
            disabled_collisions=disabled_collisions,
        )

    def _parse_virtual_joint_elem(self, elem: ET.Element) -> VirtualJoint:
        """Parse virtual_joint element."""
        return VirtualJoint(
            name=elem.get("name", "unnamed_vj"),
            type=elem.get("type", "fixed"),
            parent_frame=elem.get("parent_frame", "world"),
            child_link=elem.get("child_link", "base_link"),
        )

    def _parse_end_effector_elem(self, elem: ET.Element) -> EndEffector:
        """Parse end_effector element."""
        return EndEffector(
            name=elem.get("name", "unnamed_ee"),
            group=elem.get("group", ""),
            parent_link=elem.get("parent_link", ""),
            parent_group=elem.get("parent_group"),
        )

    def _parse_disable_collisions_elem(self, elem: ET.Element) -> DisabledCollision:
        """Parse disable_collisions element."""
        return DisabledCollision(
            link1=elem.get("link1", ""),
            link2=elem.get("link2", ""),
            reason=elem.get("reason"),
        )

    @overload
    def parse(
        self,
        source: Path | str | ResolvedXacro,
        robot: None = None,
        **kwargs: Any,
    ) -> SemanticRobotDescription: ...

    @overload
    def parse(
        self,
        source: Path | str | ResolvedXacro,
        robot: Robot,
        **kwargs: Any,
    ) -> Robot: ...

    def parse(
        self,
        source: Path | str | ResolvedXacro,
        robot: Robot | None = None,
        **kwargs: Any,
    ) -> SemanticRobotDescription | Robot:
        """Parse SRDF content from a file path, string, or resolved XACRO payload."""
        if isinstance(source, ResolvedXacro):
            return self.parse_string(source.xml, robot=robot, base_directory=source.base_directory)

        if isinstance(source, str):
            return self.parse_string(source, robot=robot)

        filepath = source
        if not filepath.exists():
            raise RobotParserIOError(filepath=filepath, reason="Missing file")

        # Security check: File size
        file_size = filepath.stat().st_size
        if file_size > self.max_file_size:
            raise RobotParserIOError(filepath=filepath, reason="File too large")

        try:
            if filepath.suffix == ".xacro" or filepath.name.endswith(".srdf.xacro"):
                raise XacroDetectedError(filepath.name)

            content = filepath.read_text(encoding="utf-8")
            return self.parse_string(content, robot=robot, base_directory=filepath.parent, **kwargs)

        except Exception as e:
            if isinstance(e, RobotParserError):
                raise
            raise RobotParserIOError(filepath=filepath, reason=str(e)) from e

    @overload
    def parse_xacro(
        self, filepath: Path, robot: None = None, **kwargs: Any
    ) -> SemanticRobotDescription: ...

    @overload
    def parse_xacro(self, filepath: Path, robot: Robot, **kwargs: Any) -> Robot: ...

    def parse_xacro(
        self,
        filepath: Path,
        robot: Robot | None = None,
        **kwargs: Any,
    ) -> SemanticRobotDescription | Robot:
        """Resolve a XACRO file and parse the resulting SRDF."""
        xacro_kwargs = {"search_paths": self.search_paths, **kwargs}
        resolved = XACROParser().parse(filepath, **xacro_kwargs)
        return self.parse(resolved, robot=robot)
