import pandas as pd

df = pd.read_csv('data/raw/fbref_PL_2024-25.csv')

print("="*60)
print(f"TOUTES LES COLONNES ({len(df.columns)} total)")
print("="*60)

for i, col in enumerate(df.columns, 1):
    print(f"{i:3}. {col}")

