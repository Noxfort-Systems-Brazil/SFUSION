# SFUSION (SYNAPSE Fusion) Mapper - "Day Zero" ETL Configuration Tool
# Copyright (C) 2026 Gabriel Moraes - Noxfort Systems
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

# File: src/slm/neuro_symbolic_resolver.py
# Author: Gabriel Moraes
# Date: June 2026
# Description:
#    Traffic Physics Neuro-Symbolic Resolver.
#    Applies heuristic validation, disambiguation, and unit of measurement inference
#    to build validated KinematicMap instances.

import logging
from typing import Dict, List, Optional
from src.core.schemas import KinematicMap

logger = logging.getLogger(__name__)


class NeuroSymbolicResolver:
    """
    Validates and enriches raw schema mappings extracted from the SLM.
    Enforces deterministic traffic physics rules and unit inference.
    """

    SPEED_CANDIDATES = [
        'estimated_speed_kmh', 'speed', 'jams.speed', 'currentspeed',
        'flowsegmentdata.currentspeed', 'speed_kmh', 'currentspeed_kmh',
        'speedkmh', 'velocity', 'velocidade', 'v'
    ]

    FLOW_CANDIDATES = [
        'flow', 'flow_rate', 'volume', 'vehicle_count', 'count', 'q', 'nvehcontrib'
    ]

    INTENSITY_CANDIDATES = [
        'density', 'jam_level', 'congestion_level', 'intensity', 'level', 'k'
    ]

    OCCUPANCY_CANDIDATES = [
        'occupancy_ms', 'occupancy_pct', 'occupancy', 'occ'
    ]

    @classmethod
    def infer_speed_unit(cls, speed_col: Optional[str], raw_unit: Optional[str]) -> str:
        """Infers normalized speed unit (km/h, m/s, mph)."""
        if raw_unit:
            u = raw_unit.lower().strip()
            if "mph" in u: return "mph"
            if "m/s" in u or "mps" in u: return "m/s"
            if "km" in u: return "km/h"
        if speed_col:
            col_l = speed_col.lower()
            if "mph" in col_l: return "mph"
            if "_mps" in col_l or "m_s" in col_l: return "m/s"
            if "kmh" in col_l or "km_h" in col_l or "kmph" in col_l: return "km/h"
        return "km/h"

    @classmethod
    def infer_occupancy_unit(cls, occ_col: Optional[str], raw_unit: Optional[str]) -> Optional[str]:
        """Infers occupancy unit (ms, s, pct)."""
        if raw_unit:
            u = raw_unit.lower().strip()
            if "ms" in u or "milli" in u: return "ms"
            if "pct" in u or "%" in u or "percent" in u: return "pct"
            if "s" in u or "sec" in u: return "s"
        if occ_col:
            col_l = occ_col.lower()
            if "ms" in col_l or "milli" in col_l: return "ms"
            if "pct" in col_l or "percent" in col_l or "%" in col_l: return "pct"
            if "sec" in col_l or "_s" in col_l: return "s"
        return None

    @classmethod
    def infer_distance_unit(cls, dist_col: Optional[str], raw_unit: Optional[str]) -> Optional[str]:
        """Infers distance unit (m, km, miles)."""
        if raw_unit:
            u = raw_unit.lower().strip()
            if "mile" in u: return "miles"
            if "km" in u: return "km"
            if "m" in u: return "m"
        if dist_col:
            col_l = dist_col.lower()
            if "mile" in col_l: return "miles"
            if "km" in col_l or "kilometer" in col_l: return "km"
            if "meter" in col_l or "_m" in col_l: return "m"
        return None

    @classmethod
    def infer_time_unit(cls, time_col: Optional[str], raw_unit: Optional[str]) -> Optional[str]:
        """Infers time unit (s, ms, min, hours)."""
        if raw_unit:
            u = raw_unit.lower().strip()
            if "ms" in u or "milli" in u: return "ms"
            if "hour" in u or "h" in u: return "hours"
            if "min" in u: return "min"
            if "s" in u or "sec" in u: return "s"
        if time_col:
            col_l = time_col.lower()
            if "ms" in col_l or "millis" in col_l: return "ms"
            if "hour" in col_l or "_h" in col_l: return "hours"
            if "min" in col_l: return "min"
            if "sec" in col_l or "_s" in col_l: return "s"
        return None

    @classmethod
    def resolve_schema(
        cls,
        raw_schema_data: Dict[str, str],
        available_keys: List[str],
        assoc_type: str = "LOCAL"
    ) -> KinematicMap:
        """
        Applies neuro-symbolic heuristics to disambiguate and complete kinematic mappings and units.
        """
        data = dict(raw_schema_data)

        # 1. SPEED DISAMBIGUATION & FALLBACK
        if data.get("speed_col") in [None, "jams.speedKMH", "speedKMH"]:
            if "jams.speed" in available_keys or "speed" in available_keys:
                target_key = "jams.speed" if "jams.speed" in available_keys else "speed"
                data["speed_col"] = target_key
                logger.info(f"NeuroSymbolicResolver: Prioritized measured speed -> {target_key}")

        if not data.get("speed_col"):
            for cand in cls.SPEED_CANDIDATES:
                matched = next((k for k in available_keys if k.lower() == cand or k.lower().endswith('.' + cand)), None)
                if matched:
                    data['speed_col'] = matched
                    logger.info(f"NeuroSymbolicResolver: Resolved speed_col -> {matched}")
                    break

        # 2. LOCAL SENSOR FLOW & DENSITY/OCCUPANCY RESOLUTION
        if assoc_type.upper() == "LOCAL":
            if not data.get("flow_col"):
                for cand in cls.FLOW_CANDIDATES:
                    matched = next((k for k in available_keys if k.lower() == cand or k.lower().endswith('.' + cand)), None)
                    if matched:
                        data['flow_col'] = matched
                        logger.info(f"NeuroSymbolicResolver: Resolved flow_col -> {matched}")
                        break

            if not data.get("intensity_col") and not data.get("occupancy_col"):
                for cand in cls.INTENSITY_CANDIDATES:
                    matched = next((k for k in available_keys if k.lower() == cand or k.lower().endswith('.' + cand)), None)
                    if matched:
                        data['intensity_col'] = matched
                        logger.info(f"NeuroSymbolicResolver: Resolved intensity_col -> {matched}")
                        break

                if not data.get("intensity_col"):
                    for cand in cls.OCCUPANCY_CANDIDATES:
                        matched = next((k for k in available_keys if k.lower() == cand or k.lower().endswith('.' + cand)), None)
                        if matched:
                            data['occupancy_col'] = matched
                            logger.info(f"NeuroSymbolicResolver: Resolved occupancy_col -> {matched}")
                            break
        else:
            # Enforce null constraints for GLOBAL sensors
            data["flow_col"] = None
            data["intensity_col"] = None
            data["distance_col"] = None
            data["time_col"] = None
            data["occupancy_col"] = None

        # 3. UNIT OF MEASUREMENT INFERENCE & NORMALIZATION
        speed_unit = cls.infer_speed_unit(data.get("speed_col"), data.get("speed_unit"))
        occupancy_unit = cls.infer_occupancy_unit(data.get("occupancy_col"), data.get("occupancy_unit"))
        distance_unit = cls.infer_distance_unit(data.get("distance_col"), data.get("distance_unit"))
        time_unit = cls.infer_time_unit(data.get("time_col"), data.get("time_unit"))

        return KinematicMap(
            speed_col=data.get("speed_col"),
            flow_col=data.get("flow_col"),
            intensity_col=data.get("intensity_col"),
            distance_col=data.get("distance_col"),
            time_col=data.get("time_col"),
            occupancy_col=data.get("occupancy_col"),
            speed_unit=speed_unit,
            occupancy_unit=occupancy_unit,
            distance_unit=distance_unit,
            time_unit=time_unit,
            confidence_score=0.99
        )
