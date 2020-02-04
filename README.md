# cameraInferno-maya
Autodesk Maya Plug-in for visualising camera burn-in text.

The _Camera Inferno_ tool is a Maya Viewport 2.0 visualisation tool for
displaying helpful, dynamic information for pre-vis, post-vis and
tech-vis in Visual Effects.

The _Camera Inferno_ tool has the following features:

- Display Film Gate
- Display Mask for an aspect ratio
- Display Fields with configurable information.
- Unlimited number of fields to be displayed on the screen.
- Python-based formatting options for dynamic text display.
- Allows connections from Maya DAG/DG nodes into the text displays.
- Drawing straight lines, and dots in the viewport, in 2D or 3D space.

# Dynamic Text

This tool differs from others because we can display dynamic text information.
Dynamic text can be generated via Maya's DAG or DG node evaluation, or
using the internally provided keywords.
Finally it is possible to embed environment variables directly into the text.

The formatting for _Camera Inferno_ uses
[Python String Formatting Operations](https://docs.python.org/2.7/library/stdtypes.html#string-formatting-operations).
Please see the Python documentation for the small details of formatting strings.

| Keyword Name              | Example Usage                     | Description                                                | Type            | Unit       |
| -------------             | -------------                     | ------------                                               | ----            | ----       |
| `a` or index 0            | `{a}` or `{0}`                    | Current field's value "A" DG evaluation value.             | Float or String | N/A        |
| `b` or index 1            | `{b}` or `{1}`                    | Current field's value "B" DG evaluation value.             | Float or String | N/A        |
| `c` or index 2            | `{c}` or `{2}`                    | Current field's value "C" DG evaluation value.             | Float or String | N/A        |
| `d` or index 3            | `{d}` or `{3}`                    | Current field's value "D" DG evaluation value.             | Float or String | N/A        |
| `user_name`               | `{user_name}`                     | User name currently logged in.                             | String          | N/A        |
| `file_path`               | `{file_path}`                     | Full file path to the currently open Maya Scene file.      | String          | N/A        |
| `file_name`               | `{file_name}`                     | Short file name to the currently open Maya Scene file.     | String          | N/A        |
| `time`                    | `{time}`                          | Current time, as '9:42PM' format.                          | String          | N/A        |
| `date`                    | `{date}`                          | Current date, as 'Mon 03 Feb 2020' format.                 | String          | N/A        |
| `datetime`                | `{datetime}`                      | Current date and time, as 'Mon 03 Feb 9:42PM 2020' format. | String          | N/A        |
| `time_iso`                | `{time_iso}`                      | Current time, as '21:42' format.                           | String          | N/A        |
| `date_iso`                | `{date_iso}`                      | Current date, as '2020-02-03' format.                      | String          | N/A        |
| `datetime_iso`            | `{datetime_iso}`                  | Current date and time, as '2020-02-03 21:42' format.       | String          | N/A        |
| `camera_short_name`       | `{camera_short_name}`             | Name of the camera transform node, as short as possible.   | String          | N/A        |
| `camera_long_name`        | `{camera_long_name}`              | Name of the camera transform node, as long as possible.    | String          | N/A        |
| `frame_integer`           | `{frame_integer:04d}`             | Current frame number.                                      | Integer         | Frame      |
| `frame_float`             | `{frame_float:.1f}`               | Current frame number.                                      | Float           | Frame      |
| `film_back_width_inches`  | `{film_back_width_mm:.2f} in`     | Camera film back width                                     | Float           | Inch       |
| `film_back_height_inches` | `{film_back_height_mm:.2f} in`    | Camera film back height                                    | Float           | Inch       |
| `film_back_width_mm`      | `{film_back_width_mm:.2f} mm`     | Camera film back width                                     | Float           | Millimeter |
| `film_back_height_mm`     | `{film_back_height_mm:.2f} mm`    | Camera film back height                                    | Float           | Millimeter |
| `camera_tilt`             | `{camera_tilt:+.01f} deg`         | Camera world-space tilt (X axis in ZXY rotation order)     | Float           | Degree     |
| `camera_pan`              | `{camera_pan:+.01f} deg`          | Camera world-space pan (Y axis in ZXY rotation order)      | Float           | Degree     |
| `camera_roll`             | `{camera_roll:+.01f} deg`         | Camera world-space roll (Z axis in ZXY rotation order)     | Float           | Degree     |
| `camera_shutter_angle`    | `{camera_shutter_angle:.02f} deg` | Camera shutter angle                                       | Float           | Degree     |
| `lens_focal_length`       | `{lens_focal_length:.01f} mm`     | Lens focal length                                          | Float           | Millimeter |
| `lens_focus_distance`     | `{lens_focus_distance:.01f}`      | Lens focus distance                                        | Float           | Maya Unit  |
| `lens_f_stop`             | `{lens_f_stop:.01f}`              | Lens F-Stop number                                         | Float           | 1/F Number |
| `lens_angle_of_view_x`    | `{lens_angle_of_view_x:.01f}`     | Lens horizontal angle of view                              | Float           | Degree     |
| `lens_angle_of_view_y`    | `{lens_angle_of_view_y:.01f}`     | Lens vertical angle of view                                | Float           | Degree     |

Each field attribute contains attributes `fieldValueA`, `..B`, `..C` and
`..D`. By connecting DG node attributes and using `{a}` in the
`field_text_value` attribute, you may add arbitrary values and display
them in the viewport. Any numeric (boolean, integer, float, double,
etc) or string data type can be connected and used.

Additionally, after keywords are substituted, any strings that appear
as a (UNIX-style) environment variable will be replaced.
For example `$USER $PROJECT/$SHOT`, may become `David MyProject/001_0010`,
if environment variables are set up correctly.

# Usage

The current usage is very bare, simply create the node under a camera
transform, and configure the node as desired. Below is an example set up.

```python
import maya.cmds

maya.cmds.loadPlugin("dcCameraInferno", quiet=False)
sel = maya.cmds.ls(selection=True, long=True, type="transform") or []
tfm = maya.cmds.createNode("transform", name="cameraInferno1", parent=sel[0])
node = maya.cmds.createNode("dcCameraInferno", parent=tfm)
maya.cmds.setAttr(tfm + ".template", 1)
maya.cmds.setAttr(node + ".maskAspectRatio", 1.7777)
maya.cmds.select(node, replace=True)
```

# Known Issues

- This is a Maya plug-in only, no configuration or friendly
  user-interface is provided; only the Maya Attribute Editor.
- The mask screen space depth cannot be changed, it is currently
  hard-coded to 1.0 units from camera.
- Maya versions below 2017 are not supported.
- Performance is not optimised.
- The use of the Maya camera's "Lens Squeeze Ratio" attribute may
  produce unexpected results.

# Installation

The installation is basic and manual, simply copy the Python and MEL
files to your home directory's `maya` folder.

- Copy `./plug-ins/dcCameraInferno.py` into the `${HOME}/maya/<maya version>/plug-ins`.
- Copy `./scripts/AEdcCameraInfernoTemplate.mel` into the `${HOME}/maya/<maya version>/scripts`.

Both Windows and Linux are supported, and Maya 2017 and 2018 have been tested.
