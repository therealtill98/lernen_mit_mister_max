import sys
import pandas as pd
import ast
import networkx as nx
from networkx.algorithms import bipartite
import community as community_louvain
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
print("✅ 1/8 Imports OK")

# 1) Load & filter metadata (use 'id' as TMDb ID)
meta = pd.read_csv("02_datasets/kaggle_movies/movies_metadata.csv", low_memory=False)
meta['release_year'] = pd.to_datetime(meta['release_date'], errors='coerce').dt.year
meta = meta.dropna(subset=['release_year']).query("release_year >= 2000")
meta['movie_id'] = pd.to_numeric(meta['id'], errors='coerce').astype(int)
meta = meta[['movie_id','title','vote_average']]
print(f"✅ 2/8 meta filtered: {len(meta)} movies ≥2000")

# 2) Load & parse credits (join on 'id')
credits = pd.read_csv("02_datasets/kaggle_movies/credits.csv", low_memory=False)
credits['movie_id']   = credits['id'].astype(int)
credits['cast_parsed'] = credits['cast'].apply(ast.literal_eval)
print(f"✅ 3/8 credits loaded: {len(credits)} rows")

# 3) Build actor–movie edge list
valid_ids = set(meta['movie_id'])
rows = []
for _, r in credits.iterrows():
    if r['movie_id'] not in valid_ids:
        continue
    for m in r['cast_parsed']:
        rows.append((r['movie_id'], m['name']))
# how many post-2000 movies never appeared?
seen_ids = {mid for mid, _ in rows}
missing_count = len(valid_ids - seen_ids)
print(f"ℹ️ {missing_count} movies had no actor data")
# dedupe actor–movie pairs
edge_df = (
    pd.DataFrame(rows, columns=['movie_id','actor'])
      .drop_duplicates()
      .merge(meta[['movie_id','title']], on='movie_id', how='left')
)
print(f"✅ 4/8 edge_df built: {len(edge_df)} actor–movie edges (deduped)")
print(f"   Unique actors: {edge_df['actor'].nunique()}")
print(f"   Unique movies: {edge_df['movie_id'].nunique()}")

# 4) Bipartite graph B
B = nx.Graph()
B.add_edges_from(edge_df[['actor','movie_id']].itertuples(index=False, name=None))
print(f"✅ 5/8 Bipartite B built: nodes={B.number_of_nodes()}, edges={B.number_of_edges()}")

# 5) Actor–actor graph G
actors = {n for n in B.nodes() if isinstance(n, str)}
G = bipartite.weighted_projected_graph(B, actors)
print(f"✅ 6/8 Actor–actor G built: nodes={G.number_of_nodes()}, edges={G.number_of_edges()}")

# 6) Focused graph H & Louvain (hover fix: add node_trace last)
top20 = meta.nlargest(10,'vote_average')
top10_ids = top20.head(10)['movie_id'].tolist()
focus = edge_df[edge_df.movie_id.isin(top10_ids)]
B2 = nx.Graph(); B2.add_edges_from(focus[['actor','movie_id']].itertuples(index=False,name=None))
H = bipartite.weighted_projected_graph(B2, set(focus['actor']))
partition = community_louvain.best_partition(H, weight='weight')
nx.set_node_attributes(H, partition, 'community')
print(f"✅ 7/8 Focused graph H built: nodes={H.number_of_nodes()}, edges={H.number_of_edges()}")

# 1) Compute a layout for H
pos_h = nx.kamada_kawai_layout(H)

# 2) Build edge‐line trace (no hover)
edge_x, edge_y = [], []
for u, v, d in H.edges(data=True):
    x0, y0 = pos_h[u]; x1, y1 = pos_h[v]
    edge_x += [x0, x1, None]
    edge_y += [y0, y1, None]

edge_trace = go.Scattergl(
    x=edge_x, y=edge_y,
    mode="lines",
    line=dict(width=1, color="#888"),
    hoverinfo="none"
)

# 3) Build invisible midpoints for edge hovers
mid_x, mid_y, mid_text = [], [], []
for u, v, d in H.edges(data=True):
    x0, y0 = pos_h[u]; x1, y1 = pos_h[v]
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    mid_x.append(mx)
    mid_y.append(my)
    mid_text.append(f"{u} ⇄ {v}: {d['weight']} mutual films")

edge_mid_trace = go.Scattergl(
    x=mid_x, y=mid_y,
    mode="markers",
    marker=dict(size=12, color="rgba(0,0,0,0)"),
    hoverinfo="text",
    text=mid_text,
    showlegend=False
)

# 4) Build node trace with correct hover
node_x, node_y, node_color, node_text = [], [], [], []
for n, d in H.nodes(data=True):
    x, y = pos_h[n]
    node_x.append(x)
    node_y.append(y)
    node_color.append(d["community"])
    node_text.append(f"{n}<br>Co-stars: {H.degree(n)}")

node_trace = go.Scattergl(
    x=node_x, y=node_y,
    mode="markers",
    marker=dict(
        size=10,
        color=node_color,
        colorscale="Jet",
        showscale=True,
        colorbar=dict(title="Community")
    ),
    hoverinfo="text",
    text=node_text
)

# 5) Assemble figure (midpoints before nodes)
fig = go.Figure()
fig.add_trace(edge_trace)
fig.add_trace(edge_mid_trace)
fig.add_trace(node_trace)

fig.update_layout(
    title="Actor Network from Top-10 Rated Movies",
    hovermode="closest",
    showlegend=False,
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    margin=dict(l=0, r=0, t=40, b=0)
)

fig.write_html("focused_H_fixed.html")
print("✅ Saved focused_H_fixed.html with working hovers!")