elevi = ["Ana", "Bogdan", "Carmen", "Darius", "Elena"]
note = [9, 7, 10, 4, 8]

elev_nou = "Felix"
nota_elev_nou = 6
elev_de_sters = "Darius"

interogari_nume = ["Ana", "Mara", "Elena", "stop"]

absente = [1, 0, 2, 3, 0]
#1
for i in range(len(elevi)):
    print(f"{elevi[i]} are nota {note[i]}")
#2
nota_maxima = max(note)
nota_minima = min(note)
print(f"Nota maximă este: {nota_maxima}")
print(f"Nota minimă este: {nota_minima}")
print("\nElevii cu nota maximă:")
for i in range(len(note)):
    if note[i] == nota_maxima:
        print(f" - {elevi[i]}")

print("\nElevii cu nota minimă:")
for i in range(len(note)):
    if note[i] == nota_minima:
        print(f" - {elevi[i]}")
        #f
        for i in range(len(elevi)):
            print(f"{elevi[i]} are nota {note[i]}")
#3
media = sum(note) / len(note)
print(f"Media clasei este: {media:.2f}")
# 4
for i in range(len(elevi)):
    if note[i] >= 5:
        print(f" - {elevi[i]} (nota {note[i]})")

#B5
for i in range(len(elevi)):
    if note[i] >= 5:
        print(f" - {elevi[i]} (nota {note[i]})")
        #b 1
for i in range(len(note)):
    note[i] = note[i] + 1
    if note[i] > 10:
        note[i] = 10

print("Notele după mărire:", note)
# 6.
elev_nou = "Andrei"
nota_elev_nou = 9
elevi.append(elev_nou)
note.append(nota_elev_nou)
print("Lista actualizată de elevi:", elevi)
print("Lista actualizată de note:", note)
#7
elev_de_sters = "Darius"
if elev_de_sters in elevi:
    pozitie = elevi.index(elev_de_sters)
    elevi.pop(pozitie)
    note.pop(pozitie)
    print(f"Elevul '{elev_de_sters}' a fost șters.")
else:
    print(f"Elevul '{elev_de_sters}' nu se află în listă.")
#8
print("Lista actualizată de elevi:", elevi)
print("Lista actualizată de note:", note)
#9
i=0
while i < len(interogari_nume):
    nume = interogari_nume[i]

    if nume.lower() == "stop":
        break

    if nume in elevi:
        index = elevi.index(nume)
        print(f"{nume} are nota {note[index]}")
    else:
        print(f"{nume} nu există în listă.")

    i += 1
# 10
promovati = 0
respins = 0
for nota in note:
    if nota >= 5:
        promovati += 1
    else:
        respins += 1
print(f"Număr de elevi promovați: {promovati}")
print(f"Număr de elevi respinși: {respins}")
# 11
note_promovati = []
for nota in note:
    if nota >= 5:
        note_promovati.append(nota)
if len(note_promovati) > 0:
    media_promovati = sum(note_promovati) / len(note_promovati)
    print(f"Media promovaților este: {media_promovati:.2f}")
else:
    print("Nu există elevi promovați pentru a calcula media.")