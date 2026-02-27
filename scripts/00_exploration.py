"""
Script d'exploration des données Premier League 2024-25
Objectif : Comprendre la structure des CSV avant nettoyage
Auteur : Anis
Date : Février 2025
"""

import pandas as pd
import numpy as np

def explore_csv(filepath, nom_fichier):
    """Explore un fichier CSV et affiche les infos clés"""
    
    print("\n" + "="*80)
    print(f"📄 EXPLORATION : {nom_fichier}")
    print("="*80)
    
    # Charger le CSV
    df = pd.read_csv(filepath)
    
    # Infos générales
    print(f"\n📊 DIMENSIONS")
    print(f"   Lignes  : {len(df)}")
    print(f"   Colonnes   : {len(df.columns)}")
    
    # Aperçu colonnes
    print(f"\n📋 COLONNES ({len(df.columns)} total)")
    # Afficher toutes les colonnes si < 20, sinon seulement les 20 premières
    if len(df.columns) <= 20:
        print("   Toutes les colonnes :")
        for i, col in enumerate(df.columns, 1):
            print(f"      {i}. {col}")
    else:
        print("   Premières 20 colonnes :")
        for i, col in enumerate(df.columns[:20], 1):
            print(f"      {i}. {col}")
        print(f"   ... et {len(df.columns) - 20} autres colonnes")
    
    # Types de données
    print(f"\n🔢 TYPES DE DONNÉES")
    types_count = df.dtypes.value_counts()
    for dtype, count in types_count.items():
        print(f"   {dtype} : {count} colonnes")
    
    # Valeurs manquantes
    print(f"\n⚠️  VALEURS MANQUANTES")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(1)
    missing_df = pd.DataFrame({
        'Colonnes': missing.index,
        'Manquantes': missing.values,
        'Pourcentage': missing_pct.values
    })
    missing_df = missing_df[missing_df['Manquantes'] > 0].sort_values('Manquantes', ascending=False)
    
    if len(missing_df) > 0:
        print(f"   {len(missing_df)} colonnes avec valeurs manquantes")
        print("\n   Top 10 colonnes avec le plus de valeurs manquantes :")
        for idx, row in missing_df.head(10).iterrows():
            print(f"      {row['Colonnes']}: {row['Manquantes']} ({row['Pourcentage']}%)")
    else:
        print("   ✅ Aucune valeur manquante !")
    
    # Aperçu des données
    print(f"\n👀 APERÇU DES DONNÉES (5 premières lignes)")
    print(df.head().to_string())
    
    # Colonnes importantes identifiées
    print(f"\n🎯 COLONNES CLÉS IDENTIFIÉES")
    colonnes_cles = []
    
    # Chercher colonnes d'identité
    identity_cols = ['Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born']
    for col in identity_cols:
        if col in df.columns:
            colonnes_cles.append(col)
    
    # Chercher colonnes de performance
    perf_cols = ['Goals', 'Assists', 'xG', 'npxG', 'xAG', 'Sh', 'SoT', 'MP', 'Starts', 'Min']
    for col in perf_cols:
        if col in df.columns:
            colonnes_cles.append(col)
    
    print(f"   {len(colonnes_cles)} colonnes clés trouvées :")
    for col in colonnes_cles:
        print(f"      ✓ {col}")
    
    # Stats descriptives sur colonnes numériques
    print(f"\n📈 STATISTIQUES DESCRIPTIVES (colonnes numériques)")
    numeric_cols = df.select_dtypes(include=[np.number]).columns[:5]  # 5 premières
    if len(numeric_cols) > 0:
        print(df[numeric_cols].describe().to_string())
    
    return df

def compare_files(df1, df2):
    """Compare les 2 fichiers pour voir s'ils sont complémentaires"""
    
    print("\n" + "="*80)
    print("🔄 COMPARAISON DES 2 FICHIERS")
    print("="*80)
    
    # Colonnes communes
    common_cols = set(df1.columns) & set(df2.columns)
    print(f"\n📊 Colonnes communes : {len(common_cols)}")
    if len(common_cols) > 0:
        print("   Exemples :", list(common_cols)[:10])
    
    # Colonnes uniques fichier 1
    unique_df1 = set(df1.columns) - set(df2.columns)
    print(f"\n📄 Colonnes uniquement dans fichier 1 : {len(unique_df1)}")
    if len(unique_df1) > 0:
        print("   Exemples :", list(unique_df1)[:10])
    
    # Colonnes uniques fichier 2
    unique_df2 = set(df2.columns) - set(df1.columns)
    print(f"\n📄 Colonnes uniquement dans fichier 2 : {len(unique_df2)}")
    if len(unique_df2) > 0:
        print("   Exemples :", list(unique_df2)[:10])
    


def main():
    """Fonction principale"""
    
    print("="*80)
    print("🚀 EXPLORATION DES DONNÉES PREMIER LEAGUE 2024-25")
    print("="*80)
    
    # Fichier 1
    df1 = explore_csv('data/raw/premier_league_stats_2024-25.csv', 'premier_league_stats_2024-25.csv')
    
    # Fichier 2
    df2 = explore_csv('data/raw/fbref_PL_2024-25.csv', 'fbref_PL_2024-25.csv')
    
    # Comparaison
    compare_files(df1, df2)
    
    # Résumé final
    print("\n" + "="*80)
    print("✅ EXPLORATION TERMINÉE")
    print("="*80)

if __name__ == "__main__":
    main()