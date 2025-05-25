import pandas as pd
import numpy as np
from itertools import combinations
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv('euromillions.csv', sep=";")

# init empty matrix
# --- NUMBERS (N1 to N5) ---
max_num = 50
co_matrix = np.zeros((max_num, max_num), dtype=int)

# Browse each print run
for _, row in df[['N1', 'N2', 'N3', 'N4', 'N5']].iterrows():
    nums = [row['N1'], row['N2'], row['N3'], row['N4'], row['N5']]
    for a, b in combinations(nums, 2):
        co_matrix[a-1, b-1] += 1
        co_matrix[b-1, a-1] += 1 # symetric matrix

hover_text_num = [[f"Numéros : {i+1} & {j+1}<br>Co-occurrences : {co_matrix[i][j]}"
                   for j in range(max_num)] for i in range(max_num)]
        
# --- STARS (E1 and E2) ---
max_star = 12
star_matrix = np.zeros((max_star, max_star), dtype=int)

for _, row in df[['E1', 'E2']].iterrows():
    e1, e2 = row['E1'], row['E2']
    star_matrix[e1-1, e2-1] += 1
    star_matrix[e2-1, e1-1] += 1

hover_text_star = [[f"Étoiles : {i+1} & {j+1}<br>Co-occurrences : {star_matrix[i][j]}"
                    for j in range(max_star)] for i in range(max_star)]
        
# --- Create Plotly subplots ---
fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=(
        "Matrice interactive des co-occurrences des numéros (N1 à N5)",
        "Matrice interactive des co-occurrences des étoiles (E1 et E2)"
    )
)

# Heatmap numbers
fig.add_trace(go.Heatmap(
    z=co_matrix,
    x=list(range(1, max_num + 1)),
    y=list(range(1, max_num + 1)),
    colorscale='YlGnBu',
    hoverinfo='text',
    text=hover_text_num,
    zauto=False,
    zmin=0,
    zmax=np.max(co_matrix),
    colorbar=dict(title="Co-occurrences des numéros", len=0.4, y=0.75)
), row=1, col=1)

# Heatmap stars
fig.add_trace(go.Heatmap(
    z=star_matrix,
    x=list(range(1, max_star + 1)),
    y=list(range(1, max_star + 1)),
    colorscale='Oranges',
    hoverinfo='text',
    text=hover_text_star,
    zauto=False,
    zmin=0,
    zmax=np.max(star_matrix),
    colorbar=dict(title="Co-occurrences des étoiles", len=0.4, y=0.25)
), row=2, col=1)

# Layout
fig.update_layout(
    height=1600,
    width=1000,
    title_text="Analyse interactive des co-occurrences des tirages EuroMillions",
    showlegend=False
)

fig.update_xaxes(tickmode="linear", dtick=1, row=1, col=1, title="Numéro")
fig.update_yaxes(tickmode="linear", dtick=1, row=1, col=1, title="Numéro")
fig.update_xaxes(tickmode="linear", dtick=1, row=2, col=1, title="Étoile")
fig.update_yaxes(tickmode="linear", dtick=1, row=2, col=1, title="Étoile")

fig.show()
