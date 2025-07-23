import psycopg2

conn = psycopg2.connect(
    dbname="tmdb",
    user="tmdb",
    password="tmdb",
    host="localhost",
    port=5432
)

with conn.cursor() as cur:
    # Example 1: one movie + its cast
    cur.execute("""
        SELECT m.title, p.name, mc.character_name, mc.cast_order
        FROM movie m
        JOIN movie_cast mc ON m.movie_id = mc.movie_id
        JOIN person p ON p.person_id = mc.person_id
        WHERE m.title ILIKE %s
        ORDER BY mc.cast_order
        LIMIT 10;
    """, ('%Toy Story%',))
    rows = cur.fetchall()
    for r in rows:
        print(r)

    # Example 2: top 10 most cast actors
    cur.execute("""
        SELECT p.name, COUNT(*) AS roles
        FROM movie_cast mc
        JOIN person p ON p.person_id = mc.person_id
        GROUP BY p.person_id, p.name
        ORDER BY roles DESC
        LIMIT 10;
    """)
    print("\nTop 10 actors by roles:")
    for r in cur.fetchall():
        print(r)

conn.close()
