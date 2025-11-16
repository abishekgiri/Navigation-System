# Navigation-System
Overview
This project implements a real-time navigation engine similar to Google Maps. It loads real road network data from OpenStreetMap, constructs a graph, computes shortest paths using A* and Dijkstra algorithms, supports traffic-aware weights, and visualizes routes.
Core Data Structures and Algorithms
- Graph (Adjacency List)
- Weighted Edges
- Min-Heap Priority Queue
- Dijkstra’s Algorithm
- A* Search with Haversine heuristic
- Spatial Index (Nearest Node Search)
- Optional: Contraction Hierarchies for faster preprocessing
Technologies Used
- Python 3
- OSMnx for OpenStreetMap data
- NetworkX (internally by OSMnx)
- Matplotlib for visual route plotting
- Shapely / Rtree (optional spatial indexing)
Features Implemented
1. Load real-world road network using OSMnx.
2. Build a custom adjacency-list graph.
3. Compute shortest routes using A* search.
4. Support traffic multiplier on edges.
5. Visualize the full street map + computed route.
6. Nearest-node search from GPS coordinates.
7. Clean and modern route visualization.
Project Folder Structure
nav_engine/
  app.py
  nav/
	graph.py
	loader_osm.py
	shortest_path.py
	spatial_index.py
  viz/
	plot_route.py
How it Works (Step-by-Step)
1. **Load Map Data**: OSMnx downloads road network for a given city.
2. **Build Graph**: Nodes store lat/lon; edges store travel times.
3. **Nearest Node Lookup**: Converts GPS coords → graph nodes.
4. **Compute Route**: A* search computes fastest route.
5. **Traffic Handling**: Edge weights scaled by traffic factor.
6. **Plotting**: Full street map drawn in gray; route in blue.
Sample Output Description
The resulting visualization shows all city roads in light gray and the computed shortest path highlighted in blue. This mimics how navigation systems generate and display routes.
Next Steps / Possible Enhancements
- Add turn-by-turn voice/text navigation instructions.
- Add Contraction Hierarchies for ultra-fast routing.
- Add live traffic simulation.
- Add Flask/FastAPI web interface.
- Add Folium interactive map output.

