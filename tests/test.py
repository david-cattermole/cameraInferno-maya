"""
Tests for Camera Inferno toolset.

Each on-screen value should have the following functionality::

- Should have an optional prefix value (blank by default)

- Should have an optional suffix value (blank by default)

- Main string is actually a Python formatter.

- Value(s) should connectable as any type (numeric or string)

- Each field has multiple dynamic value inputs (perhaps 3?) and can be
  formatted into the string with {0}, {1} or {3}.

- System environment variables can be expanded automatically by adding
  a '$' symbol prefix to a existing word.

- Each value be aligned to a position corner; top-left, top-right,
  top-center, etc.

- Each value can be positioned on the screen, with the screen
  coordinates 0.0(?), 0.0(?) in the center.

- Display;
  - Shot name
  - Scene file name
  - Artist Name (User Name)
  - Frame number; 4 padded.
  - Camera Height (with a level adjustment)
  - Camera Tilt
  - Camera Focal Length
  - Camera Angle Of View
  - Camera Film Back (Name)

"""

import maya.cmds
import dcCameraInferno.tool as tool


def test_create():
    maya.cmds.file(force=True, new=True)
    maya.cmds.unloadPlugin('dcCameraInferno', force=True)
    maya.cmds.loadPlugin("dcCameraInferno", quiet=False)
    tfm = maya.cmds.createNode("transform", parent='|persp')
    node = maya.cmds.createNode("dcCameraInferno", parent=tfm)
    mult_node = maya.cmds.createNode("multiplyDivide")
    anno_node = maya.cmds.createNode("annotationShape")

    maya.cmds.setAttr("persp.visibility", 1)  # vertical
    maya.cmds.setAttr("perspShape.filmFit", 1)  # vertical
    maya.cmds.setAttr("perspShape.displayFilmGate", 1)
    maya.cmds.setAttr("perspShape.displayGateMaskOpacity", 0)
    maya.cmds.setAttr("perspShape.overscan", 2.0)
    maya.cmds.setAttr(node + ".maskAspectRatio", 1.7777)
    # maya.cmds.setAttr("perspShape.panZoomEnabled", 1)
    # maya.cmds.setAttr("perspShape.lensSqueezeRatio", 1.5)
    # maya.cmds.setAttr("perspShape.horizontalPan", 0.709)
    # maya.cmds.setAttr("perspShape.verticalPan", 0.209)
    # maya.cmds.setAttr("perspShape.horizontalFilmOffset", -0.709)
    # maya.cmds.setAttr("perspShape.verticalFilmOffset", -0.709)
    # maya.cmds.setAttr("perspShape.horizontalFilmAperture", 2.0)
    # maya.cmds.setAttr("perspShape.verticalFilmAperture", 1.0)

    maya.cmds.setAttr(node + ".field[0].fieldType", 1)
    maya.cmds.setAttr(node + ".field[0].fieldTextValue", "Artist: {user_name} Value: {a:+.01f}  AOV:{lens_angle_of_view_x:.01f}", type='string')
    maya.cmds.setAttr(node + ".field[0].fieldTextAlign", 6)
    maya.cmds.setAttr(node + ".field[0].fieldTextColor", 1, 1, 1, type='double3')
    maya.cmds.setAttr(node + ".field[0].fieldPositionAX", -1.0)
    maya.cmds.setAttr(node + ".field[0].fieldPositionAY", 1.0)

    maya.cmds.setAttr(node + ".field[1].fieldTextAlign", 8)
    maya.cmds.setAttr(node + ".field[1].fieldPositionAX", 1.0)
    maya.cmds.setAttr(node + ".field[1].fieldPositionAY", 1.0)
    maya.cmds.setAttr(node + ".field[1].fieldTextColor", 1, 1, 1, type='double3')
    maya.cmds.setAttr(node + ".field[1].fieldTextValue", "Scene: {file_name} Value: {a} Lens: {lens_focal_length:.01f} mm", type='string')

    maya.cmds.setAttr(node + ".field[2].fieldTextAlign", 0)
    maya.cmds.setAttr(node + ".field[2].fieldPositionAX", -1.0)
    maya.cmds.setAttr(node + ".field[2].fieldPositionAY", -1.0)
    maya.cmds.setAttr(node + ".field[2].fieldTextColor", 1, 1, 1, type='double3')
    maya.cmds.setAttr(node + ".field[2].fieldTextValue", "File Path: {file_path} Value: {a} Shutter {camera_shutter_angle:.02f} deg", type='string')

    maya.cmds.setAttr(node + ".field[3].fieldTextAlign", 2)
    maya.cmds.setAttr(node + ".field[3].fieldPositionAX", 1.0)
    maya.cmds.setAttr(node + ".field[3].fieldPositionAY", -1.0)
    maya.cmds.setAttr(node + ".field[3].fieldTextColor", 1, 1, 1, type='double3')
    maya.cmds.setAttr(node + ".field[3].fieldTextValue", "Date/Time: {datetime}", type='string')

    maya.cmds.setAttr(node + ".field[4].fieldTextAlign", 2)
    maya.cmds.setAttr(node + ".field[4].fieldPositionAX", 1.0)
    maya.cmds.setAttr(node + ".field[4].fieldPositionAY", -0.5)
    maya.cmds.setAttr(node + ".field[4].fieldTextColor", 1, 1, 1, type='double3')
    maya.cmds.setAttr(node + ".field[4].fieldTextValue", "Pan: {camera_pan:+.01f} Tilt: {camera_tilt:+.01f} Roll: {camera_roll:+.01f}", type='string')

    maya.cmds.setAttr(node + ".field[5].fieldTextAlign", 3)
    maya.cmds.setAttr(node + ".field[5].fieldPositionAX", -1.0)
    maya.cmds.setAttr(node + ".field[5].fieldPositionAY", 0.0)
    maya.cmds.setAttr(node + ".field[5].fieldTextColor", 1, 1, 1, type='double3')
    maya.cmds.setAttr(node + ".field[5].fieldTextValue", "Camera: {camera_short_name}", type='string')

    maya.cmds.setAttr(node + ".field[6].fieldTextAlign", 3)
    maya.cmds.setAttr(node + ".field[6].fieldPositionAX", -1.0)
    maya.cmds.setAttr(node + ".field[6].fieldPositionAY", 0.1)
    maya.cmds.setAttr(node + ".field[6].fieldTextColor", 1, 1, 1, type='double3')
    maya.cmds.setAttr(node + ".field[6].fieldTextValue", "Frame: {frame_integer:04d} {frame_float:.1f}", type='string')

    maya.cmds.setAttr(node + ".field[7].fieldTextAlign", 3)
    maya.cmds.setAttr(node + ".field[7].fieldPositionAX", -1.0)
    maya.cmds.setAttr(node + ".field[7].fieldPositionAY", 0.2)
    maya.cmds.setAttr(node + ".field[7].fieldTextColor", 1, 1, 1, type='double3')
    maya.cmds.setAttr(node + ".field[7].fieldTextValue", "Film Back: {film_back_width_mm:.2f} mm X {film_back_height_mm:.2f} mm", type='string')

    maya.cmds.setAttr(mult_node + ".input1X", 2.0)
    maya.cmds.setAttr(mult_node + ".input2X", 2.0)
    src = mult_node + ".outputX"
    dst = node + ".field[0].fieldValueA"
    maya.cmds.connectAttr(src, dst)

    maya.cmds.setAttr(anno_node + ".text", "hello world", type='string')
    src = anno_node + ".text"
    dst = node + ".field[1].fieldValueA"
    maya.cmds.connectAttr(src, dst)

    src = anno_node + ".displayArrow"
    dst = node + ".field[2].fieldValueA"
    maya.cmds.connectAttr(src, dst)

    maya.cmds.select("perspShape", replace=True)
    maya.cmds.select(node, replace=True)


