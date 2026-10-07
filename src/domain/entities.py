from dataclasses import dataclass, field
from enum import Enum
import uuid
from typing import List, Tuple, Any



class AssociationType(str, Enum):
    """ Defines how a DataSource is associated with the map. """
    UNASSOCIATED = "UNASSOCIATED"
    GLOBAL = "GLOBAL"
    LOCAL = "LOCAL"


@dataclass
class DataSource:
    """
    Entity (Model) representing a single data source.
    """
    path: str
    
    # Display name for the data source
    name: str
    
    # List of detected file types (e.g., ["JSON", "CSV"])
    file_types: list[str] = field(default_factory=list)
    

    id: str = field(default_factory=lambda: f"src_{uuid.uuid4().hex[:8]}")
    parser_id: str | None = None
    
    association_type: AssociationType = AssociationType.UNASSOCIATED
    
    # Generic element ID (can be a node or edge)
    associated_element_id: str | None = None
    



@dataclass
class MapNode:
    """
    Entity (Model) representing a single map node (junction).
    """
    id: str
    x: float
    y: float
    

    node_type: str = "unknown"
    

    real_name: str | None = None


@dataclass
class MapEdge:
    """
    Entity (Model) representing a single map edge (road).
    """
    id: str
    

    from_node: str
    to_node: str
    shape: List[Tuple[float, float]] = field(default_factory=list)
    

    real_name: str | None = None