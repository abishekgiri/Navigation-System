from nav.loader_osm import load_graph_from_place
from nav.spatial_index import find_nearest_node_linear
from nav.shortest_path import astar, TrafficMap
from viz.plot_route import plot_graph_and_route


def main():
    place = "Atlantic City, New Jersey, USA"
    print(f"Loading graph for: {place}")
    graph = load_graph_from_place(place)
    print(f"Loaded graph with {len(graph.coords)} nodes")

    # Example start/end coordinates (roughly inside the city)
    # You can replace these with real GPS points.
    start_lat, start_lon = 39.3643, -74.4229  # near AC boardwalk
    end_lat, end_lon = 39.3800, -74.4520      # another point in city

    src = find_nearest_node_linear(graph, start_lat, start_lon)
    dst = find_nearest_node_linear(graph, end_lat, end_lon)

    print(f"Source node: {src}, Dest node: {dst}")

    # Example: simulate heavy traffic on nothing for now (empty)
    traffic: TrafficMap = {}

    total_time, path = astar(graph, src, dst, traffic=traffic)
    print(f"Travel time: {total_time/60:.1f} minutes, path length: {len(path)} nodes")

    plot_graph_and_route(graph, path)


if __name__ == "__main__":
    main()
