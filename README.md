# Premier League Analytics 2024-25

Plateforme complète d'analyse des performances de la Premier League 2024-25 avec pipeline ETL, base PostgreSQL et dashboards Power BI.

## Table des matières

1. [Objectif](#objectif)
2. [Données](#données)
3. [Stack technique](#stack-technique)
4. [Structure du projet](#structure-du-projet)
5. [Installation](#installation)
6. [Pipeline ETL](#pipeline-etl)
7. [Requêtes SQL](#requêtes-sql)
8. [Dashboards Power BI](#dashboards-power-bi)
9. [Insights clés](#insights-clés)
10. [Compétences démontrées](#compétences-démontrées)

## Objectif

Analyser les performances de 574 joueurs et 20 clubs de Premier League avec :
- Pipeline ETL complet (extraction, transformation, chargement)
- Base de données PostgreSQL relationnelle
- 10 requêtes SQL analytiques avancées
-  dashboards Power BI interactifs

## Données

**Source** : FBref.com (statistiques officielles Premier League)  
**Saison** : 2024-25  
**Volume** : 574 joueurs, 20 clubs  
**Métriques** : 36 colonnes par joueur

**Catégories de statistiques** :
- Identité : nom, club, nationalité, poste, âge
- Temps de jeu : matchs joués, minutes
- Performance offensive : buts, assists, Expected Goals (xG)
- Progression : courses progressives, passes progressives
- Discipline : cartons jaunes, cartons rouges
- Stats normalisées par 90 minutes
- Métriques calculées : overperformance, score impact

## Stack technique

**Langages** :
- Python 3.10+
- SQL (PostgreSQL)
- DAX (Power BI)

**Outils** :
- PostgreSQL 16
- Power BI Desktop
- Git / GitHub

**Bibliothèques Python** :
- pandas 2.1.4 : manipulation données tabulaires
- numpy 1.26.3 : calculs numériques
- psycopg2-binary 2.9.9 : connecteur PostgreSQL

## Structure du projet
```
football-analytics-bi/
├── data/
│   ├── raw/                          
│   │   ├── premier_league_stats_2024-25.csv
│   │   └── fbref_PL_2024-25.csv
│   └── processed/
│       ├── joueurs_clean.csv         (574 × 36 colonnes)
│       └── clubs_aggregated.csv      (20 × 16 colonnes)
│
├── scripts/
│   ├── 00_exploration.py             Analyse exploratoire
│   ├── 01_cleaning_data.py           Nettoyage et feature engineering
│   └── 02_import_postgres.py         Import PostgreSQL
│
├── sql/
│   ├── schema.sql                    Structure BDD (2 tables, 3 vues)
│   └── queries.sql                   10 requêtes analytiques
│
├── powerbi/
│   └── scouts.pbix                   Dashboard scouts (Power BI)
│
├── docs/
│   ├── GLOSSAIRE_STATS_COMPLET.md    Définitions 36 statistiques
│   └── screenshots/                  Captures dashboards
│
├── requirements.txt
└── README.md
```

## Installation

**Prérequis** :
- Python 3.10 ou supérieur
- PostgreSQL 16 ou supérieur
- Power BI Desktop (Windows)

**Étapes** :
```bash
# Cloner le repository
git clone https://github.com/AnissT/premier-league-analytics.git
cd premier-league-analytics

# Installer les dépendances Python
pip install -r requirements.txt --break-system-packages

# Créer la base de données PostgreSQL
createdb -U votre_user football_db

# Exécuter le schéma SQL
psql -U votre_user -d football_db -f sql/schema.sql

# Importer les données
python3 scripts/02_import_postgres.py
```

## Pipeline ETL

### 1. Extraction (00_exploration.py)

Analyse des fichiers CSV bruts :
- Identification des 36 colonnes pertinentes parmi 150+ colonnes
- Détection de 4 joueurs avec valeurs manquantes
- Analyse des types de données

### 2. Transformation (01_cleaning_data.py)

**Nettoyage** :
- Sélection de 30 colonnes pertinentes
- Renommage des colonnes (anglais vers français)
- Correction manuelle de 4 joueurs avec données manquantes
- Conversion des types de données (int, float, str)

**Feature Engineering (6 métriques calculées)** :

1. contribution_offensive = buts + assists
2. G_minus_xG = buts - xG (overperformance buts)
3. A_minus_xAG = assists - xAG (overperformance assists)
4. minutes_par_match = minutes_jouees / matchs_joues
5. pct_titulaire = (matchs_titulaire / matchs_joues) × 100
6. score_impact = buts×2 + assists×1.5 + courses×0.1 + passes×0.1

**Agrégation clubs** :
- Regroupement des 574 joueurs par club
- Calcul des totaux et moyennes par équipe
- Création du fichier clubs_aggregated.csv

**Output** :
- joueurs_clean.csv : 574 joueurs × 36 colonnes
- clubs_aggregated.csv : 20 clubs × 16 colonnes

### 3. Chargement (02_import_postgres.py)

**Actions** :
- Connexion à PostgreSQL avec psycopg2
- Insertion de 20 clubs dans la table clubs
- Insertion de 574 joueurs dans la table joueurs
- Vérifications d'intégrité

**Résultat** : Base PostgreSQL football_db opérationnelle

## Requêtes SQL

10 requêtes analytiques pour répondre à des questions business :

1. **Top 10 buteurs** : Meilleurs finisseurs de la saison
2. **Top 10 passeurs** : Meilleurs créateurs de jeu
3. **Overperformance xG** : Joueurs qui finissent mieux que prévu (buts > xG)
4. **Underperformance xG** : Joueurs qui gaspillent des occasions
5. **Jeunes talents** : Joueurs de moins de 23 ans avec forte contribution
6. **Joueurs polyvalents** : Impact global (buts + assists + progression)
7. **Meilleurs par poste** : Top 3 de chaque position (utilise CTE + Window Function)
8. **Comparaison clubs** : Performance xG vs réalité par équipe
9. **Stats moyennes par poste** : Benchmarks positionnels
10. **Joueurs sous-utilisés** : Bon ratio mais peu de temps de jeu

**Techniques SQL utilisées** :
- Window Functions (ROW_NUMBER, PARTITION BY)
- Common Table Expressions (CTE)
- Agrégations (GROUP BY, AVG, SUM, COUNT)
- Filtres conditionnels complexes

## Dashboards Power BI

### Dashboard Scout (Analyse Joueurs)

**KPIs** :
- Top buteur de la saison
- Top passeur de la saison
- Meilleur overperformance xG

**Filtres dynamiques** :
- Poste (FW, MF, DF, GK)
- Club (20 équipes)
- Âge (17-39 ans)
- Minutes minimum jouées

**Visualisations** :
- Top 10 buteurs (graphique en barres)
- Scatter plot xG vs Buts (identification overperformance)
- Tableau top 20 joueurs (tri dynamique)

**Interactivité** : Cross-filtering complet entre tous les visuels

## Insights clés

### Performance Individuelle

**Mohamed Salah (Liverpool)** :
- 47 contributions (29 buts + 18 assists)
- Overperformance : +3.8 buts vs xG
- Score impact : 114.90

**Bryan Mbeumo (Brentford)** :
- Overperformance exceptionnelle : +7.7 buts vs xG
- 20 buts marqués avec xG de 12.3

**Cole Palmer (Chelsea)** :
- Jeune talent star : 22 ans
- 23 contributions (15 buts + 8 assists)

### Performance Collective

**Liverpool** :
- Meilleure attaque : 150 contributions totales
- 85 buts, 65 assists
- Âge moyen : 25.6 ans

**Nottingham Forest** :
- Plus grande overperformance : +10.3 buts vs xG
- Efficacité exceptionnelle devant le but

**Brentford** :
- Équipe la plus jeune : 24.0 ans moyen
- 2 joueurs dans le top 10 buteurs



## Auteur

Anis  
Projet réalisé : Février 2025

GitHub : https://github.com/AnissT/premier-league-analytics



