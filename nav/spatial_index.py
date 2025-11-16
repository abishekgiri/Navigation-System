from __future__ import annotations
from typing import Tuple, Optional

from .graph import Graph
from .shortest_path import haversine


def find_nearest_node_linear(graph: Graph, lat: float, lon: float) -> int:
    """
    Brute force nearest node search (O(N)).
    Upgrade this later to use R-tree / quadtree.
    """
    best_node: Optional[int] = None
    best_dist: float = float("inf")

    for node_id, (nlat, nlon) in graph.coords.items():
        d = haversine(lat, lon, nlat, nlon)
        if d < best_dist:
            best_dist = d
            best_node = node_id

    assert best_node is not None
    return best_node
