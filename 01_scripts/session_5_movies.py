# Imports
import sys
import pandas as pd
print("pandas imported")import ast
print("ast imported")
import networkx as nx
print("networkx imported")
from networkx.drawing.layout import bipartite_layout
print("bipartite layout imported")
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
print("matplotlib imported")
print("all imports ok")


# Loading data
meta = pd.read_csv("datasets/kaggle_movies/movies_metadata.csv", low_memory=False)
credits = pd.read_csv("datasets/kaggle_movies/credits.csv", low_memory=False)


# Keep only the columns we need from meta and cast the id to integer
meta = meta[['id','title']].drop_duplicates().rename(columns={'id':'movie_id'})
meta['movie_id'] = pd.to_numeric(meta['movie_id'], errors='coerce')
meta = meta.dropna(subset=['movie_id']).astype({'movie_id': int})

# Parse cast
credits ["cast_parsed"] = credits["cast"].apply(ast.literal_eval)
credits['movie_id'] = pd.to_numeric(credits['id'], errors='coerce')
credits = credits.dropna(subset=['movie_id']).astype({'movie_id': int})

# Build edge data frame
rows = []
for _, row in credits.iterrows():
    movie = row['id']
    for member in row['cast_parsed']:
        rows.append(( movie, member['name'] ))
edge_df = pd.DataFrame(rows, columns=['movie_id','actor'])

# Merge titles onto edge_df
edge_df = edge_df.merge(meta, on='movie_id', how='left')

# Choose top 5 movies by cast size as data sample
cast_counts = edge_df.groupby("title").size()
top5_titles = cast_counts.nlargest(5).index
sample = edge_df[edge_df['title'].isin(top5_titles)]

# Build bipartite graph
B = nx.Graph()
B.add_edges_from(sample[['actor','title']].itertuples(index=False, name=None))

# Compute layout
actors = set(sample["actor"])
pos    = bipartite_layout(B, actors)

# Draw
plt.figure(figsize=(12, 8))
nx.draw(B, pos,
        with_labels=True,
        node_size=200,
        font_size=9,
        node_color=['lightblue' if n in actors else 'salmon' for n in B.nodes()])
plt.title("Actor–Movie Bipartite Graph (Top 5 Movies by Cast Size)")
plt.tight_layout()
plt.savefig("bipartite_titles.png")
print("Saved bipartite_titles.png")

print(edge_df.head(100))

