-- ============================================================================
-- REQUÊTES SQL ANALYTIQUES - PREMIER LEAGUE 2024-25
-- Auteur : Anis
-- Date : Février 2025
-- ============================================================================

-- ============================================================================
-- 1. TOP 10 BUTEURS
-- ============================================================================
SELECT 
    nom,
    club,
    buts,
    buts_per_90,
    xG,
    G_minus_xG as overperformance,
    minutes_jouees
FROM joueurs
WHERE minutes_jouees > 500  -- Minimum 500 minutes
ORDER BY buts DESC
LIMIT 10;

-- ============================================================================
-- 2. TOP 10 PASSEURS
-- ============================================================================
SELECT 
    nom,
    club,
    assists,
    assists_per_90,
    xAG,
    A_minus_xAG as overperformance_assists,
    minutes_jouees
FROM joueurs
WHERE minutes_jouees > 500
ORDER BY assists DESC
LIMIT 10;

-- ============================================================================
-- 3. OVERPERFORMANCE xG (finisseurs exceptionnels)
-- ============================================================================
SELECT 
    nom,
    club,
    poste,
    buts,
    xG,
    G_minus_xG as overperformance,
    buts_per_90
FROM joueurs
WHERE G_minus_xG > 3 AND minutes_jouees > 1000
ORDER BY G_minus_xG DESC;

-- ============================================================================
-- 4. UNDERPERFORMANCE xG (gaspillent occasions)
-- ============================================================================
SELECT 
    nom,
    club,
    poste,
    buts,
    xG,
    G_minus_xG as underperformance,
    buts_per_90
FROM joueurs
WHERE G_minus_xG < -3 AND minutes_jouees > 1000
ORDER BY G_minus_xG ASC;

-- ============================================================================
-- 5. JEUNES TALENTS (<23 ans, forte contribution)
-- ============================================================================
SELECT 
    nom,
    age,
    club,
    poste,
    buts,
    assists,
    contribution_offensive,
    score_impact,
    minutes_jouees
FROM joueurs
WHERE age < 23 AND minutes_jouees > 1000
ORDER BY contribution_offensive DESC
LIMIT 15;

-- ============================================================================
-- 6. JOUEURS POLYVALENTS (buts + assists + progression)
-- ============================================================================
SELECT 
    nom,
    club,
    poste,
    buts,
    assists,
    courses_progressives,
    passes_progressives,
    score_impact,
    (buts + assists + (courses_progressives + passes_progressives)/10) as score_polyvalence
FROM joueurs
WHERE minutes_jouees > 1500
ORDER BY score_polyvalence DESC
LIMIT 10;

-- ============================================================================
-- 7. MEILLEURS PAR POSTE (top 3 chaque poste)
-- ============================================================================
WITH ranked_by_position AS (
    SELECT 
        nom,
        club,
        poste,
        contribution_offensive,
        score_impact,
        ROW_NUMBER() OVER (PARTITION BY poste ORDER BY score_impact DESC) as rang
    FROM joueurs
    WHERE minutes_jouees > 1000
)
SELECT nom, club, poste, contribution_offensive, score_impact
FROM ranked_by_position
WHERE rang <= 3
ORDER BY poste, rang;

-- ============================================================================
-- 8. COMPARAISON CLUBS (xG vs réalité)
-- ============================================================================
SELECT 
    nom as club,
    total_buts,
    total_xG,
    buts_moins_xG as overperformance_club,
    total_assists,
    total_xAG,
    assists_moins_xAG as overperformance_assists_club,
    age_moyen
FROM clubs
ORDER BY overperformance_club DESC;

-- ============================================================================
-- 9. STATS MOYENNES PAR POSTE
-- ============================================================================
SELECT 
    poste,
    COUNT(*) as nombre_joueurs,
    ROUND(AVG(buts), 2) as buts_moyen,
    ROUND(AVG(assists), 2) as assists_moyen,
    ROUND(AVG(xG), 2) as xG_moyen,
    ROUND(AVG(minutes_jouees), 0) as minutes_moyennes,
    ROUND(AVG(age), 1) as age_moyen
FROM joueurs
WHERE minutes_jouees > 500
GROUP BY poste
ORDER BY buts_moyen DESC;

-- ============================================================================
-- 10. JOUEURS SOUS-UTILISÉS (bon ratio mais peu de minutes)
-- ============================================================================
SELECT 
    nom,
    club,
    age,
    poste,
    minutes_jouees,
    matchs_joues,
    pct_titulaire,
    buts_per_90,
    assists_per_90,
    contribution_per_90
FROM joueurs
WHERE 
    minutes_jouees < 1500 
    AND contribution_per_90 > 0.4
    AND matchs_joues > 10
ORDER BY contribution_per_90 DESC
LIMIT 15;
