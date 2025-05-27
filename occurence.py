import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv('euromillions.csv', sep=";")

# --- NUMBERS ---
number_columns = ['N1', 'N2', 'N3', 'N4', 'N5']
all_numbers = df[number_columns].values.flatten()
number_counts = Counter(all_numbers)
number_counts_sorted = dict(sorted(number_counts.items()))

# --- STAR NUMBERS ---
star_columns = ['E1', 'E2']
all_stars = df[star_columns].values.flatten()
star_counts = Counter(all_stars)
star_counts_sorted = dict(sorted(star_counts.items()))

# histogramme
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Fréquence des numéros (N1 à N5)", "Fréquence des étoiles (E1 et E2)")
)

# Bar plot numbers
fig.add_trace(go.Bar(
    x=list(number_counts_sorted.keys()),
    y=list(number_counts_sorted.values()),
    marker_color='skyblue',
    hovertemplate='Numéro %{x}<br>Occurences : %{y}<extra></extra>'
), row=1, col=1)

fig.add_trace(go.Bar(
    x=list(star_counts_sorted.keys()),
    y=list(star_counts_sorted.values()),
    marker_color='orange',
    hovertemplate='Etoile %{x}<br>Occurences : %{y}<extra></extra>'
), row=1, col=2)

fig.update_layout(
    title="Analyse des fréquences d'apparitions des numéros et étoiles",
    autosize=True,
    height=None,
    margin=dict(l=40, r=40, t=80, b=40),
    showlegend=False
)

fig.update_xaxes(title="Numéro", tickmode="linear", dtick=1, row=1, col=1)
fig.update_yaxes(title="Occurences", row=1, col=1)
fig.update_xaxes(title="Etoile", tickmode="linear", dtick=1, row=1, col=2)
fig.update_yaxes(title="Occurences", row=1, col=2)

fig.show()
