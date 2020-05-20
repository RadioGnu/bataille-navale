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
BOATS = {2:[1], 3:[2], 4:[1], 5:[1]}    #Les bateaux organisés sous la forme taille:nombre

# Erreurs
class OverlapError(Exception):
    """Erreur quand on essaye de placer une case bateau sur une case
    qui a déjà un bateau."""
    pass

class NoMoreBoatsError(Exception):
    """Erreur quand on essaye de placer un bateau d'une taille qui
    n'est plus disponible."""
    pass

class AttackedError(Exception):
    """Erreur quand on attaque une case déjà attaquée."""
    pass

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

def isBigger(coord1, coord2):
    """Détermine si coord1 est plus grand que coord2."""
    if type(coord1) is str and type(coord2) is str:
        return ord(coord1) > ord(coord2)
    elif type(coord1) is int and type(coord2) is int:
        return coord1 > coord2
    else:
        raise TypeError

def difference(coord1, coord2):
    """Fait la différence entre deux coordonnées.
    Coord 1 < coord2.  
    Ex: 3-1 = 2 et C - A = 2"""
    if type(coord1) is int:
        diff = coord2 - coord1 +1
    if type(coord1) is str:
        diff = ord(coord2) - ord(coord1) +1
    return diff

def changeSquares(map, lign, begin, end, value):
    """Change plusieurs cases, sur la carte map, 
    sur la ligne lign, de begin à end."""
    if type(lign) is str:
        if value == 2:      #On essaye de placer un bateau, donc on vérifie si il y en a déjà un.
            for otherLign in range(begin, end+1):
                if map[lign][otherLign] == 2:
                    raise OverlapError
        for otherLign in range(begin, end+1):
            map[lign][otherLign] = value
    if type(lign) is int:
        begin = COLUMN_IDENTIFIERS.index(begin)
        end = COLUMN_IDENTIFIERS.index(end)
        if value == 2:
            for otherLign in COLUMN_IDENTIFIERS[begin:end+1]:
                if map[otherLign][lign] == 2:
                    raise OverlapError
        for otherLign in COLUMN_IDENTIFIERS[begin:end+1]:
            map[otherLign][lign] = value

def placeBoat(map, lign, begin, end, diff, boats):
    """Place un bateau en vérifiant si il n'y a pas déjà
    de bateau là où il est placé."""
    noBoats = boats[diff][0] == 0
    if noBoats:
        raise NoMoreBoatsError
    else:
        boats[diff][0] -= 1
        changeSquares(map, lign, begin, end, 2)

def resetBoat(map, lign, begin, end, diff, boats):
    """Enlève un bateau de la carte."""
    boats[diff][0] += 1    #On remet le bateau dans le compteur
    changeSquares(map, lign, begin, end, 0)

def placeOrReset(map, lign, begin, end, boats):
    """Place le bateau demandé par l'utilisateur et lui demande si
    il veut l'enlever."""
    try:
        diff = difference(begin, end)
        placeBoat(map, lign, begin, end, diff, boats)
        displayMapPrep(map)
        reset = input("Voulez vous enlever le dernier bateau placé?(o/n) ")
        if reset == 'o':
            resetBoat(map, lign, begin, end, diff, boats)
        boats[diff].append((lign, begin, end))
    except KeyError:
        print("Erreur! Le bateau n'est pas d'une taille existante.\n")
    except OverlapError:
        print("Erreur! Il y a un déjà un bateau sur une des cases.\n")
    except NoMoreBoatsError:
        print("Erreur! Il n'y a plus de bateaux de cette taille.\n")

def isSinked(map, row, column):
    """Regarde si un bateau doit couler."""
    pass

def attackSquare(map, row, column, boats):
    """Attaque d'une case par un joueur. Cela modifie l'état de cette case."""
    value = map[row][column]
    if value == 0:
        print("Plouf! C'est raté.\n")
        map[row][column] = 1
    elif value == 2:
        print("Touché! C'est réussi.\n")
        map[row][column] = 3
        isSinked(map, row, column)
    else:
        raise AttackedError

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
            return 'B'
    if square == 0 or square == 2:
        return '~'
    elif square == 1:
        return 'x'
    elif square == 3:
        return 'o'
    elif square == 4:
        return 'c'

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
    print("\n########### Joueur 1 ##########\t",
            "########### Joueur 2 ##########")
    for _ in range(2):
        print("\t", end="")
        for column_name in range(10):
            print(column_name+1,end=" ")
        print("\t", end="")    
    print("")
    
    for (row_name1, row1), (row_name2, row2) in zip(map1.items(), map2.items()):
        print(row_name1,end="\t")
        for square1 in row1:
            print(displaySquare(square1),end=" ")
        print("\t", row_name2, end="\t")
        for square2 in row2:
            print(displaySquare(square2),end=" ")
        print("")
    print("\n")

## Fonctions principales

def prepPhase(map, boats):
    """Prépare la carte pour un des joueurs.
    C'est la phase de placement des bateaux."""
    displayMapPrep(EMPTY_MAP)
    while True:
        number_boats = 0
        for i in boats.values():
            number_boats += i[0]
        if number_boats == 0:
            break
        print("Donner les cases de début et de fin de votre bateau.")
        print("Il vous reste : ")
        for taille, nombre in boats.items():
            print("{} bateau(x) de taille {}".format(nombre[0], taille))
        row1, column1 = squareInput()
        row2, column2 = squareInput()
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

'''def battlePhase(map1, map2, boats):
    """Les joueurs choississent à tour de rôle les cases qu'ils veulent attaquer."""
    boatsP1, boatsP2 = boats.copy(), boats.copy()
    displayMaps(mapP1, mapP2)
    while True:
        noBoatsP1 = sum(boatsP1.values()) == 0
        noBoatsP2 = sum(boatsP2.values()) == 0
        if noBoatsP1:
            print("Le joueur 2 a gagné !")
            break
        elif noBoatsP2:
            print("Le joueur 1 a gagné !")
            break
        for turn in range(1,3):
            print("Joueur " + str(turn) + ", attaquez une case.")
            while turn == 1:
                try:
                    row, column = squareInput()
                    attackSquare(map2, row, column, boatsP2)
                    turn = 0    #Le tour est passé
                except AttackedError:
                    print("Vous avez déjà attaqué cette case.")
            while turn == 2:
                try:
                    row, column = squareInput()
                    attackSquare(map1, row, column, boatsP2)
                    turn = 0
                except AttackedError:
                    print("Vous avez déjà attaqué cette case.")
            displayMaps(map1,map2)'''

# Main 
mapP1 = deepcopy(EMPTY_MAP)
mapP2 = deepcopy(EMPTY_MAP)

boatsP1 = BOATS.copy()
boatsP2 = BOATS.copy()

print("C'est au tour du joueur 1 de placer ses bateaux.\n")
prepPhase(mapP1, boatsP1)
print(boatsP1)
"""print("C'est au tour du joueur 2 de placer ses bateaux.\n")
prepPhase(mapP2, BOATS.copy())"""
#changeSquares(mapP1, 'B', 1, 5, 2)
#changeSquares(mapP2, 'B', 1, 5, 2)

#battlePhase(mapP1, mapP2, BOATS)