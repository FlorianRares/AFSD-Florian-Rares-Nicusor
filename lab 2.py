import csv


def initializare_glosar():
    """Inițializează glosarul cu câțiva termeni de exemplu."""
    return {
        "variabilă": {
            "definiție": "nume asociat unei valori",
            "categorie": "fundamente",
            "exemplu": "x = 10"
        },
        "dicționar": {
            "definiție": "structură de date bazată pe perechi cheie-valoare",
            "categorie": "structuri de date",
            "exemplu": "{'a': 1, 'b': 2}"
        }
    }


def afiseaza_meniu():
    print("\n===== GLOSAR INTERACTIV =====")
    print("1. Adaugă termen")
    print("2. Căutare exactă")
    print("3. Căutare după fragment")
    print("4. Actualizează termen")
    print("5. Șterge termen")
    print("6. Afișează tot glosarul")
    print("7. Afișează statistici")
    print("8. Salvează în CSV")
    print("9. Încarcă din CSV")
    print("0. Ieșire")


def adauga_termen(glosar):
    termen = input("Introdu termenul nou: ").strip().lower()

    if termen == "":
        print("Eroare: termenul nu poate fi gol.")
        return

    if termen in glosar:
        print("Eroare: termenul există deja în glosar.")
        return

    definitie = input("Introdu definiția: ").strip()
    categorie = input("Introdu categoria: ").strip()
    exemplu = input("Introdu exemplul: ").strip()

    if definitie == "" or categorie == "" or exemplu == "":
        print("Eroare: toate câmpurile trebuie completate.")
        return

    glosar[termen] = {
        "definiție": definitie,
        "categorie": categorie,
        "exemplu": exemplu
    }

    print(f'Termenul "{termen}" a fost adăugat cu succes.')


def cautare_exacta(glosar):
    termen = input("Introdu termenul căutat: ").strip().lower()

    if termen in glosar:
        print(f'\nTermen: {termen}')
        print(f'Definiție: {glosar[termen]["definiție"]}')
        print(f'Categorie: {glosar[termen]["categorie"]}')
        print(f'Exemplu: {glosar[termen]["exemplu"]}')
    else:
        print("Termenul nu există în glosar.")


def cautare_fragment(glosar):
    fragment = input("Introdu un fragment de text: ").strip().lower()

    if fragment == "":
        print("Eroare: fragmentul nu poate fi gol.")
        return

    rezultate = []

    for termen, informatii in glosar.items():
        if (
            fragment in termen.lower()
            or fragment in informatii["definiție"].lower()
            or fragment in informatii["categorie"].lower()
            or fragment in informatii["exemplu"].lower()
        ):
            rezultate.append((termen, informatii))

    if rezultate:
        print("\nRezultate găsite:")
        for termen, informatii in rezultate:
            print(f'\nTermen: {termen}')
            print(f'Definiție: {informatii["definiție"]}')
            print(f'Categorie: {informatii["categorie"]}')
            print(f'Exemplu: {informatii["exemplu"]}')
            return

        print("Nu s-au găsit termeni care să conțină fragmentul introdus.")


def actualizeaza_termen(glosar):
    termen = input("Introdu termenul de actualizat: ").strip().lower()

    if termen not in glosar:
        print("Termenul nu există în glosar.")
        return

    print("\nCe dorești să modifici?")
    print("1. Definiție")
    print("2. Categorie")
    print("3. Exemplu")

    optiune = input("Alege opțiunea: ").strip()

    if optiune == "1":
        valoare_noua = input("Introdu noua definiție: ").strip()
        if valoare_noua == "":
            print("Eroare: definiția nu poate fi goală.")
            return
        glosar[termen]["definiție"] = valoare_noua
        print("Definiția a fost actualizată.")
    elif optiune == "2":
        valoare_noua = input("Introdu noua categorie: ").strip()
        if valoare_noua == "":
            print("Eroare: categoria nu poate fi goală.")
            return
        glosar[termen]["categorie"] = valoare_noua
        print("Categoria a fost actualizată.")
    elif optiune == "3":
        valoare_noua = input("Introdu noul exemplu: ").strip()
        if valoare_noua == "":
            print("Eroare: exemplul nu poate fi gol.")
            return
        glosar[termen]["exemplu"] = valoare_noua
        print("Exemplul a fost actualizat.")
    else:
        print("Opțiune invalidă.")


