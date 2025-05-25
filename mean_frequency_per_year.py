import pandas as pd
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

hover_text = [
    [f"Année : {year}<br>Numéro : {num}<br>Occurrences : {freq_table.loc[year, num]}"
     for num in freq_table.columns]
    for year in freq_table.index
]

fig = go.Figure(data=go.Heatmap(
    z=freq_table.values,
    x=freq_table.columns,
    y=freq_table.index,
    text=hover_text,
    hoverinfo='text',
    colorscale='YlGnBu',
    colorbar=dict(title="Occurrences (numéros)")
))

fig.update_layout(
    title='Fréquence d’apparition des NUMÉROS par année',
    xaxis=dict(title="Numéro", tickmode="linear", dtick=1),
    yaxis=dict(title="Année"),
    height=800,
    width=1100
)

fig.show()

mean_per_year = freq_table.mean(axis=0).sort_values(ascending=False)
variance_per_year = freq_table.var(axis=0).sort_values(ascending=False)

print("\nFréquence moyenne d'apparition des NUMÉROS par année (décroissant) :")
print(mean_per_year)

print("\nVariance de la fréquence d'apparition des NUMÉROS par année (décroissant) :")
print(variance_per_year)


# ---------------- STAR NUMBERS ----------------
stars_per_year = []

for _, row in df.iterrows():
    year = row['YEAR']
    stars = [row['E1'], row['E2']]
    for star in stars:
        stars_per_year.append((year, star))

df_star = pd.DataFrame(stars_per_year, columns=['YEAR', 'STAR'])
freq_table_star = df_star.groupby(['YEAR', 'STAR']).size().unstack(fill_value=0)

hover_text_star = [
    [f"Année : {year}<br>Étoile : {star}<br>Occurrences : {freq_table_star.loc[year, star]}"
     for star in freq_table_star.columns]
    for year in freq_table_star.index
]

fig_star = go.Figure(data=go.Heatmap(
    z=freq_table_star.values,
    x=freq_table_star.columns,
    y=freq_table_star.index,
    text=hover_text_star,
    hoverinfo='text',
    colorscale='Oranges',
    colorbar=dict(title="Occurrences (étoiles)")
))

fig_star.update_layout(
    title="Fréquence d’apparition des numéros étoile par année",
    xaxis=dict(title="Étoile", tickmode="linear", dtick=1),
    yaxis=dict(title="Année"),
    height=600,
    width=800
)

fig_star.show()

mean_star = freq_table_star.mean(axis=0).sort_values(ascending=False)
variance_star = freq_table_star.var(axis=0).sort_values(ascending=False)

print("\nMoyenne annuelle d'apparition des ÉTOILES (décroissant) :")
print(mean_star)

print("\nVariance annuelle d'apparition des ÉTOILES (décroissant) :")
print(variance_star)
