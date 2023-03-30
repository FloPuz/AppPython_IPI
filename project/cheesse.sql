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
                       nom NVARCHAR(255) NOT NULL,
                       urlImg NVARCHAR(255),
                       urlFlag NVARCHAR(255)
);

INSERT INTO cheese(idCheese,nom,urlImg,urlFlag) VALUES (1,'Parmigiano Regiano','assets/images/cheeses/parmigiano.png','assets/images/flags/italy.png');
INSERT INTO cheese(idCheese,nom,urlImg,urlFlag) VALUES (2,'Burrata','assets/images/cheeses/burratta.png','assets/images/flags/italy.png');
INSERT INTO cheese(idCheese,nom,urlImg,urlFlag) VALUES (3,'Grana Padano','assets/images/cheeses/padano.png','assets/images/flags/italy.png');
INSERT INTO cheese(idCheese,nom,urlImg,urlFlag) VALUES (4,'Oaxaca cheese','assets/images/cheeses/oaxaca.png','assets/images/flags/mexico.png');
INSERT INTO cheese(idCheese,nom,urlImg,urlFlag) VALUES (5,'Bundz','assets/images/cheeses/bundz.png','assets/images/flags/poland.png');
INSERT INTO cheese(idCheese,nom,urlImg,urlFlag) VALUES (6,'Canastra','assets/images/cheeses/canastra.png','assets/images/flags/brazil.png');
INSERT INTO cheese(idCheese,nom,urlImg,urlFlag) VALUES (7,'Old Amsterdam','assets/images/cheeses/old_amsterdam.png','assets/images/flags/netherlands.png');
INSERT INTO cheese(idCheese,nom,urlImg,urlFlag) VALUES (8,'Sirene','assets/images/cheeses/sirene.png','assets/images/flags/bulgarie.png');
INSERT INTO cheese(idCheese,nom,urlImg,urlFlag) VALUES (9,'Graviera Naxou','assets/images/cheeses/graviera.png','assets/images/flags/greece.png');
INSERT INTO cheese(idCheese,nom,urlImg,urlFlag) VALUES (10,'Sulguni','assets/images/cheeses/sulguni.png','assets/images/flags/georgia.png');


INSERT INTO user(login,password,prenom,idCheese) VALUES ('floflo', '123', 'Flow',1);

