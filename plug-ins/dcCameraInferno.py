# Copyright (C) 2020, David Cattermole.
#
# This file is part of dcCameraInferno.
#
# mmSolver is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# mmSolver is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with mmSolver.  If not, see <https://www.gnu.org/licenses/>.
#
"""Camera Inferno is a plug-in used to display dynamic information in
a Maya Playblast.


Usage::
1) Create 'dcCameraInferno' node type, under a transform.

2) Parent transform under camera transform node.

Note: you may get a list of font names for your computer with this Python command:

   import maya.api.OpenMayaRender
   print maya.api.OpenMayaRender.MUIDrawManager.getFontList()

And here you can get a list of icon names.

   import maya.api.OpenMayaRender
   print maya.api.OpenMayaRender.MUIDrawManager.getIconNames()

"""

import datetime
import math
import collections
import getpass
import maya.cmds
import os
import string

import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.api.OpenMayaRender as OpenMayaRender

# Registered Node Id.
PLUGIN_NODE_ID = 0x0012F183

# Types of field indices.
FIELD_TYPE_NONE_INDEX = 0
FIELD_TYPE_TEXT_2D_INDEX = 1
FIELD_TYPE_TEXT_3D_INDEX = 2
FIELD_TYPE_POINT_2D_INDEX = 3
FIELD_TYPE_POINT_3D_INDEX = 4
FIELD_TYPE_LINE_2D_INDEX = 5
FIELD_TYPE_LINE_3D_INDEX = 6

# Types of field names.
FIELD_TYPE_NONE_NAME = 'None'
FIELD_TYPE_TEXT_2D_NAME = 'Text 2D'
FIELD_TYPE_TEXT_3D_NAME = 'Text 3D'
FIELD_TYPE_POINT_2D_NAME = 'Point 2D'
FIELD_TYPE_POINT_3D_NAME = 'Point 3D'
FIELD_TYPE_LINE_2D_NAME = 'Line 2D'
FIELD_TYPE_LINE_3D_NAME = 'Line 3D'

# Links both name and indices together.
FIELD_TYPES = [
    (FIELD_TYPE_NONE_INDEX, FIELD_TYPE_NONE_NAME),
    (FIELD_TYPE_TEXT_2D_INDEX, FIELD_TYPE_TEXT_2D_NAME),
    (FIELD_TYPE_TEXT_3D_INDEX, FIELD_TYPE_TEXT_3D_NAME),
    (FIELD_TYPE_POINT_2D_INDEX, FIELD_TYPE_POINT_2D_NAME),
    (FIELD_TYPE_POINT_3D_INDEX, FIELD_TYPE_POINT_3D_NAME),
    (FIELD_TYPE_LINE_2D_INDEX, FIELD_TYPE_LINE_2D_NAME),
    (FIELD_TYPE_LINE_3D_INDEX, FIELD_TYPE_LINE_3D_NAME),
]

# Alignment values.
ALIGN_BOTTOM_LEFT_VALUE = 0
ALIGN_BOTTOM_CENTER_VALUE = 1
ALIGN_BOTTOM_RIGHT_VALUE = 2
ALIGN_MIDDLE_LEFT_VALUE = 3
ALIGN_MIDDLE_CENTER_VALUE = 4
ALIGN_MIDDLE_RIGHT_VALUE = 5
ALIGN_TOP_LEFT_VALUE = 6
ALIGN_TOP_CENTER_VALUE = 7
ALIGN_TOP_RIGHT_VALUE = 8

# Text alignment values and names.
TEXT_ALIGN_TYPES = [
    (ALIGN_BOTTOM_LEFT_VALUE, "Bottom-Left"),
    (ALIGN_BOTTOM_CENTER_VALUE, "Bottom-Center"),
    (ALIGN_BOTTOM_RIGHT_VALUE, "Bottom-Right"),
    (ALIGN_MIDDLE_LEFT_VALUE, "Middle-Left"),
    (ALIGN_MIDDLE_CENTER_VALUE, "Middle-Center"),
    (ALIGN_MIDDLE_RIGHT_VALUE, "Middle-Right"),
    (ALIGN_TOP_LEFT_VALUE, "Top-Left"),
    (ALIGN_TOP_CENTER_VALUE, "Top-Center"),
    (ALIGN_TOP_RIGHT_VALUE, "Top-Right"),
]

# Alignment mapping node values to VP2 values.
MAP_TEXT_ALIGN_TO_ALIGN_HORIZONTAL = {
    ALIGN_BOTTOM_LEFT_VALUE: OpenMayaRender.MUIDrawManager.kLeft,
    ALIGN_BOTTOM_CENTER_VALUE: OpenMayaRender.MUIDrawManager.kCenter,
    ALIGN_BOTTOM_RIGHT_VALUE: OpenMayaRender.MUIDrawManager.kRight,
    ALIGN_MIDDLE_LEFT_VALUE: OpenMayaRender.MUIDrawManager.kLeft,
    ALIGN_MIDDLE_CENTER_VALUE: OpenMayaRender.MUIDrawManager.kCenter,
    ALIGN_MIDDLE_RIGHT_VALUE: OpenMayaRender.MUIDrawManager.kRight,
    ALIGN_TOP_LEFT_VALUE: OpenMayaRender.MUIDrawManager.kLeft,
    ALIGN_TOP_CENTER_VALUE: OpenMayaRender.MUIDrawManager.kCenter,
    ALIGN_TOP_RIGHT_VALUE: OpenMayaRender.MUIDrawManager.kRight,
}

# Vertical alignment values
ALIGN_BOTTOM_VALUE = 0
ALIGN_MIDDLE_VALUE = 1
ALIGN_TOP_VALUE = 2

# Alignment mapping VP2 values to node values.
MAP_TEXT_ALIGN_TO_ALIGN_VERTICAL = {
    0: ALIGN_BOTTOM_VALUE,
    1: ALIGN_BOTTOM_VALUE,
    2: ALIGN_BOTTOM_VALUE,
    3: ALIGN_MIDDLE_VALUE,
    4: ALIGN_MIDDLE_VALUE,
    5: ALIGN_MIDDLE_VALUE,
    6: ALIGN_TOP_VALUE,
    7: ALIGN_TOP_VALUE,
    8: ALIGN_TOP_VALUE,
}

# Line styles names and values.
LINE_STYLE_TYPES = [
    (OpenMayaRender.MUIDrawManager.kSolid, "Solid Line"),
    (OpenMayaRender.MUIDrawManager.kShortDotted, "Short Dotted Line"),
    (OpenMayaRender.MUIDrawManager.kShortDashed, "Short Dashed Line"),
    (OpenMayaRender.MUIDrawManager.kDashed, "Dashed Line"),
    (OpenMayaRender.MUIDrawManager.kDotted, "Dotted Line"),
]

# Scene scale names.
SCENE_SCALE_MILLIMETER_NAME = "millimeter"
SCENE_SCALE_CENTIMETER_NAME = "centimeter"
SCENE_SCALE_METER_NAME = "meter"
SCENE_SCALE_DECIMETER_NAME = "decimeter"
SCENE_SCALE_KILOMETER_NAME = "kilometer"

# Scene scale values.
SCENE_SCALE_MILLIMETER_VALUE = 0
SCENE_SCALE_CENTIMETER_VALUE = 1
SCENE_SCALE_METER_VALUE = 2
SCENE_SCALE_DECIMETER_VALUE = 3
SCENE_SCALE_KILOMETER_VALUE = 4

# Scene scale.
SCENE_SCALES = [
    (SCENE_SCALE_MILLIMETER_NAME, SCENE_SCALE_MILLIMETER_VALUE),
    (SCENE_SCALE_CENTIMETER_NAME, SCENE_SCALE_CENTIMETER_VALUE),
    (SCENE_SCALE_METER_NAME, SCENE_SCALE_METER_VALUE),
    (SCENE_SCALE_DECIMETER_NAME, SCENE_SCALE_DECIMETER_VALUE),
    (SCENE_SCALE_KILOMETER_NAME, SCENE_SCALE_KILOMETER_VALUE)
]

# Default sizes for various on-screen stuff.
TEXT_SIZE_DEFAULT_VALUE = 1.0
POINT_SIZE_DEFAULT_VALUE = 1.0
LINE_WIDTH_DEFAULT_VALUE = 1.0
FIELD_TEXT_SIZE_DEFAULT_VALUE = 1.0
FIELD_POINT_SIZE_DEFAULT_VALUE = 1.0
FIELD_LINE_WIDTH_DEFAULT_VALUE = 1.0


def maya_useNewAPI():
    """With this function's existence, Maya knows to use API2 for loading."""
    pass


