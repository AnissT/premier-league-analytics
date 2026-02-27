-- ============================================================================
-- SCHÉMA  : FOOTBALL ANALYTICS - PREMIER LEAGUE 2024-25
-- Auteur : Anis
-- Structure : 2 tables (clubs + joueurs)
-- ============================================================================

-- Supprimer les tables si elles existent
DROP TABLE IF EXISTS joueurs CASCADE;
DROP TABLE IF EXISTS clubs CASCADE;

-- ============================================================================
-- TABLE 1 : CLUBS (stats agrégées)
-- Source : clubs_aggregated.csv
-- ============================================================================

CREATE TABLE clubs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL,
    
    -- Stats agrégées depuis joueurs
    total_joueurs INTEGER,
    age_moyen DECIMAL(4,1),
    total_buts INTEGER,
    total_assists INTEGER,
    contribution_offensive INTEGER,
    total_xG DECIMAL(6,2),
    total_npxG DECIMAL(6,2),
    total_xAG DECIMAL(6,2),
    total_minutes INTEGER,
    total_cartons_jaunes INTEGER,
    total_cartons_rouges INTEGER,
    total_courses_progressives INTEGER,
    total_passes_progressives INTEGER,
    buts_moins_xG DECIMAL(6,2),
    assists_moins_xAG DECIMAL(6,2)
);

CREATE INDEX idx_clubs_nom ON clubs(nom);

COMMENT ON TABLE clubs IS 'Stats agrégées par club - 20 clubs Premier League 2024-25';

-- ============================================================================
-- TABLE 2 : JOUEURS (identité + toutes les stats)
-- Source : joueurs_clean.csv
-- ============================================================================

CREATE TABLE joueurs (
    id SERIAL PRIMARY KEY,
    
    -- Identité
    nom VARCHAR(100) NOT NULL,
    club VARCHAR(100),
    nationalite VARCHAR(50),
    poste VARCHAR(20),
    age INTEGER,
    annee_naissance INTEGER,
    
    -- Temps de jeu
    matchs_joues INTEGER DEFAULT 0,
    matchs_titulaire INTEGER DEFAULT 0,
    minutes_jouees INTEGER DEFAULT 0,
    
    -- Performance offensive
    buts INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    buts_hors_penalty INTEGER DEFAULT 0,
    penalties_marques INTEGER DEFAULT 0,
    
    -- Stats avancées (Expected)
    xG DECIMAL(5,2) DEFAULT 0,
    npxG DECIMAL(5,2) DEFAULT 0,
    xAG DECIMAL(5,2) DEFAULT 0,
    npxG_plus_xAG DECIMAL(5,2) DEFAULT 0,
    
    -- Progression
    courses_progressives INTEGER DEFAULT 0,
    passes_progressives INTEGER DEFAULT 0,
    receptions_progressives INTEGER DEFAULT 0,
    
    -- Discipline
    cartons_jaunes INTEGER DEFAULT 0,
    cartons_rouges INTEGER DEFAULT 0,
    
    -- Stats normalisées par 90 min
    buts_per_90 DECIMAL(4,2) DEFAULT 0,
    assists_per_90 DECIMAL(4,2) DEFAULT 0,
    buts_hors_penalty_per_90 DECIMAL(4,2) DEFAULT 0,
    xG_per_90 DECIMAL(4,2) DEFAULT 0,
    xAG_per_90 DECIMAL(4,2) DEFAULT 0,
    npxG_per_90 DECIMAL(4,2) DEFAULT 0,
    contribution_per_90 DECIMAL(4,2) DEFAULT 0,
    npxG_plus_xAG_per_90 DECIMAL(4,2) DEFAULT 0,
    
    -- Métriques calculées
    contribution_offensive INTEGER DEFAULT 0,
    G_minus_xG DECIMAL(5,2) DEFAULT 0,
    A_minus_xAG DECIMAL(5,2) DEFAULT 0,
    minutes_par_match DECIMAL(5,1) DEFAULT 0,
    pct_titulaire DECIMAL(5,1) DEFAULT 0,
    score_impact DECIMAL(7,2) DEFAULT 0,
    
    -- Contraintes
    CONSTRAINT age_valide CHECK (age >= 15 AND age <= 45),
    CONSTRAINT matchs_valides CHECK (matchs_joues >= 0 AND matchs_joues <= 38),
    CONSTRAINT titulaire_valide CHECK (matchs_titulaire <= matchs_joues)
);

-- Index pour recherches et performances
CREATE INDEX idx_joueurs_nom ON joueurs(nom);
CREATE INDEX idx_joueurs_club ON joueurs(club);
CREATE INDEX idx_joueurs_poste ON joueurs(poste);
CREATE INDEX idx_joueurs_buts ON joueurs(buts DESC);
CREATE INDEX idx_joueurs_assists ON joueurs(assists DESC);
CREATE INDEX idx_joueurs_contribution ON joueurs(contribution_offensive DESC);

COMMENT ON TABLE joueurs IS 'Joueurs Premier League 2024-25 avec toutes leurs stats';

-- ============================================================================
-- VUES UTILES
-- ============================================================================

-- Vue : Top buteurs
CREATE OR REPLACE VIEW vue_top_buteurs AS
SELECT 
    nom,
    club,
    buts,
    buts_per_90,
    xG,
    G_minus_xG,
    minutes_jouees
FROM joueurs
WHERE minutes_jouees > 500
ORDER BY buts DESC;

-- Vue : Jeunes talents
CREATE OR REPLACE VIEW vue_jeunes_talents AS
SELECT 
    nom,
    age,
    club,
    buts,
    assists,
    contribution_offensive,
    minutes_jouees
FROM joueurs
WHERE age < 23 AND minutes_jouees > 1000
ORDER BY contribution_offensive DESC;

-- Vue : Stats clubs
CREATE OR REPLACE VIEW vue_clubs_complet AS
SELECT 
    nom,
    total_joueurs,
    age_moyen,
    total_buts,
    total_assists,
    contribution_offensive,
    buts_moins_xG
FROM clubs
ORDER BY contribution_offensive DESC;
