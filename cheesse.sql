PRAGMA foreign_keys = ON;
DROP TABLE userCheese IF EXISTS
CREATE TABLE userCheese(
    idUser INTEGER NOT NULL PRIMARY KEY,
    idCheese INTEGER NOT NULL PRIMARY KEY,
    CONSTRAINT idUser FOREIGN KEY(idUser) REFERENCES user(idUser)
    CONSTRAINT idCheese FOREIGN KEY(idCheese) REFERENCES cheese(idCheese)
    );
INSERT INTO genre (libelle) VALUES ('Florent', 'floflo', '123', 'Flow');


DROP TABLE user IF EXISTS
CREATE TABLE user(
    idUser INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    login NVARCHAR(255) NOT NULL,
    password NVARCHAR(255) NOT NULL,
    prenom NVARCHAR(255) NOT NULL,
    );
INSERT INTO genre (libelle) VALUES ('Florent', 'floflo', '123', 'Flow');

DROP TABLE cheese IF EXISTS
CREATE TABLE cheese(
    idCheese INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nom NVARCHAR(255) NOT NULL
);
INSERT INTO cheese(nom) VALUES ('camembert')