class HUDNode(OpenMayaUI.MPxLocatorNode):
    node_id = OpenMaya.MTypeId(PLUGIN_NODE_ID)
    draw_db_classification = "drawdb/geometry/dcCameraInferno"
    draw_registrant_id = "dcCameraInfernoNodePlugin"

    # Global Size Values
    m_text_size = None
    m_line_width = None
    m_point_size = None

    # Values
    m_scene_scale = None
    m_frames_per_second = None

    # Film Gate Attributes
    m_film_gate_enable = None
    m_film_gate_color = None
    m_film_gate_alpha = None

    # Mask Attributes
    m_mask_enable = None
    m_mask_enable_top = None
    m_mask_enable_bot = None
    m_mask_color = None
    m_mask_alpha = None
    m_mask_aspect_ratio = None

    # Field Attributes
    m_field = None
    m_field_enable = None
    m_field_type = None
    m_field_pos_a = None
    m_field_pos_b = None

    m_field_point_size = None
    m_field_point_color = None
    m_field_point_alpha = None

    m_field_line_width = None
    m_field_line_style = None
    m_field_line_color = None
    m_field_line_alpha = None

    m_field_text_size = None
    m_field_text_align = None
    m_field_text_font_name = None
    m_field_text_bold = None
    m_field_text_italic = None
    m_field_text_color = None
    m_field_text_alpha = None
    m_field_text_value = None

    m_field_value_a = None
    m_field_value_b = None
    m_field_value_c = None
    m_field_value_d = None

    @staticmethod
    def creator():
        """Creates an instance of the node."""
        return HUDNode()

    @staticmethod
    def initialize():
        """Set up the attributes and other details of the node."""

        # Create the plug-in Attributes
        nAttr = OpenMaya.MFnNumericAttribute()
        tAttr = OpenMaya.MFnTypedAttribute()
        cAttr = OpenMaya.MFnCompoundAttribute()
        eAttr = OpenMaya.MFnEnumAttribute()
        gAttr = OpenMaya.MFnGenericAttribute()
        uAttr = OpenMaya.MFnUnitAttribute()
        mAttr = OpenMaya.MFnMessageAttribute()

        # Text Size
        HUDNode.m_text_size = nAttr.create(
            "textSize", "txtsz",
            OpenMaya.MFnNumericData.kDouble,
            TEXT_SIZE_DEFAULT_VALUE)
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = True
        OpenMaya.MPxNode.addAttribute(HUDNode.m_text_size)

        # Line Width
        HUDNode.m_line_width = nAttr.create(
            "lineWidth", "lnwdth",
            OpenMaya.MFnNumericData.kDouble,
            LINE_WIDTH_DEFAULT_VALUE)
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = True
        OpenMaya.MPxNode.addAttribute(HUDNode.m_line_width)

        # Point Size
        HUDNode.m_point_size = nAttr.create(
            "pointSize", "pntsz",
            OpenMaya.MFnNumericData.kDouble,
            POINT_SIZE_DEFAULT_VALUE)
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = True
        OpenMaya.MPxNode.addAttribute(HUDNode.m_point_size)

        # Frames Per-Second
        HUDNode.m_frames_per_second = nAttr.create(
            "framesPerSecond", "fps",
            OpenMaya.MFnNumericData.kDouble, 24.0)
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = True
        OpenMaya.MPxNode.addAttribute(HUDNode.m_frames_per_second)

        # Scene Scale
        HUDNode.m_scene_scale = eAttr.create(
            "sceneScale", "scnscl",
            SCENE_SCALE_DECIMETER_VALUE)
        for name, value in SCENE_SCALES:
            eAttr.addField(name, value)
        eAttr.readable = True
        eAttr.writable = True
        eAttr.storable = True
        eAttr.keyable = False
        OpenMaya.MPxNode.addAttribute(HUDNode.m_scene_scale)
        # Film Gate Enable attribute
        HUDNode.m_film_gate_enable = nAttr.create(
            "filmGateEnable", "flmgtenbl",
            OpenMaya.MFnNumericData.kBoolean, False)
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = True

        # Film Gate Color attribute
        HUDNode.m_film_gate_color = nAttr.createColor(
            "filmGateColor", "flmgtcol")
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = False

        # Film Gate Alpha attribute
        HUDNode.m_film_gate_alpha = nAttr.create(
            "filmGateAlpha", "flmgtalp",
            OpenMaya.MFnNumericData.kFloat, 0.5)
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = True

        # Film Gate attribute
        HUDNode.m_film_gate = cAttr.create("filmGate", "flmgt")
        cAttr.readable = True
        cAttr.writable = True
        cAttr.storable = True
        cAttr.keyable = False
        cAttr.hidden = False
        cAttr.addChild(HUDNode.m_film_gate_enable)
        cAttr.addChild(HUDNode.m_film_gate_color)
        cAttr.addChild(HUDNode.m_film_gate_alpha)
        OpenMaya.MPxNode.addAttribute(HUDNode.m_film_gate)

        # Mask Enable attribute
        HUDNode.m_mask_enable = nAttr.create(
            "maskEnable", "mskenbl",
            OpenMaya.MFnNumericData.kBoolean, True)
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = True

        # Mask Top attribute
        HUDNode.m_mask_enable_top = nAttr.create(
            "maskEnableTop", "mskenbltop",
            OpenMaya.MFnNumericData.kBoolean, True)
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = True

        # Mask Bottom attribute
        HUDNode.m_mask_enable_bot = nAttr.create(
            "maskEnableBottom", "mskenblbot",
            OpenMaya.MFnNumericData.kBoolean, True)
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = True

        # Mask Aspect Ratio attribute
        HUDNode.m_mask_aspect_ratio = nAttr.create(
            "maskAspectRatio", "mskasprto",
            OpenMaya.MFnNumericData.kDouble, 1.0)
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = False

        # Mask Color attribute
        HUDNode.m_mask_color = nAttr.createColor(
            "maskColor", "mskcol")
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = False

        # Mask Alpha attribute
        HUDNode.m_mask_alpha = nAttr.create(
            "maskAlpha", "mskalp",
            OpenMaya.MFnNumericData.kFloat, 1.0)
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = True

        # Mask attribute
        HUDNode.m_mask = cAttr.create("mask", "msk")
        cAttr.readable = True
        cAttr.writable = True
        cAttr.storable = True
        cAttr.keyable = False
        cAttr.hidden = False
        cAttr.addChild(HUDNode.m_mask_enable)
        cAttr.addChild(HUDNode.m_mask_enable_top)
        cAttr.addChild(HUDNode.m_mask_enable_bot)
        cAttr.addChild(HUDNode.m_mask_aspect_ratio)
        cAttr.addChild(HUDNode.m_mask_color)
        cAttr.addChild(HUDNode.m_mask_alpha)
        OpenMaya.MPxNode.addAttribute(HUDNode.m_mask)

        # Field Enable attribute
        HUDNode.m_field_enable = nAttr.create(
            "fieldEnable", "fldenbl",
            OpenMaya.MFnNumericData.kBoolean, True)
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = True

        # Field Type attribute
        HUDNode.m_field_type = eAttr.create(
            "fieldType", "fldtyp",
            FIELD_TYPE_TEXT_2D_INDEX)
        for index, name in FIELD_TYPES:
            eAttr.addField(name, index)
        eAttr.readable = True
        eAttr.writable = True
        eAttr.storable = True
        eAttr.keyable = False

        # Field Position A attribute
        HUDNode.m_field_pos_a = nAttr.createPoint(
            "fieldPositionA", "fldposa")
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = False

        # Field Position B attribute
        HUDNode.m_field_pos_b = nAttr.createPoint(
            "fieldPositionB", "fldposb")
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = False

        # Field Point Size attribute
        #
        # The size is a percentage of the full film back height
        # size. 100.0% equals full height, 50.0% equals half height.
        HUDNode.m_field_point_size = nAttr.create(
            "fieldPointSize", "fldpntsz",
            OpenMaya.MFnNumericData.kFloat,
            FIELD_POINT_SIZE_DEFAULT_VALUE,
        )
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = True

        # Field Point Color attribute
        HUDNode.m_field_point_color = nAttr.createColor(
            "fieldPointColor", "fldpntcol")
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = False

        # Field Point Alpha attribute
        HUDNode.m_field_point_alpha = nAttr.create(
            "fieldPointAlpha", "fldpntalp",
            OpenMaya.MFnNumericData.kFloat, 1.0)
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = True

        # Field Line Width attribute
        #
        # The width is a percentage of the full film back height
        # width. 100.0% equals full height, 50.0% equals half height.
        HUDNode.m_field_line_width = nAttr.create(
            "fieldLineWidth", "fldlnwdth",
            OpenMaya.MFnNumericData.kFloat,
            FIELD_LINE_WIDTH_DEFAULT_VALUE
        )
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = True

        # Field Line_Style attribute
        HUDNode.m_field_line_style = eAttr.create(
            "fieldLineStyle", "fldlnstyl",
            OpenMayaRender.MUIDrawManager.kSolid)
        for index, name in LINE_STYLE_TYPES:
            eAttr.addField(name, index)
        eAttr.readable = True
        eAttr.writable = True
        eAttr.storable = True
        eAttr.keyable = False

        # Field Line Color attribute
        HUDNode.m_field_line_color = nAttr.createColor(
            "fieldLineColor", "fldlncol")
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = False

        # Field Line Alpha attribute
        HUDNode.m_field_line_alpha = nAttr.create(
            "fieldLineAlpha", "fldlnalp",
            OpenMaya.MFnNumericData.kFloat, 1.0)
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = True

        # Field Text Align attribute
        HUDNode.m_field_text_align = eAttr.create(
            "fieldTextAlign", "fldtxtalg", 0)
        for index, name in TEXT_ALIGN_TYPES:
            eAttr.addField(name, index)
        eAttr.readable = True
        eAttr.writable = True
        eAttr.storable = True
        eAttr.keyable = False

        # Field Text Bold attribute
        HUDNode.m_field_text_bold = nAttr.create(
            "fieldTextBold", "fldtxtbld",
            OpenMaya.MFnNumericData.kBoolean, False)
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = True

        # Field Text Italic attribute
        HUDNode.m_field_text_italic = nAttr.create(
            "fieldTextItalic", "fldtxtitlc",
            OpenMaya.MFnNumericData.kBoolean, False)
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = True

        # Field Text Font Name attribute
        string_data = OpenMaya.MFnStringData()
        # Some research suggests 'San Serif' is a plesant and easy
        # font to read, and has become common in advertising for this
        # reason.
        # data_object = string_data.create("San Serif")
        data_object = string_data.create("Consolas")
        HUDNode.m_field_text_font_name = tAttr.create(
            "fieldTextFontName", "fldtxtfntnm",
            OpenMaya.MFnData.kString,
            data_object)
        tAttr.readable = True
        tAttr.writable = True
        tAttr.storable = True
        tAttr.keyable = False

        # Field Text Size attribute
        #
        # The size is a percentage of the full film back height
        # size. 100.0% equals full height, 50.0% equals half height.
        HUDNode.m_field_text_size = nAttr.create(
            "fieldTextSize", "fldtxtsz",
            OpenMaya.MFnNumericData.kFloat,
            FIELD_TEXT_SIZE_DEFAULT_VALUE,
        )
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = True

        # Field Text Color attribute
        HUDNode.m_field_text_color = nAttr.createColor(
            "fieldTextColor", "fldtxtcol")
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = False

        # Field Text Alpha attribute
        HUDNode.m_field_text_alpha = nAttr.create(
            "fieldTextAlpha", "fldtxtalp",
            OpenMaya.MFnNumericData.kFloat, 1.0)
        nAttr.readable = True
        nAttr.writable = True
        nAttr.storable = True
        nAttr.keyable = True

        # Field Text Value attribute
        string_data = OpenMaya.MFnStringData()
        data_object = string_data.create("Text")
        HUDNode.m_field_text_value = tAttr.create(
            "fieldTextValue", "fldtxtv",
            OpenMaya.MFnData.kString,
            data_object)
        tAttr.readable = True
        tAttr.writable = True
        tAttr.storable = True
        tAttr.keyable = False

        # Field ValueA attribute
        HUDNode.m_field_value_a = gAttr.create(
            "fieldValueA", "fldvala")
        gAttr.readable = True
        gAttr.writable = True
        gAttr.keyable = False
        gAttr.addDataType(OpenMaya.MFnData.kString)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kBoolean)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kByte)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kChar)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kShort)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kInt)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kLong)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kFloat)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kDouble)

        # Field ValueB attribute
        HUDNode.m_field_value_b = gAttr.create(
            "fieldValueB", "fldvalb")
        gAttr.readable = True
        gAttr.writable = True
        gAttr.keyable = False
        gAttr.addDataType(OpenMaya.MFnData.kString)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kBoolean)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kByte)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kChar)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kShort)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kInt)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kLong)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kFloat)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kDouble)

        # Field ValueC attribute
        HUDNode.m_field_value_c = gAttr.create(
            "fieldValueC", "fldvalc")
        gAttr.readable = True
        gAttr.writable = True
        gAttr.keyable = False
        gAttr.addDataType(OpenMaya.MFnData.kString)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kBoolean)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kByte)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kChar)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kShort)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kInt)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kLong)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kFloat)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kDouble)

        # Field ValueD attribute
        HUDNode.m_field_value_d = gAttr.create(
            "fieldValueD", "fldvald")
        gAttr.readable = True
        gAttr.writable = True
        gAttr.keyable = False
        gAttr.addDataType(OpenMaya.MFnData.kString)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kBoolean)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kByte)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kChar)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kShort)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kInt)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kLong)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kFloat)
        gAttr.addNumericType(OpenMaya.MFnNumericData.kDouble)

        # Field attribute array
        HUDNode.m_field = cAttr.create("field", "fld")
        cAttr.readable = True
        cAttr.writable = True
        cAttr.storable = True
        cAttr.keyable = False
        cAttr.hidden = False
        cAttr.array = True
        cAttr.indexMatters = False
        cAttr.addChild(HUDNode.m_field_enable)
        cAttr.addChild(HUDNode.m_field_type)
        cAttr.addChild(HUDNode.m_field_pos_a)
        cAttr.addChild(HUDNode.m_field_pos_b)
        cAttr.addChild(HUDNode.m_field_point_size)
        cAttr.addChild(HUDNode.m_field_point_color)
        cAttr.addChild(HUDNode.m_field_point_alpha)
        cAttr.addChild(HUDNode.m_field_line_width)
        cAttr.addChild(HUDNode.m_field_line_style)
        cAttr.addChild(HUDNode.m_field_line_color)
        cAttr.addChild(HUDNode.m_field_line_alpha)
        cAttr.addChild(HUDNode.m_field_text_size)
        cAttr.addChild(HUDNode.m_field_text_align)
        cAttr.addChild(HUDNode.m_field_text_bold)
        cAttr.addChild(HUDNode.m_field_text_italic)
        cAttr.addChild(HUDNode.m_field_text_font_name)
        cAttr.addChild(HUDNode.m_field_text_color)
        cAttr.addChild(HUDNode.m_field_text_alpha)
        cAttr.addChild(HUDNode.m_field_text_value)
        cAttr.addChild(HUDNode.m_field_value_a)
        cAttr.addChild(HUDNode.m_field_value_b)
        cAttr.addChild(HUDNode.m_field_value_c)
        cAttr.addChild(HUDNode.m_field_value_d)
        OpenMaya.MPxNode.addAttribute(HUDNode.m_field)
        return

    def __init__(self):
        super(HUDNode, self).__init__()

    def compute(self, plug, data):
        # We don't need to compute anything in this node.
        return None

    def isBounded(self):
        return False


