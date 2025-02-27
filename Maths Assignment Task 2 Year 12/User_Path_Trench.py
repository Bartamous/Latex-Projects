import plotly.graph_objects as go
import networkx as nx

G = nx.Graph()

# edges with weights
edges = [
    ("D", "P", 6),
("P", "K", 6),
("K", "C", 14),
("C", "F", 18),
("C", "B", 8),
("C", "J", 18),
("D", "F", 10),
("F", "J", 8),
("F", "Q", 6),
("J", "E", 10),
("B", "E", 20),
("B", "A", 26),
("E", "A", 16),
("Q", "M", 18),
("M", "H", 12),
("M", "E", 12),
("H", "E", 44),
("H", "L", 14),
("L", "T", 14),
("T", "I", 8),
("I", "N", 14),
("N", "G", 56),
("N", "S", 22),
("S", "G", 28),
("A", "G", 20)
]

for edge in edges:
    G.add_edge(edge[0], edge[1], weight=edge[2])

pos = nx.spring_layout(G, weight='weight', seed=30)

# user  path
def get_user_path():
    path_input = input("Enter the path as a sequence of nodes separated by spaces (e.g., P D F J): ")
    path = path_input.strip().split()
    return path

user_path = get_user_path()
user_path_edges = list(zip(user_path[:-1], user_path[1:]))

# plotly
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

# highlight path
for edge in user_path_edges:
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
                    title=f'Path: {" -> ".join(user_path)}',
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                ))

filename = "_".join(user_path) + ".png"
fig.write_image(filename)
print(f"Graph saved as {filename}")
