import pandas as pd
import numpy as np
import plotly.graph_objects as go

df = pd.read_csv('euromillions.csv', sep=";")

df['DATE'] = pd.to_datetime(df['DATE'])
df['YEAR'] = df['DATE'].dt.year

numbers_per_year = []

for _, row in df.iterrows():
    year = row['YEAR']
    numbers = [row['N1'], row['N2'], row['N3'], row['N4'], row['N5']]
    for number in numbers:
        numbers_per_year.append((year, number))
        
df_freq = pd.DataFrame(numbers_per_year, columns=['YEAR', 'NUMBER'])

# frequency table per year and number
freq_table = df_freq.groupby(['YEAR', 'NUMBER']).size().unstack(fill_value=0)

hover_text = []
for year in freq_table.index:
    row = []
    for num in freq_table.columns:
        count = freq_table.loc[year, num]
        row.append(f"Année : {year}<br>Numéro : {num}<br>Occurrences : {count}")
    hover_text.append(row)

# Interactive heatmap
fig = go.Figure(data=go.Heatmap(
    z=freq_table.values,
    x=freq_table.columns,
    y=freq_table.index,
    text=hover_text,
    hoverinfo='text',
    colorscale='YlGnBu',
    colorbar=dict(title="Occurrences")
))

fig.update_layout(
    title='🔥 Fréquence d’apparition des numéros par année',
    xaxis=dict(title="Numéro", tickmode="linear", dtick=1),
    yaxis=dict(title="Année"),  # to display years from recent to oldest
    height=800,
    width=1100
)

fig.show()

mean_per_year = freq_table.mean(axis=0).sort_values(ascending=False)
print("\nFréquence moyenne d'apparition des numéros par année (décroissant) :")
print(mean_per_year)

variance_per_year = freq_table.var(axis=0).sort_values(ascending=False)
print("\nVariance de la fréquence d'apparition des numéros par année (décroissant) :")
print(variance_per_year)
