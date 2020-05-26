# Copyright (C) 2020, David Cattermole.
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
"""Calculate the Velocity of an input point.

This is a port of the C++ 'velocity' node to Maya Python API 2.0.
https://github.com/david-cattermole/velocity-maya
"""

import math

import maya.api.OpenMaya as OpenMaya

# Registered Node Id.
PLUGIN_NODE_ID = 0x0012F184
PLUGIN_NODE_NAME = "dcVelocity"
PLUGIN_NODE_AUTHOR_STRING = "David Cattermole"
PLUGIN_NODE_VERSION_STRING = "0.2"

# Time node constants.
TIME_NODE_NAME = "time1"
OUT_TIME_ATTR_NAME = "outTime"

# Display unit names.
DISPLAY_UNIT_KM_PER_HOUR_NAME = "km/h"
DISPLAY_UNIT_MILES_PER_HOUR_NAME = "mph"
DISPLAY_UNIT_METERS_PER_HOUR_NAME = "m/h"
DISPLAY_UNIT_METERS_PER_SECOND_NAME = "m/s"
DISPLAY_UNIT_FEET_PER_HOUR_NAME = "ft/h"
DISPLAY_UNIT_FEET_PER_SECOND_NAME = "ft/s"

# Display unit values.
DISPLAY_UNIT_KM_PER_HOUR_VALUE = 0
DISPLAY_UNIT_MILES_PER_HOUR_VALUE = 1
DISPLAY_UNIT_METERS_PER_HOUR_VALUE = 2
DISPLAY_UNIT_METERS_PER_SECOND_VALUE = 3
DISPLAY_UNIT_FEET_PER_HOUR_VALUE = 4
DISPLAY_UNIT_FEET_PER_SECOND_VALUE = 5

# Scene scale.
DISPLAY_UNITS = [
    (DISPLAY_UNIT_KM_PER_HOUR_NAME, DISPLAY_UNIT_KM_PER_HOUR_VALUE),
    (DISPLAY_UNIT_MILES_PER_HOUR_NAME, DISPLAY_UNIT_MILES_PER_HOUR_VALUE),
    (DISPLAY_UNIT_METERS_PER_HOUR_NAME, DISPLAY_UNIT_METERS_PER_HOUR_VALUE),
    (DISPLAY_UNIT_METERS_PER_SECOND_NAME, DISPLAY_UNIT_METERS_PER_SECOND_VALUE),
    (DISPLAY_UNIT_FEET_PER_HOUR_NAME, DISPLAY_UNIT_FEET_PER_HOUR_VALUE),
    (DISPLAY_UNIT_FEET_PER_SECOND_NAME, DISPLAY_UNIT_FEET_PER_SECOND_VALUE),
]

# Scene scale names.
UNIT_SCALE_MILLIMETER_NAME = "millimeter"
UNIT_SCALE_CENTIMETER_NAME = "centimeter"
UNIT_SCALE_METER_NAME = "meter"
UNIT_SCALE_DECIMETER_NAME = "decimeter"
UNIT_SCALE_KILOMETER_NAME = "kilometer"

# Scene scale values.
UNIT_SCALE_MILLIMETER_VALUE = 0
UNIT_SCALE_CENTIMETER_VALUE = 1
UNIT_SCALE_METER_VALUE = 2
UNIT_SCALE_DECIMETER_VALUE = 3
UNIT_SCALE_KILOMETER_VALUE = 4

# Scene scale.
UNIT_SCALES = [
    (UNIT_SCALE_MILLIMETER_NAME, UNIT_SCALE_MILLIMETER_VALUE),
    (UNIT_SCALE_CENTIMETER_NAME, UNIT_SCALE_CENTIMETER_VALUE),
    (UNIT_SCALE_METER_NAME, UNIT_SCALE_METER_VALUE),
    (UNIT_SCALE_DECIMETER_NAME, UNIT_SCALE_DECIMETER_VALUE),
    (UNIT_SCALE_KILOMETER_NAME, UNIT_SCALE_KILOMETER_VALUE)
]


def maya_useNewAPI():
    """With this function's existence, Maya knows to use API2 for loading."""
    pass


