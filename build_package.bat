@ECHO OFF
SETLOCAL
::
:: Copyright (C) 2021 David Cattermole.
::
:: This file is part of dcCameraInferno.
::
:: dcCameraInferno is free software: you can redistribute it and/or modify it
:: under the terms of the GNU Lesser General Public License as
:: published by the Free Software Foundation, either version 3 of the
:: License, or (at your option) any later version.
::
:: dcCameraInferno is distributed in the hope that it will be useful,
:: but WITHOUT ANY WARRANTY; without even the implied warranty of
:: MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
:: GNU Lesser General Public License for more details.
::
:: You should have received a copy of the GNU Lesser General Public License
:: along with dcCameraInferno.  If not, see <https://www.gnu.org/licenses/>.
:: ---------------------------------------------------------------------
::
:: Builds the Camera Inferno project.

:: Where to install the module?
::
:: Note: In Windows 8 and 10, "My Documents" is no longer visible,
::       however files copying to "My Documents" automatically go
::       to the "Documents" directory.
::
:: The "$HOME/maya/2022/modules" directory is automatically searched
:: for Maya module (.mod) files. Therefore we can install directly.
::
:: SET INSTALL_MODULE_DIR="%PROJECT_ROOT%\modules"
SET INSTALL_MODULE_DIR="%USERPROFILE%\My Documents\maya\2022\modules"

:: Do not edit below, unless you know what you're doing.
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: Clear all build information before re-compiling.
:: Turn this off when wanting to make small changes and recompile.
SET FRESH_BUILD=1

:: Build ZIP Package.
SET BUILD_PACKAGE=1

:: To Generate a Visual Studio 'Solution' file, change the '0' to a '1'.
SET GENERATE_SOLUTION=0

:: The root of this project.
SET PROJECT_ROOT=%CD%
ECHO Project Root: %PROJECT_ROOT%

:: Build plugin
MKDIR build_windows64
CHDIR build_windows64
IF "%FRESH_BUILD%"=="1" (
    DEL /S /Q *
    FOR /D %%G in ("*") DO RMDIR /S /Q "%%~nxG"
)

IF "%GENERATE_SOLUTION%"=="1" (

REM To Generate a Visual Studio 'Solution' file
    cmake -G "Visual Studio 14 2015 Win64" -T "v140" ^
        -DCMAKE_INSTALL_PREFIX=%INSTALL_MODULE_DIR% ^
        ..

) ELSE (

    cmake -G "NMake Makefiles" ^
        -DCMAKE_INSTALL_PREFIX=%INSTALL_MODULE_DIR% ^
        ..

    nmake /F Makefile clean
    nmake /F Makefile all

REM Comment this line out to stop the automatic install into the home directory.
    nmake /F Makefile install

REM Create a .zip package.
IF "%BUILD_PACKAGE%"=="1" (
       nmake /F Makefile package
   )

)

:: Return back to project root directory.
CHDIR "%PROJECT_ROOT%"
