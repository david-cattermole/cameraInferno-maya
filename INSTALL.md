# Download

***Camera Inferno*** is available for the following
platforms and can be downloaded from the
[Releases](https://github.com/david-cattermole/cameraInferno-maya/releases)
page on the GitHub [project page](https://github.com/david-cattermole/cameraInferno-maya).

Download the archive format (`.zip` or `.tar.gz`) for your Maya
version and operating system.

For a simple installation, **do not** install from the
`Source code (zip)` or `Source code (tar.gz)` archives. These archives
are for developers only.

# Install Maya Module

***Camera Inferno*** can be installed by un-zipping the archive
(`.zip` or `.tar.gz`) file, and copying the contents into the
following directory on your computer:

On Windows:
```
C:\Users\<Your User Name>\My Documents\maya\<Maya Version>\modules
```

On Linux:
```
~/maya/<Maya Version>/modules
```

On MacOS:
```
~/Library/Preferences/Autodesk/maya/<Maya Version>/modules
```

Note: The MacOS Finder App hides the "Library" folder. To open the
Maya preferences folder, open Finder, and use the menu `Go > Go to
Folder...`, then type `~/Library/Preferences/Autodesk/maya` and press
"Go".

You may need to create the *modules* directory manually, as it is not
created default by Maya.

You should now have one file and one directory like this:
```
<maya user directory>\2017\modules\cameraInferno-0.1.0-mayaAll-allOS.mod (module file)
<maya user directory>\2017\modules\cameraInferno-0.1.0-mayaAll-allOS (directory)
```

You can open Maya as normal and the tool will be recognised
automatically at start-up.  You will see a message in the Script
Editor `# root : MM Solver Startup... #`, and a new shelf will
automatically be created for you named *dcCameraInferno*.

***Note:*** Please remove the `<module root>/python_qt` directory, if
`Qt.py` is already installed, see the above note
*Install Qt.py (in a Professional Environment)*.

# Manual Installation

The installation is basic and manual, simply copy the Python and MEL
files to your home directory's `maya` folder.

- Copy `./plug-ins/dcCameraInferno.py` into the directory `${HOME}/maya/<maya version>/plug-ins`.
- Copy `./plug-ins/dcVelocity.py` into the directory `${HOME}/maya/<maya version>/plug-ins`.
- Copy `./scripts/AEdcCameraInfernoTemplate.mel` into the directory `${HOME}/maya/<maya version>/scripts`.
- Copy `./python/dcCameraInferno` into the directory `${HOME}/maya/<maya version>/scripts`.

Both Windows and Linux are supported, and Maya 2017 and 2018 have been tested.

