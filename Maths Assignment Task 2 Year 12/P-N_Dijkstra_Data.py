import plotly.graph_objects as go
import networkx as nx

G = nx.Graph()

edges = [
    ("A", "B", 34), ("A", "E", 18), ("A", "G", 36), ("A", "H", 52),
    ("B", "A", 34), ("B", "C", 8), ("B", "E", 22),
    ("C", "B", 8), ("C", "F", 18), ("C", "K", 14),
    ("D", "F", 14), ("D", "P", 6),
    ("E", "A", 18), ("E", "B", 22), ("E", "J", 14), ("E", "M", 12), ("E", "Q", 16),
    ("F", "C", 18), ("F", "D", 14), ("F", "J", 8), ("F", "Q", 8),
    ("G", "A", 36), ("G", "N", 58), ("G", "S", 22),
    ("H", "A", 52), ("H", "E", 48), ("H", "L", 16), ("H", "M", 14), ("H", "T", 32),
    ("I", "N", 14), ("I", "T", 10),
    ("J", "E", 14), ("J", "F", 8),
    ("K", "C", 14), ("K", "P", 6),
    ("L", "H", 16), ("L", "T", 22),
    ("M", "E", 12), ("M", "H", 14), ("M", "Q", 18),
    ("N", "G", 58), ("N", "I", 14), ("N", "S", 24), ("N", "T", 36),
    ("P", "D", 6), ("P", "K", 6),
    ("Q", "E", 16), ("Q", "F", 8), ("Q", "M", 18),
    ("S", "G", 22), ("S", "N", 24),
    ("T", "H", 32), ("T", "L", 22), ("T", "N", 36)
]

for edge in edges:
    G.add_edge(edge[0], edge[1], weight=edge[2])

pos = nx.spring_layout(G, weight='weight', seed=30)

start_node = 'P'
end_node = 'N'
shortest_path = nx.dijkstra_path(G, start_node, end_node, weight='weight')
shortest_path_edges = list(zip(shortest_path[:-1], shortest_path[1:]))

# Plotly
edge_trace = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace.append(go.Scatter(
        x=[x0, x1, None], y=[y0, y1, None],
        line=dict(width=1, color='gray'),
        hoverinfo='none',
        mode='lines'
    ))

# Highlight path
for edge in shortest_path_edges:
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace.append(go.Scatter(
        x=[x0, x1, None], y=[y0, y1, None],
        line=dict(width=2, color='red'),
        hoverinfo='none',
        mode='lines'
    ))

node_trace = go.Scatter(
    x=[pos[node][0] for node in G.nodes()],
    y=[pos[node][1] for node in G.nodes()],
    mode='markers+text',
    text=[node for node in G.nodes()],
    textposition="top center",
    marker=dict(size=20, color='lightblue'),
    hoverinfo='text'
)

edge_labels = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_labels.append(go.Scatter(
        x=[(x0 + x1) / 2], y=[(y0 + y1) / 2],
        text=[str(G.edges[edge]['weight'])],
        mode='text',
        textposition="middle center",
        hoverinfo='none'
    ))

fig = go.Figure(data=edge_trace + [node_trace] + edge_labels,
                layout=go.Layout(
                    title=f'Shortest Path from {start_node} to {end_node}',
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                ))

fig.show()
