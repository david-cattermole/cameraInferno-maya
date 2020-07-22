# Camera Inferno for Maya
Autodesk Maya Plug-in for visualising camera burn-in text.

The _Camera Inferno_ tool is a Maya Viewport 2.0 visualisation tool
for displaying helpful, dynamic information for pre-vis, post-vis and
tech-vis in Visual Effects.

The _Camera Inferno_ tool has the following features:

- Display Film Gate
- Display Mask for an aspect ratio
- Display Fields with configurable information.
- Unlimited number of fields to be displayed on the screen.
- Python-based formatting options for dynamic text display.
- Allows connections from Maya DAG/DG nodes into the text displays.
- Drawing straight lines, and dots in the viewport, in 2D or 3D space.

# Dynamic Text Keywords

This tool differs from other publicly available HUD tools because it
can display dynamic text information.
Dynamic text can be generated via Maya's DAG or DG node evaluation, or
using the internally provided keywords.
Finally it is possible to embed environment variables directly into the text.

The formatting for _Camera Inferno_ uses
[Python String Formatting Operations](https://docs.python.org/2.7/library/stdtypes.html#string-formatting-operations).
Please see the Python documentation for the small details of formatting strings.

The supported keywords are listed below.

## Scene Keywords

The scene details, such as file paths, and the current user name.

| Example Usage | Description                                                                | Type   | Unit |
| ------------- | ------------                                                               | ----   | ---- |
| `{user_name}` | User name currently logged in.                                             | String | N/A  |
| `{file_path}` | Full file path to the currently open Maya Scene file.                      | String | N/A  |
| `{file_name}` | Short file name (no file extension) to the currently open Maya Scene file. | String | N/A  |

## Date and Time Keywords

The current date and time, in various formats.

| Example Usage    | Description                                                | Type   | Unit |
| -------------    | ------------                                               | ----   | ---- |
| `{time}`         | Current time, as '9:42PM' format.                          | String | N/A  |
| `{date}`         | Current date, as 'Mon 03 Feb 2020' format.                 | String | N/A  |
| `{datetime}`     | Current date and time, as 'Mon 03 Feb 9:42PM 2020' format. | String | N/A  |
| `{time_iso}`     | Current time, as '21:42' format.                           | String | N/A  |
| `{date_iso}`     | Current date, as '2020-02-03' format.                      | String | N/A  |
| `{datetime_iso}` | Current date and time, as '2020-02-03 21:42' format.       | String | N/A  |
| `{date_year}`    | Current date year as #### number.                          | String | N/A  |
| `{date_month}`   | Current date month as ## number.                           | String | N/A  |
| `{date_day}`     | Current date day as ## number.                             | String | N/A  |
| `{time_hour}`    | Current time hour as 24 hour number.                       | String | N/A  |
| `{time_minute}`  | Current time minute as ## number.                          | String | N/A  |

## Camera Name Keywords

The name of the camera transform node name.

| Example Usage         | Description                     | Type   | Unit |
| -------------         | ------------                    | ----   | ---- |
| `{camera_short_name}` | Node name as short as possible. | String | N/A  |
| `{camera_long_name}`  | Node name as long as possible.  | String | N/A  |

## Frame / Time Keywords

Frame numbers and time related keywords.

| Example Usage         | Description           | Type    | Unit  |
| -------------         | ------------          | ----    | ----  |
| `{frame_integer:04d}` | Current frame number. | Integer | Frame |
| `{frame_float:.1f}`   | Current frame number. | Float   | Frame |

## Camera Attributes Keywords

Camera rotation and Shutter Angle keywords.
The rotation values are calculated in ZXY rotation order.

| Example Usage                  | Description                      | Type  | Unit   |
| -------------                  | ------------                     | ----  | ----   |
| `{camera_tilt:+.01f}°`         | Camera world-space tilt (X axis) | Float | Degree |
| `{camera_pan:+.01f}°`          | Camera world-space pan (Y axis)  | Float | Degree |
| `{camera_roll:+.01f}°`         | Camera world-space roll (Z axis) | Float | Degree |
| `{camera_shutter_angle:.02f}°` | Camera shutter angle             | Float | Degree |

## Camera Height Keywords

The camera's height with measurement unit. 

| Example Usage                 | Description              | Type  | Unit       |
| -------------                 | ------------             | ----  | ----       |
| `{camera_height:.01f}`        | Height of camera (units) | Float | Maya Unit  |
| `{camera_height_mm:.01f}`     | Height of camera (mm)    | Float | Millimeter |
| `{camera_height_cm:.01f}`     | Height of camera (cm)    | Float | Centimeter |
| `{camera_height_dm:.01f}`     | Height of camera (dm)    | Float | Decimeter  |
| `{camera_height_m:.01f}`      | Height of camera (m)     | Float | Meter      |
| `{camera_height_km:.01f}`     | Height of camera (km)    | Float | Kilometer  |
| `{camera_height_inches:.01f}` | Height of camera (in)    | Float | Inch       |
| `{camera_height_feet:.01f}`   | Height of camera (ft)    | Float | Foot       |
| `{camera_height_yards:.01f}`  | Height of camera (yd)    | Float | Yard       |
| `{camera_height_miles:.01f}`  | Height of camera (mi)    | Float | Mile       |

## Camera Speed Keywords

Measure the speed (velocity) of the camera transform node.
These keywords use the `dcCameraInferno` node's `cameraSpeedRaw` attribute.

The `cameraSpeedRaw` attribute expects values in the current Maya time
unit (usually seconds). This feature is expected to work with the
`dcVelocity` node type, and `outSpeedRaw` attribute.  

| Example Usage                             | Description                | Type  | Unit          |
| -------------                             | ------------               | ----  | ----          |
| `{camera_speed_kmph:.01f}`                | Speed of the camera (km/h) | Float | km/h          |
| `{camera_speed_km_per_hr:.01f}`           | Speed of the camera (km/h) | Float | km/h          |
| `{camera_speed_kilometers_per_hour:.01f}` | Speed of the camera (km/h) | Float | km/h          |
| `{camera_speed_mph:.01f}`                 | Speed of the camera (mph)  | Float | mph           |
| `{camera_speed_mi_per_hr:.01f}`           | Speed of the camera (mph)  | Float | mph           |
| `{camera_speed_miles_per_hour:.01f}`      | Speed of the camera (mph)  | Float | mph           |
| `{camera_speed_ft_per_hr:.01f}`           | Speed of the camera (ft/h) | Float | Feet/Hour     |
| `{camera_speed_feet_per_hour:.01f}`       | Speed of the camera (ft/h) | Float | Feet/Hour     |
| `{camera_speed_ft_per_sec:.01f}`          | Speed of the camera (ft/s) | Float | Feet/Second   |
| `{camera_speed_feet_per_second:.01f}`     | Speed of the camera (ft/s) | Float | Feet/Second   |
| `{camera_speed_m_per_hr:.01f}`            | Speed of the camera (m/h)  | Float | Meters/Hour   |
| `{camera_speed_meters_per_hour:.01f}`     | Speed of the camera (m/h)  | Float | Meters/Hour   |
| `{camera_speed_m_per_sec:.01f}`           | Speed of the camera (m/s)  | Float | Meters/Second |
| `{camera_speed_meters_per_second:.01f}`   | Speed of the camera (m/s)  | Float | Meters/Second |

## Camera Film Back Keywords

Film Back size keywords, with choice of measurement unit.

| Example Usage                     | Description             | Type  | Unit       |
| -------------                     | ------------            | ----  | ----       |
| `{film_back_width_inches:.2f}in`  | Camera film back width  | Float | Inch       |
| `{film_back_height_inches:.2f}in` | Camera film back height | Float | Inch       |
| `{film_back_width_mm:.2f}mm`      | Camera film back width  | Float | Millimeter |
| `{film_back_height_mm:.2f}mm`     | Camera film back height | Float | Millimeter |

## Lens Attributes Keywords

Lens attributes are available via keywords, and sometimes multiple 
different measurement units.

| Example Usage                       | Description                   | Type  | Unit       |
| -------------                       | ------------                  | ----  | ----       |
| `{lens_focal_length:.01f}mm`        | Lens focal length             | Float | Millimeter |
| `{lens_angle_of_view_x:.01f}°`      | Lens horizontal angle of view | Float | Degree     |
| `{lens_angle_of_view_y:.01f}°`      | Lens vertical angle of view   | Float | Degree     |
| `{lens_focus_distance:.01f}`        | Lens focus distance (units)   | Float | Maya Unit  |
| `{lens_focus_distance_mm:.01f}`     | Lens focus distance (mm)      | Float | Millimeter |
| `{lens_focus_distance_cm:.01f}`     | Lens focus distance (cm)      | Float | Centimeter |
| `{lens_focus_distance_dm:.01f}`     | Lens focus distance (dm)      | Float | Decimeter  |
| `{lens_focus_distance_m:.01f}`      | Lens focus distance (m)       | Float | Meter      |
| `{lens_focus_distance_km:.01f}`     | Lens focus distance (km)      | Float | Kilometer  |
| `{lens_focus_distance_feet:.01f}`   | Lens focus distance (ft)      | Float | Foot       |
| `{lens_focus_distance_yards:.01f}`  | Lens focus distance (yd)      | Float | Yard       |
| `{lens_focus_distance_inches:.01f}` | Lens focus distance (in)      | Float | Inch       |
| `{lens_focus_distance_miles:.01f}`  | Lens focus distance (mi)      | Float | Mile       |
| `{lens_f_stop:.01f}`                | Lens F-Stop number            | Float | 1/F Number |

## Unit Keywords

Unit keywords define a list of symbols/names for metric and imperial
measurement systems.

| Example Usage                | Description                     | Type   |
| -------------                | ------------                    | ----   |
| `{unit_mm}`                  | Millimeter unit name            | String |
| `{unit_millimeter}`          | Millimeter unit name            | String |
| `{unit_cm}`                  | Centimeter unit name            | String |
| `{unit_centimeter}`          | Centimeter unit name            | String |
| `{unit_m}`                   | Meter unit name                 | String |
| `{unit_meter}`               | Meter unit name                 | String |
| `{unit_dm}`                  | Decimeter unit name             | String |
| `{unit_decimeter}`           | Decimeter unit name             | String |
| `{unit_km}`                  | Kilometer unit name             | String |
| `{unit_kilometer}`           | Kilometer unit name             | String |
| `{unit_in}`                  | Inch unit name                  | String |
| `{unit_inch}`                | Inch unit name                  | String |
| `{unit_ft}`                  | Feet unit name                  | String |
| `{unit_feet}`                | Feet unit name                  | String |
| `{unit_mi}`                  | Miles unit name                 | String |
| `{unit_mile}`                | Miles unit name                 | String |
| `{unit_hour}`                | Hour unit name                  | String |
| `{unit_hr}`                  | Hour unit name                  | String |
| `{unit_second}`              | Second unit name                | String |
| `{unit_sec}`                 | Second unit name                | String |
| `{unit_kmph}`                | Kilometers per-second unit name | String |
| `{unit_km_per_hr}`           | Kilometers per-second unit name | String |
| `{unit_kilometers_per_hour}` | Kilometers per-second unit name | String |
| `{unit_mph}`                 | Miles per-second unit name      | String |
| `{unit_mi_per_hr}`           | Miles per-second unit name      | String |
| `{unit_miles_per_hour}`      | Miles per-second unit name      | String |
| `{unit_ft_per_hr}`           | Feet per-hour unit name         | String |
| `{unit_feet_per_hour}`       | Feet per-hour unit name         | String |
| `{unit_ft_per_sec}`          | Feet per-second unit name       | String |
| `{unit_feet_per_second}`     | Feet per-second unit name       | String |
| `{unit_m_per_hr}`            | Meters per-hour unit name       | String |
| `{unit_meters_per_hour}`     | Meters per-hour unit name       | String |
| `{unit_m_per_sec}`           | Meters per-second unit name     | String |
| `{unit_meters_per_second}`   | Meters per-second unit name     | String |
| `{scene_scale_unit}`         | Scene scale unit name           | String |
| `{scene_scale_factor}`       | Scene scale factor name         | Float  |

## Custom Values Keywords

| Example Usage  | Description                                    | Type            | Unit |
| -------------  | ------------                                   | ----            | ---- |
| `{a}` or `{0}` | Current field's value "A" DG evaluation value. | Float or String | N/A  |
| `{b}` or `{1}` | Current field's value "B" DG evaluation value. | Float or String | N/A  |
| `{c}` or `{2}` | Current field's value "C" DG evaluation value. | Float or String | N/A  |
| `{d}` or `{3}` | Current field's value "D" DG evaluation value. | Float or String | N/A  |

Each field attribute contains attributes `fieldValueA`, `..B`, `..C` and
`..D`. By connecting DG node attributes and using `{a}` in the
`field_text_value` attribute, you may add arbitrary values and display
them in the viewport. Any numeric (boolean, integer, float, double,
etc) or string data type can be connected and used.

## Environment Variable Keywords

After all keywords are substituted, any strings that appear as a 
(UNIX-style) environment variable will be replaced.

For example `$USER $PROJECT/$SHOT`, may become `David MyProject/001_0010`,
if environment variables are set up correctly.

This feature can be very helpful in a studio pipeline when environment
variables are automatically-available consistently.

# Usage

The scripts installed with Camera Inferno will allow you to create a
set up fairly easily.

Run the code below to create a new camera with the Camera Inferno HUD set up:

```python
import dcCameraInferno.tool as tool
tool.main()
```

If you wish to apply the Camera Inferno HUD to an existing camera,
first select a camera node and run the Python code above.

# Installation

The installation is basic and manual, simply copy the Python and MEL
files to your home directory's `maya` folder.

- Copy `./plug-ins/dcCameraInferno.py` into the directory `${HOME}/maya/<maya version>/plug-ins`.
- Copy `./plug-ins/dcVelocity.py` into the directory `${HOME}/maya/<maya version>/plug-ins`.
- Copy `./scripts/AEdcCameraInfernoTemplate.mel` into the directory `${HOME}/maya/<maya version>/scripts`.
- Copy `./python/dcCameraInferno` into the directory `${HOME}/maya/<maya version>/scripts`.

Both Windows and Linux are supported, and Maya 2017 and 2018 have been tested.

# Known Issues

- This is a Maya plug-in only, no configuration or friendly
  user-interface is provided; only the Maya Attribute Editor.
- The mask screen space depth cannot be changed, it is currently
  hard-coded to 1.0 units from camera.
  - To workaround this issue, you may scale the node under the camera
    to allow moving the physical mask closer than 1.0 unit from the
    camera.
- Maya versions below 2017 are not supported.
- Performance is not optimised.
- The use of the Maya camera's "Lens Squeeze Ratio" attribute may
  produce unexpected results of the film gate or film mask.

# Planned Features

- A graphical user interface with presets, and easy customisation.
- Ability to add static images to the burn-in, such as a logo.
- Ability to draw directly on-top of the image, rather than needing to
  worry about clipping planes or objects near/far from camera.
- Use Maya "Modules" to simplify installation of the scripts and plug-in.
