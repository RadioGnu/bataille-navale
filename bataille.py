"""
Titre: Bataille navale
Auteur: Paul Georges
Description: 
-Implémentation du jeu de bataille navale(https://fr.wikipedia.org/wiki/Bataille_navale_(jeu))
"""

# Constantes

EMPTY_ROW = [0 for _ in range(10)] #Ligne vide, c'est à dire que avec des zéros.
COLUMN_IDENTIFIERS = ['A','B','C','D','E','F','G','H','I','J'] #Identifiants des colonnes.
EMPTY_MAP = {}
for i in COLUMN_IDENTIFIERS:
    EMPTY_MAP[i] = EMPTY_ROW.copy()

# Fonctions

## Fonctions d'input
def squareInput():
    """Fonction qui demande une case à l'utilisateur."""
    square = input("Donner la case(ligne, colonne): ")
    row = square[0]
    column = int(square[1])
    return row, column

## Fonctions d'affichage
def displaySquare(square, beginning=False):
    """Renvoie l'affichage de la case par rapport à sa valeur.\n
    -0: Case vide non révélée.
    -1: Case vide révélée.
    -2: Case bateau.
    -3: Case bateau touché.
    -4: Case bateau coulé.
    Le paramètre beginning permet d'afficher ou non les cases bateaux."""
    if beginning:
        if square == 2:
            return '='
    if square == 0 or square == 2:
        return '~'
    if square == 1:
        return 'o'
    if square == 3:
        return 'x'
    if square == 4:
        return 'X'

def displayMapPrep(map):
    """Affiche la carte d'un des joueurs, avec les emplacements des bateaux.
    On appelle cette fonction pour que le joueur puisse voir où sont ses bateaux."""
    print("\t", end="")
    for column_name in range(10):
        print(column_name+1,end=" ")
    print("")

    for row_name, row in map.items():
        print(row_name,end="\t")
        for square in row:
            print(displaySquare(square,True),end=" ")
        print("")

def displayMaps(map1, map2):
    """Affiche les deux cartes simultanément, sans donner d'information à l'adversaire."""
    for _ in range(2):
        print("\t", end="")
        for column_name in range(10):
            print(column_name+1,end=" ")
    print("")
    
    for row_name1, row1 in map1.items():
        print(row_name1,end="\t")
        for square1 in row1:
            print(displaySquare(square1),end=" ")
        """print(row_name2, end="\t")
        for square2 in row2:
            print(displaySquare(square2),end=" ")"""
        print("")


# Main 
mapP1 = EMPTY_MAP.copy()
mapP2 = EMPTY_MAP.copy()

displayMaps(mapP1, mapP2)