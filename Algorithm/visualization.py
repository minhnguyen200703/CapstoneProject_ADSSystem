import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(G, node_colors=None, title="Graph"):
    """
    Draw the graph with specified node colors and title.

    Parameters:
    - G: The NetworkX graph object.
    - node_colors: A list of colors for each node.
    - title: The title of the graph.
    """
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(G)  # Use spring layout to spread out the nodes

    # Draw the nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=300, cmap=plt.cm.Blues)
    
    # Draw the edges with specified thickness and color
    nx.draw_networkx_edges(G, pos, edge_color="black", width=1.5)
    
    # Draw the labels
    nx.draw_networkx_labels(G, pos, font_size=12, font_color="white")
    
    plt.title(title)
    plt.show()

def visualize_graphs(G, AvailableTruckList, AvailableContainerList, AwaitingTaskJob):
    """
    Visualize the graphs with different node colorings.

    Parameters:
    - G: The NetworkX graph object.
    - AvailableTruckList: Dictionary with truck locations.
    - AvailableContainerList: Dictionary with container locations.
    - AwaitingTaskJob: List of task jobs with start and end locations.
    """
    # 1. All nodes and edges
    draw_graph(G, title="Graph with All Nodes and Edges")
    
    # 2. Nodes with trucks in blue
    truck_locations = set(AvailableTruckList.values())
    node_colors = ["blue" if node in truck_locations else "grey" for node in G.nodes]
    draw_graph(G, node_colors=node_colors, title="Graph with Truck Locations in Blue")
    
    # 3. Nodes with containers in red
    container_locations = set(AvailableContainerList.values())
    node_colors = ["red" if node in container_locations else "grey" for node in G.nodes]
    draw_graph(G, node_colors=node_colors, title="Graph with Container Locations in Red")
    
    # 4. Task job start points in yellow and end points in green
    start_locations = set(taskjob["Locations"][0] for taskjob in AwaitingTaskJob)
    end_locations = set(taskjob["Locations"][1] for taskjob in AwaitingTaskJob)
    node_colors = []
    
    for node in G.nodes:
        if node in start_locations:
            node_colors.append("yellow")
        elif node in end_locations:
            node_colors.append("green")
        else:
            node_colors.append("grey")
    
    draw_graph(G, node_colors=node_colors, title="Graph with Task Job Start and End Locations")