def sterge_termen(glosar):
    termen = input("Introdu termenul de șters: ").strip().lower()

    if termen in glosar:
        del glosar[termen]
        print(f'Termenul "{termen}" a fost șters.')
    else:
        print("Termenul nu există în glosar.")


def afiseaza_tot(glosar):
    if not glosar:
        print("Glosarul este gol.")
        return

    print("\n===== TOȚI TERMENII DIN GLOSAR =====")
    for termen, informatii in glosar.items():
        print(f'\nTermen: {termen}')
        print(f'Definiție: {informatii["definiție"]}')
        print(f'Categorie: {informatii["categorie"]}')
        print(f'Exemplu: {informatii["exemplu"]}')


def afiseaza_statistici(glosar):
    total = len(glosar)
    categorii = {}

    for informatii in glosar.values():
        categorie = informatii["categorie"]
        if categorie in categorii:
            categorii[categorie] += 1
        else:
            categorii[categorie] = 1

    print("\n===== STATISTICI =====")
    print(f"Număr total de termeni: {total}")
    print("Număr de termeni pe categorii:")

    if categorii:
        for categorie, numar in categorii.items():
            print(f"- {categorie}: {numar}")
    else:
        print("Nu există categorii.")


def salveaza_csv(glosar, nume_fisier="glosar.csv"):
    try:
        with open(nume_fisier, mode="w", newline="", encoding="utf-8") as fisier:
            writer = csv.writer(fisier)
            writer.writerow(["termen", "definiție", "categorie", "exemplu"])

            for termen, informatii in glosar.items():
                writer.writerow([
                    termen,
                    informatii["definiție"],
                    informatii["categorie"],
                    informatii["exemplu"]
                ])

        print(f'Glosarul a fost salvat în fișierul "{nume_fisier}".')
    except Exception as e:
        print(f"Eroare la salvare: {e}")


def incarca_csv(nume_fisier="glosar.csv"):
    glosar_nou = {}

    try:
        with open(nume_fisier, mode="r", newline="", encoding="utf-8") as fisier:
            reader = csv.DictReader(fisier)

            for linie in reader:
                termen = linie["termen"].strip().lower()
                glosar_nou[termen] = {
                    "definiție": linie["definiție"].strip(),
                    "categorie": linie["categorie"].strip(),
                    "exemplu": linie["exemplu"].strip()
                }

        print(f'Glosarul a fost încărcat din fișierul "{nume_fisier}".')
        return glosar_nou

    except FileNotFoundError:
        print("Eroare: fișierul nu există.")
        return None
    except KeyError:
        print("Eroare: fișierul CSV nu are formatul corect.")
        return None
    except Exception as e:
        print(f"Eroare la încărcare: {e}")
        return None


def ruleaza_aplicatia():
    glosar = initializare_glosar()

    while True:
        afiseaza_meniu()
        optiune = input("Alege o opțiune: ").strip()

        if optiune == "1":
            adauga_termen(glosar)
        elif optiune == "2":
            cautare_exacta(glosar)
        elif optiune == "3":
            cautare_fragment(glosar)
        elif optiune == "4":
            actualizeaza_termen(glosar)
        elif optiune == "5":
            sterge_termen(glosar)
        elif optiune == "6":
            afiseaza_tot(glosar)
        elif optiune == "7":
            afiseaza_statistici(glosar)
        elif optiune == "8":
            nume = input("Introdu numele fișierului CSV (sau Enter pentru glosar.csv): ").strip()
            if nume == "":
                nume = "glosar.csv"
            salveaza_csv(glosar, nume)
        elif optiune == "9":
            nume = input("Introdu numele fișierului CSV (sau Enter pentru glosar.csv): ").strip()
            if nume == "":
                nume = "glosar.csv"
            glosar_incarcat = incarca_csv(nume)
            if glosar_incarcat is not None:
                glosar = glosar_incarcat
        elif optiune == "0":
            print("Programul s-a încheiat.")
            break
        else:
            print("Opțiune invalidă. Te rog alege o variantă din meniu.")


if __name__ == "__main__":
    ruleaza_aplicatia()