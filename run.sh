#!/bin/bash
# SFUSION (Smart Fusion) is an open-source visual data engineering platform for kinematic normalization and telemetry fusion.
# SPDX-FileCopyrightText: 2026 Noxfort Systems <dev@noxfort.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# File: run.sh
# Author: Gabriel Moraes
# Date: October 2026

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment (.venv or venv)
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Error: Virtual environment (.venv or venv) not found in directory $SCRIPT_DIR"
    exit 1
fi

# Execute python script forwarding any arguments
python sfusion.py "$@"
