#  GLOSSAIRE DES STATISTIQUES - VERSION COURTE

**Projet :** Premier League Analytics 2024-25  
**Fichiers :** fbref_PL_2024-25.csv → joueurs_clean.csv (574 joueurs × 36 colonnes)

---

##  IDENTITÉ (6 colonnes)

| Colonne | Avant | Définition |
|---------|-------|------------|
| `nom` | Player | Nom complet du joueur |
| `nationalite` | Nation | Code pays (ex: "eng ENG", "no NOR") |
| `poste` | Pos | Position : FW (Attaquant), MF (Milieu), DF (Défenseur), GK (Gardien) |
| `club` | Squad | Nom de l'équipe |
| `age` | Age | Âge en années |
| `annee_naissance` | Born | Année de naissance |

---

##  TEMPS DE JEU (3 colonnes)

| Colonne | Avant | Définition |
|---------|-------|------------|
| `matchs_joues` | MP | Nombre de matchs disputés (max 38) |
| `matchs_titulaire` | Starts | Matchs commencés comme titulaire |
| `minutes_jouees` | Min | Total minutes jouées dans la saison |

---

##  PERFORMANCE OFFENSIVE (8 colonnes)

| Colonne | Avant | Définition |
|---------|-------|------------|
| `buts` | Gls | Nombre de buts marqués |
| `assists` | Ast | Nombre de passes décisives |
| `buts_hors_penalty` | G-PK | Buts marqués sans compter les penalties |
| `penalties_marques` | PK | Penalties transformés |
| `xG` | xG | **Expected Goals** : buts attendus selon qualité des occasions |
| `npxG` | npxG | xG sans penalties |
| `xAG` | xAG | **Expected Assists** : passes décisives attendues |
| `npxG_plus_xAG` | npxG+xAG | Somme npxG + xAG (contribution offensive attendue) |

** xG expliqué simplement :**
- xG = 10, Buts = 12 → Joueur finit bien (+2 overperformance)
- xG = 10, Buts = 7 → Joueur gaspille (-3 underperformance)

---

##  PROGRESSION (3 colonnes)

| Colonne | Avant | Définition |
|---------|-------|------------|
| `courses_progressives` | PrgC | Courses avec ballon qui font progresser vers le but adverse |
| `passes_progressives` | PrgP | Passes qui font progresser vers le but adverse |
| `receptions_progressives` | PrgR | Réceptions de balle en zones dangereuses |

---

##  DISCIPLINE (2 colonnes)

| Colonne | Avant | Définition |
|---------|-------|------------|
| `cartons_jaunes` | CrdY | Nombre de cartons jaunes reçus |
| `cartons_rouges` | CrdR | Nombre de cartons rouges reçus |

---

##  STATS NORMALISÉES PAR 90 MINUTES (8 colonnes)

**Pourquoi "par 90" ?** Pour comparer équitablement joueurs avec temps de jeu différent

| Colonne | Avant | Définition |
|---------|-------|------------|
| `buts_per_90` | Gls.1 | Buts par 90 minutes |
| `assists_per_90` | Ast.1 | Assists par 90 minutes |
| `buts_hors_penalty_per_90` | G-PK.1 | Buts hors penalty par 90 min |
| `xG_per_90` | xG.1 | Expected Goals par 90 min |
| `xAG_per_90` | xAG.1 | Expected Assists par 90 min |
| `npxG_per_90` | npxG.1 | npxG par 90 min |
| `contribution_per_90` | G+A.1 | (Buts + Assists) par 90 min |
| `npxG_plus_xAG_per_90` | npxG+xAG.1 | Contribution attendue par 90 min |

** Exemple :**
- Joueur A : 10 buts en 1000 min → 0.90 buts/90
- Joueur B : 15 buts en 2500 min → 0.54 buts/90
- **Joueur A est plus efficace !**

---

##  MÉTRIQUES CALCULÉES - CRÉÉES PAR NOUS (6 colonnes)

| Colonne | Formule | Définition |
|---------|---------|------------|
| `contribution_offensive` | `buts + assists` | Total buts + assists |
| `G_minus_xG` | `buts - xG` | Overperformance buts (finition vs attendu) |
| `A_minus_xAG` | `assists - xAG` | Overperformance assists |
| `minutes_par_match` | `minutes_jouees / matchs_joues` | Moyenne minutes par match |
| `pct_titulaire` | `(matchs_titulaire / matchs_joues) × 100` | % de fois titulaire |
| `score_impact` | `buts×2 + assists×1.5 + courses×0.1 + passes×0.1` | Score impact global pondéré |

---

##  INTERPRÉTATION RAPIDE

### `G_minus_xG` (Overperformance buts)
- **+5 ou plus** : Finisseur exceptionnel
- **+1 à +5** : Bonne finition 
- **-1 à +1** : Normal
- **-5 ou moins** : Gaspille beaucoup 

### `pct_titulaire`
- **90-100%** : Titulaire indiscutable
- **70-90%** : Titulaire régulier
- **40-70%** : Rotation
- **< 40%** : Remplaçant

### `score_impact`
- **60+** : Impact majeur (stars)
- **30-60** : Impact élevé
- **15-30** : Impact moyen
- **< 15** : Impact limité

---

##  EXEMPLES CONCRETS

### Mohamed Salah (Liverpool)
```
Buts : 29
Assists : 18
xG : 25.2
G_minus_xG : +3.8      → Finit mieux que prévu 
contribution_offensive : 47
buts_per_90 : 0.77     → Presque 1 but par match
score_impact : 114.9   → Impact ÉNORME
```

### Erling Haaland (Man City)
```
Buts : 22
Assists : 3
xG : 22.0
G_minus_xG : 0.0       → Finition normale
buts_per_90 : 0.72     → Excellent ratio
pct_titulaire : 100%   → Indiscutable
```

### Remplaçant typique
```
matchs_joues : 15
matchs_titulaire : 2
minutes_par_match : 20
pct_titulaire : 13%    → Remplaçant
```

---

##  COLONNES SUPPRIMÉES (non gardées)

| Colonne originale | Raison |
|-------------------|--------|
| `Rk` | Rang inutile (on retrie nous-mêmes) |
| `90s` | Calculable : `Min / 90` |
| `G+A` | Calculable → créé `contribution_offensive` |
| `PKatt` | Peu utile (on garde juste `PK`) |
| `G+A-PK` | Redondant |
| `xG+xAG` | Redondant avec `npxG+xAG` |

---

##  RÉSUMÉ FINAL

**Total colonnes :** 36

- **30 colonnes originales** (renommées)
- **6 colonnes calculées** (créées par nous)

**Fichiers produits :**
1. `joueurs_clean.csv` : 574 joueurs × 36 colonnes
2. `clubs_aggregated.csv` : 20 clubs avec stats agrégées

---

**Dernière mise à jour :** Février 2025  
**Auteur :** Anis

