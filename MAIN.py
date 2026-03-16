
elevi = ["Ana", "Bogdan", "Carmen", "Darius", "Elena"]
note  = [9,       7,        10,       4,        8]

elev_nou        = "Felix"
nota_elev_nou   = 6
elev_de_sters   = "Darius"

interogari_nume = ["Ana", "Mara", "Elena", "stop"]

absente = [1, 0, 2, 3, 0]
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


#new*
    print ('hello')
