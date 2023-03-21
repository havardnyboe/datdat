-- Brukerhistorie a)
-- Databasen skal kunne registrere data om alle jernbanestrekninger i Norge. Dere skal legge inn
-- data for Nordlandsbanen (som vist i figuren). Dette kan gjøres med et skript, dere trenger ikke å
-- programmere støtte for denne funksjonaliteten.

INSERT INTO Jernbanestasjon VALUES ("Trondheim S", 5.1);
INSERT INTO Jernbanestasjon VALUES ("Steinkjer", 3.6);
INSERT INTO Jernbanestasjon VALUES ("Mosjøen", 6.8);
INSERT INTO Jernbanestasjon VALUES ("Mo i Rana", 3.5);
INSERT INTO Jernbanestasjon VALUES ("Fauske", 34);
INSERT INTO Jernbanestasjon VALUES ("Bodø", 4.1);

INSERT INTO Banestrekning VALUES (0, "Nordlandsbanen", "Diesel", "Trondheim S", "Bodø");

INSERT INTO Delstrekning VALUES (0, 120, "Dobbeltspor", "Trondheim S", "Steinkjer");
INSERT INTO Delstrekning VALUES (1, 280, "Enkeltspor", "Steinkjer", "Mosjøen");
INSERT INTO Delstrekning VALUES (2, 90, "Enkeltspor", "Mosjøen", "Mo i Rana");
INSERT INTO Delstrekning VALUES (3, 170, "Enkeltspor", "Mo i Rana", "Fauske");
INSERT INTO Delstrekning VALUES (4, 60, "Enkeltspor", "Fauske", "Bodø");

INSERT INTO DelstrekningIBane VALUES (0, 0);
INSERT INTO DelstrekningIBane VALUES (0, 1);
INSERT INTO DelstrekningIBane VALUES (0, 2);
INSERT INTO DelstrekningIBane VALUES (0, 3);
INSERT INTO DelstrekningIBane VALUES (0, 4);