class HUDNodeData(OpenMaya.MUserData):
    """Custom data to be persisteted after each draw call."""
    def __init__(self):
        delete_after_use = False
        super(HUDNodeData, self).__init__(delete_after_use)
        self.m_text_size = 1.0
        self.m_point_size = 1.0
        self.m_line_width = 1.0

        self.m_film_gate_enable = True
        self.m_film_gate_color = OpenMaya.MColor()
        self.m_film_gate_alpha = 1.0

        self.m_mask_enable = True
        self.m_mask_enable_top = True
        self.m_mask_enable_bot = True
        self.m_mask_color = OpenMaya.MColor()
        self.m_mask_alpha = 1.0
        self.m_mask_aspect_ratio = 1.0

        self.m_field_enable = OpenMaya.MIntArray()
        self.m_field_type = OpenMaya.MIntArray()
        self.m_field_pos_a = OpenMaya.MPointArray()
        self.m_field_pos_b = OpenMaya.MPointArray()

        self.m_field_point_size = OpenMaya.MFloatArray()
        self.m_field_point_color = OpenMaya.MPointArray()
        self.m_field_point_alpha = OpenMaya.MFloatArray()

        self.m_field_line_width = OpenMaya.MFloatArray()
        self.m_field_line_style = OpenMaya.MIntArray()
        self.m_field_line_color = OpenMaya.MPointArray()
        self.m_field_line_alpha = OpenMaya.MFloatArray()

        self.m_field_text_size = OpenMaya.MFloatArray()
        self.m_field_text_align = OpenMaya.MIntArray()
        self.m_field_text_font_name = []
        self.m_field_text_bold = OpenMaya.MIntArray()
        self.m_field_text_italic = OpenMaya.MIntArray()
        self.m_field_text_color = OpenMaya.MPointArray()
        self.m_field_text_alpha = OpenMaya.MFloatArray()
        self.m_field_text_values = []

        self.m_field_general_values = {}
        self.m_field_value_a = []
        self.m_field_value_b = []
        self.m_field_value_c = []
        self.m_field_value_d = []
        return


def get_generic_attr_value_from_plug(x):
    """
    Query the value from a generic attribute plug.

    :param x: The plug.
    :type x: OpenMaya.MPlug

    :return: The value from the attribute plug.
    """
    data_handle = OpenMaya.MPlug.asMDataHandle(x)
    is_generic, is_numeric, is_null = data_handle.isGeneric()
    if not is_generic:
        return None
    if is_null:
        return None
    if is_numeric:
        # TODO: I cannot work out how to detect which type of
        # numeric data has been given, and convert it to an
        # equal Python data type.
        if data_handle.type() == OpenMaya.MFnData.kNumeric:
            return data_handle.asGenericDouble()
    else:
        if data_handle.type() == OpenMaya.MFnData.kString:
            return data_handle.asString()
    return None


