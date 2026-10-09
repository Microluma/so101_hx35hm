# Third-Party Components and Attribution

This repository is a ROS 2 workspace that combines project-specific integration code with upstream and vendor-derived components. The repository does not currently apply one blanket license to every file.

## `src/so101-ros-physical-ai/`

- Upstream project: [legalaspro/so101-ros-physical-ai](https://github.com/legalaspro/so101-ros-physical-ai)
- Upstream author identified by the included README: Dmitri Manajev
- Declared license: Apache License 2.0
- Included license text: [`src/so101-ros-physical-ai/LICENSE`](src/so101-ros-physical-ai/LICENSE)
- Role in this workspace: SO101 ROS 2 descriptions, bringup, MoveIt, teleoperation, recording, dataset conversion, inference, and related tooling. This workspace integrates and adapts these components for the HX-35HM hardware and the project-specific vision/grasping workflow.

## `src/ros_robot_controller-ros2/`

- Role: STM32 and bus-servo communication dependency used by the HX-35HM bridge.
- Current metadata: the included packages retain their original maintainer information, but their `package.xml` and `setup.py` files still contain `TODO: License declaration`.
- Status: the original source and redistribution terms must be verified before the complete workspace can be assigned a single license or redistributed as a fully licensed release.

## `src/so101_hx35hm_bridge/`

- Role: project-specific HX-35HM integration, hardware utilities, camera compatibility, target detection, and table estimation.
- Package metadata currently declares MIT. A root-level license decision and copyright holder information still need to be added by the repository owner.

## Other package licenses

Individual ROS packages declare Apache-2.0, MIT, or BSD-3-Clause in their own `package.xml` files. Those declarations continue to apply to their respective components. The root workspace should not be described as using one uniform license until the repository owner completes a component-by-component review.

## Vendor documents and mechanical assets

The workspace contains hardware manuals, CAD meshes, and other assets derived from hardware or upstream projects. Their copyright and redistribution status may be separate from the source-code licenses. Before publishing a formal release, verify the redistribution rights for:

- `src/00 舵机二次开发之驱动电路说明.pdf`
- `src/1.HX-35HM总线舵机使用说明.pdf`
- duplicated mesh and Onshape-derived assets under `so101_description/`

## Before a formal release

1. Identify the original repository and license for `ros_robot_controller-ros2`.
2. Select a license for the repository owner's original top-level contributions.
3. Resolve remaining placeholder maintainer names only where the package's authorship can be verified; do not relabel upstream work as project-original code.
4. Retain all upstream license texts and required notices.
5. Review vendor PDFs and mechanical assets for redistribution permission.
