import plotly.express as px
from pandas import DataFrame

df: DataFrame = px.data.tips()

sorted_df = df.sort_values("total_bill", ascending=False)
df.sort_values("total_bill", ascending=False,inplace=True)
print(sorted_df.head(20))
# fig = px.scatter(
   #  df, x='total_bill', y='tip', opacity=0.65,
   #  trendline='ols', trendline_color_override='darkblue'
# )
# fig.show()