import csv
import json


def citeste_produse_csv(fisier):
    produse = {}
    try:
        with open(fisier, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for linie in reader:
                id_produs = linie["id"]
                produse[id_produs] = {
                    "nume": linie["nume"],
                    "pret": float(linie["pret"]),
                    "stoc": int(linie["stoc"])
                }
    except FileNotFoundError:
        print(f"Fisierul {fisier} nu a fost gasit.")
    except Exception as e:
        print(f"Eroare la citirea fisierului CSV: {e}")
    return produse


def citeste_reduceri_json(fisier):
    try:
        with open(fisier, mode="r", encoding="utf-8") as f:
            reduceri = json.load(f)
            return reduceri
    except FileNotFoundError:
        print(f"Fisierul {fisier} nu a fost gasit.")
    except Exception as e:
        print(f"Eroare la citirea fisierului JSON: {e}")
    return {}


def afiseaza_meniu(produse):
    print("\n--- MENIU PRODUSE ---")
    for id_produs, detalii in produse.items():
        print(
            f"ID: {id_produs} | "
            f"Nume: {detalii['nume']} | "
            f"Pret: {detalii['pret']} lei | "
            f"Stoc: {detalii['stoc']}"
        )


def adauga_produs(comanda, produse, id_produs, cantitate):
    if id_produs not in produse:
        print("Produs inexistent.")
        return

    if cantitate <= 0:
        print("Cantitatea trebuie sa fie mai mare decat 0.")
        return

    deja_comandat = comanda.get(id_produs, 0)
    stoc_disponibil_real = produse[id_produs]["stoc"] - deja_comandat

    if cantitate > stoc_disponibil_real:
        print("Cantitatea depaseste stocul disponibil.")
        return

    comanda[id_produs] = deja_comandat + cantitate
    print("Produs adaugat cu succes.")


def scade_produs(comanda, id_produs, cantitate):
    if id_produs not in comanda:
        print("Produsul nu exista in comanda.")
        return

    if cantitate <= 0:
        print("Cantitatea trebuie sa fie mai mare decat 0.")
        return

    if cantitate > comanda[id_produs]:
        print("Nu poti scadea mai mult decat exista in comanda.")
        return

    comanda[id_produs] -= cantitate

    if comanda[id_produs] == 0:
        del comanda[id_produs]

    print("Comanda a fost actualizata.")


def calculeaza_total(comanda, produse):
    total = 0
    for id_produs, cantitate in comanda.items():
        total += produse[id_produs]["pret"] * cantitate
    return total


def calculeaza_reducere(total, tip_reducere, reduceri):
    if tip_reducere == "" or tip_reducere not in reduceri:
        return 0

    regula = reduceri[tip_reducere]
    prag = regula["prag"]
    tip = regula["tip"]
    valoare = regula["valoare"]

    if total < prag:
        print(f"Pragul minim pentru reducerea '{tip_reducere}' nu este indeplinit.")
        return 0

    if tip == "procent":
        return total * valoare / 100
    elif tip == "fix":
        return valoare

    return 0


def genereaza_bon(comanda, produse, total, reducere):
    linii = []
    linii.append("===== BON FISCAL =====")

    for id_produs, cantitate in comanda.items():
        nume = produse[id_produs]["nume"]
        pret = produse[id_produs]["pret"]
        subtotal = pret * cantitate
        linii.append(
            f"{nume} | cantitate: {cantitate} | pret unitar: {pret:.2f} lei | subtotal: {subtotal:.2f} lei"
        )

    total_final = total - reducere
    linii.append("----------------------")
    linii.append(f"Total: {total:.2f} lei")
    linii.append(f"Reducere: {reducere:.2f} lei")
    linii.append(f"Total final: {total_final:.2f} lei")
    linii.append("======================")

    return "\n".join(linii)


def scrie_bon_txt(fisier, text_bon):
    try:
        with open(fisier, mode="w", encoding="utf-8") as f:
            f.write(text_bon)
        print(f"Bonul a fost salvat in fisierul {fisier}.")
    except Exception as e:
        print(f"Eroare la scrierea bonului: {e}")


def goleste_comanda(comanda):
    comanda.clear()


def main():
    produse = citeste_produse_csv("produse.csv")
    reduceri = citeste_reduceri_json("reduceri.json")
    comanda = {}
    reducere_curenta = ""

    if not produse:
        print("Nu exista produse disponibile. Programul se opreste.")
        return

    while True:
        print("\n===== MENIU PRINCIPAL =====")
        print("1 - Afisare meniu produse")
        print("2 - Adaugare produs in comanda")
        print("3 - Scadere/eliminare produs din comanda")
        print("4 - Aplicare reducere")
        print("5 - Finalizare comanda")
        print("6 - Anulare comanda")
        print("0 - Iesire")

        optiune = input("Alege o optiune: ")

        if optiune == "1":
            afiseaza_meniu(produse)

        elif optiune == "2":
            id_produs = input("Introdu ID-ul produsului: ")
            try:
                cantitate = int(input("Introdu cantitatea: "))
                adauga_produs(comanda, produse, id_produs, cantitate)
            except ValueError:
                print("Cantitatea trebuie sa fie un numar intreg.")

        elif optiune == "3":
            id_produs = input("Introdu ID-ul produsului de scazut: ")
            try:
                cantitate = int(input("Introdu cantitatea de scazut: "))
                scade_produs(comanda, id_produs, cantitate)
            except ValueError:
                print("Cantitatea trebuie sa fie un numar intreg.")

        elif optiune == "4":
            total = calculeaza_total(comanda, produse)

            if total == 0:
                print("Comanda este goala.")
                continue

            print("\n--- MENIU REDUCERI ---")
            print("1 - student")
            print("2 - happy")
            print("3 - cupon")
            print("4 - fara reducere")
            print("0 - inapoi")

            opt_reducere = input("Alege reducerea: ")

            if opt_reducere == "1":
                reducere_curenta = "student"
                reducere = calculeaza_reducere(total, reducere_curenta, reduceri)
                print(f"Reducere aplicata: {reducere:.2f} lei")
            elif opt_reducere == "2":
                reducere_curenta = "happy"
                reducere = calculeaza_reducere(total, reducere_curenta, reduceri)
                print(f"Reducere aplicata: {reducere:.2f} lei")
            elif opt_reducere == "3":
                reducere_curenta = "cupon"
                reducere = calculeaza_reducere(total, reducere_curenta, reduceri)
                print(f"Reducere aplicata: {reducere:.2f} lei")
            elif opt_reducere == "4":
                reducere_curenta = ""
                print("Reducerea a fost eliminata.")
            elif opt_reducere == "0":
                pass
            else:
                print("Optiune invalida.")

        elif optiune == "5":
            if not comanda:
                print("Comanda este goala.")
                continue

            total = calculeaza_total(comanda, produse)
            reducere = calculeaza_reducere(total, reducere_curenta, reduceri)
            text_bon = genereaza_bon(comanda, produse, total, reducere)

            print("\n" + text_bon)
            scrie_bon_txt("bon.txt", text_bon)

            for id_produs, cantitate in comanda.items():
                produse[id_produs]["stoc"] -= cantitate

            goleste_comanda(comanda)
            reducere_curenta = ""
            print("Comanda a fost finalizata.")

        elif optiune == "6":
            goleste_comanda(comanda)
            reducere_curenta = ""
            print("Comanda a fost anulata.")

        elif optiune == "0":
            print("Program inchis.")
            break

        else:
            print("Optiune invalida.")


if __name__ == "__main__":
    main()