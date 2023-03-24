import sqlite3
from print_table import print_table
import datetime
con = sqlite3.connect("jernbanenett.db")
cursor = con.cursor()


def findFutureTrips(email):
    # date = datetime.date.today()
    date = datetime.date(2023, 3, 26)
    cursor.execute("""
        SELECT Billett.ID, Kunde.Navn, Kundeordre.Tidspunkt, Billett.SengNummer, Billett.SengVogn, Billett.SeteNummer, Billett.SeteVogn, A.Jernbanestasjon, B.Jernbanestasjon, A.Avgangstid, B.Ankomsttid, Togruteforekomst.Dato, A.Stasjonnummer, B.Stasjonnummer
        FROM StasjonerITabell A, StasjonerITabell B, Togrute
        INNER JOIN Togruteforekomst ON (Togrute.ID = Togruteforekomst.Togrute)
        INNER JOIN Billett ON (Togruteforekomst.ID = Billett.Togruteforekomst)
        INNER JOIN BillettTilStrekning ON (Billett.ID = BillettTilStrekning.BillettID)
        INNER JOIN Delstrekning ON (BillettTilStrekning.DelstrekningID = Delstrekning.ID)
        INNER JOIN Kundeordre ON (Billett.Kundeordrenummer = Kundeordre.Ordrenummer)
        INNER JOIN Kunde ON (Kundeordre.Kunde = Kunde.Kundenummer)
        WHERE A.TogrutetabellID = B.TogrutetabellID
        AND A.TogrutetabellID = Togrute.Togrutetabell
        AND A.Stasjonnummer < B.Stasjonnummer
        AND ((A.Jernbanestasjon = Delstrekning.Stasjon1)
            OR (A.Jernbanestasjon = Delstrekning.Stasjon2))
        AND ((B.Jernbanestasjon = Delstrekning.Stasjon2)
            OR (B.Jernbanestasjon = Delstrekning.Stasjon1))
        AND Kunde.Epostadresse LIKE ?
        AND Togruteforekomst.Dato >= ?;
""", (email, date))

    alleDelstrekningBilletter = cursor.fetchall()
    billetter = []

    billettIDer = set([x[0] for x in alleDelstrekningBilletter])
    for bid in billettIDer:
        delstrekningbilletter = [
            s for s in alleDelstrekningBilletter if s[0] == bid]
        strekninger = []
        for s in sorted(delstrekningbilletter, key=lambda item: item[12]):
            strekninger.append([s[7], s[9], s[8], s[10]])

        dsb = delstrekningbilletter[0]
        billett = (dsb[1], dsb[3], dsb[4], dsb[5], dsb[6], dsb[11], strekninger[0]
                   [0], strekninger[0][1], strekninger[-1][2], strekninger[-1][3])

        billetter.append(billett)

        for i, line in enumerate(billetter):
            billetter[i] = tuple(e for e in line if e != None)

        billetter = sorted(billetter, key=lambda item: (
            item[3], item[5], item[7]))

    return billetter


print_table(findFutureTrips(input("Epost: ")), [
            "Navn", "Plass Nummer", "Vogn Nummer", "Dato", "Startstasjon", "Avgangstid", "Sluttstasjon", "Ankomsttid"])