class VelocityNode(OpenMaya.MPxNode):
    node_id = OpenMaya.MTypeId(PLUGIN_NODE_ID)

    # Input Point
    m_input_point = None
    m_input_point_x = None
    m_input_point_y = None
    m_input_point_z = None

    # Time, Frame Rate and Scene Scale
    m_time = None
    m_time_interval = None
    m_frames_per_second = None
    m_text_precision = None
    m_unit_scale = None
    m_display_unit = None

    # Output
    m_out_speed = None
    m_out_speed_raw = None
    m_out_speed_text = None
    m_out_dummy_float = None
    m_out_dummy_string = None

    @staticmethod
    def creator():
        """Creates an instance of the node."""
        return VelocityNode()

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

        # Input Point X
        VelocityNode.m_input_point_x = nAttr.create(
            "inputPointX", "ipx",
            OpenMaya.MFnNumericData.kDouble, 0.0)
        nAttr.storable = True
        nAttr.keyable = True
        OpenMaya.MPxNode.addAttribute(VelocityNode.m_input_point_x)

        # Input Point Y
        VelocityNode.m_input_point_y = nAttr.create(
            "inputPointY", "ipy",
            OpenMaya.MFnNumericData.kDouble, 0.0)
        nAttr.storable = True
        nAttr.keyable = True
        OpenMaya.MPxNode.addAttribute(VelocityNode.m_input_point_y)

        # Input Point Z
        VelocityNode.m_input_point_z = nAttr.create(
            "inputPointZ", "ipz",
            OpenMaya.MFnNumericData.kDouble, 0.0)
        nAttr.storable = True
        nAttr.keyable = True
        OpenMaya.MPxNode.addAttribute(VelocityNode.m_input_point_z)

        # Input Point (parent of input Point* attributes)
        VelocityNode.m_input_point = nAttr.create(
            "inputPoint", "ip",
            VelocityNode.m_input_point_x,
            VelocityNode.m_input_point_y,
            VelocityNode.m_input_point_z)
        nAttr.storable = True
        nAttr.keyable = True
        OpenMaya.MPxNode.addAttribute(VelocityNode.m_input_point)

        # Time
        VelocityNode.m_time = uAttr.create(
            "time", "time",
            OpenMaya.MFnUnitAttribute.kTime, 0.0)
        OpenMaya.MPxNode.addAttribute(VelocityNode.m_time)

        # Time Interval
        VelocityNode.m_time_interval = uAttr.create(
            "timeInterval", "timeInterval",
            OpenMaya.MFnUnitAttribute.kTime, 1.0)
        OpenMaya.MPxNode.addAttribute(VelocityNode.m_time_interval)

        # Frames Per-Second
        VelocityNode.m_frames_per_second = nAttr.create(
            "framesPerSecond", "framesPerSecond",
            OpenMaya.MFnNumericData.kDouble, 24.0)
        nAttr.storable = True
        nAttr.keyable = True
        OpenMaya.MPxNode.addAttribute(VelocityNode.m_frames_per_second)

        # Text Precision
        VelocityNode.m_text_precision = nAttr.create(
            "textPrecision", "textPrecision",
            OpenMaya.MFnNumericData.kInt, 3)
        nAttr.storable = True
        nAttr.keyable = True
        OpenMaya.MPxNode.addAttribute(VelocityNode.m_text_precision)

        # Unit Scale
        VelocityNode.m_unit_scale = eAttr.create(
            "scale", "scale",
            UNIT_SCALE_DECIMETER_VALUE)
        for name, value in UNIT_SCALES:
            eAttr.addField(name, value)
        OpenMaya.MPxNode.addAttribute(VelocityNode.m_unit_scale)

        # Display Unit
        VelocityNode.m_display_unit = eAttr.create(
            "displayUnit", "displayUnit",
            DISPLAY_UNIT_KM_PER_HOUR_VALUE)
        for name, value in DISPLAY_UNITS:
            eAttr.addField(name, value)
        OpenMaya.MPxNode.addAttribute(VelocityNode.m_display_unit)

        # Out Speed
        VelocityNode.m_out_speed = nAttr.create(
                "outSpeed", "outSpeed",
                OpenMaya.MFnNumericData.kDouble, 0.0)
        nAttr.storable = False
        nAttr.keyable = False
        nAttr.readable = True
        nAttr.writable = False
        OpenMaya.MPxNode.addAttribute(VelocityNode.m_out_speed)

        # Out Speed
        VelocityNode.m_out_speed_raw = nAttr.create(
            "outSpeedRaw", "outSpeedRaw",
            OpenMaya.MFnNumericData.kDouble, 0.0)
        nAttr.storable = False
        nAttr.keyable = False
        nAttr.readable = True
        nAttr.writable = False
        OpenMaya.MPxNode.addAttribute(VelocityNode.m_out_speed_raw)

        # Out Speed Text
        string_data = OpenMaya.MFnStringData()
        string_obj = string_data.create()
        VelocityNode.m_out_speed_text = tAttr.create(
            "outSpeedText", "outSpeedText",
            OpenMaya.MFnData.kString, string_obj)
        tAttr.storable = False
        tAttr.keyable = False
        tAttr.readable = True
        tAttr.writable = False
        OpenMaya.MPxNode.addAttribute(VelocityNode.m_out_speed_text)

        # Out Dummy node
        #
        # The attribute is used to trigger this node to compute values.
        # The value itself is not set, it is only used to help trigger a
        # compute.
        VelocityNode.m_out_dummy_float = nAttr.create(
            "outDummyFloat", "outDummyNodeFloat",
            OpenMaya.MFnNumericData.kDouble, 0.0)
        nAttr.storable = False
        nAttr.keyable = False
        nAttr.readable = True
        nAttr.writable = False
        OpenMaya.MPxNode.addAttribute(VelocityNode.m_out_dummy_float)

        # Out Dummy String
        #
        # The attribute is used to trigger this node to compute values.
        # The value itself is not set, it is only used to help trigger a
        # compute.
        string_data = OpenMaya.MFnStringData()
        string_obj = string_data.create()
        VelocityNode.m_out_dummy_string = tAttr.create(
            "outDummyString", "outDummyString",
            OpenMaya.MFnData.kString, string_obj)
        tAttr.storable = False
        tAttr.keyable = False
        tAttr.readable = True
        tAttr.writable = False
        OpenMaya.MPxNode.addAttribute(VelocityNode.m_out_dummy_string)

        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_input_point, VelocityNode.m_out_speed)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_input_point, VelocityNode.m_out_speed_raw)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_input_point, VelocityNode.m_out_speed_text)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_input_point, VelocityNode.m_out_dummy_float)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_input_point, VelocityNode.m_out_dummy_string)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_time, VelocityNode.m_out_speed)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_time, VelocityNode.m_out_speed_raw)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_time, VelocityNode.m_out_speed_text)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_time, VelocityNode.m_out_dummy_float)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_time, VelocityNode.m_out_dummy_string)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_time_interval, VelocityNode.m_out_speed)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_time_interval, VelocityNode.m_out_speed_raw)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_time_interval, VelocityNode.m_out_speed_text)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_time_interval, VelocityNode.m_out_dummy_float)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_time_interval, VelocityNode.m_out_dummy_string)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_frames_per_second, VelocityNode.m_out_speed)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_frames_per_second, VelocityNode.m_out_speed_raw)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_frames_per_second, VelocityNode.m_out_speed_text)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_frames_per_second, VelocityNode.m_out_dummy_float)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_frames_per_second, VelocityNode.m_out_dummy_string)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_text_precision, VelocityNode.m_out_speed_text)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_text_precision, VelocityNode.m_out_dummy_string)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_unit_scale, VelocityNode.m_out_speed)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_unit_scale, VelocityNode.m_out_speed_raw)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_unit_scale, VelocityNode.m_out_speed_text)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_unit_scale, VelocityNode.m_out_dummy_float)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_unit_scale, VelocityNode.m_out_dummy_string)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_display_unit, VelocityNode.m_out_speed)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_display_unit, VelocityNode.m_out_speed_raw)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_display_unit, VelocityNode.m_out_speed_text)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_display_unit, VelocityNode.m_out_dummy_float)
        OpenMaya.MPxNode.attributeAffects(VelocityNode.m_display_unit, VelocityNode.m_out_dummy_string)
        return

    def __init__(self):
        super(VelocityNode, self).__init__()

    def compute(self, plug, data_block):
        """
        Perform the computation.
        """
        this_node = self.thisMObject()
        if ((plug == VelocityNode.m_out_speed)
                or (plug == VelocityNode.m_out_speed_text)
                or (plug == VelocityNode.m_out_dummy_float)
                or (plug == VelocityNode.m_out_dummy_string)):
            # Get the translate plug creating the MDataHandle with a DG context.
            point_plug = OpenMaya.MPlug(this_node, VelocityNode.m_input_point)

            # Get Data Handles
            time_handle = data_block.inputValue(VelocityNode.m_time)
            time_interval_handle = data_block.inputValue(VelocityNode.m_time_interval)
            fps_handle = data_block.inputValue(VelocityNode.m_frames_per_second)
            precision_handle = data_block.inputValue(VelocityNode.m_text_precision)
            point_now_handle = data_block.inputValue(VelocityNode.m_input_point)

            # Get value
            time = time_handle.asTime()
            time_interval = time_interval_handle.asTime()
            interval = time_interval.asUnits(OpenMaya.MTime.uiUnit()) * 2
            fps = fps_handle.asDouble()
            precision = precision_handle.asInt()
            point_now = point_now_handle.asVector()

            # Point at previous frame
            dg_context_prev = OpenMaya.MDGContext(time - time_interval)
            point_prev_handle = point_plug.asMDataHandle(dg_context_prev)
            point_prev = point_prev_handle.asVector()

            # Point at next frame
            dg_context_next = OpenMaya.MDGContext(time + time_interval)
            point_next_handle = point_plug.asMDataHandle(dg_context_next)
            point_next = point_next_handle.asVector()

            # Scene Scale
            scale_handle = data_block.inputValue(VelocityNode.m_unit_scale)
            scale_factor = 1.0
            scale_index = scale_handle.asShort()
            if scale_index == UNIT_SCALE_MILLIMETER_VALUE:
                scale_factor = 0.001
            elif scale_index == UNIT_SCALE_CENTIMETER_VALUE:
                scale_factor = 0.01
            elif scale_index == UNIT_SCALE_DECIMETER_VALUE:
                scale_factor = 0.1
            elif scale_index == UNIT_SCALE_METER_VALUE:
                scale_factor = 1.0
            elif scale_index == UNIT_SCALE_KILOMETER_VALUE:
                scale_factor = 1000.0

            # Display Unit
            display_unit_handle = data_block.inputValue(VelocityNode.m_display_unit)
            display_unit_str = ""
            display_unit_factor = 0.0
            display_unit = display_unit_handle.asShort()
            if display_unit == DISPLAY_UNIT_KM_PER_HOUR_VALUE:
                display_unit_factor = fps * 60 * 60 * 0.001
                display_unit_str = "km/h"
            elif display_unit == DISPLAY_UNIT_MILES_PER_HOUR_VALUE:
                display_unit_factor = fps * 60 * 60 * 0.000621371192
                display_unit_str = "mph"
            elif display_unit == DISPLAY_UNIT_METERS_PER_HOUR_VALUE:
                display_unit_factor = fps * 60 * 60
                display_unit_str = "m/h"
            elif display_unit == DISPLAY_UNIT_METERS_PER_SECOND_VALUE:
                display_unit_factor = fps
                display_unit_str = "m/s"
            elif display_unit == DISPLAY_UNIT_FEET_PER_HOUR_VALUE:
                display_unit_factor = fps * 60 * 60 * 3.28084
                display_unit_str = "ft/h"
            elif display_unit == DISPLAY_UNIT_FEET_PER_SECOND_VALUE:
                display_unit_factor = fps * 3.28084
                display_unit_str = "ft/s"

            # Distance
            dx = point_now[0] - point_prev[0]
            dy = point_now[1] - point_prev[1]
            dz = point_now[2] - point_prev[2]
            speed_raw = math.sqrt((dx * dx) + (dy * dy) + (dz * dz))
            dx = point_now[0] - point_next[0]
            dy = point_now[1] - point_next[1]
            dz = point_now[2] - point_next[2]
            speed_raw += math.sqrt((dx * dx) + (dy * dy) + (dz * dz))
            speed = (speed_raw * scale_factor * display_unit_factor) / interval
            speed_raw = speed_raw / interval

            # Output Speed
            out_speed_handle = data_block.outputValue(VelocityNode.m_out_speed)
            out_speed_handle.setDouble(speed)
            out_speed_handle.setClean()

            # Output Speed Raw
            out_speed_raw_handle = data_block.outputValue(VelocityNode.m_out_speed_raw)
            out_speed_raw_handle.setDouble(speed_raw)
            out_speed_raw_handle.setClean()

            # Output Speed String
            speed_str = "{:" + str(precision) + "} " + display_unit_str
            speed_str = speed_str.format(speed)
            out_text_handle = data_block.outputValue(VelocityNode.m_out_speed_text)
            out_text_handle.setString(speed_str)
            out_text_handle.setClean()

            # Output Dummy attributes
            out_dummy_float_handle = data_block.outputValue(VelocityNode.m_out_dummy_float)
            out_dummy_float_handle.setDouble(0.0)
            out_dummy_float_handle.setClean()

            # Output Speed String
            out_dummy_string_handle = data_block.outputValue(VelocityNode.m_out_dummy_string)
            out_dummy_string_handle.setString('')
            out_dummy_string_handle.setClean()

            data_block.setClean(plug)
        else:
            return None

    def postConstructor(self):
        """
        Called after the node is created.
        We are able to modify the DG in this method.

        Connect this node to time1.outTime, and set the FPS from the
        current scene's FPS value.
        """
        # Get Node
        OpenMaya.MPxNode.postConstructor(self)
        node_mobject = self.thisMObject()
        node_dependency_node = OpenMaya.MFnDependencyNode(node_mobject)

        # Get 'time1' Node
        selection = OpenMaya.MSelectionList().add(TIME_NODE_NAME)
        time_node = selection.getDependNode(0)
        time_dependency_node = OpenMaya.MFnDependencyNode(time_node)

        # Get the frame per-second value, based on the scene preferences.
        #
        # NOTE: 'OpenMaya.MTime.uiUnit' will look up the current UI
        # time values, then we convert 1 second into the UI time values.
        second_time_value = OpenMaya.MTime(1.0, OpenMaya.MTime.kSeconds)
        fps_value = second_time_value.asUnits(OpenMaya.MTime.uiUnit())

        # Get time attributes
        input_time_attr = node_dependency_node.attribute("time")
        output_time_attr = time_dependency_node.attribute(OUT_TIME_ATTR_NAME)

        # FPS attribute
        frame_rate_attr = node_dependency_node.attribute("framesPerSecond")
        frame_rate_plug = OpenMaya.MPlug(node_mobject, frame_rate_attr)

        dg_mod = OpenMaya.MDGModifier()
        # Connect to 'time1.outTime' to 'node_mobject.time' attribute.
        dg_mod.connect(time_node, output_time_attr,
                       node_mobject, input_time_attr)
        # Set the FPS from the scene preferences.
        dg_mod.newPlugValueDouble(frame_rate_plug, fps_value)
        dg_mod.doIt()
        return


def initializePlugin(obj):
    """Called to load and allocate the new plug-in."""
    plugin = OpenMaya.MFnPlugin(
        obj,
        PLUGIN_NODE_AUTHOR_STRING,
        PLUGIN_NODE_VERSION_STRING, "Any")
    try:
        plugin.registerNode(
            PLUGIN_NODE_NAME,
            VelocityNode.node_id,
            VelocityNode.creator,
            VelocityNode.initialize)
    except:
        OpenMaya.MGlobal.displayError("Failed to register node")
        raise
    return


def uninitializePlugin(obj):
    """Called to deallocate the plug-in."""
    plugin = OpenMaya.MFnPlugin(obj)
    try:
        plugin.deregisterNode(VelocityNode.node_id)
    except:
        OpenMaya.MGlobal.displayError("Failed to deregister node")
