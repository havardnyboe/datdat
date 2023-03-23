import sqlite3 
from print_table import print_table 
con = sqlite3.connect("jernbanenett.db")
cursor = con.cursor()

def findFutureTrips(Epost):
    cursor.execute("""
    SELECT Billett.ID, Kunde.Navn, Kundeordre.Tidspunkt, Billett.SengNummer, Billett.SengVogn, Billett.SeteNummer, Billett.SeteVogn, Delstrekning.Stasjon1, Delstrekning.Stasjon2, StrekningPåRute.Avgangstid, StrekningPåRute.Ankomsttid, Togrute.ID, Togruteforekomst.Dato
    FROM Kunde
    INNER JOIN Kundeordre ON (Kunde.Kundenummer = Kundeordre.Kunde)  
    INNER JOIN Billett ON (Billett.Kundeordrenummer = Kundeordre.Ordrenummer)
    INNER JOIN BillettTilStrekning ON (Billett.ID = BillettTilStrekning.BillettID)
    INNER JOIN Delstrekning ON (BillettTilStrekning.DelstrekningID = Delstrekning.ID)
    INNER JOIN StrekningPåRute ON (StrekningPåRute.DelstrekningID = Delstrekning.ID)
    INNER JOIN Togruteforekomst ON (Togruteforekomst.ID = Billett.Togruteforekomst)
    INNER JOIN Togrute ON (Togruteforekomst.Togrute = Togrute.ID)
    WHERE StrekningPåRute.TogruteID = Togrute.ID
    AND Kunde.Epostadresse LIKE ?;
    """, (Epost, ))

    ordreWithStrekninger = cursor.fetchall()
    resultat = []
    prevOrdre = ""
    startStasjon = ""
    sluttStasjon = ""
    for i, ordre in enumerate(ordreWithStrekninger):
        if prevOrdre != ordre[0] or i == len(ordreWithStrekninger)-1:
            if i == len(ordreWithStrekninger)-1:
                if ordreWithStrekninger[i-1][11] == "3":
                    sluttStasjon = startStasjon
                    startStasjon = (ordre[8], ordre[9])
                else:
                    sluttStasjon = (ordre[8], ordre[10])
                resultat.append((ordre[1], ordre[3], ordre[4], ordre[5], ordre[6], ordre[12], startStasjon[0], startStasjon[1], sluttStasjon[0], sluttStasjon[1]))
            elif i != 0:
                if ordreWithStrekninger[i-1][11] == "3":
                    sluttStasjon = startStasjon
                    startStasjon = (ordreWithStrekninger[i-1][8], ordreWithStrekninger[i-1][9])
                else:
                    sluttStasjon = (ordreWithStrekninger[i-1][8], ordreWithStrekninger[i-1][10])
                resultat.append((ordre[1], ordre[3], ordre[4], ordre[5], ordre[6], ordre[12], startStasjon[0], startStasjon[1], sluttStasjon[0], sluttStasjon[1]))
            if ordre[11] == "3":
                startStasjon = (ordre[7], ordre[10])
            else:
                startStasjon = (ordre[7], ordre[9])

            prevOrdre = ordre[0]

    for i, line in enumerate(resultat):
        # print(tuple(e for e in line if e != None))
        resultat[i] = tuple(e for e in line if e != None)

    return resultat

# for res in findFutureTrips(input("Epost: ")):
#     print(res)

print_table(findFutureTrips(input("Epost: ")), ["Navn", "Plass Nummer", "Vogn Nummer", "Dato", "Startstasjon", "Avgangstid", "Sluttstasjon", "Ankomsttid"])




