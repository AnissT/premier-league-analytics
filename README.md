# ⚽ Premier League Analytics 2024-25

**Plateforme complète d'analyse football avec PostgreSQL, SQL avancé et Power BI**

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![Power BI](https://img.shields.io/badge/Power_BI-Desktop-yellow)

---

## 🎯 Objectif

Analyser les performances de 574 joueurs et 20 clubs de Premier League 2024-25 avec :
- Pipeline ETL complet (nettoyage, transformation, chargement)
- Base PostgreSQL relationnelle optimisée
- 10 requêtes SQL analytiques avancées
- 2 dashboards Power BI interactifs

---

## 📊 Données

- **Source :** FBref.com (statistiques officielles Premier League)
- **Saison :** 2024-25
- **Joueurs :** 574
- **Clubs :** 20
- **Métriques :** 36 colonnes (buts, assists, xG, progression, discipline, etc.)

---

## 🛠️ Stack Technique

**Langages :**
- Python 3.10+
- SQL
- DAX (Power BI)

**Outils :**
- PostgreSQL 16
- Power BI Desktop
- Git/GitHub

**Bibliothèques Python :**
```
pandas==2.1.4
numpy==1.26.3
psycopg2-binary==2.9.9
```

---

## 📁 Structure du Projet
```
football-analytics-bi/
├── data/
│   ├── raw/                          # CSV originaux
│   └── processed/                    # CSV nettoyés
│       ├── joueurs_clean.csv         # 574 joueurs × 36 colonnes
│       └── clubs_aggregated.csv      # 20 clubs agrégés
│
├── scripts/
│   ├── 00_exploration.py            # Analyse exploratoire
│   ├── 01_cleaning_data.py          # Nettoyage + feature engineering
│   └── 02_import_postgres.py        # Import PostgreSQL
│
├── sql/
│   ├── schema.sql                   # Structure BDD (2 tables, 3 vues)
│   └── queries.sql                  # 10 requêtes analytiques
│
├── powerbi/
│   ├── dashboard_scout.pbix         # Dashboard joueurs
│   └── dashboard_club.pbix          # Dashboard clubs
│
├── docs/
│   ├── GLOSSAIRE_STATS_COMPLET.md   # Définitions 36 stats
│   ├── PRESENTATION_PROJET.md       # Présentation complète
│   └── screenshots/                 # Captures dashboards
│
└── README.md                        # Ce fichier
```

---

## 🚀 Installation

### Prérequis

- Python 3.10+
- PostgreSQL 16+
- Power BI Desktop (Windows)

### Setup
```bash
# Cloner le repo
git clone https://github.com/AnissT/premier-league-analytics.git
cd premier-league-analytics

# Installer les dépendances
pip install -r requirements.txt --break-system-packages

# Créer la base PostgreSQL
createdb -U anis football_db

# Exécuter le schéma
psql -U anis -d football_db -f sql/schema.sql

# Importer les données
python3 scripts/02_import_postgres.py
```

---

## 📈 Pipeline ETL

### 1. Exploration (`00_exploration.py`)
- Analyse 2 CSV (150+ colonnes brutes)
- Identification valeurs manquantes
- Sélection colonnes pertinentes

### 2. Nettoyage (`01_cleaning_data.py`)
- **Réduction :** 150+ colonnes → 40 colonnes pertinentes
- **Correction :** 4 joueurs avec données manquantes
- **Feature Engineering :** 6 métriques calculées
  - `contribution_offensive` = buts + assists
  - `G_minus_xG` = overperformance buts
  - `A_minus_xAG` = overperformance assists
  - `minutes_par_match`
  - `pct_titulaire`
  - `score_impact` (pondéré)
- **Output :** `joueurs_clean.csv` + `clubs_aggregated.csv`

### 3. Modélisation PostgreSQL (`schema.sql`)
- **2 tables :**
  - `clubs` (20 lignes) : stats agrégées par équipe
  - `joueurs` (574 lignes) : identité + toutes stats
- **6 index** pour optimisation requêtes
- **3 vues SQL :** top_buteurs, jeunes_talents, clubs_complet

### 4. Import (`02_import_postgres.py`)
- Lecture CSV propres
- Insertion PostgreSQL
- Vérifications intégrité

---

## 🔍 Requêtes SQL Analytiques

**10 analyses business prêtes à l'emploi :**

1. **Top 10 buteurs** - Meilleurs finisseurs
2. **Top 10 passeurs** - Meilleurs créateurs
3. **Overperformance xG** - Finisseurs exceptionnels (buts > xG attendu)
4. **Underperformance xG** - Joueurs gaspillant occasions
5. **Jeunes talents** - <23 ans, forte contribution
6. **Joueurs polyvalents** - Impact global (buts + assists + progression)
7. **Meilleurs par poste** - Top 3 chaque position (CTE avancée)
8. **Comparaison clubs** - xG vs réalité par équipe
9. **Stats moyennes par poste** - Benchmarks positionnels
10. **Joueurs sous-utilisés** - Bon ratio mais peu de minutes

**Techniques SQL utilisées :**
- Window functions (ROW_NUMBER, PARTITION BY)
- CTEs (Common Table Expressions)
- Agrégations (GROUP BY, AVG, SUM)
- Jointures
- Filtres conditionnels complexes

---

## 📊 Dashboards Power BI

### Dashboard Scout (Analyse Joueurs)
- **KPIs :** Top buteur, top passeur, meilleur overperformance xG
- **Filtres :** Poste, Club, Âge, Minutes min
- **Visualisations :**
  - Top 10 buteurs (barres)
  - Scatter plot xG vs Buts (overperformance)
  - Tableau top 20 (tri dynamique)
  - Efficacité tirs
- **Interactivité :** Cross-filtering complet

### Dashboard Club (Analyse Équipes)
- **KPIs :** Leader, meilleure attaque, plus jeune équipe
- **Visualisations :**
  - Classement buts par club
  - Scatter xG total vs Buts totaux
  - Tableau clubs (buts, assists, âge moyen)
  - Top 5 overperformance xG clubs

---

## 💡 Insights Clés

### Performance Individuelle
- **Mohamed Salah** : 47 contributions (29 buts + 18 assists), overperformance +3.8
- **Bryan Mbeumo** : Overperformance exceptionnelle (+7.7 buts vs xG)
- **Cole Palmer** : Jeune talent star (22 ans, 23 contributions)

### Performance Collective
- **Liverpool** : Meilleure attaque (150 contributions totales)
- **Nottingham Forest** : Plus grande overperformance (+10.3 buts vs xG)
- **Brentford** : Équipe la plus jeune (24.0 ans moyen)

---

## 📚 Documentation

- **[GLOSSAIRE_STATS_COMPLET.md](docs/GLOSSAIRE_STATS_COMPLET.md)** - Définitions 36 statistiques
- **[PRESENTATION_PROJET.md](docs/PRESENTATION_PROJET.md)** - Présentation technique complète

---

## 🎯 Compétences Démontrées

- ✅ **ETL** : Pipeline complet Extract-Transform-Load
- ✅ **Data Cleaning** : Gestion valeurs manquantes, normalisation
- ✅ **Feature Engineering** : Création métriques business
- ✅ **SQL Avancé** : Window functions, CTEs, optimisation
- ✅ **Modélisation BDD** : Schéma relationnel, index, contraintes
- ✅ **Business Intelligence** : Dashboards interactifs, storytelling
- ✅ **Version Control** : Git, commits structurés

---

## 👨‍💻 Auteur

**Anis**  
Étudiant L3 Informatique 
Projet réalisé : Février 2025

**GitHub :** [@AnissT](https://github.com/AnissT)

---




