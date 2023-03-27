PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS user;
CREATE TABLE user(
     idUser INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
     login NVARCHAR(255) NOT NULL,
     password NVARCHAR(255) NOT NULL,
     prenom NVARCHAR(255) NOT NULL
);

INSERT INTO user(idUSer,login,password,prenom) VALUES (1,'floflo', '123', 'Flow');

DROP TABLE IF EXISTS cheese;
CREATE TABLE cheese(
   idCheese INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
   nom NVARCHAR(255) NOT NULL
);
INSERT INTO cheese(idCheese,nom) VALUES (1,'camembert');

DROP TABLE IF EXISTS userCheese;
CREATE TABLE userCheese(
    idUser INTEGER,
    idCheese INTEGER,
    CONSTRAINT idUser FOREIGN KEY(idUser) REFERENCES user(idUser),
    CONSTRAINT idCheese FOREIGN KEY(idCheese) REFERENCES cheese(idCheese)
);

INSERT INTO userCheese (idUser,idCheese) VALUES (1,1);
