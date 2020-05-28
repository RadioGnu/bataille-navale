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
    """Détermine si coord1 est plus grand que coord2.
    Si coord1 et coord2 ne sont pas du même type, appelle TypeError."""
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
    elif type(coord1) is str:
        diff = ord(coord2) - ord(coord1) +1
    return diff

def changeSquares(map, lign, begin, end, value):
    """Change plusieurs cases, sur la carte map, 
    sur la ligne lign, de begin à end.
    Si il y a déjà un bateau sur une des cases, appelle OverlapError."""
    if type(lign) is str:
        if value == 2:      #On essaye de placer un bateau, donc on vérifie si il y en a déjà un.
            for otherLign in range(begin, end+1):
                if map[lign][otherLign] == 2:
                    raise OverlapError
        for otherLign in range(begin, end+1):
            map[lign][otherLign] = value
    elif type(lign) is int:
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
    noBoats = boats[diff][0] == 0   #Il n'y a plus de bateaux de la taille demandée.
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
    """Regarde si il reste des bateaux à un des joueurs.
    Pendant la phase de bataille."""
    noBoats = True
    for i in boats.values():
        noBoats = noBoats and len(i) == 1
    return noBoats

def sinkBoat(lign, begin, end):
    """Fait couler le bateau et créée un message pour prévenir les joueurs."""
    changeSquares(map, lign, begin, end, 4)
    sinkMsg = "Le bateau allant de {}{} à {}{} est coulé!".format(
            lign, begin+1, lign, end+1)
    return sinkMsg

def checkSinkedAndSink(map, row, column, boats):
    """Regarde si un bateau est touché sur chacune de ces cases.\n
    Dans ce cas, le fait couler, et renvoie un message."""
    sinkMsg = ""
    for coords in boats.values():
        for index, boat in enumerate(coords):
            isSinked = True
            lign, begin, end = boat
            if row == lign:         #La case touchée est sur la même ligne que le bateau. (horizontal)
                for otherLign in range(begin, end+1):
                    isSinked = isSinked and map[lign][otherLign] == 3
                if isSinked:
                    lign, begin, end = coords.pop(index)
                    sinkMsg = sinkBoat(lign, begin, end)
            elif column == lign:    #La case touchée est sur la même ligne que le bateau. (vertical)
                identifiers = map.keys()
                begin = identifiers.index(begin)
                end = identifiers.index(end)
                row = identifiers.index(row)
                for otherLign in identifiers[begin:end+1]:
                    isSinked = isSinked and map[otherLign][lign] == 3
                if isSinked:
                    lign, begin, end = coords.pop(index)
                    sinkMsg = sinkBoat(lign, begin, end)
    return sinkMsg