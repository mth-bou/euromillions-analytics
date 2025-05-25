import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv('euromillions.csv', sep=";")

df['DATE'] = pd.to_datetime(df['DATE'])
df['YEAR'] = df['DATE'].dt.year

# --- NUMBERS ---
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

# --- STAR NUMBERS ---
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

# ---------- SUBPLOTS ----------
fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=[
        "Fréquence des NUMÉROS par année",
        "Fréquence des ÉTOILES par année"
    ]
)

# Heatmap NUMBERS
fig.add_trace(go.Heatmap(
    z=freq_table.values,
    x=freq_table.columns,
    y=freq_table.index,
    text=hover_text,
    hoverinfo='text',
    colorscale='YlGnBu',
    colorbar=dict(title="Occurrences (numéros)", len=0.45, y=0.78)
), row=1, col=1)

# Heatmap STARS
fig.add_trace(go.Heatmap(
    z=freq_table_star.values,
    x=freq_table_star.columns,
    y=freq_table_star.index,
    text=hover_text_star,
    hoverinfo='text',
    colorscale='Oranges',
    colorbar=dict(title="Occurrences (étoiles)", len=0.45, y=0.22)
), row=2, col=1)

# Layout
fig.update_layout(
    height=1400,
    width=1100,
    title_text="Fréquences annuelles des numéros et étoiles EuroMillions",
)

# Axes X/Y
fig.update_xaxes(title_text="Numéro", tickmode="linear", dtick=1, row=1, col=1)
fig.update_yaxes(title_text="Année", row=1, col=1)
fig.update_xaxes(title_text="Étoile", tickmode="linear", dtick=1, row=2, col=1)
fig.update_yaxes(title_text="Année", row=2, col=1)

fig.show()

# ---------- ANALYTICS ----------
mean_per_year = freq_table.mean(axis=0).sort_values(ascending=False)
variance_per_year = freq_table.var(axis=0).sort_values(ascending=False)
mean_star = freq_table_star.mean(axis=0).sort_values(ascending=False)
variance_star = freq_table_star.var(axis=0).sort_values(ascending=False)

print("\nMoyenne annuelle d'apparition des NUMÉROS :")
print(mean_per_year)

print("\nVariance annuelle d'apparition des NUMÉROS :")
print(variance_per_year)

print("\nMoyenne annuelle d'apparition des ÉTOILES :")
print(mean_star)

print("\nVariance annuelle d'apparition des ÉTOILES :")
print(variance_star)