def test_use_tool():
    cam_tfm = maya.cmds.createNode('transform')
    cam_shp = maya.cmds.createNode('camera')
    maya.cmds.select(cam_tfm, replace=True)
    tool.main()
    return


def test_velocity():
    maya.cmds.file(new=True, force=True)

    # Load and create velocity node.
    maya.cmds.unloadPlugin('dcVelocity')
    maya.cmds.loadPlugin('matrixNodes', quiet=True)
    maya.cmds.loadPlugin('dcVelocity', quiet=True)
    node = maya.cmds.createNode('dcVelocity')

    # transform node
    tfm = maya.cmds.createNode('transform')
    decompose = maya.cmds.createNode('decomposeMatrix')

    maya.cmds.connectAttr('%s.worldMatrix[0]' % tfm, '%s.inputMatrix' % decompose)
    maya.cmds.connectAttr('%s.outputTranslate' % decompose, '%s.inputPoint' % node)

    # Annotation
    annot = maya.cmds.createNode('annotationShape', parent=tfm)
    maya.cmds.setAttr('%s.displayArrow' % annot, False)

    # create 'speed' attribute
    maya.cmds.addAttr(tfm, ln='speed', at='double' )
    maya.cmds.setAttr('%s.speed' % tfm, edit=True, keyable=True)
    maya.cmds.connectAttr('%s.outSpeed' % node, '%s.speed' % tfm)
    maya.cmds.connectAttr('%s.outSpeedText' % node, '%s.text' % annot)

    # Add example animation
    infinity = 'linear'
    tangent = 'spline'
    maya.cmds.setKeyframe(tfm, attribute='translateX',
                          time=0, value=0,
                          inTangentType=tangent,
                          outTangentType=tangent)
    maya.cmds.setKeyframe(tfm, attribute='translateX',
                          time=24, value=100,
                          inTangentType=tangent,
                          outTangentType=tangent)
    maya.cmds.setInfinity(tfm,
                          attribute=['translateX'],
                          preInfinite=infinity,
                          postInfinite=infinity)
    return
