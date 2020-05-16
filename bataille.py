"""
Titre: Bataille navale
Auteur: Paul Georges
Description: 
-Implémentation du jeu de bataille navale(https://fr.wikipedia.org/wiki/Bataille_navale_(jeu))
"""

# Importations
from copy import deepcopy   #Pour que les cartes des joueurs soient différentes, la méthode .copy() ne marche pas.

# Constantes

EMPTY_ROW = [0 for _ in range(10)] #Ligne vide, c'est à dire que avec des zéros.
COLUMN_IDENTIFIERS = ['A','B','C','D','E','F','G','H','I','J'] #Identifiants des colonnes.
EMPTY_MAP = {}
for i in COLUMN_IDENTIFIERS:
    EMPTY_MAP[i] = EMPTY_ROW.copy()
BOATS = {2:1, 3:2, 4:1, 5:1}    #Les bateaux organisés sous la forme taille:nombre

# Fonctions

## Fonctions d'input
def squareInput():
    """Fonction qui demande une case à l'utilisateur, et convertit la chaine en tuple.\n
    Dépend de EMPTY_MAP."""
    while True:
        try:
            square = input("Donner la case(ligne, colonne): ")
            row = square[0]        #row prend le premier caractère.
            column = int(square[1:])  #column prend le reste des caractères, convertit en entier.
            test_squ = EMPTY_MAP[row][int(column)-1]
            return (row, column-1)
        except ValueError:
            print("Erreur! Plus ou moins de deux caractères, ou colonne qui n'est pas un nombre.\n")
        except KeyError:
            print("Erreur! La case {} n'est pas sur la grille.\n".format(square))
        except IndexError:
            print("Erreur! La case {} n'est pas sur la grille.\n".format(square))

## Fonctions d'exécution

def rowSubstraction(row1, row2):
    return ord(row1) - ord(row2)

def changeSquare(userSquare, map, value):
    """Permet de changer la valeur d'une case à partir
    de l'info donner par l'utilisateur."""
    row, column = userSquare
    map[row][column] = value

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
    print("#############################")
    print("\t", end="")
    for column_name in range(10):
        print(column_name+1,end=" ")
    print("")

    for row_name, row in map.items():
        print(row_name,end="\t")
        for square in row:
            print(displaySquare(square,True),end=" ")
        print("")
    print("#############################\n")

def displayMaps(map1, map2):
    """Affiche les deux cartes simultanément, sans donner d'information à l'adversaire."""
    print("#############################")
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
    print("#############################\n")

## Fonctions principales

def prepPhase(map, boats):
    """Prépare la carte pour un des joueurs.
    C'est la phase de placement des bateaux."""
    number_boats = sum(boats.values())
    while number_boats != 0:
        print("Donner les cases de début et de fin de votre bateau.")
        print("Il vous reste : ")
        for taille, nombre in boats.items():
            print("{} bateau de taille {}".format(nombre, taille))
        square1 = squareInput()
        square2 = squareInput()
        row1, column1 = square1
        row2, column2 = square2
        print(row1, column1, row2, column2)
    #displayMapPrep(map)
    #return map

# Main 
mapP1 = deepcopy(EMPTY_MAP)
mapP2 = deepcopy(EMPTY_MAP)

displayMapPrep(mapP1)