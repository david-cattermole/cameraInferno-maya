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
# Configure and install Python scripts.
#

# Install Python API and tools
install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/"
        DESTINATION "${MODULE_FULL_NAME}/plug-ins"
        FILES_MATCHING PATTERN "*.py")
