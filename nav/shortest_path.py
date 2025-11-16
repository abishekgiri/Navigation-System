from __future__ import annotations
from typing import Dict, Tuple, List, Optional
import heapq
import math

from .graph import Graph, Edge


TrafficMap = Dict[Tuple[int, int], float]  # (u, v) -> traffic multiplier


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Great-circle distance between two points on Earth in meters.
    """
    R = 6371000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def reconstruct_path(prev: Dict[int, int], source: int, target: int) -> List[int]:
    path = []
    cur = target
    while cur != source:
        path.append(cur)
        cur = prev[cur]
    path.append(source)
    path.reverse()
    return path


def edge_cost(edge: Edge, u: int, traffic: Optional[TrafficMap]) -> float:
    if traffic is None:
        return edge.base_time
    factor = traffic.get((u, edge.target), 1.0)
    return edge.base_time * factor


def dijkstra(
    graph: Graph,
    source: int,
    target: int,
    traffic: Optional[TrafficMap] = None,
) -> Tuple[float, List[int]]:
    """
    Classic Dijkstra on our adjacency list.
    Returns (total_time_seconds, path_node_ids).
    """
    INF = float("inf")
    dist: Dict[int, float] = {node: INF for node in graph.adj.keys()}
    prev: Dict[int, int] = {}

    dist[source] = 0.0
    pq: List[Tuple[float, int]] = [(0.0, source)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == target:
            break

        for e in graph.neighbors(u):
            w = edge_cost(e, u, traffic)
            nd = d + w
            if nd < dist[e.target]:
                dist[e.target] = nd
                prev[e.target] = u
                heapq.heappush(pq, (nd, e.target))

    if target not in prev and source != target:
        raise ValueError("No path found")

    path = reconstruct_path(prev, source, target) if source != target else [source]
    return dist[target], path


def astar(
    graph: Graph,
    source: int,
    target: int,
    traffic: Optional[TrafficMap] = None,
    avg_speed_mps: float = 13.9,  # ~50 km/h
) -> Tuple[float, List[int]]:
    """
    A* using straight-line distance / avg speed as an admissible heuristic on time.
    """
    INF = float("inf")
    dist: Dict[int, float] = {node: INF for node in graph.adj.keys()}
    prev: Dict[int, int] = {}

    dist[source] = 0.0

    def h(node: int) -> float:
        lat1, lon1 = graph.coords[node]
        lat2, lon2 = graph.coords[target]
        d_m = haversine(lat1, lon1, lat2, lon2)
        return d_m / avg_speed_mps  # estimated seconds

    pq: List[Tuple[float, int]] = [(h(source), source)]  # (f = g + h, node)

    while pq:
        f, u = heapq.heappop(pq)
        if u == target:
            break

        g_u = dist[u]
        for e in graph.neighbors(u):
            w = edge_cost(e, u, traffic)
            tentative_g = g_u + w
            if tentative_g < dist[e.target]:
                dist[e.target] = tentative_g
                prev[e.target] = u
                f_new = tentative_g + h(e.target)
                heapq.heappush(pq, (f_new, e.target))

    if target not in prev and source != target:
        raise ValueError("No path found")

    path = reconstruct_path(prev, source, target) if source != target else [source]
    return dist[target], path
