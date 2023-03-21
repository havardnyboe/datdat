
-- Legg inn de tre togrutene på Nordhordlandsbanen

-- Opprette de tre respektive togrutene
INSERT INTO Togrute
VALUES (1, 1, "Trondheim S", "Bodø", 1, 0, time("07:49"), time("17:34"));
-- VALUES (1, 1, "Trondheim S", "Bodø", 1, NULL, time("07:49"), time("17:34"));

INSERT INTO Togrute
VALUES (2, 2, "Trondheim S", "Bodø", 2, 1, time("23:05"), time("09:05"));
-- VALUES (2, 2, "Trondheim S", "Bodø", 2, NULL, time("23:05"), time("09:05"));

INSERT INTO Togrute
VALUES (3, 3, "Mo i Rana", "Trondheim S", 3, 2, time("08:11"), time("14:13"));
-- VALUES (3, 3, "Mo i Rana", "Trondheim S", 3, NULL, time("08:11"), time("14:13"));

-- Fest delstrekninger til togrutene (ved strekningPåRute)
-- Rute 1:
INSERT INTO StrekningPåRute VALUES (1, 0, time("07:49"), time("09:51"));
INSERT INTO StrekningPåRute VALUES (1, 1, time("09:51"), time("13:20"));
INSERT INTO StrekningPåRute VALUES (1, 2, time("13:20"), time("14:31"));
INSERT INTO StrekningPåRute VALUES (1, 3, time("14:31"), time("16:49"));
INSERT INTO StrekningPåRute VALUES (1, 4, time("16:49"), time("17:34"));

-- Rute 2:
INSERT INTO StrekningPåRute VALUES (2, 0, time("23:05"), time("00:57"));
INSERT INTO StrekningPåRute VALUES (2, 1, time("00:57"), time("04:41"));
INSERT INTO StrekningPåRute VALUES (2, 2, time("04:41"), time("05:55"));
INSERT INTO StrekningPåRute VALUES (2, 3, time("05:55"), time("08:19"));
INSERT INTO StrekningPåRute VALUES (2, 4, time("08:19"), time("09:05"));

-- Rute 3:
INSERT INTO StrekningPåRute VALUES (3, 2, time("08:11"), time("09:14"));
INSERT INTO StrekningPåRute VALUES (3, 1, time("09:14"), time("12:31"));
INSERT INTO StrekningPåRute VALUES (3, 0, time("12:31"), time("14:31"));

-- Opprett Togrutetabeller
INSERT INTO Togrutetabell VALUES (1, 1, 0);
INSERT INTO Togrutetabell VALUES (2, 1, 1);
INSERT INTO Togrutetabell VALUES (3, 1, 0);

-- Fest Stasjonene til tabellene
-- Rute 1:
INSERT INTO StasjonerITabell VALUES (1, 'Trondheim S', time("07:49"), time("07:49"));
INSERT INTO StasjonerITabell VALUES (1, 'Steinskjer', time("09:51"), time("09:51"));
INSERT INTO StasjonerITabell VALUES (1, 'Mosjøen', time("13:20"), time("13:20"));
INSERT INTO StasjonerITabell VALUES (1, 'Mo i Rana', time("14:31"), time("14:31"));
INSERT INTO StasjonerITabell VALUES (1, 'Fauske', time("16:49"), time("16:49"));
INSERT INTO StasjonerITabell VALUES (1, 'Bodø', time("17:34"), time("17:34"));

-- Rude 2:
INSERT INTO StasjonerITabell VALUES (2, 'Trondheim S', time("23:05"), time("23:05"));
INSERT INTO StasjonerITabell VALUES (2, 'Steinskjer', time("00:57"), time("00:57"));
INSERT INTO StasjonerITabell VALUES (2, 'Mosjøen', time("04:41"), time("04:41"));
INSERT INTO StasjonerITabell VALUES (2, 'Mo i Rana', time("05:55"), time("05:55"));
INSERT INTO StasjonerITabell VALUES (2, 'Fauske', time("08:19"), time("08:19"));
INSERT INTO StasjonerITabell VALUES (2, 'Bodø', time("09:05"), time("09:05"));

-- Rute 3:
INSERT INTO StasjonerITabell VALUES (3, 'Mo i Rana', time("08:11"), time("08:11"));
INSERT INTO StasjonerITabell VALUES (3, 'Mosjøen', time("09:14"), time("09:14"));
INSERT INTO StasjonerITabell VALUES (3, 'Stenskjer', time("12:31"), time("12:31"));
INSERT INTO StasjonerITabell VALUES (3, 'Trondheim S', time("14:13"), time("14:13"));

-- Kunderegister
INSERT INTO Kunderegister VALUES (0);

-- Operatør
INSERT INTO Operatør VALUES ("SJ", 0);

