# Copyright (C) 2019, 2020 David Cattermole.
#
# This file is part of dcCameraInferno.
#
# dcCameraInferno is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# dcCameraInferno is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with dcCameraInferno.  If not, see <https://www.gnu.org/licenses/>.
#
"""
Tools to use Camera Inferno.
"""

from __future__ import absolute_import
import maya.cmds


def load_plugins():
    maya.cmds.loadPlugin("dcCameraInferno", quiet=True)
    maya.cmds.loadPlugin('matrixNodes', quiet=True)
    maya.cmds.loadPlugin('dcVelocity', quiet=True)


def add_speed_attributes_to_transform(tfm_node):
    velocity_node = maya.cmds.createNode('dcVelocity')
    decompose = maya.cmds.createNode('decomposeMatrix')

    src = '%s.worldMatrix[0]' % tfm_node
    dst = '%s.inputMatrix' % decompose
    maya.cmds.connectAttr(src, dst)

    src = '%s.outputTranslate' % decompose
    dst = '%s.inputPoint' % velocity_node
    maya.cmds.connectAttr(src, dst)

    annot_tfm = maya.cmds.createNode('transform', parent=tfm_node, name='dummy')
    annot_shp = maya.cmds.createNode('annotationShape', parent=annot_tfm, name='dummyShape')
    maya.cmds.setAttr('%s.displayArrow' % annot_shp, 0)
    src = '%s.outDummyString' % velocity_node
    dst = '%s.text' % annot_shp
    maya.cmds.connectAttr(src, dst)

    # create 'speedRaw' attribute
    maya.cmds.addAttr(
        tfm_node, longName='speedRaw', attributeType='double', hidden=True)
    src = '%s.outSpeedRaw' % velocity_node
    dst = '%s.speedRaw' % tfm_node
    maya.cmds.setAttr(dst, edit=True, keyable=True)
    maya.cmds.connectAttr(src, dst)

    # create 'speed' attribute
    maya.cmds.addAttr(
        tfm_node, longName='speed', attributeType='double', hidden=False)
    src = '%s.outSpeed' % velocity_node
    dst = '%s.speed' % tfm_node
    maya.cmds.setAttr(dst, edit=True, keyable=True)
    maya.cmds.connectAttr(src, dst)
    return velocity_node


def create_node(cam_tfm):
    # Create Node
    tfm = maya.cmds.createNode("transform", name="cameraInferno1", parent=cam_tfm)
    node = maya.cmds.createNode("dcCameraInferno", parent=tfm)

    # Make non-selectable.
    maya.cmds.setAttr(tfm + ".template", 1)

    # Create a default mask aspect ratio.
    maya.cmds.setAttr(node + ".maskAspectRatio", 1.7777)
    return tfm, node


def connect_camera_to_hud(velocity_node, hud_node):
    assert maya.cmds.nodeType(velocity_node) == 'dcVelocity'
    assert maya.cmds.nodeType(hud_node) == 'dcCameraInferno'
    src = velocity_node + '.outSpeedRaw'
    dst = hud_node + '.cameraSpeedRaw'
    maya.cmds.connectAttr(src, dst)
    return


def main():
    load_plugins()

    # Create node from selection.
    sel = maya.cmds.ls(selection=True, long=True, type="transform") or []
    cam_tfm = None
    if len(sel) == 0:
        cam_tfm = maya.cmds.createNode(
            "transform", name="camera1")
        cam_shp = maya.cmds.createNode(
            "camera", name="cameraShape1", parent=cam_tfm)
    else:
        cam_tfm = sel[0]

    # Create the node.
    velocity_node = add_speed_attributes_to_transform(cam_tfm)
    hud_tfm, hud_node = create_node(cam_tfm)
    connect_camera_to_hud(velocity_node, hud_node)

    # Select the newly created node.
    maya.cmds.select(hud_node, replace=True)
    return


# def open_window():
#     import dcCameraInferno.ui.main
#     ui = dcCameraInferno.ui.main.open_window()
