import networkx as nx
import plotly.graph_objects as go
import heapq
import pandas as pd

def dijkstra(graph, start, end):
    queue = [(0, start)]  # (cost, node)
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}
    
    table_data = []
    
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        
        # Append the table data only when a node is popped
        table_data.append({
            'Current Node': current_node,
            'Distances': dict(distances)
        })
        
        if current_node == end:
            break
        
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))
    
    path = []
    node = end
    while node is not None:
        path.insert(0, node)
        node = previous_nodes[node]
    
    return path, distances[end], table_data

def visualize_graph_with_plotly(graph, path):
    G = nx.Graph()
    for node in graph:
        for neighbor, weight in graph[node].items():
            G.add_edge(node, neighbor, weight=weight)
    
    pos = nx.spring_layout(G, seed=42, weight='weight', scale=2)
    
    edge_traces = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace = go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            line=dict(width=2, color='gray'),
            hoverinfo='none',
            mode='lines')
        edge_traces.append(edge_trace)
    
    path_edges = list(zip(path, path[1:]))
    for edge in path_edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace = go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            line=dict(width=4, color='red'),
            hoverinfo='none',
            mode='lines')
        edge_traces.append(edge_trace)
    
    node_trace = go.Scatter(
        x=[], y=[], text=[], mode='markers+text', textposition="top center",
        hoverinfo='text', marker=dict(
            color='lightblue', size=20, line=dict(width=2, color='darkblue'))
    )
    
    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += (x,)
        node_trace['y'] += (y,)
        node_trace['text'] += (node,)
    
    annotations = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        x_mid = (x0 + x1) / 2
        y_mid = (y0 + y1) / 2
        annotations.append(
            dict(
                x=x_mid, y=y_mid,
                xref='x', yref='y',
                text=str(G[edge[0]][edge[1]]['weight']),  # Edge weight
                showarrow=False,
                font=dict(size=12, color='black')
            )
        )
    
    fig = go.Figure(data=edge_traces + [node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        title="Dijkstra's Shortest Path Visualization",
                        annotations=annotations  # Add annotations for edge weights
                    ))
    
    fig.show()

def display_table(table_data):
    df = pd.DataFrame(table_data)
    print(df.to_string(index=False))

def export_table_to_csv(table_data, filename="dijkstra_steps.csv"):
    df = pd.DataFrame(table_data)
    df.to_csv(filename, index=False)
    print(f"Table data exported to {filename}")

if __name__ == "__main__":
    graph = {
        'A': {'B': 34, 'E': 18, 'G': 36, 'H': 52},
        'B': {'A': 34, 'C': 8, 'E': 22},
        'C': {'B': 8, 'F': 18, 'J': 22, 'K': 14},
        'D': {'F': 14, 'P': 6},
        'E': {'A': 18, 'B': 22, 'J': 14, 'M': 12, 'Q': 16},
        'F': {'C': 18, 'D': 14, 'J': 8, 'Q': 8},
        'G': {'A': 36, 'N': 58, 'S': 22},
        'H': {'A': 52, 'E': 48, 'L': 16, 'M': 14, 'T': 32},
        'I': {'N': 14, 'T': 10},
        'J': {'C': 22, 'E': 14, 'F': 8},
        'K': {'C': 14, 'P': 6},
        'L': {'H': 16, 'T': 22},
        'M': {'E': 12, 'H': 14, 'Q': 18},
        'N': {'G': 58, 'I': 14, 'S': 24, 'T': 36},
        'P': {'D': 6, 'K': 6},
        'Q': {'E': 16, 'F': 8, 'M': 18},
        'S': {'G': 22, 'N': 24},
        'T': {'H': 32, 'L': 22, 'N': 36}
    }
    
    start = input("Enter start node: ")
    end = input("Enter end node: ")
    path, cost, table_data = dijkstra(graph, start, end)
    print(f"Shortest path from {start} to {end}: {path} with cost {cost}")
    display_table(table_data)
    export_table_to_csv(table_data)
    visualize_graph_with_plotly(graph, path)
