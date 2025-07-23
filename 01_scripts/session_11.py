import pandas as pd
from ast import literal_eval

# -------- Load --------
movies = pd.read_csv("02_datasets/kaggle_movies/movies_metadata.csv", low_memory=False)
credits = pd.read_csv("02_datasets/kaggle_movies/credits.csv", low_memory=False)

# -------- Movies table --------
movies['movie_id'] = pd.to_numeric(movies['id'], errors='coerce')
movies = movies.dropna(subset=['movie_id'])
movies['movie_id'] = movies['movie_id'].astype('int64')

movies['release_date'] = pd.to_datetime(movies['release_date'], errors='coerce')

movie_df = movies[['movie_id', 'title', 'release_date']].drop_duplicates()

# -------- Helper for JSON-ish strings --------
def parse_list(s):
    if pd.isna(s) or s == '':
        return []
    try:
        return literal_eval(s)
    except Exception:
        return []

# -------- Cast & Person tables --------
cast_rows = []
person_rows = []

for _, row in credits[['id', 'cast']].iterrows():
    mid = pd.to_numeric(row['id'], errors='coerce')
    if pd.isna(mid):
        continue
    mid = int(mid)

    for c in parse_list(row['cast']):
        pid = int(c['id'])
        person_rows.append({
            'person_id': pid,
            'name': c.get('name'),
            'gender': c.get('gender')
        })
        cast_rows.append({
            'movie_id': mid,
            'person_id': pid,
            'character_name': c.get('character'),
            'cast_order': c.get('order')
        })

person_df = pd.DataFrame(person_rows).drop_duplicates(subset=['person_id'])
cast_df   = pd.DataFrame(cast_rows).drop_duplicates(subset=['movie_id','person_id'])

print("movie_df:", movie_df.shape)
print("person_df:", person_df.shape)
print("cast_df:", cast_df.shape)
print(movie_df.head(), "\n")
print(person_df.head(), "\n")
print(cast_df.head())

# Clean: drop movies without a title
movie_df = movie_df.dropna(subset=['title'])

# Optional: also ensure person names aren’t null
person_df = person_df.dropna(subset=['name'])

valid_movies = set(movie_df['movie_id'])
cast_df = cast_df[cast_df['movie_id'].isin(valid_movies)]



from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://tmdb:tmdb@localhost:5432/tmdb")

# Load in parent tables first
movie_df.to_sql("movie", engine, if_exists="append", index=False, method="multi", chunksize=5000)
person_df.to_sql("person", engine, if_exists="append", index=False, method="multi", chunksize=5000)

# Then the bridge table
cast_df.to_sql("movie_cast", engine, if_exists="append", index=False, method="multi", chunksize=5000)
