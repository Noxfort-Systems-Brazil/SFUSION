try:
    import orjson
    HAS_ORJSON = True
except ImportError:
    import json
    HAS_ORJSON = False

import csv
import io
import logging
from src.utils.i18n import backend_i18n
from datetime import datetime
from typing import List, Dict, Any

class BaseExtractor:
    """Base class for the universal extractor."""
    def extract(self, filename: str, raw_content: bytes, source_name: str = "") -> List[Dict[str, Any]]:
        raise NotImplementedError

class UniversalExtractor(BaseExtractor):
    """ 
    UNIVERSAL Source: Agnostic JSON/CSV parser for any sensor. 
    Obeys SOLID (OCP/SRP). Uses high-performance orjson (Rust/C) when available
    to extract events directly from raw bytes.
    """
    def extract(self, filename: str, raw_content: bytes, source_name: str = "") -> List[Dict[str, Any]]:
        results = []
        try:
            sensor_id = source_name if source_name else "generic_sensor"
            timestamp = datetime.now()

            # --- Attempt Excel Parsing if extension indicates Excel ---
            if filename.lower().endswith(('.xlsx', '.xls')):
                try:
                    import pandas as pd
                    excel_df = pd.read_excel(io.BytesIO(raw_content))
                    for record in excel_df.to_dict(orient='records'):
                        ev_ts = timestamp
                        for ts_key in ['timestamp', 'time', 'date', 'datetime', 'pubmillis', 'pubMillis', 'event_timestamp']:
                            matched_k = next((k for k in record if str(k).lower() == ts_key.lower()), None)
                            if matched_k and record[matched_k] is not None:
                                val = record[matched_k]
                                if isinstance(val, datetime):
                                    ev_ts = val
                                elif isinstance(val, (int, float)):
                                    try:
                                        if val > 1e11:
                                            ev_ts = datetime.fromtimestamp(val / 1000.0)
                                        else:
                                            ev_ts = datetime.fromtimestamp(val)
                                    except Exception:
                                        pass
                                elif isinstance(val, str):
                                    try:
                                        ev_ts = datetime.fromisoformat(val.replace('Z', '+00:00'))
                                    except Exception:
                                        pass
                                break
                        clean_payload = {str(k): (None if pd.isna(v) else v) for k, v in record.items()}
                        results.append({
                            "event_timestamp": ev_ts,
                            "sensor_id": sensor_id,
                            "data_payload": clean_payload
                        })
                    return results
                except Exception as e:
                    logging.debug(f"Excel parsing fallback skipped: {e}")

            # --- Attempt Fast JSON Parsing ---
            parsed_json = None
            try:
                if HAS_ORJSON:
                    parsed_json = orjson.loads(raw_content)
                else:
                    parsed_json = json.loads(raw_content.decode('utf-8', errors='ignore'))
            except Exception:
                parsed_json = None

            if parsed_json is not None:
                data = parsed_json
                events = []
                
                if isinstance(data, list):
                    events = data
                elif isinstance(data, dict):
                    # Find ALL arrays inside the JSON and merge them.
                    for key, val in data.items():
                        if isinstance(val, list) and len(val) > 0 and isinstance(val[0], dict):
                            events.extend(val)
                    
                    if not events:
                        events = [data]
                
                for ev in events:
                    if not isinstance(ev, dict): continue
                    
                    ev_ts = timestamp
                    for ts_key in ['timestamp', 'time', 'date', 'pubMillis', 'event_timestamp']:
                        if ts_key in ev:
                            try:
                                val = ev[ts_key]
                                if isinstance(val, (int, float)):
                                    if val > 1e11: ev_ts = datetime.fromtimestamp(val / 1000.0)
                                    else: ev_ts = datetime.fromtimestamp(val)
                                elif isinstance(val, str):
                                    ev_ts = datetime.fromisoformat(val.replace('Z', '+00:00'))
                            except Exception:
                                pass
                            break
                            
                    payload = ev.copy()
                    
                    results.append({
                        "event_timestamp": ev_ts,
                        "sensor_id": sensor_id,
                        "data_payload": payload
                    })
                return results

            # --- Fallback to CSV Parsing ---
            text = raw_content.decode('utf-8', errors='ignore')
            f = io.StringIO(text)
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    payload = dict(row)
                    ev_ts = timestamp
                    for ts_key in ['timestamp', 'time', 'date', 'datetime', 'pubmillis', 'pubMillis', 'event_timestamp']:
                        matched_k = next((k for k in payload if k.lower() == ts_key.lower()), None)
                        if matched_k and payload[matched_k]:
                            val = payload[matched_k]
                            try:
                                num_val = float(val)
                                if num_val > 1e11:
                                    ev_ts = datetime.fromtimestamp(num_val / 1000.0)
                                else:
                                    ev_ts = datetime.fromtimestamp(num_val)
                            except ValueError:
                                try:
                                    ev_ts = datetime.fromisoformat(str(val).replace('Z', '+00:00'))
                                except Exception:
                                    pass
                            break
                    results.append({
                        "event_timestamp": ev_ts,
                        "sensor_id": sensor_id,
                        "data_payload": payload
                    })
                except Exception:
                    continue

        except Exception as e:
            logging.error(f"UniversalExtractor: {backend_i18n.t('errors.extractors.processing_failed', file=filename, error=str(e))}")
            
        return results
