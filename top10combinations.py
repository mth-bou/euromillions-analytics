import pandas as pd
from collections import Counter

df = pd.read_csv('euromillions.csv', sep=";")

def get_top_combinations(counter: Counter, top_n: int = 10, min_occurences: int = 2):
    return [
        {
            "combination": [int(n) for n in sorted(list(comb))],
            "occurences": count
        }
        for comb, count in counter.items()
        if count >= min_occurences
    ][:top_n]
    
# --- TOP 10 numbers ---
num_combinations = [frozenset(row) for row in df[['N1', 'N2', 'N3', 'N4', 'N5']].values]
num_counter = Counter(num_combinations)
top_numbers = get_top_combinations(num_counter)

# --- TOP 10 stars ---
star_combinations = [frozenset(row) for row in df[['E1', 'E2']].values]
star_counter = Counter(star_combinations)
top_stars = get_top_combinations(star_counter)
top_stars = sorted(top_stars, key=lambda x: x['occurences'], reverse=True)

# --- TOP 10 numbers + stars ---
full_combinations = [
    frozenset(list(row[['N1', 'N2', 'N3', 'N4', 'N5']]) + list(row[['E1', 'E2']]))
    for _, row in df.iterrows()
]
full_counter = Counter(full_combinations)
top_full = get_top_combinations(full_counter)

# --- Display console ---
print("Top 10 combinaisons NUMÉROS avec occurrences > 1 :")
for item in top_numbers:
    print(f"{item['combination']} → {item['occurences']} fois")

print("\nTop 10 combinaisons ÉTOILES avec occurrences > 1 :")
for item in top_stars:
    print(f"{item['combination']} → {item['occurences']} fois")

print("\nTop 10 combinaisons NUMÉROS + ÉTOILES avec occurrences > 1 :")
for item in top_full:
    print(f"{item['combination']} → {item['occurences']} fois")