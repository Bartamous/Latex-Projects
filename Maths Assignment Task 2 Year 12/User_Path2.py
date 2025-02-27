import plotly.graph_objects as go
import networkx as nx

G = nx.Graph()

edges = [
    ("A","B",34), ("A","E",18), ("A","G",36), ("A","H",52),
    ("B","C",8), ("B","E",22),
    ("C","F",18), ("C","J",22), ("C","K",14),
    ("D","F",14), ("D","P",6),
    ("E","J",14), ("E","M",12), ("E","Q",16),
    ("F","J",8), ("F","Q",8),
    ("G","N",58), ("G","S",22),
    ("H","E",48), ("H","L",16), ("H","M",14), ("H","T",32),
    ("I","N",14), ("I","T",10),
    ("K","P",6),
    ("L","T",22),
    ("M","Q",18),
    ("N","S",24), ("N","T",36)
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
