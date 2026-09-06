# SFusion (SYNAPSE Fusion) Mapper - "Day Zero" ETL Configuration Tool
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

# File: src/etl/sensor_processor.py
# Author: Gabriel Moraes
# Date: June 2026
# Description:
#    Sensor Batch Processor.
#    Handles physical file I/O, binary hashing, zlib compression,
#    universal event extraction, and neural/vector physics application.

import os
import zlib
import hashlib
import logging
from typing import List, Tuple, Dict, Any, Optional

try:
    import orjson
    def fast_dumps(obj: Any) -> str:
        return orjson.dumps(obj).decode('utf-8')
except ImportError:
    import json
    def fast_dumps(obj: Any) -> str:
        return json.dumps(obj, default=str)

from src.services.extractors import UniversalExtractor
from src.services.neural_transformer import NeuralTransformer
from src.core.schemas import KinematicMap
from src.utils.i18n import backend_i18n

logger = logging.getLogger(__name__)


class SensorBatchProcessor:
    """
    Handles sensor file reading, compression, data extraction, and physical calculations.
    Follows Single Responsibility Principle (SRP) by being isolated from database and Qt UI concerns.
    """

    def __init__(
        self,
        extractor: Optional[UniversalExtractor] = None,
        transformer: Optional[NeuralTransformer] = None
    ):
        self.extractor = extractor or UniversalExtractor()
        self.transformer = transformer or NeuralTransformer()

    @staticmethod
    def calculate_hash(raw_content: bytes) -> str:
        """Calculates MD5 hash of raw file bytes."""
        return hashlib.md5(raw_content).hexdigest()

    @staticmethod
    def compress_content(raw_content: bytes) -> bytes:
        """Compresses binary content using zlib."""
        return zlib.compress(raw_content)

    def process_file(
        self,
        file_path: str,
        source_name: str,
        folder_schema: Optional[KinematicMap],
        assoc_type: str = "LOCAL"
    ) -> Tuple[Tuple[str, str, str, int, str, bytes], List[Tuple[str, str, str, str]]]:
        """
        Reads a single file, hashes and compresses it, extracts events, applies physics,
        and returns the formatted tuples for raw storage and section events.
        """
        filename_only = os.path.basename(file_path)
        _, file_extension = os.path.splitext(filename_only)

        with open(file_path, "rb") as f:
            raw_content = f.read()

        file_size = len(raw_content)
        file_hash = self.calculate_hash(raw_content)
        compressed_content = self.compress_content(raw_content)

        raw_storage_tuple = (
            source_name,
            filename_only,
            file_extension.lower(),
            file_size,
            file_hash,
            compressed_content
        )

        events_tuples: List[Tuple[str, str, str, str]] = []
        events = self.extractor.extract(file_path, raw_content, source_name)
        if events:
            transformed_events = self.transformer.apply_physics(
                events,
                folder_schema,
                assoc_type=assoc_type
            )
            for event in transformed_events:
                json_payload = fast_dumps(event['data_payload'])
                timestamp_str = str(event['event_timestamp'])
                events_tuples.append((
                    timestamp_str,
                    event['sensor_id'],
                    json_payload,
                    filename_only
                ))

        return raw_storage_tuple, events_tuples
