"""Module logique du programme."""

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
        identifiers = list(map.keys())
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
                        msg = "Le bateau allant de {}{} à {}{} est coulé!".format(
                            lign, begin+1, lign, end+1)
                        changeSquares(map, lign, begin, end, 4)
                        return msg
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
                        msg = "Le bateau allant de {}{} à {}{} est coulé!".format(
                            begin, lign+1, end, lign+1)
                        changeSquares(map, lign, begin, end, 4)
                        return msg
    return ""