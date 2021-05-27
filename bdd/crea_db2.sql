drop database if exists journaux_db2;
create database journaux_db2
    DEFAULT CHARACTER  SET 'UTF8';
use journaux_db2;

CREATE TABLE type_journaux (
    Id_type INT(3) NOT NULL AUTO_INCREMENT,
    Type VARCHAR(100) NOT NULL,	
    Type_description VARCHAR(1000) NOT NULL,
    PRIMARY KEY (Id_type)
);

CREATE TABLE journaux (
    Id_journal INT(4) NOT NULL AUTO_INCREMENT,
    Id_type INT(3) NOT NULL,
    Nom_journal VARCHAR(100) NOT NULL,
    Journal_description VARCHAR(100) NOT NULL,
    PRIMARY KEY (Id_journal),
	FOREIGN KEY (Id_type) REFERENCES type_journaux(Id_type)
);

CREATE TABLE journalistes (
    Id_journaliste INT(4) NOT NULL AUTO_INCREMENT,
    Id_type INT(3) NOT NULL,
    Nom_journaliste VARCHAR(100) NOT NULL,
    Prenom_journaliste VARCHAR(100),
    PRIMARY KEY (Id_journaliste)
);


CREATE TABLE articles (
    Url_art VARCHAR(150) NOT NULL ,
    Id_journal INT(4) NOT NULL,
    Id_journaliste INT(4),
    Titre VARCHAR(700) NOT NULL,
    Article VARCHAR(2000) NOT NULL,
	Date_art VARCHAR (20) NOT NULL,	
    Theme VARCHAR (30),
    Theme_mod VARCHAR (30),
    PRIMARY KEY (Url_art),
	FOREIGN KEY (Id_journal) REFERENCES journaux(Id_journal),
    FOREIGN KEY (Id_journaliste) REFERENCES journalistes(Id_journaliste)
);

CREATE TABLE utilisateurs (
    Id_utilisateur INT(4) NOT NULL AUTO_INCREMENT,
    Mail_utilisateur VARCHAR(100) NOT NULL,
    Pseudo_utilisateur VARCHAR(100) NOT NULL,
    Nom_utilisateur VARCHAR(100),
    Prenom_utilisateur VARCHAR(100),
    Age_utilisateur INT(3),
    PRIMARY KEY (Id_utilisateur)
);

CREATE TABLE histo_utilisateurs (
    Id_utilisateur INT(4) NOT NULL AUTO_INCREMENT,
    Url_art VARCHAR(150) NOT NULL ,
	FOREIGN KEY (Id_utilisateur) REFERENCES utilisateurs(Id_utilisateur),
    FOREIGN KEY (Url_art) REFERENCES articles(Url_art)
);