class HUDNodeDrawOverride(OpenMayaRender.MPxDrawOverride):
    """Control the viewport display of HUDNode in Viewport 2.0."""

    @staticmethod
    def creator(obj):
        return HUDNodeDrawOverride(obj)

    def __init__(self, obj):
        """
        Construct new Draw Override.

        :param obj: Maya Object to attach draw override to.
        :type obj: MObject
        """
        # If always dirty, the draw override will always be called,
        # regardless of any DG data updating, which will be slow.
        is_always_dirty = True
        callback = None
        super(HUDNodeDrawOverride, self).__init__(obj, callback, is_always_dirty)

    def supportedDrawAPIs(self):
        """Support all Draw APIs"""
        return (OpenMayaRender.MRenderer.kOpenGL
                | OpenMayaRender.MRenderer.kDirectX11
                | OpenMayaRender.MRenderer.kOpenGLCoreProfile)

    def isBounded(self, obj_path, camera_path):
        """Node does not have a bounding box size."""
        return False

    def disableInternalBoundingBoxDraw(self):
        return True

    def prepareForDraw(self, obj_path, camera_path, frame_context, old_data):
        # Retrieve data cache (create if does not exist)
        data = old_data
        if not isinstance(data, HUDNodeData):
            data = HUDNodeData()
        node_obj = obj_path.node()

        # Global Size attributes.
        text_size_plug = OpenMaya.MPlug(node_obj, HUDNode.m_text_size)
        point_size_plug = OpenMaya.MPlug(node_obj, HUDNode.m_point_size)
        line_width_plug = OpenMaya.MPlug(node_obj, HUDNode.m_line_width)
        data.m_text_size = text_size_plug.asDouble()
        data.m_point_size = point_size_plug.asDouble()
        data.m_line_width = line_width_plug.asDouble()

        # Get Film Gate data.
        film_gate_enable_plug = OpenMaya.MPlug(node_obj, HUDNode.m_film_gate_enable)
        film_gate_color_plug = OpenMaya.MPlug(node_obj, HUDNode.m_film_gate_color)
        film_gate_alpha_plug = OpenMaya.MPlug(node_obj, HUDNode.m_film_gate_alpha)
        data.m_film_gate_enable = film_gate_enable_plug.asInt()
        data.m_film_gate_color = film_gate_color_plug.asMDataHandle().asFloat3()
        data.m_film_gate_alpha = film_gate_alpha_plug.asFloat()

        # Mask data.
        mask_enable_plug = OpenMaya.MPlug(node_obj, HUDNode.m_mask_enable)
        mask_enable_top_plug = OpenMaya.MPlug(node_obj, HUDNode.m_mask_enable_top)
        mask_enable_bot_plug = OpenMaya.MPlug(node_obj, HUDNode.m_mask_enable_bot)
        mask_color_plug = OpenMaya.MPlug(node_obj, HUDNode.m_mask_color)
        mask_alpha_plug = OpenMaya.MPlug(node_obj, HUDNode.m_mask_alpha)
        mask_aspect_ratio_plug = OpenMaya.MPlug(node_obj, HUDNode.m_mask_aspect_ratio)
        data.m_mask_enable = mask_enable_plug.asInt()
        data.m_mask_enable_top = mask_enable_top_plug.asInt()
        data.m_mask_enable_bot = mask_enable_bot_plug.asInt()
        data.m_mask_color = mask_color_plug.asMDataHandle().asFloat3()
        data.m_mask_alpha = mask_alpha_plug.asFloat()
        data.m_mask_aspect_ratio = mask_aspect_ratio_plug.asDouble()

        # Field general data.
        data.m_field_enable.clear()
        data.m_field_type.clear()
        data.m_field_pos_a.clear()
        data.m_field_pos_b.clear()
        data.m_field_enable = self.get_field_enable(
            obj_path,
            data.m_field_enable)
        data.m_field_type = self.get_field_type(
            obj_path,
            data.m_field_type)
        data.m_field_pos_a = self.get_field_position_a(
            obj_path,
            data.m_field_pos_a)
        data.m_field_pos_b = self.get_field_position_b(
            obj_path,
            data.m_field_pos_b)

        # Field Point data
        data.m_field_point_size.clear()
        data.m_field_point_color.clear()
        data.m_field_point_alpha.clear()
        data.m_field_point_size = self.get_field_point_size(
            obj_path,
            data.m_field_point_size)
        data.m_field_point_color = self.get_field_point_color(
            obj_path,
            data.m_field_point_color)
        data.m_field_point_alpha = self.get_field_point_alpha(
            obj_path,
            data.m_field_point_alpha)

        # Field Line data
        data.m_field_line_width.clear()
        data.m_field_line_style.clear()
        data.m_field_line_color.clear()
        data.m_field_line_alpha.clear()
        data.m_field_line_width = self.get_field_line_width(
            obj_path,
            data.m_field_line_width)
        data.m_field_line_style = self.get_field_line_style(
            obj_path,
            data.m_field_line_style)
        data.m_field_line_color = self.get_field_line_color(
            obj_path,
            data.m_field_line_color)
        data.m_field_line_alpha = self.get_field_line_alpha(
            obj_path,
            data.m_field_line_alpha)

        # Field Text data
        data.m_field_text_size.clear()
        data.m_field_text_align.clear()
        data.m_field_text_font_name = []
        data.m_field_text_bold.clear()
        data.m_field_text_italic.clear()
        data.m_field_text_color.clear()
        data.m_field_text_alpha.clear()
        data.m_field_text_values = []

        data.m_field_text_size = self.get_field_text_size(
            obj_path,
            data.m_field_text_size)
        data.m_field_text_align = self.get_field_text_align(
            obj_path,
            data.m_field_text_align)
        data.m_field_text_font_name = self.get_field_text_font_name(
            obj_path,
            data.m_field_text_font_name)
        data.m_field_text_bold = self.get_field_text_bold(
            obj_path,
            data.m_field_text_bold)
        data.m_field_text_italic = self.get_field_text_italic(
            obj_path,
            data.m_field_text_italic)
        data.m_field_text_color = self.get_field_text_color(
            obj_path,
            data.m_field_text_color)
        data.m_field_text_alpha = self.get_field_text_alpha(
            obj_path,
            data.m_field_text_alpha)
        data.m_field_text_values = self.get_field_text_value(
            obj_path,
            data.m_field_text_values)

        # Scene Scale
        scene_scale_plug = OpenMaya.MPlug(node_obj, HUDNode.m_scene_scale)
        scene_scale = scene_scale_plug.asDouble()
        scene_scale_factor = 1.0
        scale_to_mm = 1.0
        scale_to_cm = 1.0
        scale_to_dm = 1.0
        scale_to_m = 1.0
        scale_to_km = 1.0
        scale_to_inches = 1.0
        scale_to_feet = 1.0
        scale_to_yards = 1.0
        scale_to_miles = 1.0
        scene_scale_unit = 'unit'
        if scene_scale == SCENE_SCALE_MILLIMETER_VALUE:
            scene_scale_unit = UNIT_MILLIMETERS
            scene_scale_factor = 0.001
            # Millimeters to...
            scale_to_mm = 1.0
            scale_to_cm = 0.1
            scale_to_dm = 0.01
            scale_to_m = 0.001
            scale_to_km = 1e-6
            scale_to_inches = 0.1 / 2.54
            scale_to_feet = 0.1 / (2.54 * 12.0)
            scale_to_yards = 0.01 / 9.144
            scale_to_miles = 1.0 / 1609340.0
        elif scene_scale == SCENE_SCALE_CENTIMETER_VALUE:
            scene_scale_unit = UNIT_CENTIMETERS
            scene_scale_factor = 0.01
            # Centimeters to...
            scale_to_mm = 10.0
            scale_to_cm = 1.0
            scale_to_dm = 10.0
            scale_to_m = 0.01
            scale_to_km = 1e-5
            scale_to_inches = 1.0 / 2.54
            scale_to_feet = 1.0 / (2.54 * 12.0)
            scale_to_yards = 0.1 / 9.144
            scale_to_miles = 1.0 / 160934.0
        elif scene_scale == SCENE_SCALE_DECIMETER_VALUE:
            scene_scale_unit = UNIT_DECIMETERS
            scene_scale_factor = 0.1
            # Decimeters to...
            scale_to_mm = 100.0
            scale_to_cm = 10.0
            scale_to_dm = 1.0
            scale_to_m = 0.1
            scale_to_km = 1e-4
            scale_to_inches = 10.0 / 2.54
            scale_to_feet = 10.0 / (2.54 * 12.0)
            scale_to_yards = 1.0 / 9.144
            scale_to_miles = 1.0 / 16093.4
        elif scene_scale == SCENE_SCALE_METER_VALUE:
            scene_scale_unit = UNIT_METERS
            scene_scale_factor = 1.0
            # Meters to...
            scale_to_mm = 1000.0
            scale_to_cm = 100.0
            scale_to_dm = 10.0
            scale_to_m = 1.0
            scale_to_km = 1e-3
            scale_to_inches = 100.0 / 2.54
            scale_to_feet = 100.0 / (2.54 * 12.0)
            scale_to_yards = 10.0 / 9.144
            scale_to_miles = 10.0 / 16093.4
        elif scene_scale == SCENE_SCALE_KILOMETER_VALUE:
            scene_scale_unit = UNIT_KILOMETERS
            scene_scale_factor = 1000.0
            # Kilometers to...
            scale_to_mm = 1000000.0
            scale_to_cm = 100000.0
            scale_to_dm = 10000.0
            scale_to_m = 1000.0
            scale_to_km = 1.0
            scale_to_inches = 100000.0 / 2.54
            scale_to_feet = 100000.0 / (2.54 * 12.0)
            scale_to_yards = 10000.0 / 9.144
            scale_to_miles = 10000.0 / 16093.4

        camera_fn = OpenMaya.MFnCamera(camera_path)
        camera_tfm_path = camera_path.pop()
        camera_tfm_fn = OpenMaya.MFnTransform(camera_tfm_path)
        space = OpenMaya.MSpace.kWorld
        camera_quat_rotation = camera_tfm_fn.rotation(space, asQuaternion=True)
        camera_rotation = camera_quat_rotation.asEulerRotation()
        rotation_order = OpenMaya.MEulerRotation.kZXY
        camera_rotation.reorderIt(rotation_order)
        camera_tilt = math.degrees(camera_rotation.x)
        camera_pan = math.degrees(camera_rotation.y)
        camera_roll = math.degrees(camera_rotation.z)

        camera_short_name = camera_tfm_path.partialPathName()
        camera_long_name = camera_tfm_path.fullPathName()

        film_back_width = camera_fn.horizontalFilmAperture
        film_back_height = camera_fn.verticalFilmAperture
        film_back_aspect_ratio = camera_fn.aspectRatio()

        angle_of_view_x = math.degrees(camera_fn.horizontalFieldOfView())
        angle_of_view_y = math.degrees(camera_fn.verticalFieldOfView())

        focal_length = camera_fn.focalLength
        lens_f_stop = camera_fn.fStop
        focus_distance = camera_fn.focusDistance
        shutter_angle = math.degrees(camera_fn.shutterAngle)

        date_and_time_now = datetime.datetime.now()
        time_now = date_and_time_now.time()
        date_now = date_and_time_now.date()

        frame = maya.cmds.currentTime(query=True)
        user_name = getpass.getuser()
        file_path = maya.cmds.file(query=True, sceneName=True) or 'Untitled'
        file_name = os.path.basename(file_path)
        file_name, file_ext = os.path.splitext(file_name)
        data.m_field_general_values = {
            # Environment Details
            'user_name': user_name,
            'file_path': file_path,
            'file_name': file_name,

            # Date and Time
            'time_iso': time_now.strftime('%H:%M'),
            'date_iso': date_now.strftime('%Y-%M-%d'),
            'datetime_iso': date_and_time_now.strftime('%Y-%M-%d %H:%M'),
            'time': time_now.strftime('%I:%M%p'),
            'date': date_now.strftime('%a %b %d %Y'),
            'datetime': date_and_time_now.strftime('%a %b %d %I:%M%p %Y'),

            # Camera Name
            'camera_short_name': camera_short_name,
            'camera_long_name': camera_long_name,

            # Shot Frame
            'frame_integer': int(frame),
            'frame_float': frame,

            # Film Back
            'film_back_width_inches': film_back_width,
            'film_back_height_inches': film_back_height,
            'film_back_width_mm': film_back_width * 25.4,
            'film_back_height_mm': film_back_height * 25.4,

            # Camera
            'camera_tilt': camera_tilt,
            'camera_pan': camera_pan,
            'camera_roll': camera_roll,
            'camera_shutter_angle': shutter_angle,

            # Lens
            'lens_focal_length': focal_length,
            'lens_focus_distance': focus_distance,
            'lens_f_stop': lens_f_stop,
            'lens_angle_of_view_x': angle_of_view_x,
            'lens_angle_of_view_y': angle_of_view_y,
        }

        # Query Generic data.
        data.m_field_value_a = []
        data.m_field_value_b = []
        data.m_field_value_c = []
        data.m_field_value_d = []
        data.m_field_value_a = self.get_field_value_a(
            obj_path,
            data.m_field_value_a)
        data.m_field_value_b = self.get_field_value_b(
            obj_path,
            data.m_field_value_b)
        data.m_field_value_c = self.get_field_value_c(
            obj_path,
            data.m_field_value_c)
        data.m_field_value_d = self.get_field_value_d(
            obj_path,
            data.m_field_value_d)
        return data

    def query_attribute_value_array(self,
                                    obj_path,
                                    attribute,
                                    child_attribute,
                                    read_value_func,
                                    array,
                                    default_value):
        """Query an array of values from a child attribute inside an array
        compound attribute."""
        assert len(array) == 0
        cls_node = obj_path.node()
        array_plug = OpenMaya.MPlug(cls_node, attribute)
        if array_plug.isNull:
            return array
        number_of_array_elements = array_plug.evaluateNumElements()
        for i in range(number_of_array_elements):
            compound_plug = array_plug.elementByPhysicalIndex(i)
            if compound_plug.isNull:
                array.append(default_value)
                continue
            child_plug = compound_plug.child(child_attribute)
            if child_plug.isNull:
                array.append(default_value)
                continue
            value = read_value_func(child_plug)
            array.append(value)
        assert len(array) == number_of_array_elements
        return array

    def get_field_enable(self, obj_path, values):
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_enable,
            OpenMaya.MPlug.asInt,
            values,
            0,  # disabled by default.
        )
        return values

    def get_field_type(self, obj_path, values):
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_type,
            OpenMaya.MPlug.asShort,
            values,
            FIELD_TYPE_NONE_INDEX,
        )
        return values

    def get_field_position_a(self, obj_path, values):
        default_value = OpenMaya.MPoint(0.0, 0.0, 0.0)
        get_value_func = lambda x: OpenMaya.MPlug.asMDataHandle(x).asFloat3()
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_pos_a,
            get_value_func,
            values,
            default_value,
        )
        return values

    def get_field_position_b(self, obj_path, values):
        default_value = OpenMaya.MPoint(0.0, 0.0, 0.0)
        get_value_func = lambda x: OpenMaya.MPlug.asMDataHandle(x).asFloat3()
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_pos_b,
            get_value_func,
            values,
            default_value,
        )
        return values

    def get_field_point_size(self, obj_path, values):
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_point_size,
            OpenMaya.MPlug.asFloat,
            values,
            1.0,
        )
        return values

    def get_field_point_color(self, obj_path, values):
        default_value = OpenMaya.MPoint(0.0, 0.0, 0.0)
        get_value_func = lambda x: OpenMaya.MPlug.asMDataHandle(x).asFloat3()
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_point_color,
            get_value_func,
            values,
            default_value
        )
        return values

    def get_field_point_alpha(self, obj_path, values):
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_point_alpha,
            OpenMaya.MPlug.asFloat,
            values,
            1.0,
        )
        return values

    def get_field_line_width(self, obj_path, values):
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_line_width,
            OpenMaya.MPlug.asFloat,
            values,
            1.0,
        )
        return values

    def get_field_line_style(self, obj_path, values):
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_line_style,
            OpenMaya.MPlug.asShort,
            values,
            OpenMayaRender.MUIDrawManager.kSolid,
        )
        return values

    def get_field_line_color(self, obj_path, values):
        default_value = OpenMaya.MPoint(0.0, 0.0, 0.0)
        get_value_func = lambda x: OpenMaya.MPlug.asMDataHandle(x).asFloat3()
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_line_color,
            get_value_func,
            values,
            default_value
        )
        return values

    def get_field_line_alpha(self, obj_path, values):
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_line_alpha,
            OpenMaya.MPlug.asFloat,
            values,
            1.0,
        )
        return values

    def get_field_text_align(self, obj_path, values):
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_text_align,
            OpenMaya.MPlug.asShort,
            values,
            ALIGN_BOTTOM_LEFT_VALUE,
        )
        return values

    def get_field_text_font_name(self, obj_path, values):
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_text_font_name,
            OpenMaya.MPlug.asString,
            values,
            "No text defined.",
        )
        return values

    def get_field_text_bold(self, obj_path, values):
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_text_bold,
            OpenMaya.MPlug.asInt,
            values,
            0,  # disabled by default.
        )
        return values

    def get_field_text_italic(self, obj_path, values):
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_text_italic,
            OpenMaya.MPlug.asInt,
            values,
            0,  # disabled by default.
        )
        return values

    def get_field_text_size(self, obj_path, values):
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_text_size,
            OpenMaya.MPlug.asFloat,
            values,
            1.0,
        )
        return values

    def get_field_text_color(self, obj_path, values):
        default_value = OpenMaya.MPoint(0.0, 0.0, 0.0)
        get_value_func = lambda x: OpenMaya.MPlug.asMDataHandle(x).asFloat3()
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_text_color,
            get_value_func,
            values,
            default_value
        )
        return values

    def get_field_text_alpha(self, obj_path, values):
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_text_alpha,
            OpenMaya.MPlug.asFloat,
            values,
            1.0,
        )
        return values

    def get_field_text_value(self, obj_path, values):
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_text_value,
            OpenMaya.MPlug.asString,
            values,
            "No text defined.",
        )
        return values

    def get_field_value_a(self, obj_path, values):
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_value_a,
            get_generic_attr_value_from_plug,
            values,
            None,
        )
        return values

    def get_field_value_b(self, obj_path, values):
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_value_b,
            get_generic_attr_value_from_plug,
            values,
            None,
        )
        return values

    def get_field_value_c(self, obj_path, values):
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_value_c,
            get_generic_attr_value_from_plug,
            values,
            None,
        )
        return values

    def get_field_value_d(self, obj_path, values):
        values = self.query_attribute_value_array(
            obj_path,
            HUDNode.m_field,
            HUDNode.m_field_value_d,
            get_generic_attr_value_from_plug,
            values,
            None,
        )
        return values

    def hasUIDrawables(self):
        """We will use the addUIDrawables method to draw things."""
        return True

    @staticmethod
    def get_film_coord_corners_in_pixels(camera_fn, port_width, port_height):
        lens_squeeze = camera_fn.lensSqueezeRatio
        filmback_width = camera_fn.horizontalFilmAperture
        filmback_height = camera_fn.verticalFilmAperture
        filmback_aspect_ratio = (filmback_width / filmback_height) * lens_squeeze
        port_aspect_ratio = float(port_width) / float(port_height)

        apply_overscan = True
        apply_squeeze = True
        apply_pan_zoom = True
        aperture_x, aperture_y, offset_x, offset_y = camera_fn.getViewParameters(
            filmback_aspect_ratio,
            apply_overscan,
            apply_squeeze,
            apply_pan_zoom,
        )

        # Calculate Film Fit Logic
        gate_width = None
        gate_height = None
        vertical_factor = 1.0
        horizontal_factor = 1.0
        port_aspect_ratio = float(port_width) / float(port_height)
        port_horiz = port_aspect_ratio > filmback_aspect_ratio
        overscan = camera_fn.overscan
        # Determine vertical or horizontal film fit for 'Fill' or
        # 'Overscan' modes.
        film_fit = camera_fn.filmFit
        if film_fit == OpenMaya.MFnCamera.kFillFilmFit:
            if port_horiz:
                film_fit = OpenMaya.MFnCamera.kHorizontalFilmFit
            else:
                film_fit = OpenMaya.MFnCamera.kVerticalFilmFit
        elif film_fit == OpenMaya.MFnCamera.kOverscanFilmFit:
            if port_horiz:
                film_fit = OpenMaya.MFnCamera.kVerticalFilmFit
            else:
                film_fit = OpenMaya.MFnCamera.kHorizontalFilmFit
        if film_fit == OpenMaya.MFnCamera.kHorizontalFilmFit:
            gate_width = port_width * lens_squeeze
            gate_height = gate_width / filmback_aspect_ratio
            vertical_factor = (port_aspect_ratio / filmback_aspect_ratio) * lens_squeeze
        elif film_fit == OpenMaya.MFnCamera.kVerticalFilmFit:
            gate_height = port_height
            gate_width = gate_height * filmback_aspect_ratio * lens_squeeze
            horizontal_factor = (1.0 / port_aspect_ratio) * filmback_aspect_ratio

        hfa = camera_fn.horizontalFilmAperture
        vfa = camera_fn.verticalFilmAperture
        film_width = (hfa / aperture_x) * gate_width * lens_squeeze
        film_height = (vfa / aperture_y) * gate_height

        view_offset_x = (offset_x / hfa) * (hfa / aperture_x)
        view_offset_y = (offset_y / vfa) * (vfa / aperture_y)

        hfo = camera_fn.horizontalFilmOffset
        vfo = camera_fn.verticalFilmOffset
        film_offset_x = ((hfo / hfa) * (hfa / aperture_x)) / lens_squeeze
        film_offset_y = (vfo / vfa) * (vfa / aperture_y)

        film_left = (port_width - film_width) * 0.5
        film_left += -view_offset_x * port_width * horizontal_factor
        film_left += film_offset_x * port_width * horizontal_factor

        film_right = port_width - ((port_width - film_width) * 0.5)
        film_right -= view_offset_x * port_width * horizontal_factor
        film_right -= -film_offset_x * port_width * horizontal_factor

        film_bot = (port_height - film_height) * 0.5
        film_bot += -view_offset_y * port_height * vertical_factor
        film_bot += film_offset_y * port_height * vertical_factor

        film_top = port_height - ((port_height - film_height) * 0.5)
        film_top -= view_offset_y * port_height * vertical_factor
        film_top -= -film_offset_y * port_height * vertical_factor

        lower_left = (film_left, film_bot)
        upper_right = (film_right, film_top)
        return film_width, film_height, lower_left, upper_right

    @classmethod
    def get_film_coord_corners_in_screen(cls, camera_fn,
                                         port_width, port_height):
        film_width_px, film_height_px, film_lower_left_px, film_upper_right_px = \
            cls.get_film_coord_corners_in_pixels(
                camera_fn,
                port_width,
                port_height
            )

        # New width and height for Film Back
        film_width_screen = film_width_px
        film_height_screen = film_height_px

        # Re-calculate the Film Back corners into screen-space.
        left = ((film_lower_left_px[0] - (port_width / 2)) / port_width) * 2.0
        bot = ((film_lower_left_px[1] - (port_height / 2)) / port_height) * 2.0
        right = ((film_upper_right_px[0] - (port_width / 2)) / port_width) * 2.0
        top = ((film_upper_right_px[1] - (port_height / 2)) / port_height) * 2.0

        film_lower_left_screen = (left, bot)
        film_upper_right_screen = (right, top)
        return (
            film_width_screen,
            film_height_screen,
            film_lower_left_screen,
            film_upper_right_screen
        )

    @staticmethod
    def film_coord_to_corners(x, y, film_lower_left, film_upper_right):
        # Convert from '-1.0 ... 1.0' to '0.0 ... 1.0'
        new_x = (x + 1.0) * 0.5
        new_y = (y + 1.0) * 0.5

        left = film_lower_left[0]
        right = film_upper_right[0]
        bot = film_lower_left[1]
        top = film_upper_right[1]

        def lerp(a, b, v):
            return (1.0 - v) * a + v * b

        new_x = lerp(left, right, new_x)
        new_y = lerp(bot, top, new_y)
        return new_x, new_y

    @staticmethod
    def format_text_data(text, field_general_values,
                         value_a, value_b, value_c, value_d):
        values = {}
        values.update(field_general_values)
        values.update({
            'a': value_a,
            'b': value_b,
            'c': value_c,
            'd': value_d,
        })
        args = (value_a, value_b, value_c, value_d)

        def make_str():
            return str('<UNKNOWN>')

        values_with_defaults = collections.defaultdict(make_str, **values)
        text = string.Formatter().vformat(text, args, values_with_defaults)
        text = os.path.expandvars(text)
        return text

    @staticmethod
    def draw_film_gate(draw_manager,
                       color, alpha,
                       projection_inverse_matrix,
                       lower_left, lower_right,
                       upper_left, upper_right,
                       film_width, film_height,
                       film_lower_left, film_upper_right,
                       port_width, port_height):
        port_width = 1.0
        port_height = 1.0
        depth = 1.0

        positions = OpenMaya.MPointArray()
        positions.append(OpenMaya.MPoint(-1, -1, depth))
        positions.append(OpenMaya.MPoint(-1, port_height + 1, depth))
        positions.append(OpenMaya.MPoint(upper_left[0], upper_left[1], depth))

        positions.append(OpenMaya.MPoint(upper_left[0], upper_left[1], depth))
        positions.append(OpenMaya.MPoint(lower_left[0], lower_left[1], depth))
        positions.append(OpenMaya.MPoint(-1, -1, depth))

        positions.append(OpenMaya.MPoint(-1, port_height + 1, depth))
        positions.append(OpenMaya.MPoint(port_width + 1, port_height + 1, depth))
        positions.append(OpenMaya.MPoint(upper_left[0], upper_left[1], depth))

        positions.append(OpenMaya.MPoint(upper_left[0], upper_left[1], depth))
        positions.append(OpenMaya.MPoint(port_width + 1, port_height + 1, depth))
        positions.append(OpenMaya.MPoint(upper_right[0], upper_right[1], depth))

        positions.append(OpenMaya.MPoint(upper_right[0], upper_right[1], depth))
        positions.append(OpenMaya.MPoint(port_width + 1, port_height + 1))
        positions.append(OpenMaya.MPoint(port_width + 1, -1))

        positions.append(OpenMaya.MPoint(lower_right[0], lower_right[1], depth))
        positions.append(OpenMaya.MPoint(upper_right[0], upper_right[1], depth))
        positions.append(OpenMaya.MPoint(port_width + 1, -1, depth))

        positions.append(OpenMaya.MPoint(lower_left[0], lower_left[1], depth))
        positions.append(OpenMaya.MPoint(lower_right[0], lower_right[1], depth))
        positions.append(OpenMaya.MPoint(port_width + 1, -1, depth))

        positions.append(OpenMaya.MPoint(-1, -1, depth))
        positions.append(OpenMaya.MPoint(lower_left[0], lower_left[1], depth))
        positions.append(OpenMaya.MPoint(port_width + 1, -1, depth))

        view_positions = OpenMaya.MPointArray(positions)
        for i, position in enumerate(positions):
            view_positions[i] = position * projection_inverse_matrix

        draw_color = OpenMaya.MColor((color[0], color[1], color[2], alpha))
        draw_manager.setColor(draw_color)
        prim = OpenMayaRender.MUIDrawManager.kTriangles
        draw_manager.mesh(prim, view_positions)
        return

    @classmethod
    def draw_mask(cls,
                  draw_manager,
                  draw_top,
                  draw_bottom,
                  aspect_ratio,
                  color, alpha,
                  projection_inverse_matrix,
                  lower_left, lower_right,
                  upper_left, upper_right,
                  film_width_screen, film_height_screen,
                  film_lower_left_screen, film_upper_right_screen,
                  port_width, port_height):
        aspect = (film_width_screen / film_height_screen) / aspect_ratio

        depth = 1.0
        positions = OpenMaya.MPointArray()
        if draw_bottom:
            screen_x, screen_y = cls.film_coord_to_corners(
                1.0, -1.0 * aspect,
                film_lower_left_screen,
                film_upper_right_screen)
            # First Triangle.
            positions.append(OpenMaya.MPoint(lower_left[0], lower_left[1], depth))
            positions.append(OpenMaya.MPoint(lower_left[0], screen_y, depth))
            positions.append(OpenMaya.MPoint(screen_x, screen_y, depth))
            # Second Triangle.
            positions.append(OpenMaya.MPoint(lower_left[0], lower_left[1], depth))
            positions.append(OpenMaya.MPoint(screen_x, screen_y, depth))
            positions.append(OpenMaya.MPoint(lower_right[0], lower_right[1], depth))

        if draw_top:
            screen_x, screen_y = cls.film_coord_to_corners(
                1.0, 1.0 * aspect,
                film_lower_left_screen,
                film_upper_right_screen)
            # First triangle.
            positions.append(OpenMaya.MPoint(upper_left[0], upper_left[1], depth))
            positions.append(OpenMaya.MPoint(upper_left[0], screen_y, depth))
            positions.append(OpenMaya.MPoint(screen_x, screen_y, depth))
            # Second triangle.
            positions.append(OpenMaya.MPoint(upper_left[0], upper_left[1], depth))
            positions.append(OpenMaya.MPoint(screen_x, screen_y, depth))
            positions.append(OpenMaya.MPoint(upper_right[0], upper_right[1], depth))

        draw_color = OpenMaya.MColor((color[0], color[1], color[2], alpha))
        draw_manager.setColor(draw_color)

        view_positions = OpenMaya.MPointArray(positions)
        for i, position in enumerate(positions):
            view_positions[i] = position * projection_inverse_matrix

        prim = OpenMayaRender.MUIDrawManager.kTriangles
        draw_manager.mesh(prim, view_positions)
        return

    @classmethod
    def draw_field_2d_text(cls, draw_manager,
                           position,
                           text_size,
                           text_align,
                           text_bold,
                           text_italic,
                           text_font_name,
                           color, alpha,
                           text,
                           pos_lower_left, pos_lower_right,
                           pos_upper_left, pos_upper_right,
                           film_width, film_height,
                           film_lower_left, film_upper_right,
                           port_width, port_height):
        text_align_vertical = \
            MAP_TEXT_ALIGN_TO_ALIGN_VERTICAL.get(text_align, 0)
        text_align_horizontal = \
            MAP_TEXT_ALIGN_TO_ALIGN_HORIZONTAL.get(text_align, 0)

        # Font properties
        weight = OpenMayaRender.MUIDrawManager.kWeightLight
        incline = OpenMayaRender.MUIDrawManager.kInclineNormal
        if text_bold:
            weight = OpenMayaRender.MUIDrawManager.kWeightBold
        if text_italic:
            incline = OpenMayaRender.MUIDrawManager.kInclineItalic

        # Calculate position and font size.
        position_x, position_y = cls.film_coord_to_corners(
            position.x, position.y,
            film_lower_left,
            film_upper_right)
        text_size_film_coord = cls.film_coord_to_corners(
            -1.0, -1.0 + (text_size * 0.01 * 2.0),
            film_lower_left,
            film_upper_right)
        text_font_size = text_size_film_coord[1] - pos_lower_left[1]
        if text_align_vertical == ALIGN_MIDDLE_VALUE:
            position_y += -text_font_size
        elif text_align_vertical == ALIGN_TOP_VALUE:
            position_y += -text_font_size * 2.0
        text_font_size = int(text_font_size)

        position = OpenMaya.MPoint(position_x, position_y)
        draw_color = OpenMaya.MColor((color[0], color[1], color[2], alpha))
        draw_manager.setColor(draw_color)
        draw_manager.setFontSize(text_font_size)
        draw_manager.setFontWeight(weight)
        draw_manager.setFontIncline(incline)
        draw_manager.setFontName(text_font_name)
        draw_manager.text2d(position, text, text_align_horizontal)
        return

    @classmethod
    def draw_field_3d_text(cls,
                           draw_manager,
                           obj_path, position,
                           text_size,
                           text_align,
                           text_bold,
                           text_italic,
                           text_font_name,
                           color, alpha,
                           text,
                           pos_lower_left, pos_lower_right,
                           pos_upper_left, pos_upper_right,
                           film_width, film_height,
                           film_lower_left, film_upper_right,
                           port_width, port_height):
        text_align_horizontal = \
            MAP_TEXT_ALIGN_TO_ALIGN_HORIZONTAL.get(text_align, 0)

        # Font properties
        weight = OpenMayaRender.MUIDrawManager.kWeightLight
        incline = OpenMayaRender.MUIDrawManager.kInclineNormal
        if text_bold:
            weight = OpenMayaRender.MUIDrawManager.kWeightBold
        if text_italic:
            incline = OpenMayaRender.MUIDrawManager.kInclineItalic

        # Convert position into world space.
        matrix_inverse = obj_path.inclusiveMatrixInverse()
        world_position = position * matrix_inverse

        # TODO: Support bottom or top aligned text for 3D
        # Text.
        text_size_film_coord = cls.film_coord_to_corners(
            -1.0, -1.0 + (text_size * 0.01 * 2.0),
            film_lower_left,
            film_upper_right)
        text_font_size = text_size_film_coord[1] - pos_lower_left[1]
        text_font_size = int(text_font_size)

        draw_color = OpenMaya.MColor((color[0], color[1], color[2], alpha))
        draw_manager.setColor(draw_color)
        draw_manager.setFontSize(text_font_size)
        draw_manager.setFontWeight(weight)
        draw_manager.setFontIncline(incline)
        draw_manager.setFontName(text_font_name)
        draw_manager.text(world_position, text, text_align_horizontal)
        return

    @classmethod
    def draw_field_2d_point(cls, draw_manager,
                            position, size,
                            color, alpha,
                            pos_lower_left, pos_lower_right,
                            pos_upper_left, pos_upper_right,
                            film_width, film_height,
                            film_lower_left, film_upper_right,
                            port_width, port_height):
        point_size_film_coord = cls.film_coord_to_corners(
            -1.0, -1.0 + (size * 0.01 * 2.0),
            film_lower_left,
            film_upper_right)
        point_size = point_size_film_coord[1] - pos_lower_left[1]

        position_x, position_y = cls.film_coord_to_corners(
            position.x, position.y,
            film_lower_left,
            film_upper_right)
        position = OpenMaya.MPoint(position_x, position_y)

        draw_color = OpenMaya.MColor((color[0], color[1], color[2], alpha))
        draw_manager.setColor(draw_color)
        draw_manager.setPointSize(point_size)
        draw_manager.point2d(position)
        return

    @classmethod
    def draw_field_3d_point(cls, draw_manager,
                            obj_path, position, size,
                            color, alpha,
                            pos_lower_left, pos_lower_right,
                            pos_upper_left, pos_upper_right,
                            film_width, film_height,
                            film_lower_left, film_upper_right,
                            port_width, port_height):
        point_size_film_coord = cls.film_coord_to_corners(
            -1.0, -1.0 + (size * 0.01 * 2.0),
            film_lower_left,
            film_upper_right)
        point_size = point_size_film_coord[1] - pos_lower_left[1]

        # Convert position into world space.
        matrix_inverse = obj_path.inclusiveMatrixInverse()
        world_position = position * matrix_inverse

        draw_color = OpenMaya.MColor((color[0], color[1], color[2], alpha))
        draw_manager.setColor(draw_color)
        draw_manager.setPointSize(point_size)
        draw_manager.point(world_position)
        return

    @classmethod
    def draw_field_2d_line(cls,
                           draw_manager,
                           pos_a, pos_b,
                           width, style,
                           color, alpha,
                           pos_lower_left, pos_lower_right,
                           pos_upper_left, pos_upper_right,
                           film_width, film_height,
                           film_lower_left, film_upper_right,
                           port_width, port_height):
        pos_a_x, pos_a_y = cls.film_coord_to_corners(
            pos_a.x, pos_a.y,
            film_lower_left,
            film_upper_right)
        pos_b_x, pos_b_y = cls.film_coord_to_corners(
            pos_b.x, pos_b.y,
            film_lower_left,
            film_upper_right)
        pos_a = OpenMaya.MPoint(pos_a_x, pos_a_y)
        pos_b = OpenMaya.MPoint(pos_b_x, pos_b_y)

        line_width_film_coord = cls.film_coord_to_corners(
            -1.0, -1.0 + (width * 0.01 * 2.0),
            film_lower_left,
            film_upper_right)
        line_width = line_width_film_coord[1] - pos_lower_left[1]

        draw_color = OpenMaya.MColor((color[0], color[1], color[2], alpha))
        draw_manager.setColor(draw_color)
        draw_manager.setLineStyle(style)
        draw_manager.setLineWidth(line_width)
        draw_manager.line2d(pos_a, pos_b)
        return

    @classmethod
    def draw_field_3d_line(cls,
                           draw_manager,
                           obj_path, pos_a, pos_b,
                           width, style,
                           color, alpha,
                           pos_lower_left, pos_lower_right,
                           pos_upper_left, pos_upper_right,
                           film_width, film_height,
                           film_lower_left, film_upper_right,
                           port_width, port_height):
        # Convert position into world space.
        matrix_inverse = obj_path.inclusiveMatrixInverse()
        world_pos_a = pos_a * matrix_inverse
        world_pos_b = pos_b * matrix_inverse

        line_width_film_coord = cls.film_coord_to_corners(
            -1.0, -1.0 + (width * 0.01 * 2.0),
            film_lower_left,
            film_upper_right)
        line_width = line_width_film_coord[1] - pos_lower_left[1]

        draw_color = OpenMaya.MColor((color[0], color[1], color[2], alpha))
        draw_manager.setColor(draw_color)
        draw_manager.setLineStyle(style)
        draw_manager.setLineWidth(line_width)
        draw_manager.line(world_pos_a, world_pos_b)
        return

    @classmethod
    def draw_field(cls,
                   draw_manager,
                   text_size_multiplier,
                   point_size_multiplier,
                   line_width_multiplier,
                   field_data,
                   field_general_values,
                   obj_path,
                   pos_lower_left, pos_lower_right,
                   pos_upper_left, pos_upper_right,
                   film_width, film_height,
                   film_lower_left, film_upper_right,
                   port_width, port_height):

        # Unpack the field data.
        enable, field_type, \
            pos_a, pos_b, \
            point_size, point_color, point_alpha, \
            line_width, line_style, line_color, line_alpha, \
            text_size, text_align, \
            text_bold, text_italic, text_font_name, \
            text_color, text_alpha, \
            text, \
            value_a, value_b, value_c, value_d = field_data

        if not enable:
            return

        if field_type == FIELD_TYPE_NONE_INDEX:
            return

        elif field_type == FIELD_TYPE_TEXT_2D_INDEX:
            draw_text = cls.format_text_data(
                text,
                field_general_values,
                value_a, value_b, value_c, value_d
            )
            cls.draw_field_2d_text(
                draw_manager,
                pos_a,
                text_size * text_size_multiplier,
                text_align,
                text_bold, text_italic, text_font_name,
                text_color, text_alpha,
                draw_text,
                pos_lower_left, pos_lower_right,
                pos_upper_left, pos_upper_right,
                film_width, film_height,
                film_lower_left, film_upper_right,
                port_width, port_height)

        elif field_type == FIELD_TYPE_TEXT_3D_INDEX:
            draw_text = cls.format_text_data(
                text,
                field_general_values,
                value_a, value_b, value_c, value_d
            )
            cls.draw_field_3d_text(
                draw_manager,
                obj_path, pos_a,
                text_size * text_size_multiplier,
                text_align,
                text_bold, text_italic, text_font_name,
                text_color, text_alpha,
                draw_text,
                pos_lower_left, pos_lower_right,
                pos_upper_left, pos_upper_right,
                film_width, film_height,
                film_lower_left, film_upper_right,
                port_width, port_height)

        elif field_type == FIELD_TYPE_POINT_2D_INDEX:
            cls.draw_field_2d_point(
                draw_manager,
                pos_a,
                point_size * point_size_multiplier,
                point_color, point_alpha,
                pos_lower_left, pos_lower_right,
                pos_upper_left, pos_upper_right,
                film_width, film_height,
                film_lower_left, film_upper_right,
                port_width, port_height)

        elif field_type == FIELD_TYPE_POINT_3D_INDEX:
            cls.draw_field_3d_point(
                draw_manager,
                obj_path, pos_a,
                point_size * point_size_multiplier,
                point_color, point_alpha,
                pos_lower_left, pos_lower_right,
                pos_upper_left, pos_upper_right,
                film_width, film_height,
                film_lower_left, film_upper_right,
                port_width, port_height)

        elif field_type == FIELD_TYPE_LINE_2D_INDEX:
            cls.draw_field_2d_line(
                draw_manager,
                pos_a, pos_b,
                line_width * line_width_multiplier,
                line_style,
                line_color, line_alpha,
                pos_lower_left, pos_lower_right,
                pos_upper_left, pos_upper_right,
                film_width, film_height,
                film_lower_left, film_upper_right,
                port_width, port_height)

        elif field_type == FIELD_TYPE_LINE_3D_INDEX:
            cls.draw_field_3d_line(
                draw_manager,
                obj_path, pos_a, pos_b,
                line_width * line_width_multiplier,
                line_style,
                line_color, line_alpha,
                pos_lower_left, pos_lower_right,
                pos_upper_left, pos_upper_right,
                film_width, film_height,
                film_lower_left, film_upper_right,
                port_width, port_height)

        else:
            msg = 'Field Type value is invalid; %r'
            raise ValueError(msg % field_type)
        return

    def addUIDrawables(self, obj_path, draw_manager, frame_context, data):
        user_data = data
        if not isinstance(user_data, HUDNodeData):
            return

        # Global size multipliers.
        text_size_multiplier = user_data.m_text_size
        point_size_multiplier = user_data.m_point_size
        line_width_multiplier = user_data.m_line_width

        # Get the camera.
        #
        # A valid camera is a camera that is above the current
        # transform node in the DAG hierachy. For example parent this
        # locator node under a camera, and the camera will display the
        # camera burn-ins.
        camera_path = frame_context.getCurrentCameraPath()
        camera_tfm_dag_path = camera_path.pop()
        valid_camera = False
        node_dag_path = obj_path
        while node_dag_path.length() > 0:
            if camera_tfm_dag_path == node_dag_path:
                valid_camera = True
                break
            node_dag_path = node_dag_path.pop()
        if valid_camera is False:
            return
        camera_fn = OpenMaya.MFnCamera(camera_path)

        matrix_type = OpenMayaRender.MFrameContext.kProjectionInverseMtx
        projection_inverse_matrix = frame_context.getMatrix(matrix_type)

        # Viewport origin is upper-left to bottom-right.
        _, _, port_width, port_height = frame_context.getViewportDimensions()
        film_width_px, film_height_px, \
        film_lower_left_px, film_upper_right_px = \
            self.get_film_coord_corners_in_pixels(
                camera_fn,
                port_width,
                port_height
            )

        film_width_screen, film_height_screen, \
        film_lower_left_screen, film_upper_right_screen = \
            self.get_film_coord_corners_in_screen(
                camera_fn,
                port_width,
                port_height
            )

        # Viewport Pixel corners
        lower_left_px = self.film_coord_to_corners(
            -1.0, -1.0,
            film_lower_left_px,
            film_upper_right_px)
        upper_left_px = self.film_coord_to_corners(
            -1.0, 1.0,
            film_lower_left_px,
            film_upper_right_px)
        lower_right_px = self.film_coord_to_corners(
            1.0, -1.0,
            film_lower_left_px,
            film_upper_right_px)
        upper_right_px = self.film_coord_to_corners(
            1.0, 1.0,
            film_lower_left_px,
            film_upper_right_px)

        # Screen Space Corners.
        lower_left_screen = self.film_coord_to_corners(
            -1.0, -1.0,
            film_lower_left_screen,
            film_upper_right_screen)
        upper_left_screen = self.film_coord_to_corners(
            -1.0, 1.0,
            film_lower_left_screen,
            film_upper_right_screen)
        lower_right_screen = self.film_coord_to_corners(
            1.0, -1.0,
            film_lower_left_screen,
            film_upper_right_screen)
        upper_right_screen = self.film_coord_to_corners(
            1.0, 1.0,
            film_lower_left_screen,
            film_upper_right_screen)

        # Generate array of field data, to unwraped and read in
        # self.draw_field.
        field_general_values = dict(user_data.m_field_general_values)
        fields_data = zip(
            user_data.m_field_enable,
            user_data.m_field_type,
            user_data.m_field_pos_a,
            user_data.m_field_pos_b,

            user_data.m_field_point_size,
            user_data.m_field_point_color,
            user_data.m_field_point_alpha,

            user_data.m_field_line_width,
            user_data.m_field_line_style,
            user_data.m_field_line_color,
            user_data.m_field_line_alpha,

            user_data.m_field_text_size,
            user_data.m_field_text_align,
            user_data.m_field_text_bold,
            user_data.m_field_text_italic,
            user_data.m_field_text_font_name,
            user_data.m_field_text_color,
            user_data.m_field_text_alpha,
            user_data.m_field_text_values,

            user_data.m_field_value_a,
            user_data.m_field_value_b,
            user_data.m_field_value_c,
            user_data.m_field_value_d,
        )

        # Draw Mask.
        mask_enable = user_data.m_mask_enable
        mask_draw_top = user_data.m_mask_enable_top
        mask_draw_bottom = user_data.m_mask_enable_bot
        if mask_enable and (mask_draw_top or mask_draw_bottom):
            draw_manager.beginDrawable()
            mask_color = user_data.m_mask_color
            mask_alpha = user_data.m_mask_alpha
            mask_aspect_ratio = user_data.m_mask_aspect_ratio
            self.draw_mask(
                draw_manager,
                mask_draw_top, mask_draw_bottom,
                mask_aspect_ratio,
                mask_color, mask_alpha,
                projection_inverse_matrix,
                lower_left_screen, lower_right_screen,
                upper_left_screen, upper_right_screen,
                film_width_screen, film_height_screen,
                film_lower_left_screen, film_upper_right_screen,
                port_width, port_height)
            draw_manager.endDrawable()

        # Draw Film Gate.
        film_gate_enable = user_data.m_film_gate_enable
        if film_gate_enable:
            draw_manager.beginDrawable()
            film_gate_color = user_data.m_film_gate_color
            film_gate_alpha = user_data.m_film_gate_alpha
            self.draw_film_gate(
                draw_manager,
                film_gate_color, film_gate_alpha,
                projection_inverse_matrix,
                lower_left_screen, lower_right_screen,
                upper_left_screen, upper_right_screen,
                film_width_screen, film_height_screen,
                film_lower_left_screen, film_upper_right_screen,
                port_width, port_height)
            draw_manager.endDrawable()

        # Draw fields.
        draw_manager.beginDrawable()
        for field_data in fields_data:
            self.draw_field(
                draw_manager,
                text_size_multiplier,
                point_size_multiplier,
                line_width_multiplier,
                field_data,
                field_general_values,
                obj_path,
                lower_left_px, lower_right_px,
                upper_left_px, upper_right_px,
                film_width_px, film_height_px,
                film_lower_left_px, film_upper_right_px,
                port_width, port_height)
        draw_manager.endDrawable()
        return


def initializePlugin(obj):
    """Called to load and allocate the new plug-in."""
    plugin = OpenMaya.MFnPlugin(obj, "David Cattermole", "0.1", "Any")
    try:
        plugin.registerNode(
            "dcCameraInferno",
            HUDNode.node_id,
            HUDNode.creator,
            HUDNode.initialize,
            OpenMaya.MPxNode.kLocatorNode,
            HUDNode.draw_db_classification)
    except:
        OpenMaya.MGlobal.displayError("Failed to register node")
        raise
    try:
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(
            HUDNode.draw_db_classification,
            HUDNode.draw_registrant_id,
            HUDNodeDrawOverride.creator
        )
    except:
        OpenMaya.MGlobal.displayError("Failed to register override")
        raise


def uninitializePlugin(obj):
    """Called to deallocate the plug-in."""
    plugin = OpenMaya.MFnPlugin(obj)
    try:
        plugin.deregisterNode(HUDNode.node_id)
    except:
        OpenMaya.MGlobal.displayError("Failed to deregister node")
    try:
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(
            HUDNode.draw_db_classification,
            HUDNode.draw_registrant_id
        )
    except:
        OpenMaya.MGlobal.displayError("Failed to deregister override")
