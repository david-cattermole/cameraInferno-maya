#!/usr/bin/env bash
#
# Copyright (C) 2021 David Cattermole.
#
# This file is part of mmSolver.
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
# ---------------------------------------------------------------------
#
# Builds the Camera Inferno Solver project.

# Where to install the module?
#
# The "$HOME/maya/2020/modules" directory is automatically searched
# for Maya module (.mod) files. Therefore we can install directly.
#
INSTALL_MODULE_DIR=${HOME}/maya/2020/modules

# Do not edit below, unless you know what you're doing.
###############################################################################

# Clear all build information before re-compiling.
# Turn this off when wanting to make small changes and recompile.
FRESH_BUILD=1

# Build ZIP Package.
BUILD_PACKAGE=1

# Store the current working directory, to return to.
CWD=`pwd`

# Path to this script.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# The root of this project.
PROJECT_ROOT=`readlink -f ${DIR}/..`

# Build mmSolver project
mkdir -p build_unix
cd build_unix
if [ ${FRESH_BUILD} -eq 1 ]; then
    rm --force -R *
fi
cmake -DCMAKE_INSTALL_PREFIX=${INSTALL_MODULE_DIR} ..
make clean
make
make install

# Build ZIP package.
if [ ${BUILD_PACKAGE} -eq 1 ]; then
    make package
fi

# Return back to project root directory.
cd ${CWD}
