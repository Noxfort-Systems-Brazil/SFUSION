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

# File: src/services/neural_transformer.py
# Author: Gabriel Moraes
# Date: May 2026
# Description:
#    SOLID Intermediary Layer. Orchestrates the Semantic Encoder (Phi-4-mini) 
#    and the Vector Physics Engine (Polars) to normalize heterogeneous data payloads.

import pandas as pd
import numpy as np
import polars as pl
import logging
from src.utils.i18n import backend_i18n
from typing import List, Optional, Dict

from src.agent.slm_engine import SLMEngine
from src.services.math_engine import MathEngine
from src.core.schemas import KinematicMap

class NeuralTransformer:
    def __init__(self):
        self.slm_engine = None
        self.math_engine = MathEngine()
        self._schema_cache: Dict[str, KinematicMap] = {}

    def initialize_encoder(self):
        """Loads the SLM Engine model (~5GB, instant startup with GPU)."""
        if not self.slm_engine:
            logging.info(backend_i18n.t("neural.init_engine"))
            self.slm_engine = SLMEngine()

    def cleanup_encoder(self):
        """Unloads the SLM Engine from memory."""
        if self.slm_engine:
            logging.info(backend_i18n.t("neural.unload_engine"))
            if hasattr(self.slm_engine, 'unload'):
                self.slm_engine.unload()
            del self.slm_engine
            self.slm_engine = None
        self._schema_cache.clear()

    def discover_schema(self, raw_text: str, folder_name: str, assoc_type: str = "LOCAL") -> Optional[KinematicMap]:
        """
        Uses the SLM Engine to discover schema mapping for the sensor.
        """
        # Check cache first — avoid redundant inference for the same sensor type
        if folder_name in self._schema_cache:
            logging.info(backend_i18n.t("neural.cache_hit", sensor=folder_name))
            return self._schema_cache[folder_name]
        
        logging.info(backend_i18n.t("neural.discover_schema", sensor=folder_name))
        
        if self.slm_engine:
            schema = self.slm_engine.discover_schema(raw_text, folder_name, assoc_type)
            if schema:
                # Sanity Filter: Wipe out string hallucinations like "NULL"
                for field in ['speed_col', 'flow_col', 'intensity_col', 'distance_col', 'time_col', 'occupancy_col']:
                    val = getattr(schema, field, None)
                    if isinstance(val, str) and val.upper() in ["NULL", "NONE", ""]:
                        setattr(schema, field, None)
                
                # --- PÓS-SLM VALIDATION ---
                if assoc_type.upper() == "LOCAL":
                    if not schema.speed_col and (not schema.distance_col or not schema.time_col):
                        logging.warning(backend_i18n.t('warnings.neural.missing_speed_dist_time', sensor=folder_name))
                    if not schema.intensity_col and not schema.occupancy_col:
                        logging.warning(backend_i18n.t('warnings.neural.missing_intensity_occ', sensor=folder_name))
                    if not schema.flow_col:
                        logging.warning(backend_i18n.t('warnings.neural.missing_flow', sensor=folder_name))
                
                # Cache the result for this sensor folder
                self._schema_cache[folder_name] = schema
            return schema
        
        logging.warning(backend_i18n.t('warnings.neural.engine_not_init'))
        return None

    def apply_physics(self, events: List[dict], schema: Optional[KinematicMap], assoc_type: str = "LOCAL") -> List[dict]:
        """
        Converts the payloads into a Polars vectorized graph, applies the discovered schema 
        to calculate Speed, Flow, and Intensity, and aggregates them.
        """
        if not events:
            return []
            
        def extract_flat_payloads(payload, parent_key=''):
            items = {}
            lists = {}
            for k, v in payload.items():
                new_key = f"{parent_key}.{k}" if parent_key else k
                if isinstance(v, dict):
                    sub_items, sub_lists = extract_flat_payloads(v, new_key)
                    items.update(sub_items)
                    lists.update(sub_lists)
                elif isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
                    lists[new_key] = v
                else:
                    items[new_key] = v
            return items, lists

        def explode_combinations(base_items, lists):
            if not lists:
                yield base_items
                return
                
            k_list, v_list = list(lists.items())[0]
            remaining_lists = {k: v for k, v in lists.items() if k != k_list}
            
            if not v_list:
                yield from explode_combinations(base_items, remaining_lists)
                return
                
            for item in v_list:
                if isinstance(item, dict):
                    sub_items, sub_lists = extract_flat_payloads(item, k_list)
                    new_base = dict(base_items)
                    new_base.update(sub_items)
                    new_lists = dict(remaining_lists)
                    new_lists.update(sub_lists)
                    yield from explode_combinations(new_base, new_lists)
                else:
                    yield from explode_combinations(base_items, remaining_lists)

        flat_events = []
        for event in events:
            payload = event.get('data_payload', {})
            items, lists = extract_flat_payloads(payload)
            for flat_payload in explode_combinations(items, lists):
                flat_payload['event_timestamp'] = event['event_timestamp']
                flat_payload['sensor_id'] = event['sensor_id']
                flat_events.append(flat_payload)
                
        df_payload = pd.DataFrame(flat_events)
        
        if schema:
            # Reconcile schema columns with actual DataFrame columns
            df_cols = list(df_payload.columns)
            
            def resolve_column(schema_col: Optional[str]) -> Optional[str]:
                if not schema_col: return None
                schema_col_lower = schema_col.lower()
                if schema_col_lower in [c.lower() for c in df_cols]: 
                    return next((c for c in df_cols if c.lower() == schema_col_lower), None)
                
                # Try suffix match (e.g. 'recognitions.vehicle' -> 'vehicle')
                for col in df_cols:
                    if schema_col_lower.endswith('.' + col.lower()) or col.lower().endswith('.' + schema_col_lower):
                        return col
                
                # Try exact basename match
                schema_base = schema_col_lower.split('.')[-1]
                for col in df_cols:
                    if col.lower().split('.')[-1] == schema_base:
                        return col
                        
                # Try substring match in basename as a fallback
                for col in df_cols:
                    col_base = col.lower().split('.')[-1]
                    if schema_base in col_base or col_base in schema_base:
                        return col
                        
                return None

            # Create a localized copy of the schema for this DataFrame to avoid mutating the cache
            local_schema = schema.copy()
            local_schema.speed_col = resolve_column(local_schema.speed_col)
            local_schema.flow_col = resolve_column(local_schema.flow_col)
            local_schema.intensity_col = resolve_column(local_schema.intensity_col)
            local_schema.distance_col = resolve_column(local_schema.distance_col)
            local_schema.time_col = resolve_column(local_schema.time_col)
            local_schema.occupancy_col = resolve_column(local_schema.occupancy_col)
            
            if assoc_type.upper() == "GLOBAL":
                local_schema.flow_col = None
                local_schema.intensity_col = None
            
            pl_df = pl.from_pandas(df_payload)
            exprs = self.math_engine.compile_ast(local_schema)
            pl_df = pl_df.with_columns(exprs)
            
            # --- AGGREGATION (1 Arquivo = 1 Linha) ---
            group_cols = ["sensor_id"]
            agg_exprs = self.math_engine.compile_aggregations(pl_df.columns)
            pl_df = pl_df.group_by(group_cols).agg(agg_exprs)
            
            df_payload = pl_df.to_pandas()
        else:
            logging.warning(backend_i18n.t('warnings.neural.no_kinematic_map'))
        
        # Guarantee fundamental kinematic variables exist in the payload
        required_cols = ['speed_val', 'flow_val', 'intensity_val', 'lat', 'lon']
        for col in required_cols:
            if col not in df_payload.columns:
                df_payload[col] = None
                
        # Convert pandas numeric formatting appropriately so it serializes natively
        df_payload['speed_val'] = pd.to_numeric(df_payload['speed_val'], errors='coerce')
        df_payload['flow_val'] = pd.to_numeric(df_payload['flow_val'], errors='coerce')
        df_payload['intensity_val'] = pd.to_numeric(df_payload['intensity_val'], errors='coerce')
        
        # Convert NaN to None for standard JSON compliance
        df_payload = df_payload.replace({np.nan: None})
        
        # Reconstruct events
        enriched_payloads = df_payload.to_dict(orient='records')
        
        aggregated_events = []
        for row in enriched_payloads:
            sensor_id = row.get('sensor_id', events[0]['sensor_id'])
            
            # If schema was mapped but speed_val is None due to zero vehicles/empty interval, default to 0.0
            speed_value = row.get('speed_val')
            if speed_value is None and schema and (schema.speed_col or (schema.distance_col and schema.time_col)):
                speed_value = 0.0

            # Check for genuinely failed physics calculations (missing column in schema)
            missing_kinematics = []
            if speed_value is None: 
                missing_kinematics.append('speed_val')
            if assoc_type.upper() == "LOCAL":
                if row.get('flow_val') is None: missing_kinematics.append('flow_val')
                if row.get('intensity_val') is None: missing_kinematics.append('intensity_val')
            
            if missing_kinematics:
                logging.warning(backend_i18n.t("neural.physics_failed", vars=missing_kinematics, sensor=sensor_id))
            
            # Global sensors strictly zero out flow and intensity (macro network speed only)
            if assoc_type.upper() == "GLOBAL":
                final_flow = 0.0
                final_intensity = 0.0
            else:
                final_flow = row.get('flow_val', 0.0)
                final_intensity = row.get('intensity_val', 0.0)

            clean_payload = {
                'speed_val': speed_value,
                'flow_val': final_flow,
                'intensity_val': final_intensity,
                'lat': row.get('lat'),
                'lon': row.get('lon'),
            }
                
            aggregated_events.append({
                'event_timestamp': row.get('event_timestamp', events[0]['event_timestamp']),
                'sensor_id': sensor_id,
                'data_payload': clean_payload
            })
            
        return aggregated_events