-- SJ-sittevogn-1
INSERT INTO Vogn VALUES (0, "Sittevogn", "SJ", "SJ-sittevogn-1");
INSERT INTO Rad VALUES (0, 1);
INSERT INTO Rad VALUES (0, 2);
INSERT INTO Rad VALUES (0, 3);
INSERT INTO Sete VALUES (0, 1, 1);
INSERT INTO Sete VALUES (0, 2, 1);
INSERT INTO Sete VALUES (0, 3, 1);
INSERT INTO Sete VALUES (0, 4, 1);
INSERT INTO Sete VALUES (0, 5, 2);
INSERT INTO Sete VALUES (0, 6, 2);
INSERT INTO Sete VALUES (0, 7, 2);
INSERT INTO Sete VALUES (0, 8, 2);
INSERT INTO Sete VALUES (0, 9, 3);
INSERT INTO Sete VALUES (0, 10, 3);
INSERT INTO Sete VALUES (0, 11, 3);
INSERT INTO Sete VALUES (0, 12, 3);
INSERT INTO Vogn VALUES (1, "Sittevogn", "SJ", "SJ-sittevogn-1");
INSERT INTO Rad VALUES (1, 1);
INSERT INTO Rad VALUES (1, 2);
INSERT INTO Rad VALUES (1, 3);
INSERT INTO Sete VALUES (1, 1, 1);
INSERT INTO Sete VALUES (1, 2, 1);
INSERT INTO Sete VALUES (1, 3, 1);
INSERT INTO Sete VALUES (1, 4, 1);
INSERT INTO Sete VALUES (1, 5, 2);
INSERT INTO Sete VALUES (1, 6, 2);
INSERT INTO Sete VALUES (1, 7, 2);
INSERT INTO Sete VALUES (1, 8, 2);
INSERT INTO Sete VALUES (1, 9, 3);
INSERT INTO Sete VALUES (1, 10, 3);
INSERT INTO Sete VALUES (1, 11, 3);
INSERT INTO Sete VALUES (1, 12, 3);
INSERT INTO Vogn VALUES (2, "Sittevogn", "SJ", "SJ-sittevogn-1");
INSERT INTO Rad VALUES (2, 1);
INSERT INTO Rad VALUES (2, 2);
INSERT INTO Rad VALUES (2, 3);
INSERT INTO Sete VALUES (2, 1, 1);
INSERT INTO Sete VALUES (2, 2, 1);
INSERT INTO Sete VALUES (2, 3, 1);
INSERT INTO Sete VALUES (2, 4, 1);
INSERT INTO Sete VALUES (2, 5, 2);
INSERT INTO Sete VALUES (2, 6, 2);
INSERT INTO Sete VALUES (2, 7, 2);
INSERT INTO Sete VALUES (2, 8, 2);
INSERT INTO Sete VALUES (2, 9, 3);
INSERT INTO Sete VALUES (2, 10, 3);
INSERT INTO Sete VALUES (2, 11, 3);
INSERT INTO Sete VALUES (2, 12, 3);
INSERT INTO Vogn VALUES (3, "Sittevogn", "SJ", "SJ-sittevogn-1");
INSERT INTO Rad VALUES (3, 1);
INSERT INTO Rad VALUES (3, 2);
INSERT INTO Rad VALUES (3, 3);
INSERT INTO Sete VALUES (3, 1, 1);
INSERT INTO Sete VALUES (3, 2, 1);
INSERT INTO Sete VALUES (3, 3, 1);
INSERT INTO Sete VALUES (3, 4, 1);
INSERT INTO Sete VALUES (3, 5, 2);
INSERT INTO Sete VALUES (3, 6, 2);
INSERT INTO Sete VALUES (3, 7, 2);
INSERT INTO Sete VALUES (3, 8, 2);
INSERT INTO Sete VALUES (3, 9, 3);
INSERT INTO Sete VALUES (3, 10, 3);
INSERT INTO Sete VALUES (3, 11, 3);
INSERT INTO Sete VALUES (3, 12, 3);

-- SJ-sovevogn-1
INSERT INTO Vogn VALUES (5, "Sovevogn", "SJ", "SJ-sovevogn-1");
INSERT INTO Kupe VALUES (5, 1);
INSERT INTO Kupe VALUES (5, 2);
INSERT INTO Kupe VALUES (5, 3);
INSERT INTO Kupe VALUES (5, 4);
INSERT INTO Seng VALUES (5, 1, 1);
INSERT INTO Seng VALUES (5, 2, 1);
INSERT INTO Seng VALUES (5, 3, 2);
INSERT INTO Seng VALUES (5, 4, 2);
INSERT INTO Seng VALUES (5, 5, 3);
INSERT INTO Seng VALUES (5, 6, 3);
INSERT INTO Seng VALUES (5, 7, 4);
INSERT INTO Seng VALUES (5, 8, 4);

-- Vognoppsett Rute 1
INSERT INTO Vognoppsett VALUES (0);
INSERT INTO VognIOppsett VALUES (0, 0, 1);
INSERT INTO VognIOppsett VALUES (1, 0, 2);

-- Vognoppsett Rute 2
INSERT INTO Vognoppsett VALUES (1);
INSERT INTO VognIOppsett VALUES (2, 1, 1);
INSERT INTO VognIOppsett VALUES (5, 1, 2);

-- Vognoppsett Rute 3
INSERT INTO Vognoppsett VALUES (2);
INSERT INTO VognIOppsett VALUES (3, 2, 1);
