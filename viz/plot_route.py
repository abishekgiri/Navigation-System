import matplotlib.pyplot as plt

def plot_graph_and_route(graph, path):
    plt.figure(figsize=(10, 10))
    plt.style.use("ggplot")

    # Plot roads
    for u, edges in graph.adj.items():
        lat_u, lon_u = graph.coords[u]
        for e in edges:
            lat_v, lon_v = graph.coords[e.target]
            plt.plot(
                [lon_u, lon_v],
                [lat_u, lat_v],
                color="#CCCCCC",
                linewidth=0.6,
                alpha=0.6
            )

    # Plot the route
    path_lats = []
    path_lons = []
    for node in path:
        lat, lon = graph.coords[node]
        path_lats.append(lat)
        path_lons.append(lon)

    plt.plot(
        path_lons,
        path_lats,
        color="#0078FF",
        linewidth=3.5,
    )

    plt.title("Shortest Route", fontsize=18)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.tight_layout()
    plt.show()
