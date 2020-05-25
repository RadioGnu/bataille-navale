"""
Titre: Bataille navale
Auteur: Paul Georges
Description: 
-Implémentation du jeu de bataille navale(https://fr.wikipedia.org/wiki/Bataille_navale_(jeu))
"""

# Importations
from copy import deepcopy   #Pour que les cartes des joueurs soient totalement indépendantes.

from display import displayMapPrep, displayMaps, clear
from logiccore import squareInput, placeOrReset, AttackedError, attackSquare, isBigger, hasNoBoats

# Constantes

EMPTY_ROW = [0 for _ in range(10)] #Ligne vide, c'est à dire que avec des zéros.
COLUMN_IDENTIFIERS = ['A','B','C','D','E','F','G','H','I','J'] #Identifiants des colonnes.
EMPTY_MAP = {}
for i in COLUMN_IDENTIFIERS:
    EMPTY_MAP[i] = EMPTY_ROW.copy()
BOATS = {2:[1], 3:[2], 4:[1], 5:[1]}    #Les bateaux organisés sous la forme taille:nombre


## Fonctions principales

def prepPhase(map, boats):
    """Prépare la carte pour un des joueurs.
    C'est la phase de placement des bateaux."""
    displayMapPrep(map)
    while True:
        number_boats = 0
        for boat in boats.values():
            number_boats += boat[0]
        if number_boats == 0:
            for boat in boats.values():
                del boat[0]     #On enlève le nombre de bateaux, qui n'est plus nécessaire par la suite.
                print(boats)
            break
        print("Donner les cases de début et de fin de votre bateau.")
        print("Il vous reste : ")
        for taille, nombre in boats.items():
            print("{} bateau(x) de taille {}".format(nombre[0], taille))
        row1, column1 = squareInput(map)
        row2, column2 = squareInput(map)
        clear()
        displayMapPrep(map)
        if row1 == row2:
            if isBigger(column1, column2):
                placeOrReset(map, row1, column2, column1, boats)                  
            else:
                placeOrReset(map, row1, column1, column2, boats)
        elif column1 == column2:
            if isBigger(row1, row2):
                placeOrReset(map, column1, row2, row1, boats)
            else:
                placeOrReset(map, column1, row1, row2, boats)
        elif row1 != row2 and column1 != column2:
            print("Erreur! Les cases {}{} et {}{} ne sont pas alignées.\n".format(
                row1,column1+1,row2,column2+1))
    displayMapPrep(map)
    screenClean = input("Voulez-vous effacer la carte? (o/n)")
    while screenClean not in ('o', 'O'):
        screenClean = input("Voulez-vous effacer la carte? (o/n)")
    clear()

def battlePhase(map1, map2, boats1, boats2):
    """Les joueurs choississent à tour de rôle les cases qu'ils veulent attaquer."""
    displayMaps(map1, map2)
    while True:
        noBoatsP1 = hasNoBoats(boats1)
        noBoatsP2 = hasNoBoats(boats2)
        if noBoatsP1 and noBoatsP2:
            print("Match nul!")
            break
        elif noBoatsP1:
            print("Le joueur 2 a gagné !")
            break
        elif noBoatsP2:
            print("Le joueur 1 a gagné !")
            break
        
        for turn in range(1,3):
            print("Joueur " + str(turn) + ", attaquez une case.")
            while turn == 1:
                try:
                    row, column = squareInput(map2)
                    clear()
                    attackSquare(map2, row, column, boats2)
                    turn = 0    #Le tour est passé
                except AttackedError:
                    print("Vous avez déjà attaqué cette case.")
            while turn == 2:
                try:
                    row, column = squareInput(map1)
                    clear()
                    attackSquare(map1, row, column, boats1)
                    turn = 0
                except AttackedError:
                    print("Vous avez déjà attaqué cette case.")
            displayMaps(map1,map2)

# Main 
mapP1 = deepcopy(EMPTY_MAP)
mapP2 = deepcopy(EMPTY_MAP)

boatsP1 = deepcopy(BOATS)
boatsP2 = deepcopy(BOATS)

print("C'est au tour du joueur 1 de placer ses bateaux.\n")
prepPhase(mapP1, boatsP1)

print("C'est au tour du joueur 2 de placer ses bateaux.\n")
prepPhase(mapP2, boatsP2)

battlePhase(mapP1, mapP2, boatsP1, boatsP2)