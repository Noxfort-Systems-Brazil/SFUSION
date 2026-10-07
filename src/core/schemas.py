from pydantic import BaseModel, Field
from typing import Optional
from src.utils.i18n import backend_i18n

class KinematicMap(BaseModel):
    """
    Strongly Typed Object acting as a Mathematical Blueprint.
    The SLM (Phi-4-mini) instantiates this object filling it with the actual columns
    and measurement units identified in the sensor sample so the Vector Engine (Polars) can build the AST.
    """
    
    # --- Direct Variables ---
    speed_col: Optional[str] = Field(
        None, 
        description=backend_i18n.t("schemas.desc_speed")
    )
    flow_col: Optional[str] = Field(
        None, 
        description=backend_i18n.t("schemas.desc_flow")
    )
    intensity_col: Optional[str] = Field(
        None, 
        description=backend_i18n.t("schemas.desc_intensity")
    )

    # --- Base Kinematic Variables (for Derivation) ---
    distance_col: Optional[str] = Field(
        None, 
        description=backend_i18n.t("schemas.desc_distance")
    )
    time_col: Optional[str] = Field(
        None, 
        description=backend_i18n.t("schemas.desc_time")
    )
    occupancy_col: Optional[str] = Field(
        None, 
        description=backend_i18n.t("schemas.desc_occupancy")
    )

    # --- Unit of Measurement Metadata ---
    speed_unit: Optional[str] = Field(
        "km/h",
        description="Speed unit: km/h, m/s, mph"
    )
    occupancy_unit: Optional[str] = Field(
        None,
        description="Occupancy unit: ms, s, pct"
    )
    distance_unit: Optional[str] = Field(
        None,
        description="Distance unit: m, km, miles"
    )
    time_unit: Optional[str] = Field(
        None,
        description="Time unit: s, ms, min, hours"
    )

    # --- Confidence Metadata ---
    confidence_score: Optional[float] = Field(
        None,
        description=backend_i18n.t("schemas.desc_confidence")
    )
