print("starting script")
import pandas
print("pandas imported")
import plotly.graph_objects as plotly
print("plotly imported")
import plotly.io as plotlybrowser
print("plotly.io imported")


plotlybrowser.renderers.default = "browser"
print("Browser set")

# Read data
df = pandas.read_csv("datasets/dataset_homework_session_4.csv")

print(df.head())
print(df.info())

# Finding interesting data

numeric = df.select_dtypes(include=["int64", "float64"])
print(numeric.columns)

# Understanding values for hausnummer

hausnummer = df["hausnummer"].dropna().astype(int)

print("Min Hausnummer:",   hausnummer.min())
print("Max Hausnummer:",   hausnummer.max())
print("Summary stats:\n", hausnummer.describe())

p90 = hausnummer.quantile(0.90)
print(f"90th percentile: {p90}")

# Convert Int into Str based on Int Value

df["hausgruppe"] = df["hausnummer"].apply(lambda x: str(x) if x <= 53 else ">53")

print("data conversion done")

# Define order

cat_order = []
for i in range(1, 54):
    value_to_write =str(i)
    cat_order.append(value_to_write)
cat_order.append(">53")

print("order done")

# Visualize hausnummer distribution with plotly

fig = plotly.Figure(
    data=[
        plotly.Histogram(
            x=df["hausgruppe"],
            nbinsx=52
        )
    ]
)

fig.update_layout(
    title="Verteilung der Hausnummern",
    xaxis=dict(
        title="Hausnummer",
        categoryorder="array",
        categoryarray=cat_order  # your manually defined order
    ),
    yaxis_title="Anzahl"
)

fig.show()