import json


def incarca_competitori(nume_fisier):
    try:
        with open(nume_fisier, "r", encoding="utf-8") as fisier:
            competitori = json.load(fisier)

            if not isinstance(competitori, list):
                print("Fișierul JSON nu conține o listă validă de competitori.")
                return []

            lista_valida = []
            for competitor in competitori:
                if (
                    isinstance(competitor, dict)
                    and "nume" in competitor
                    and "punctaj" in competitor
                    and "timp" in competitor
                ):
                    lista_valida.append({
                        "nume": str(competitor["nume"]).strip(),
                        "punctaj": int(competitor["punctaj"]),
                        "timp": int(competitor["timp"])
                    })

            return lista_valida

    except FileNotFoundError:
        print(f"Fișierul {nume_fisier} nu a fost găsit.")
        return []
    except json.JSONDecodeError:
        print("Fișierul JSON nu este valid.")
        return []
    except Exception as eroare:
        print(f"A apărut o eroare la citire: {eroare}")
        return []


def afiseaza_competitori(competitori):
    if not competitori:
        print("Lista competitorilor este goală.")
        return

    print("\nLista competitorilor:")
    print(f"{'Nr.':<5}{'Nume':<20}{'Punctaj':<10}{'Timp':<10}")
    print("-" * 45)

    for i, competitor in enumerate(competitori, start=1):
        print(f"{i:<5}{competitor['nume']:<20}{competitor['punctaj']:<10}{competitor['timp']:<10}")


def adauga_competitor(competitori):
    nume = input("Introduceți numele competitorului: ").strip()

    if not nume:
        print("Numele nu poate fi gol.")
        return

    try:
        punctaj = int(input("Introduceți punctajul: "))
        timp = int(input("Introduceți timpul: "))
    except ValueError:
        print("Punctajul și timpul trebuie să fie numere întregi.")
        return

    competitori.append({
        "nume": nume,
        "punctaj": punctaj,
        "timp": timp
    })

    print("Competitor adăugat cu succes.")


def actualizeaza_competitor(competitori):
    if not competitori:
        print("Nu există competitori în listă.")
        return

    nume_cautat = input("Introduceți numele competitorului pe care doriți să-l actualizați: ").strip()

    for competitor in competitori:
        if competitor["nume"].lower() == nume_cautat.lower():
            try:
                competitor["punctaj"] = int(input("Introduceți noul punctaj: "))
                competitor["timp"] = int(input("Introduceți noul timp: "))
                print("Rezultatul competitorului a fost actualizat.")
                return
            except ValueError:
                print("Punctajul și timpul trebuie să fie numere întregi.")
                return

    print("Competitor inexistent.")


def este_mai_bun(a, b):
    """
    Returnează True dacă a trebuie să fie înaintea lui b în clasament.
    Criterii:
    1. punctaj descrescător
    2. timp crescător
    3. nume alfabetic
    """
    if a["punctaj"] != b["punctaj"]:
        return a["punctaj"] > b["punctaj"]

    if a["timp"] != b["timp"]:
        return a["timp"] < b["timp"]

    return a["nume"].lower() < b["nume"].lower()


def quicksort(lista):
    if len(lista) <= 1:
        return lista

    pivot = lista[len(lista) // 2]
    stanga = []
    egal = []
    dreapta = []

    for competitor in lista:
        if (
            competitor["punctaj"] == pivot["punctaj"]
            and competitor["timp"] == pivot["timp"]
            and competitor["nume"].lower() == pivot["nume"].lower()
        ):
            egal.append(competitor)
        elif este_mai_bun(competitor, pivot):
            stanga.append(competitor)
        else:
            dreapta.append(competitor)

    return quicksort(stanga) + egal + quicksort(dreapta)


def afiseaza_clasament(competitori):
    if not competitori:
        print("Nu există competitori pentru clasament.")
        return

    clasament = quicksort(competitori)

    print("\nClasament final:")
    print(f"{'Loc':<5}{'Nume':<20}{'Punctaj':<10}{'Timp':<10}")
    print("-" * 45)

    loc_curent = 1
    for i, competitor in enumerate(clasament):
        if i == 0:
            loc_afisat = 1
        else:
            anterior = clasament[i - 1]
            if (
                competitor["punctaj"] == anterior["punctaj"]
                and competitor["timp"] == anterior["timp"]
            ):
                loc_afisat = loc_curent
            else:
                loc_afisat = i + 1
                loc_curent = loc_afisat

        print(f"{loc_afisat:<5}{competitor['nume']:<20}{competitor['punctaj']:<10}{competitor['timp']:<10}")


def afiseaza_statistici(competitori):
    if not competitori:
        print("Nu există competitori pentru statistici.")
        return

    numar_total = len(competitori)
    punctaje = [c["punctaj"] for c in competitori]
    timpi = [c["timp"] for c in competitori]

    punctaj_maxim = max(punctaje)
    punctaj_minim = min(punctaje)
    media_punctajelor = sum(punctaje) / numar_total
    cel_mai_bun_timp = min(timpi)

    print("\nStatistici competiție:")
    print(f"Număr total de competitori: {numar_total}")
    print(f"Punctaj maxim: {punctaj_maxim}")
    print(f"Punctaj minim: {punctaj_minim}")
    print(f"Media punctajelor: {media_punctajelor:.2f}")
    print(f"Cel mai bun timp: {cel_mai_bun_timp}")


def meniu():
    print("\n--- Sistem de Ranking pentru Competiții Sportive ---")
    print("1. Afișare competitori")
    print("2. Adăugare competitor")
    print("3. Actualizare rezultat competitor")
    print("4. Sortare competitori (Quicksort)")
    print("5. Afișare clasament final")
    print("6. Afișare statistici")
    print("0. Ieșire")


def main():
    nume_fisier = "competitori.json"
    competitori = incarca_competitori(nume_fisier)

    print(f"S-au încărcat {len(competitori)} competitori din fișierul {nume_fisier}.")

    while True:
        meniu()
        optiune = input("Alegeți o opțiune: ").strip()

        if optiune == "1":
            afiseaza_competitori(competitori)

        elif optiune == "2":
            adauga_competitor(competitori)

        elif optiune == "3":
            actualizeaza_competitor(competitori)

        elif optiune == "4":
            if not competitori:
                print("Lista este goală.")
            else:
                competitori = quicksort(competitori)
                print("Competitorii au fost sortați cu succes folosind Quicksort.")

        elif optiune == "5":
            afiseaza_clasament(competitori)

        elif optiune == "6":
            afiseaza_statistici(competitori)

        elif optiune == "0":
            print("Program închis.")
            break

        else:
            print("Opțiune invalidă. Încercați din nou.")


if __name__ == "__main__":
    main()