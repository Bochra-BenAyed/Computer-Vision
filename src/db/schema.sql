-- PostgreSQL schema, from section 6 of the specification.
-- Usage:  psql -U trafic -d trafic -f src/db/schema.sql

CREATE TABLE IF NOT EXISTS cameras (
    id        SERIAL PRIMARY KEY,
    nom       TEXT NOT NULL,
    troncon   TEXT,              -- road section the camera covers
    latitude  DOUBLE PRECISION,  -- the spec asks for geolocated alerts
    longitude DOUBLE PRECISION
);

CREATE TYPE type_vehicule AS ENUM ('voiture', 'camion');
CREATE TYPE statut_alerte AS ENUM ('active', 'resolue', 'faux_positif_confirme');

-- 6.1 Every detected vehicle passage
CREATE TABLE IF NOT EXISTS passages (
    id               SERIAL PRIMARY KEY,
    camera_id        INT NOT NULL REFERENCES cameras(id),
    horodatage       TIMESTAMP NOT NULL,
    type_vehicule    type_vehicule NOT NULL,
    score_confiance  REAL CHECK (score_confiance BETWEEN 0 AND 1)
);
CREATE INDEX IF NOT EXISTS idx_passages_cam_time ON passages (camera_id, horodatage);

-- 6.2 Reference profile: normal flow per camera, weekday, 5-min slot
CREATE TABLE IF NOT EXISTS profil_reference (
    camera_id        INT NOT NULL REFERENCES cameras(id),
    jour_semaine     SMALLINT NOT NULL CHECK (jour_semaine BETWEEN 1 AND 7),
    tranche_horaire  TIME NOT NULL,
    debit_moyen      REAL NOT NULL,
    ecart_type       REAL NOT NULL,
    PRIMARY KEY (camera_id, jour_semaine, tranche_horaire)  -- the spec had no PK here
);

-- 6.3 Alerts
CREATE TABLE IF NOT EXISTS alertes (
    id          SERIAL PRIMARY KEY,
    camera_id   INT NOT NULL REFERENCES cameras(id),
    debut       TIMESTAMP NOT NULL,
    fin         TIMESTAMP,                 -- NULL while the alert is ongoing
    ecart_max   REAL NOT NULL,
    statut      statut_alerte NOT NULL DEFAULT 'active'
);
