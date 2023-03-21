
#Bruker skal kunne registrere seg i kunderegisteret

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
        

def validateEmail(mail):
    if re.match("\w+@\w+\.\w+", mail):
        return mail 
    else: 
        print("Registrert data er på feil format. Prøv igjen, med format \"mail@example.com\".")


def validatePhoneNumber(number):
    if re.match("[0-9]{8}", number):
        return number 
    else: 
        print("Registrert data er på feil format. Prøv igjen, med format \"12345678\".")

#addKundeToRegister(0)
#addKunde(1, 'Navn', 'emlliveno', 907421, 0)

def main():
    name = validateName(input("Registrer navn på formatet 'Fornavn Etternavn'. "))
    mail = validateEmail(input("Registrer e-mailadresse. "))
    phone = validatePhoneNumber(input("Registrer telefonnummer, 8 tall. "))
    id = str(uuid.uuid4())
    addKunde(id, name, mail, phone, 0)
    print(f"Hei {name}! Du er nå registrert i vårt kundesystem!")

main()
