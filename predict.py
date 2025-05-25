import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

df = pd.read_csv('euromillions.csv', sep=";")

number_columns = ['N1', 'N2', 'N3', 'N4', 'N5']

all_numbers = df[number_columns].values.flatten()

number_counts = Counter(all_numbers)

number_counts_sorted = dict(sorted(number_counts.items()))

# histogramme
plt.figure(figsize=(14, 6))
plt.bar(number_counts_sorted.keys(), number_counts_sorted.values(), color='skyblue')
plt.title('Fréquence d\'apparition des numéros principaux')
plt.xlabel('Numéros')
plt.ylabel('Fréquence')
plt.xticks(np.arange(min(number_counts_sorted.keys()), max(number_counts_sorted.keys()) + 1))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Star numbers
star_columns = ['E1', 'E2']

all_stars = df[star_columns].values.flatten()

star_counts = Counter(all_stars)
star_counts_sorted = dict(sorted(star_counts.items()))

plt.figure(figsize=(10, 4))
plt.bar(star_counts_sorted.keys(), star_counts_sorted.values(), color='orange')
plt.title("Fréquence d'apparition des étoiles (E1 et E2)")
plt.xlabel("Étoile")
plt.ylabel("Nombre d'apparitions")
plt.xticks(np.arange(min(star_counts_sorted.keys()), max(star_counts_sorted.keys()) + 1))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
