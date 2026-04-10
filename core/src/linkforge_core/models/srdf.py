"""Semantic robot description models (SRDF).

This module provides data structures to represent MoveIt-style semantic information,
such as planning groups, poses, and collision filters.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from ..exceptions import RobotModelError

_VIRTUAL_JOINT = "SRDF virtual_joint"
_VIRTUAL_JOINT_NAME = f"{_VIRTUAL_JOINT} name"
_VIRTUAL_JOINT_PARENT_FRAME = f"{_VIRTUAL_JOINT} parent_frame"
_VIRTUAL_JOINT_CHILD_LINK = f"{_VIRTUAL_JOINT} child_link"
_VIRTUAL_JOINT_DIFFERENT_ENTITIES = "parent_frame and child_link must refer to different entities"

_GROUP_STATE = "SRDF group_state"
_GROUP_STATE_NAME = f"{_GROUP_STATE} name"
_GROUP_STATE_GROUP = f"{_GROUP_STATE} group"
_GROUP_STATE_EMPTY_JOINT = "contains an empty joint name"

_END_EFFECTOR = "SRDF end_effector"
_END_EFFECTOR_NAME = f"{_END_EFFECTOR} name"
_END_EFFECTOR_PARENT_LINK = f"{_END_EFFECTOR} parent_link"
_END_EFFECTOR_GROUP = f"{_END_EFFECTOR} group"
_END_EFFECTOR_PARENT_GROUP = f"{_END_EFFECTOR} parent_group"
_END_EFFECTOR_SAME_GROUP = "cannot use same group and parent_group"

_DISABLED_COLLISION = "SRDF disable_collisions"
_DISABLED_COLLISION_LINK1 = f"{_DISABLED_COLLISION} link1"
_DISABLED_COLLISION_LINK2 = f"{_DISABLED_COLLISION} link2"
_DISABLED_COLLISION_DIFFERENT_LINKS = "link1 and link2 must refer to different links"

_CHAIN = "SRDF chain"
_CHAIN_BASE_LINK = f"{_CHAIN} base_link"
_CHAIN_TIP_LINK = f"{_CHAIN} tip_link"
_CHAIN_DIFFERENT_LINKS = "base_link and tip_link must be different"

_GROUP = "SRDF group"
_GROUP_NAME = f"{_GROUP} name"
_GROUP_EMPTY_LINK = "contains empty link name"
_GROUP_EMPTY_JOINT = "contains empty joint name"
_GROUP_INCOMPLETE_CHAIN = "contains incomplete chain"
_GROUP_EMPTY_SUBGROUP = "contains empty subgroup name"
_GROUP_SELF_SUBGROUP = "cannot reference itself as subgroup"
_GROUP_DUPLICATE_LINKS = "contains duplicate link names"
_GROUP_DUPLICATE_JOINTS = "contains duplicate joint names"
_GROUP_DUPLICATE_SUBGROUPS = "contains duplicate subgroup names"
_GROUP_DUPLICATE_CHAINS = "contains duplicate chains"


def _srdf_model_error(message: str) -> RobotModelError:
    """Create a model error for SRDF validation failures."""
    return RobotModelError(message)


def _field_empty_error(field: str) -> RobotModelError:
    """Create a validation error for empty required SRDF fields."""
    return _srdf_model_error(f"{field} cannot be empty")


def _entity_error(entity: str, message: str) -> RobotModelError:
    """Create a validation error for a generic SRDF entity."""
    return _srdf_model_error(f"{entity} {message}")


def _named_entity_error(entity: str, name: str, message: str) -> RobotModelError:
    """Create a validation error for a named SRDF entity."""
    return _srdf_model_error(f"{entity} '{name}' {message}")


class VirtualJointType(str, Enum):
    """Supported SRDF virtual joint types."""

    PLANAR = "planar"
    FLOATING = "floating"
    FIXED = "fixed"


@dataclass(frozen=True)
class VirtualJoint:
    """Connects the robot to a fixed frame in the world.

    Attributes:
        name: Unique name for the virtual joint.
        type: Type of joint (e.g., 'fixed', 'planar', 'floating').
        parent_frame: Name of the parent coordinate frame (e.g., 'world').
        child_link: Name of the robot link attached to this joint.
    """

    name: str
    type: VirtualJointType
    parent_frame: str
    child_link: str

    def __post_init__(self) -> None:
        if not self.name:
            raise _field_empty_error(_VIRTUAL_JOINT_NAME)
        if not self.parent_frame:
            raise _field_empty_error(_VIRTUAL_JOINT_PARENT_FRAME)
        if not self.child_link:
            raise _field_empty_error(_VIRTUAL_JOINT_CHILD_LINK)

        if self.parent_frame == self.child_link:
            raise _entity_error(_VIRTUAL_JOINT, _VIRTUAL_JOINT_DIFFERENT_ENTITIES)


@dataclass(frozen=True)
class GroupState:
    """A named set of joint values for a planning group (a pose).

    Attributes:
        name: Unique name for this pose (e.g., 'home', 'folded').
        group: Name of the planning group this state applies to.
        joint_values: Dictionary mapping joint names to their target values.
    """

    name: str
    group: str
    joint_values: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name:
            raise _field_empty_error(_GROUP_STATE_NAME)
        if not self.group:
            raise _field_empty_error(_GROUP_STATE_GROUP)

        for joint_name in self.joint_values:
            if not joint_name:
                raise _named_entity_error(_GROUP_STATE, self.name, _GROUP_STATE_EMPTY_JOINT)


@dataclass(frozen=True)
class EndEffector:
    """Defines a planning group as an end effector.

    Attributes:
        name: Unique name for the end effector.
        group: The planning group that forms the end effector (e.g., 'hand').
        parent_link: The robot link the end effector is attached to.
        parent_group: Optional name of the group this end-effector belongs to.
    """

    name: str
    group: str
    parent_link: str
    parent_group: str | None = None

    def __post_init__(self) -> None:
        if not self.name:
            raise _field_empty_error(_END_EFFECTOR_NAME)
        if not self.parent_link:
            raise _field_empty_error(_END_EFFECTOR_PARENT_LINK)
        if not self.group:
            raise _field_empty_error(_END_EFFECTOR_GROUP)

        if self.parent_group is not None:
            if not self.parent_group:
                raise _field_empty_error(_END_EFFECTOR_PARENT_GROUP)
            if self.parent_group == self.group:
                raise _named_entity_error(_END_EFFECTOR, self.name, _END_EFFECTOR_SAME_GROUP)


@dataclass(frozen=True)
class PassiveJoint:
    """A joint that is not actuated but exists in the kinematic chain.

    Attributes:
        name: Name of the passive joint.
    """

    name: str


@dataclass(frozen=True)
class DisabledCollision:
    """Disables collision checking between two specific links.

    Attributes:
        link1: Name of the first link.
        link2: Name of the second link.
        reason: Optional human-readable reason (e.g., 'Adjacent', 'Never').
    """

    link1: str
    link2: str
    reason: str | None = None

    def __post_init__(self) -> None:
        if not self.link1:
            raise _field_empty_error(_DISABLED_COLLISION_LINK1)
        if not self.link2:
            raise _field_empty_error(_DISABLED_COLLISION_LINK2)

        if self.link1 == self.link2:
            raise _entity_error(_DISABLED_COLLISION, _DISABLED_COLLISION_DIFFERENT_LINKS)


@dataclass(frozen=True)
class Chain:
    """A group chain segment from base link to tip link."""

    base_link: str
    tip_link: str

    def __post_init__(self) -> None:
        if not self.base_link:
            raise _field_empty_error(_CHAIN_BASE_LINK)
        if not self.tip_link:
            raise _field_empty_error(_CHAIN_TIP_LINK)
        if self.base_link == self.tip_link:
            raise _entity_error(_CHAIN, _CHAIN_DIFFERENT_LINKS)


@dataclass(frozen=True)
class PlanningGroup:
    """A named collection of links, joints, or chains used for motion planning.

    Attributes:
        name: Unique name for the planning group (e.g., 'arm', 'gripper').
        links: List of link names included in the group.
        joints: List of joint names included in the group.
        chains: List of (base_link, tip_link) tuples defining kinematic chains.
        subgroups: List of other planning group names to include.
    """

    name: str
    links: list[str] = field(default_factory=list)
    joints: list[str] = field(default_factory=list)
    chains: list[tuple[str, str]] = field(default_factory=list)
    subgroups: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name:
            raise _field_empty_error(_GROUP_NAME)

        for link_name in self.links:
            if not link_name:
                raise _named_entity_error(_GROUP, self.name, _GROUP_EMPTY_LINK)

        for joint_name in self.joints:
            if not joint_name:
                raise _named_entity_error(_GROUP, self.name, _GROUP_EMPTY_JOINT)

        for base_link, tip_link in self.chains:
            if not base_link or not tip_link:
                raise _named_entity_error(_GROUP, self.name, _GROUP_INCOMPLETE_CHAIN)

        for subgroup in self.subgroups:
            if not subgroup:
                raise _named_entity_error(_GROUP, self.name, _GROUP_EMPTY_SUBGROUP)
            if subgroup == self.name:
                raise _named_entity_error(_GROUP, self.name, _GROUP_SELF_SUBGROUP)

        if len(set(self.links)) != len(self.links):
            raise _named_entity_error(_GROUP, self.name, _GROUP_DUPLICATE_LINKS)
        if len(set(self.joints)) != len(self.joints):
            raise _named_entity_error(_GROUP, self.name, _GROUP_DUPLICATE_JOINTS)
        if len(set(self.subgroups)) != len(self.subgroups):
            raise _named_entity_error(_GROUP, self.name, _GROUP_DUPLICATE_SUBGROUPS)
        if len(set(self.chains)) != len(self.chains):
            raise _named_entity_error(_GROUP, self.name, _GROUP_DUPLICATE_CHAINS)


@dataclass(frozen=True)
class SemanticRobotDescription:
    """Container for all semantic information (SRDF).

    This class serves as the central point for MoveIt-compatible metadata
    that exists alongside the kinematic URDF description.
    """

    virtual_joints: list[VirtualJoint] = field(default_factory=list)
    groups: list[PlanningGroup] = field(default_factory=list)
    group_states: list[GroupState] = field(default_factory=list)
    end_effectors: list[EndEffector] = field(default_factory=list)
    passive_joints: list[PassiveJoint] = field(default_factory=list)
    disabled_collisions: list[DisabledCollision] = field(default_factory=list)
