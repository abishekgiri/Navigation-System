from __future__ import annotations
from typing import Tuple
import osmnx as ox

from .graph import Graph


def load_graph_from_place(place_name: str) -> Graph:
    """
    Download drivable road network for a given place (city, campus, etc.)
    and convert to our custom Graph.
    """
    # Get directed graph from OSM (NetworkX MultiDiGraph)
    G_osm = ox.graph_from_place(place_name, network_type="drive")

    graph = Graph()

    # 1. Add nodes with coordinates
    for node_id, data in G_osm.nodes(data=True):
        lat = data.get("y")
        lon = data.get("x")
        if lat is None or lon is None:
            continue
        graph.add_node(int(node_id), lat, lon)

    # 2. Add edges with estimated travel time
    # osmnx can add edge speeds / travel times for us:
    G_osm = ox.add_edge_speeds(G_osm)       # adds "speed_kph"
    G_osm = ox.add_edge_travel_times(G_osm) # adds "travel_time" in seconds

    for u, v, data in G_osm.edges(data=True):
        if u not in graph.coords or v not in graph.coords:
            continue

        travel_time = data.get("travel_time")
        if travel_time is None:
            # fallback: compute using length and default speed
            length_m = data.get("length", 50.0)
            speed_kph = data.get("speed_kph", 30.0)
            speed_mps = speed_kph * 1000.0 / 3600.0
            travel_time = length_m / speed_mps

        name = data.get("name")
        graph.add_edge(int(u), int(v), base_time=float(travel_time), road_name=name, bidirectional=True)

    return graph


def get_bounds(graph: Graph) -> Tuple[float, float, float, float]:
    """
    Return (min_lat, max_lat, min_lon, max_lon) of graph, useful for plotting.
    """
    lats = [lat for (lat, _) in graph.coords.values()]
    lons = [lon for (_, lon) in graph.coords.values()]
    return min(lats), max(lats), min(lons), max(lons)
