import sqlite3
from print_table import print_table
import datetime
con = sqlite3.connect("jernbanenett.db")
cursor = con.cursor()


def findFutureTrips(email):
    # date = datetime.date.today()
    date = datetime.date(2023, 3, 26)
    cursor.execute("""
        SELECT Billett.ID, Kunde.Navn, Kundeordre.Tidspunkt, VognIOppsett.Nummer, Billett.SengNummer, Billett.SeteNummer, A.Jernbanestasjon, B.Jernbanestasjon, A.Avgangstid, B.Ankomsttid, Togruteforekomst.Dato, A.Stasjonnummer, B.Stasjonnummer, Vogn.Navn
        FROM StasjonerITabell A, StasjonerITabell B, Togrute, VognIOppsett
        INNER JOIN Togruteforekomst ON (Togrute.ID = Togruteforekomst.Togrute)
        INNER JOIN Billett ON (Togruteforekomst.ID = Billett.Togruteforekomst)
        INNER JOIN BillettTilStrekning ON (Billett.ID = BillettTilStrekning.BillettID)
        INNER JOIN Delstrekning ON (BillettTilStrekning.DelstrekningID = Delstrekning.ID)
        INNER JOIN Kundeordre ON (Billett.Kundeordrenummer = Kundeordre.Ordrenummer)
        INNER JOIN Kunde ON (Kundeordre.Kunde = Kunde.Kundenummer)
        INNER JOIN Vogn ON (VognIOppsett.VognID = Vogn.ID)
        WHERE A.TogrutetabellID = B.TogrutetabellID
        AND A.TogrutetabellID = Togrute.Togrutetabell
        AND A.Stasjonnummer < B.Stasjonnummer
        AND ((A.Jernbanestasjon = Delstrekning.Stasjon1)
            OR (A.Jernbanestasjon = Delstrekning.Stasjon2))
        AND ((B.Jernbanestasjon = Delstrekning.Stasjon2)
            OR (B.Jernbanestasjon = Delstrekning.Stasjon1))
        AND ((Billett.SeteVogn=VognIOppsett.VognID)
            OR (Billett.SengVogn=VognIOppsett.VognID))
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
            strekninger.append([s[6], s[8], s[7], s[9]])

        dsb = delstrekningbilletter[0]
        billett = (dsb[1], dsb[13], dsb[3], dsb[4], dsb[5], dsb[10], strekninger[0]
                   [0], strekninger[0][1], strekninger[-1][2], strekninger[-1][3])

        billetter.append(billett)

        for i, line in enumerate(billetter):
            billetter[i] = tuple(e for e in line if e != None)

        billetter = sorted(billetter, key=lambda item: (
            item[3], item[5], item[2]))

    return billetter


print_table(findFutureTrips(input("Skriv inn din registrerte epostadrsse: ")), [
            "Navn", "Vogntype", "Vognnummer", "Plassnummer", "Dato", "Avgangsstasjon", "Avgangstid", "Ankomststasjon", "Ankomsttid"])