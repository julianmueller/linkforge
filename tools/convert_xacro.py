#!/usr/bin/env python3
"""
Standalone utility to convert XACRO files to URDF.
Uses xacrodoc for robust conversion.
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from xacrodoc import XacroDoc
except ImportError:
    print("Error: 'xacrodoc' is not installed.")
    print("Please install it using: pip install xacrodoc")
    sys.exit(1)


def convert_xacro(
    input_path: Path, output_path: Path = None, package_paths: list[str] = None
) -> None:
    """
    Convert a XACRO file to URDF.

    Args:
        input_path: Path to the source .xacro file.
        output_path: Optional path to saving the .urdf file.
                    If None, uses same name as input with .urdf extension.
        package_paths: Optional list of paths to search for ROS packages.
    """
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' does not exist.")
        sys.exit(1)

    # Set up ROS_PACKAGE_PATH if extra search paths are provided
    if package_paths:
        current_path = os.environ.get("ROS_PACKAGE_PATH", "")
        # Filter out empty paths and join using OS-specific separator
        new_paths = os.pathsep.join(p for p in package_paths if p)
        if current_path:
            os.environ["ROS_PACKAGE_PATH"] = f"{new_paths}{os.pathsep}{current_path}"
        else:
            os.environ["ROS_PACKAGE_PATH"] = new_paths
        print(f"Search paths: {os.environ['ROS_PACKAGE_PATH']}")

    try:
        print(f"Processing '{input_path.name}'...")

        # xacrodoc handles property extraction and macro expansion
        # It internally uses rospkg which respects ROS_PACKAGE_PATH
        doc = XacroDoc.from_file(str(input_path))
        urdf_string = doc.to_urdf_string()

        if not output_path:
            output_path = input_path.with_suffix(".urdf")

        # Write converted URDF
        output_path.write_text(urdf_string)
        print(f"Successfully converted to '{output_path.name}'")

    except Exception as e:
        print(f"Error during conversion: {e}")
        if "PackageNotFoundError" in str(e) and not package_paths:
            print(
                "\nTip: If your XACRO file uses $(find package_name), use --package-path to specify where to find it."
            )
            print(
                "Example: python tools/convert_xacro.py robot.xacro --package-path /path/to/my_packages"
            )
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="LinkForge XACRO to URDF Converter Utility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example Usage:
  python tools/convert_xacro.py robot.xacro
  python tools/convert_xacro.py robot.xacro -o my_robot.urdf
  python tools/convert_xacro.py robot.xacro --package-path /path/to/ros_ws/src
        """,
    )
    parser.add_argument("input", help="Path to the input XACRO file")
    parser.add_argument("-o", "--output", help="Path to the output URDF file (optional)")
    parser.add_argument(
        "-p",
        "--package-path",
        action="append",
        help="Additional search path(s) for ROS packages (can be used multiple times)",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else None

    convert_xacro(input_path, output_path, args.package_path)


if __name__ == "__main__":
    main()
