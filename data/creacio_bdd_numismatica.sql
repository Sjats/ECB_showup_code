-- Creació de la taula de dinastia 
CREATE TABLE dinastia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    data_principi DATE,
    data_final DATE,
    foto_path TEXT
);

-- Creació de la taula de senyors
CREATE TABLE senyor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    data_neixement DATE,
    data_mort DATE,
    ordinal TEXT,
    dinastia_id INTEGER NOT NULL,
    foto_path TEXT, 
    FOREIGN KEY (dinastia_id) REFERENCES dinastia(id)
);

-- Creació de la taula de titols
CREATE TABLE titol (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    data_principi DATE,
    data_final DATE,
    territori TEXT,
    foto_path TEXT
);

-- Creació de la taula de regnes
CREATE TABLE govern (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    senyor_id INTEGER NOT NULL,
    titol_id INTEGER NOT NULL,
    numero TEXT, 
    data_debut DATE,
    data_final DATE,
    FOREIGN KEY (senyor_id) REFERENCES senyor(id),
    FOREIGN KEY (titol_id) REFERENCES titol(id)
);

-- Creació de la taula de monedes
CREATE TABLE peça (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    moneda_id INTEGER NOT NULL,
    estat TEXT,
    descripcio TEXT,
    serie_emissio TEXT,
    valor_estimat FLOAT,
    lloc TEXT,
    foto_path TEXT,
    FOREIGN KEY (moneda_id) REFERENCES moneda(id)
);

-- Creació de la taula de moneda
CREATE TABLE moneda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor_nominal FLOAT NOT NULL,
    any DATE,
    govern_id INTEGER NOT NULL,
    devisa_id INTEGER NOT NULL,
    descripcio TEXT,
    material TEXT,
    foto_path TEXT,
    FOREIGN KEY (govern_id) REFERENCES govern(id),
    FOREIGN KEY (devisa_id) REFERENCES devisa(id)
);

CREATE TABLE devisa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    data_creacio DATE,
    data_final DATE,
    foto_path TEXT
 )