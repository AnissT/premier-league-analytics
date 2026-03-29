"""
Script de nettoyage des données Premier League 2024-25
Objectif : Transformer CSV brut en CSV propre pour PostgreSQL
Auteur : Anis
Date : Février 2025
"""

import pandas as pd
import numpy as np

def clean_player_data():
    """Nettoie et enrichit les données joueurs"""

    print("="*80)
    print("NETTOYAGE DES DONNÉES JOUEURS")
    print("="*80)

    # 1. CHARGER LES DONNÉES
    print("\nChargement du fichier brut...")
    df = pd.read_csv('data/raw/fbref_PL_2024-25.csv')
    print(f"   Lignes : {len(df)}")
    print(f"   Colonnes : {len(df.columns)}")

    # 2. SÉLECTIONNER LES COLONNES UTILES (30 colonnes)
    print("\nSélection des colonnes pertinentes...")

    colonnes_a_garder = [
        # Identité (6)
        'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born',
        # Temps de jeu (3)
        'MP', 'Starts', 'Min',
        # Performance offensive (8)
        'Gls', 'Ast', 'G-PK', 'PK', 'xG', 'npxG', 'xAG', 'npxG+xAG',
        # Progression (3)
        'PrgC', 'PrgP', 'PrgR',
        # Discipline (2)
        'CrdY', 'CrdR',
        # Stats par 90 (8)
        'Gls.1', 'Ast.1', 'G-PK.1', 'xG.1', 'xAG.1', 'npxG.1', 'G+A.1', 'npxG+xAG.1'
    ]

    df = df[colonnes_a_garder].copy()
    print(f"   {len(df.columns)} colonnes gardées")

    # 3. RENOMMER LES COLONNES EN CLAIR
    print("\nRenommage des colonnes...")

    df = df.rename(columns={
        # Identité
        'Player': 'nom',
        'Nation': 'nationalite',
        'Pos': 'poste',
        'Squad': 'club',
        'Age': 'age',
        'Born': 'annee_naissance',
        # Temps de jeu
        'MP': 'matchs_joues',
        'Starts': 'matchs_titulaire',
        'Min': 'minutes_jouees',
        # Performance
        'Gls': 'buts',
        'Ast': 'assists',
        'G-PK': 'buts_hors_penalty',
        'PK': 'penalties_marques',
        'xG': 'xG',
        'npxG': 'npxG',
        'xAG': 'xAG',
        'npxG+xAG': 'npxG_plus_xAG',
        # Progression
        'PrgC': 'courses_progressives',
        'PrgP': 'passes_progressives',
        'PrgR': 'receptions_progressives',
        # Discipline
        'CrdY': 'cartons_jaunes',
        'CrdR': 'cartons_rouges',
        # Par 90 min
        'Gls.1': 'buts_per_90',
        'Ast.1': 'assists_per_90',
        'G-PK.1': 'buts_hors_penalty_per_90',
        'xG.1': 'xG_per_90',
        'xAG.1': 'xAG_per_90',
        'npxG.1': 'npxG_per_90',
        'G+A.1': 'contribution_per_90',
        'npxG+xAG.1': 'npxG_plus_xAG_per_90'
    })

    print(f"   Colonnes renommées")

    # 4. GÉRER LES VALEURS MANQUANTES
    print("\nGestion des valeurs manquantes...")

    # Afficher les valeurs manquantes
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if len(missing) > 0:
        print(f"   Colonnes avec valeurs manquantes :")
        for col, count in missing.items():
            print(f"      {col}: {count} ({count/len(df)*100:.1f}%)")

    # CORRIGER LES 4 JOUEURS MANUELLEMENT
    print("\nCorrection manuelle des 4 joueurs...")

    # Olabade Aluko
    df.loc[df['nom'] == 'Olabade Aluko', 'nationalite'] = 'eng ENG'
    df.loc[df['nom'] == 'Olabade Aluko', 'age'] = 18
    df.loc[df['nom'] == 'Olabade Aluko', 'annee_naissance'] = 2006

    # Jake Evans
    df.loc[df['nom'] == 'Jake Evans', 'nationalite'] = 'wls WAL'
    df.loc[df['nom'] == 'Jake Evans', 'age'] = 18
    df.loc[df['nom'] == 'Jake Evans', 'annee_naissance'] = 2006

    # Mateus Mané (attention à l'accent)
    df.loc[df['nom'] == 'Mateus Mane', 'nationalite'] = 'pt POR'
    df.loc[df['nom'] == 'Mateus Mane', 'age'] = 19
    df.loc[df['nom'] == 'Mateus Mane', 'annee_naissance'] = 2005

    # Jeremy Monga
    df.loc[df['nom'] == 'Jeremy Monga', 'nationalite'] = 'be BEL'
    df.loc[df['nom'] == 'Jeremy Monga', 'age'] = 17
    df.loc[df['nom'] == 'Jeremy Monga', 'annee_naissance'] = 2007

    print(f"   4 joueurs corrigés")

    # Remplir les valeurs manquantes restantes (stats numériques)
    colonnes_numeriques = df.select_dtypes(include=[np.number]).columns
    for col in colonnes_numeriques:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(0)

    print(f"   Valeurs manquantes gérées")
    print(f"   Lignes : {len(df)} (aucun joueur supprimé)")

    # 5. CORRIGER LES TYPES
    print("\nCorrection des types de données...")

    df['age'] = df['age'].astype(int)
    df['annee_naissance'] = df['annee_naissance'].astype(int)
    df['matchs_joues'] = df['matchs_joues'].astype(int)
    df['matchs_titulaire'] = df['matchs_titulaire'].astype(int)
    df['minutes_jouees'] = df['minutes_jouees'].astype(int)
    df['buts'] = df['buts'].astype(int)
    df['assists'] = df['assists'].astype(int)
    df['cartons_jaunes'] = df['cartons_jaunes'].astype(int)
    df['cartons_rouges'] = df['cartons_rouges'].astype(int)

    print(f"   Types corrigés")

    # 6. FEATURE ENGINEERING
    print("\nFeature Engineering (6 nouvelles colonnes)...")

    # 6.1 Contribution offensive
    df['contribution_offensive'] = df['buts'] + df['assists']

    # 6.2 Overperformance xG
    df['G_minus_xG'] = (df['buts'] - df['xG']).round(2)

    # 6.3 Overperformance assists
    df['A_minus_xAG'] = (df['assists'] - df['xAG']).round(2)

    # 6.4 Minutes par match (éviter division par zéro)
    df['minutes_par_match'] = np.where(
        df['matchs_joues'] > 0,
        (df['minutes_jouees'] / df['matchs_joues']).round(1),
        0
    )

    # 6.5 Pourcentage titularisations (éviter division par zéro)
    df['pct_titulaire'] = np.where(
        df['matchs_joues'] > 0,
        ((df['matchs_titulaire'] / df['matchs_joues']) * 100).round(1),
        0
    )

    # 6.6 Score impact global
    df['score_impact'] = (
        df['buts'] * 2 +
        df['assists'] * 1.5 +
        df['courses_progressives'] * 0.1 +
        df['passes_progressives'] * 0.1
    ).round(2)

    print(f"   6 nouvelles colonnes créées")
    print(f"   Total colonnes : {len(df.columns)}")

    # 7. TRIER PAR CONTRIBUTION
    df = df.sort_values('contribution_offensive', ascending=False)

    # 8. AFFICHER TOP 10
    print("\nTOP 10 CONTRIBUTEURS :")
    top10 = df[['nom', 'club', 'buts', 'assists', 'contribution_offensive']].head(10)
    print(top10.to_string(index=False))

    # 9. SAUVEGARDER
    print("\nSauvegarde...")
    output_path = 'data/processed/joueurs_clean.csv'
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"   Fichier sauvegardé : {output_path}")
    print(f"   Lignes : {len(df)}")
    print(f"   Colonnes : {len(df.columns)}")

    return df

