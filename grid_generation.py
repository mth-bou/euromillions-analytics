import pandas as pd
import numpy as np
from collections import Counter
from itertools import combinations

df = pd.read_csv('euromillions.csv', sep=";")

# --- Main Numbers ---
number_cols = ['N1', 'N2', 'N3', 'N4', 'N5']
all_numbers = df[number_cols].values.flatten()
number_counts = Counter(all_numbers)
number_freq = pd.Series(number_counts).sort_values(ascending=False)

# Cooccurrence matrix for numeros
max_num = 50
co_matrix = np.zeros((max_num, max_num), dtype=int)

for _, row in df[number_cols].iterrows():
    nums = [row[col] for col in number_cols]
    for a, b in combinations(nums, 2):
        co_matrix[a-1, b-1] += 1
        co_matrix[b-1, a-1] += 1

# combined score : frequency * average of the 5 highest co-occurrences
number_scores = []
for num in number_freq.index:
    co_row = co_matrix[num - 1]
    co_values = sorted([co_row[i] for i in range(max_num) if i != (num - 1)], reverse=True)[:5]
    mean_co = np.mean(co_values) if co_values else 0
    score = number_freq[num] * mean_co
    number_scores.append((num, number_freq[num], mean_co, score))

number_scores_df = pd.DataFrame(number_scores, columns=["Num", "Freq", "Mean", "Score"])
number_scores_df = number_scores_df.sort_values(by="Score", ascending=False)

# --- Star Num ---
star_cols = ['E1', 'E2']
all_stars = df[star_cols].values.flatten()
star_counts = Counter(all_stars)
star_freq = pd.Series(star_counts).sort_values(ascending=False)

max_star = 12
co_matrix_star = np.zeros((max_star, max_star), dtype=int)

for _, row in df[star_cols].iterrows():
    s1, s2 = row['E1'], row['E2']
    co_matrix_star[s1-1, s2-1] += 1
    co_matrix_star[s2-1, s1-1] += 1

# Combined score for stars
star_scores = []
for star in star_freq.index:
    co_row = co_matrix_star[star - 1]
    co_values = sorted([co_row[i] for i in range(max_star) if i != (star - 1)], reverse=True)[:1]
    mean_co = np.mean(co_values) if co_values else 0
    score = star_freq[star] * mean_co
    star_scores.append((star, star_freq[star], mean_co, score))

star_scores_df = pd.DataFrame(star_scores, columns=['Star', 'Freq', 'Mean', 'Score'])
star_scores_df = star_scores_df.sort_values(by='Score', ascending=False)

# --- Grid suggestions ---
suggested_numbers = sorted(number_scores_df.head(5)['Num'].astype(int).tolist())
suggested_stars = sorted(star_scores_df.head(2)['Star'].astype(int).tolist())

print("Suggested grid : ")
print('Nums : ', suggested_numbers)
print('Stars : ', suggested_stars)
