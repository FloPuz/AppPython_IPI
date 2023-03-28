PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS userCheese;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS cheese;


CREATE TABLE user(
     idUser INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
     login NVARCHAR(255) NOT NULL,
     password NVARCHAR(255) NOT NULL,
     prenom NVARCHAR(255) NOT NULL,
     idCheese INTEGER,
     CONSTRAINT idCheese FOREIGN KEY(idCheese) REFERENCES cheese(idCheese)
);

CREATE TABLE cheese(
   idCheese INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
   nom NVARCHAR(255) NOT NULL
);

INSERT INTO cheese(idCheese,nom) VALUES (1,'camembert');
INSERT INTO user(idUSer,login,password,prenom) VALUES (1,'floflo', '123', 'Flow');