def create_clubs_aggregated(df_joueurs):
    """Crée le fichier des stats agrégées par club"""

    print("\n" + "="*80)
    print("AGRÉGATION DES STATS PAR CLUB")
    print("="*80)

    # Grouper par club et agréger
    df_clubs = df_joueurs.groupby('club').agg({
        'nom': 'count',
        'age': 'mean',
        'buts': 'sum',
        'assists': 'sum',
        'contribution_offensive': 'sum',
        'xG': 'sum',
        'npxG': 'sum',
        'xAG': 'sum',
        'minutes_jouees': 'sum',
        'cartons_jaunes': 'sum',
        'cartons_rouges': 'sum',
        'courses_progressives': 'sum',
        'passes_progressives': 'sum'
    }).rename(columns={'nom': 'total_joueurs'})

    # Arrondir les moyennes
    df_clubs['age'] = df_clubs['age'].round(1)
    df_clubs['xG'] = df_clubs['xG'].round(2)
    df_clubs['npxG'] = df_clubs['npxG'].round(2)
    df_clubs['xAG'] = df_clubs['xAG'].round(2)

    # Ajouter des colonnes calculées
    df_clubs['buts_moins_xG'] = (df_clubs['buts'] - df_clubs['xG']).round(2)
    df_clubs['assists_moins_xAG'] = (df_clubs['assists'] - df_clubs['xAG']).round(2)

    # Réinitialiser l'index
    df_clubs = df_clubs.reset_index()

    # Trier par contribution offensive
    df_clubs = df_clubs.sort_values('contribution_offensive', ascending=False)

    # Sauvegarder
    output_path = 'data/processed/clubs_aggregated.csv'
    df_clubs.to_csv(output_path, index=False, encoding='utf-8')

    print(f"\nFichier clubs agrégé créé : {output_path}")
    print(f"   Lignes : {len(df_clubs)}")
    print(f"   Colonnes : {len(df_clubs.columns)}")

    # Afficher top 5
    print("\nTOP 5 CLUBS PAR CONTRIBUTION OFFENSIVE :")
    top5 = df_clubs[['club', 'total_joueurs', 'age', 'buts', 'assists', 'contribution_offensive']].head()
    print(top5.to_string(index=False))

    return df_clubs

def main():
    """Fonction principale"""

    print("="*80)
    print("NETTOYAGE DONNÉES PREMIER LEAGUE 2024-25")
    print("="*80)

    # Nettoyer données joueurs
    df_joueurs = clean_player_data()

    # Créer agrégation clubs
    df_clubs = create_clubs_aggregated(df_joueurs)

    # Résumé
    print("\n" + "="*80)
    print("NETTOYAGE TERMINÉ")
    print("="*80)
    print(f"\nRésumé :")
    print(f"   Joueurs : {len(df_joueurs)} lignes, {len(df_joueurs.columns)} colonnes")
    print(f"   Clubs   : {len(df_clubs)} lignes, {len(df_clubs.columns)} colonnes")
    print(f"\nFichiers créés :")
    print(f"   - data/processed/joueurs_clean.csv")
    print(f"   - data/processed/clubs_aggregated.csv")
    print("\nProchaine étape : PostgreSQL (script 02_import_postgres.py)")
    print("="*80)

if __name__ == "__main__":
    main()
