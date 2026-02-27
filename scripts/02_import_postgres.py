"""
Script d'import PostgreSQL simplifié - 2 tables
Auteur : Anis
Date : Février 2025
"""

import pandas as pd
import psycopg2

DB_CONFIG = {
    'dbname': 'football_db',
    'user': 'anis',
}

def connect_db():
    """Connexion PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Connexion PostgreSQL réussie")
        return conn
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return None

def import_clubs(conn):
    """Importer les 20 clubs"""
    
    print("\n" + "="*80)
    print("🏆 IMPORT DES CLUBS")
    print("="*80)
    
    df = pd.read_csv('data/processed/clubs_aggregated.csv')
    print(f"📥 {len(df)} clubs chargés")
    
    cursor = conn.cursor()
    inserted = 0
    
    for idx, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO clubs (
                    nom, total_joueurs, age_moyen, total_buts, total_assists,
                    contribution_offensive, total_xG, total_npxG, total_xAG,
                    total_minutes, total_cartons_jaunes, total_cartons_rouges,
                    total_courses_progressives, total_passes_progressives,
                    buts_moins_xG, assists_moins_xAG
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['club'], int(row['total_joueurs']), float(row['age']),
                int(row['buts']), int(row['assists']), int(row['contribution_offensive']),
                float(row['xG']), float(row['npxG']), float(row['xAG']),
                int(row['minutes_jouees']), int(row['cartons_jaunes']), int(row['cartons_rouges']),
                int(row['courses_progressives']), int(row['passes_progressives']),
                float(row['buts_moins_xG']), float(row['assists_moins_xAG'])
            ))
            inserted += 1
        except Exception as e:
            print(f"⚠️  Erreur {row['club']}: {e}")
    
    conn.commit()
    print(f"✅ {inserted} clubs insérés")
    cursor.close()

def import_joueurs(conn):
    """Importer les 574 joueurs"""
    
    print("\n" + "="*80)
    print("⚽ IMPORT DES JOUEURS")
    print("="*80)
    
    df = pd.read_csv('data/processed/joueurs_clean.csv')
    print(f"📥 {len(df)} joueurs chargés")
    
    cursor = conn.cursor()
    inserted = 0
    
    for idx, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO joueurs (
                    nom, club, nationalite, poste, age, annee_naissance,
                    matchs_joues, matchs_titulaire, minutes_jouees,
                    buts, assists, buts_hors_penalty, penalties_marques,
                    xG, npxG, xAG, npxG_plus_xAG,
                    courses_progressives, passes_progressives, receptions_progressives,
                    cartons_jaunes, cartons_rouges,
                    buts_per_90, assists_per_90, buts_hors_penalty_per_90,
                    xG_per_90, xAG_per_90, npxG_per_90, contribution_per_90, npxG_plus_xAG_per_90,
                    contribution_offensive, G_minus_xG, A_minus_xAG,
                    minutes_par_match, pct_titulaire, score_impact
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                row['nom'], row['club'], row['nationalite'], row['poste'],
                int(row['age']), int(row['annee_naissance']),
                int(row['matchs_joues']), int(row['matchs_titulaire']), int(row['minutes_jouees']),
                int(row['buts']), int(row['assists']), int(row['buts_hors_penalty']), int(row['penalties_marques']),
                float(row['xG']), float(row['npxG']), float(row['xAG']), float(row['npxG_plus_xAG']),
                int(row['courses_progressives']), int(row['passes_progressives']), int(row['receptions_progressives']),
                int(row['cartons_jaunes']), int(row['cartons_rouges']),
                float(row['buts_per_90']), float(row['assists_per_90']), float(row['buts_hors_penalty_per_90']),
                float(row['xG_per_90']), float(row['xAG_per_90']), float(row['npxG_per_90']),
                float(row['contribution_per_90']), float(row['npxG_plus_xAG_per_90']),
                int(row['contribution_offensive']), float(row['G_minus_xG']), float(row['A_minus_xAG']),
                float(row['minutes_par_match']), float(row['pct_titulaire']), float(row['score_impact'])
            ))
            inserted += 1
            
            if (idx + 1) % 100 == 0:
                print(f"   📊 {idx + 1}/{len(df)} joueurs...")
        
        except Exception as e:
            print(f"⚠️  Erreur {row['nom']}: {e}")
    
    conn.commit()
    print(f"\n✅ {inserted} joueurs insérés")
    cursor.close()

def verify(conn):
    """Vérifications"""
    
    print("\n" + "="*80)
    print("🔍 VÉRIFICATION")
    print("="*80)
    
    cursor = conn.cursor()
    
    # Counts
    cursor.execute("SELECT COUNT(*) FROM clubs")
    print(f"✅ Clubs : {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM joueurs")
    print(f"✅ Joueurs : {cursor.fetchone()[0]}")
    
    # Top 5 buteurs
    print("\n🏆 TOP 5 BUTEURS :")
    cursor.execute("SELECT nom, club, buts FROM joueurs ORDER BY buts DESC LIMIT 5")
    for nom, club, buts in cursor.fetchall():
        print(f"   {nom} ({club}) - {buts} buts")
    
    cursor.close()

def main():
    print("="*80)
    print("🚀 IMPORT POSTGRESQL")
    print("="*80)
    
    conn = connect_db()
    if not conn:
        return
    
    try:
        import_clubs(conn)
        import_joueurs(conn)
        verify(conn)
        
        print("\n" + "="*80)
        print("✅ IMPORT TERMINÉ")
        print("="*80)
        print("\n📊 20 clubs + 574 joueurs importés")
        print("🎯 Prochaine étape : Requêtes SQL (Jour 2)")
        print("="*80)
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()
