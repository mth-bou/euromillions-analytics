import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import combinations

df = pd.read_csv('euromillions.csv', sep=";")

# init empty matrix
max_num = 50
co_matrix = np.zeros((max_num, max_num), dtype=int)

# Browse each print run
for _, row in df[['N1', 'N2', 'N3', 'N4', 'N5']].iterrows():
    nums = [row['N1'], row['N2'], row['N3'], row['N4'], row['N5']]
    for a, b in combinations(nums, 2):
        co_matrix[a-1, b-1] += 1
        co_matrix[b-1, a-1] += 1 # symetric matrix
        
# convert into dataframe for seaborn
co_df = pd.DataFrame(co_matrix, index=range(1, max_num+1), columns=range(1, max_num+1))

# Display heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(co_df, cmap='YlGnBu', square=True, cbar_kws={"label": "Nombre de co-occurrences"})
plt.title("Matrice de co-occurences des numéros (N1 à N5)")
plt.xlabel("Numéro")
plt.ylabel("Numéro")
plt.tight_layout()
plt.show()

# For stars
max_star = 12
star_matrix = np.zeros((max_star, max_star), dtype=int)

for _, row in df[['E1', 'E2']].iterrows():
    e1, e2 = row['E1'], row['E2']
    star_matrix[e1-1, e2-1] += 1
    star_matrix[e2-1, e1-1] += 1
    
star_df = pd.DataFrame(star_matrix, index=range(1, max_star+1), columns=range(1, max_star+1))

plt.figure(figsize=(8, 6))
sns.heatmap(star_df, cmap='Oranges', square=True, annot=True, fmt='d', cbar_kws={"label": "Nombre de co-occurrences"})
plt.title("Matrice de co-occurrence des étoiles (E1 et E2)")
plt.xlabel("Étoile")
plt.ylabel("Étoile")
plt.tight_layout()
plt.show()

