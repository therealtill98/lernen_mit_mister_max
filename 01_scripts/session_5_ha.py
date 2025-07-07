import sys

import pandas
import plotly.express as px
import json
import plotly.io as pio
pio.templates.default = None
print("Imports OK")

# Read data
df = pandas.read_csv("datasets/dataset_homework_session_4.csv")
print("Data loaded")

# Prepare columns
plz: pandas.Series = df["postleitzahl"].dropna().astype(int)
hausnummer: pandas.Series = df["hausnummer"].dropna().astype(int)

# Understand how many different Postleitzahlen we have
plz_counts: pandas.Series = plz.value_counts().sort_index()
plz_df = plz_counts.reset_index()
plz_df.columns = ["Postleitzahl", "Anzahl"]

# Understand how many >53 values we have per Postleitzahl
filtered_df = df[df["hausnummer"] > 53]
greater_53_counts = filtered_df.groupby("postleitzahl").size().sort_index()

# Merge counts into one dataframe
plz_df = plz_df.merge(greater_53_counts.rename(">53"),how="left", left_on="Postleitzahl", right_index=True)

# Fill NaN with 0 and calculate percentage
plz_df[">53"] = plz_df[">53"].fillna(0).astype(int)
plz_df["Anteil (%)"] = ((plz_df[">53"] / plz_df["Anzahl"]) * 100).round(2)

# Print the result
print("Verteilung der Hausnummern pro Postleitzahl:")
print(plz_df.to_string(index=False))

# Load geojson
with open("datasets/rostock_plz.geojson") as f:
    geojson = json.load(f)
print("Geojson loaded")

plz_df["Postleitzahl"] = plz_df["Postleitzahl"].astype(str)

# Generate map
fig = px.choropleth_map(
    plz_df,
    geojson=geojson,
    locations="Postleitzahl",
    color="Anteil (%)",
    featureidkey="properties.postleitzahl",
    center={"lat": 54.088, "lon": 12.132},
    zoom=10,
    opacity=0.6,
    color_continuous_scale="Greens",
    hover_name="Postleitzahl",
    hover_data={">53": True, "Anteil (%)": ":.2f"},
    template="plotly_white",
    map_style="carto-positron"
)

fig.update_layout(
    margin={"r":0, "t":0, "l":0, "b":0},
    title="Anteil der Hausnummern >53 pro PLZ in Rostock"
)

pio.renderers.default = "browser"

fig.show()