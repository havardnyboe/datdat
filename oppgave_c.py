import sqlite3 as sq
from print_table import print_table

con = sq.connect("jernbanenett.db")
cursor = con.cursor()


def getRuter(station, weekday):
    weekdays = "mandag tirsdag onsdag torsdag fredag".split()
    weekends = "lørdag søndag".split()

    if (weekday in weekdays):
        cursor.execute("""
            SELECT Togrute.Startstasjon, Togrute.Endestasjon, StasjonerITabell.Jernbanestasjon, StasjonerITabell.Avgangstid, Togrute.Ankomsttid
            FROM  StasjonerITabell INNER JOIN Togrute ON (StasjonerITabell.TogrutetabellID = Togrute.Togrutetabell)
                INNER JOIN Togrutetabell ON (StasjonerITabell.TogrutetabellID = Togrutetabell.ID)
            WHERE StasjonerITabell.Jernbanestasjon LIKE ? AND Togrutetabell.KjørerUkedager = 1 
        """, (station + "%",))
    elif (weekday in weekends):
        cursor.execute("""
            SELECT Togrute.Startstasjon, Togrute.Endestasjon, StasjonerITabell.Jernbanestasjon, StasjonerITabell.Avgangstid, Togrute.Ankomsttid
            FROM  StasjonerITabell INNER JOIN Togrute ON (StasjonerITabell.TogrutetabellID = Togrute.Togrutetabell)
                INNER JOIN Togrutetabell ON (StasjonerITabell.TogrutetabellID = Togrutetabell.ID)
            WHERE StasjonerITabell.Jernbanestasjon LIKE ? AND Togrutetabell.KjørerHelger = 1 
        """, (station + "%",))
    return cursor.fetchall()


def main():
    station = input("Hvilken stasjon ønsker du informasjon om togruter fra? ")
    weekday = input("Hvilken ukedag ønsker du informasjon om? ")
    res = getRuter(station, weekday.lower())
    if len(res) == 0:
        print("Finner ikke resultat for oppgitt stasjon. Vennligst prøv en annen stasjon.")
    else:
        print_table(res, ["Startstasjon", "Endestasjon", "Valgt stasjon",
                    "Avgangstid valgt stasjon", "Ankomsttid endestasjon"])


main()

con.close()
