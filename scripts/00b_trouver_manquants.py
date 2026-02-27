"""
Script pour identifier les joueurs avec données manquantes
"""

import pandas as pd

# Charger le fichier
df = pd.read_csv('data/raw/fbref_PL_2024-25.csv')

print("="*80)
print("🔍 JOUEURS AVEC DONNÉES MANQUANTES")
print("="*80)

# Chercher les lignes avec valeurs manquantes dans Nation, Age, ou Born
mask = df[['Nation', 'Age', 'Born']].isnull().any(axis=1)
joueurs_manquants = df[mask]

print(f"\n📊 Nombre de joueurs avec données manquantes : {len(joueurs_manquants)}")

if len(joueurs_manquants) > 0:
    print("\n👤 LISTE DES JOUEURS :\n")
    
    for idx, row in joueurs_manquants.iterrows():
        print(f"Joueur #{idx + 1}")
        print(f"   Nom     : {row['Player']}")
        print(f"   Club    : {row['Squad']}")
        print(f"   Poste   : {row['Pos']}")
        print(f"   Nation  : {row['Nation'] if pd.notna(row['Nation']) else '❌ MANQUANT'}")
        print(f"   Age     : {row['Age'] if pd.notna(row['Age']) else '❌ MANQUANT'}")
        print(f"   Born    : {row['Born'] if pd.notna(row['Born']) else '❌ MANQUANT'}")
        print(f"   Matchs  : {row['MP']}")
        print(f"   Minutes : {row['Min']}")
        print()

else:
    print("\n✅ Aucun joueur avec données manquantes !")

print("="*80)

