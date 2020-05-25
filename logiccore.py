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
def squareInput(map):
    """Fonction qui demande une case à l'utilisateur, et convertit la chaine en tuple.\n"""
    while True:
        try:
            square = input("Donner la case(ligne, colonne): ")
            row = square[0].upper()   #row prend le premier caractère.
            column = int(square[1:])  #column prend le reste des caractères, convertit en entier.
            test_squ = map[row][int(column)-1]  #On teste si la case appartient bien à la carte.
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
        identifiers = map.keys()
        begin = identifiers.index(begin)
        end = identifiers.index(end)
        if value == 2:
            for otherLign in identifiers[begin:end+1]:
                if map[otherLign][lign] == 2:
                    raise OverlapError
        for otherLign in identifiers[begin:end+1]:
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
        reset = input("Voulez vous enlever le dernier bateau placé?(o/n) ")
        if reset == 'o':
            resetBoat(map, lign, begin, end, diff, boats)
        else:
            boats[diff].append((lign, begin, end))
    except KeyError:
        print("Erreur! Le bateau n'est pas d'une taille existante.\n")
    except OverlapError:
        print("Erreur! Il y a un déjà un bateau sur une des cases.\n")
    except NoMoreBoatsError:
        print("Erreur! Il n'y a plus de bateaux de cette taille.\n")

def hasNoBoats(boats):
    """Regarde si il reste des bateaux à un des joueurs."""
    noBoats = True
    for i in boats.values():
        noBoats = noBoats and len(i) == 1
    return noBoats

def sinkBoat(map, row, column, boats):
    """Fait couler un bateau."""
    for coords in boats.values():
        for index, boat in enumerate(coords):
            isSinked = True
            lign, begin, end = boat
            if row == lign:
                if column in range(begin, end+1):
                    for otherLign in range(begin, end+1):
                        isSinked = isSinked and map[lign][otherLign] == 3
                    if isSinked:
                        lign, begin, end = coords.pop(index)
                        print("Le bateau allant de {}{} à {}{} est coulé!".format(
                            lign, begin+1, lign, end+1))
                        changeSquares(map, lign, begin, end, 4)
            if column == lign:
                identifiers = map.keys()
                begin = identifiers.index(begin)
                end = identifiers.index(end)
                row = identifiers.index(row)
                if row in range(begin, end+1):
                    for otherLign in identifiers[begin:end+1]:
                        isSinked = isSinked and map[otherLign][lign] == 3
                    if isSinked:
                        lign, begin, end = coords.pop(index)
                        print("Le bateau allant de {}{} à {}{} est coulé!".format(
                            begin, lign+1, end, lign+1))
                        changeSquares(map, lign, begin, end, 4)

def attackSquare(map, row, column, boats):
    """Attaque d'une case par un joueur. Cela modifie l'état de cette case."""
    value = map[row][column]
    if value == 0:
        print("Plouf! C'est raté.\n")
        map[row][column] = 1
    elif value == 2:
        print("Touché! C'est réussi.\n")
        map[row][column] = 3
        sinkBoat(map, row, column, boats)
    else:
        raise AttackedError