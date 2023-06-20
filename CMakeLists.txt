# Copyright (C) 2021 David Cattermole.
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
# ---------------------------------------------------------------------
#
# Maya MatchMoveSolver build script.
#
cmake_minimum_required(VERSION 3.0)

# Project configuration.
project(cameraInferno)
set(PROJECT_VERSION_MAJOR 0)
set(PROJECT_VERSION_MINOR 4)
set(PROJECT_VERSION_PATCH 1)
set(PROJECT_VERSION "${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}.${PROJECT_VERSION_PATCH}")
set(PROJECT_HOMEPAGE_URL "https://github.com/david-cattermole/cameraInferno-maya")
set(PROJECT_DESCRIPTION "Autodesk Maya Plug-in for visualising camera burn-in text.")
set(PROJECT_AUTHOR "David Cattermole")
set(PROJECT_COPYRIGHT "2019, 2020, 2021, David Cattermole.")

add_subdirectory(modules)
add_subdirectory(plug-ins)
add_subdirectory(python)
add_subdirectory(scripts)
add_subdirectory(presets)

# Install misc files
#
# NOTE: ${MODULE_FULL_NAME} comes from 'modules' sub-directory.
install(FILES
  ${CMAKE_CURRENT_SOURCE_DIR}/LICENSE
  ${CMAKE_CURRENT_SOURCE_DIR}/INSTALL.md
  ${CMAKE_CURRENT_SOURCE_DIR}/README.md
  DESTINATION "${MODULE_FULL_NAME}/")

# Package Configuration.
set(CPACK_PACKAGE_NAME "${PROJECT_NAME}")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "${PROJECT_DESCRIPTION}")
set(CPACK_PACKAGE_VENDOR "${PROJECT_AUTHOR}")
set(CPACK_PACKAGE_CONTACT "cattermole91@gmail.com")
set(CPACK_PACKAGE_DESCRIPTION_FILE "${CMAKE_CURRENT_SOURCE_DIR}/README.md")
set(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/LICENSE")
set(CPACK_PACKAGE_VERSION_MAJOR "${PROJECT_VERSION_MAJOR}")
set(CPACK_PACKAGE_VERSION_MINOR "${PROJECT_VERSION_MINOR}")
set(CPACK_PACKAGE_VERSION_PATCH "${PROJECT_VERSION_PATCH}")
set(CPACK_PACKAGE_FILE_NAME "${MODULE_FULL_NAME}")
set(CPACK_INCLUDE_TOPLEVEL_DIRECTORY 1)
# Put the packages into the source directory, so that when we run
# another build, it's not removed as part of the clean up.
SET(CPACK_OUTPUT_FILE_PREFIX "${CMAKE_CURRENT_SOURCE_DIR}/packages")
# Use ZIP. ZIP files are common enough on all major platforms.
set(CPACK_GENERATOR "ZIP")

# Use CPack (part of CMake) to generate the packages...  If 'CPack' is
# not included, the 'packages' target will not be generated.
include(CPack)
