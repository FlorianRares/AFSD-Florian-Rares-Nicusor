def creeaza_tabla():
    return [['.' for _ in range(3)] for _ in range(3)]


def afiseaza(tabla):
    print("  0 1 2")
    for i in range(3):
        print(i, " ".join(tabla[i]))
    print()

def citeste_mutare(tabla, jucator):
    while True:
        try:
            print(f"Rândul jucătorului {jucator}")
            linie = int(input("Linia (0-2): "))
            coloana = int(input("Coloana (0-2): "))
            if linie < 0 or linie > 2 or coloana < 0 or coloana > 2:
                print("Eroare: coordonate în afara tablei!")
                continue
            if tabla[linie][coloana] != '.':
                print("Eroare: poziția este deja ocupată!")
                continue

            return linie, coloana

        except ValueError:
            print("Eroare: trebuie să introduceți numere întregi!")


def stare_joc(tabla):
    for i in range(3):
        if tabla[i][0] == tabla[i][1] == tabla[i][2] != '.':
            return tabla[i][0]

    for j in range(3):
        if tabla[0][j] == tabla[1][j] == tabla[2][j] != '.':
            return tabla[0][j]

    if tabla[0][0] == tabla[1][1] == tabla[2][2] != '.':
        return tabla[0][0]

    if tabla[0][2] == tabla[1][1] == tabla[2][0] != '.':
        return tabla[0][2]


    for linie in tabla:
        if '.' in linie:
            return "CONTINUA"

    return "EGAL"


def joc_x_si_0():
    tabla = creeaza_tabla()
    jucator_curent = 'X'

    while True:
        afiseaza(tabla)
        linie, coloana = citeste_mutare(tabla, jucator_curent)
        tabla[linie][coloana] = jucator_curent

        stare = stare_joc(tabla)
        if stare != "CONTINUA":
            afiseaza(tabla)
            if stare == "EGAL":
                print("Jocul s-a terminat la egalitate!")
            else:
                print(f"Jucătorul {stare} a câștigat!")
            break


        jucator_curent = 'O' if jucator_curent == 'X' else 'X'


joc_x_si_0()