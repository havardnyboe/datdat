
# Bruker skal kunne registrere seg i kunderegisteret

import sqlite3
import uuid
import re

con = sqlite3.connect("jernbanenett.db")
cursor = con.cursor()


def addKunde(kundenummer, navn, epostadresse, mobilnummer, kunderegisterID):
    cursor.execute("""
    INSERT INTO Kunde VALUES(?, ?, ?, ?, ?);
    """, (kundenummer, navn, epostadresse, mobilnummer, kunderegisterID))
    con.commit()
    con.close()


def validateName(name):
    if re.match("([A-Åa-å]+\s[A-Åa-Å])", name):
        return name
    else:
        print("Registrert data er på feil format. Prøv igjen, med format \"Fornavn Etternavn\".")
        return validateName(input("Registrer navn: "))


def validateEmail(mail):
    cursor.execute("""
        SELECT EXISTS(SELECT 1 
            FROM Kunde 
            WHERE Epostadresse = ?)
    """, (mail,))

    res = cursor.fetchone()
    print(res)
    if cursor.fetchone()[0]:
        print("Det er allerede opprettet en konto med denne epostadressen.")
        return
    if re.match("\w+@\w+\.\w+", mail):
        return mail
    else:
        print("Registrert data er på feil format. Prøv igjen, med format \"mail@example.com\".")
        return validateEmail(input("Registrer e-mailadresse: "))


def validatePhoneNumber(number):
    if re.match("[0-9]{8}", number):
        return number
    else:
        print("Registrert data er på feil format. Prøv igjen, med format \"12345678\".")
        return validatePhoneNumber(input("Registrer telefonnummer: "))


def registrerKunde():
    name = validateName(
        input("Registrer navn på formatet 'Fornavn Etternavn': "))
    mail = validateEmail(input("Registrer e-mailadresse: "))
    phone = validatePhoneNumber(input("Registrer telefonnummer, 8 tall: "))
    id = str(uuid.uuid4())
    addKunde(id, name, mail, phone, 0)
    print(f"Hei, {name}! Du er nå registrert i vårt kundesystem!")
    return mail


if __name__ == "__main__":
    registrerKunde()
