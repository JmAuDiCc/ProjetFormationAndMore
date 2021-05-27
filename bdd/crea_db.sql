drop database if exists journaux_db;
create database journaux_db
    DEFAULT CHARACTER  SET 'UTF8';
use journaux_db;




CREATE TABLE type_journaux (
    Id_type INT(3) NOT NULL AUTO_INCREMENT,
    Type VARCHAR(100) NOT NULL,	
    PRIMARY KEY (Id_type)
);

CREATE TABLE journaux (
    Id_journal INT(4) NOT NULL AUTO_INCREMENT,
    Id_type INT(3) NOT NULL,
    Nom_journal VARCHAR(100) NOT NULL,
    PRIMARY KEY (Id_journal),
	FOREIGN KEY (Id_type) REFERENCES type_journaux(Id_type)
);


CREATE TABLE articles (
    Id_art INT(15) NOT NULL AUTO_INCREMENT,
    Id_journal INT(4) NOT NULL,
    Titre VARCHAR(700) NOT NULL,
	Date_art VARCHAR (20) NOT NULL,	
    PRIMARY KEY (Id_art),
	FOREIGN KEY (Id_journal) REFERENCES journaux(Id_journal)
);

INSERT INTO type_journaux (Type)
VALUES
    ('actu'),
    ('parodique'),
    ('people'),
    ('satirique'),
    ('science');
    
INSERT INTO journaux (Id_type,Nom_journal)
VALUES
    (1,'Le Monde'),
    (1,'Libération'),
    (1,'Le Point'),
    (1,'Le Figaro'),
    (2,'Gorafi'),
    (2,'Nord Presse'),
    (3,'Closer'),
    (3,'Public'),
    (4,'Charlie Hebdo'),
    (5,'Science et Avenir');