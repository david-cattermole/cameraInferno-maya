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
# Configure the Maya module file.

# Module names
set(MODULE_NAME "${PROJECT_NAME}-${PROJECT_VERSION}")
set(MODULE_FULL_NAME "${MODULE_NAME}")
set(MODULE_BUILD_DIR "${CMAKE_BINARY_DIR}/${MODULE_FULL_NAME}")

# Create Module Description file.
configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/cameraInferno.mod
  ${CMAKE_BINARY_DIR}/${MODULE_FULL_NAME}.mod
  @ONLY)

# Install the Module Description file.
install(FILES
        "${CMAKE_BINARY_DIR}/${MODULE_FULL_NAME}.mod"
        DESTINATION "./")

# Set variables in parent scope (directory above).
set(MODULE_NAME "${MODULE_NAME}" PARENT_SCOPE)
set(MODULE_FULL_NAME "${MODULE_FULL_NAME}" PARENT_SCOPE)
set(MODULE_BUILD_DIR "${MODULE_BUILD_DIR}" PARENT_SCOPE)
