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

# File: src/utils/resources.py
# Author: Gabriel Moraes
# Date: October 2026

import sys
import os

def resource_path(relative_path):
    """ 
    Gets the absolute path to a resource.
    Works for development (dev) and for the PyInstaller executable (_MEIPASS).
    """
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)