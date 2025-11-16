from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional


@dataclass
class Edge:
    target: int               # node id of neighbor
    base_time: float          # travel time in seconds (without traffic)
    road_name: Optional[str]  # street name


class Graph:
    """
    Simple directed graph with weighted edges (travel time).
    Nodes are identified by integer ids, with lat/lon stored separately.
    """

    def __init__(self) -> None:
        # adjacency list: node_id -> list of outgoing edges
        self.adj: Dict[int, List[Edge]] = {}
        # coordinates: node_id -> (lat, lon)
        self.coords: Dict[int, Tuple[float, float]] = {}

    def add_node(self, node_id: int, lat: float, lon: float) -> None:
        if node_id not in self.adj:
            self.adj[node_id] = []
        self.coords[node_id] = (lat, lon)

    def add_edge(
        self,
        u: int,
        v: int,
        base_time: float,
        road_name: Optional[str] = None,
        bidirectional: bool = True,
    ) -> None:
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []
        self.adj[u].append(Edge(target=v, base_time=base_time, road_name=road_name))
        if bidirectional:
            self.adj[v].append(Edge(target=u, base_time=base_time, road_name=road_name))

    def neighbors(self, u: int) -> List[Edge]:
        return self.adj.get(u, [])
