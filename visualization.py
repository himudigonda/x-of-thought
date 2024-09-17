import networkx as nx
import plotly.graph_objects as go

def create_graph_visualization(G, pos, reasoning_type):
    """
    Create an interactive graph visualization using Plotly.

    Args:
        G (networkx.Graph): The graph to visualize.
        pos (dict): A dictionary of node positions.
        reasoning_type (str): The type of reasoning (not used in this function, but kept for potential future use).

    Returns:
        plotly.graph_objs._figure.Figure: A Plotly figure object representing the graph.
    """
    # Create edge traces
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color="#888"),
        hoverinfo="none",
        mode="lines")

    # Create node traces
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]

    # Determine node colors based on sentiment
    node_colors = [
        "lightblue" if node in ["Input", "Output"]
        else "green" if G.nodes[node].get("sentiment") == "Positive"
        else "red" if G.nodes[node].get("sentiment") == "Negative"
        else "lightgreen" for node in G.nodes()
    ]

    # Set node sizes
    node_sizes = [40 if node in ["Input", "Output"] else 30 for node in G.nodes()]

    # Create hover text for nodes
    node_text = [f"{node}: {G.nodes[node].get('description', '')}" for node in G.nodes()]

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        hoverinfo="text",
        marker=dict(showscale=False, color=node_colors, size=node_sizes, line_width=2),
        text=[node for node in G.nodes()],
        textposition="top center",
        hovertext=node_text,
    )

    # Set up the layout for the graph
    layout = go.Layout(
        showlegend=False,
        hovermode="closest",
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor="rgba(0,0,0,0)",
    )

    # Create and return the figure
    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
    return fig

def create_force_directed_layout(G):
    """
    Create a force-directed layout for the graph using NetworkX.

    Args:
        G (networkx.Graph): The graph to layout.

    Returns:
        dict: A dictionary of node positions.
    """
    pos = nx.spring_layout(G)
    return pos
