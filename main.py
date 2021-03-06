"""
Titre: Bataille navale
Auteur: Paul Georges
Description: 
-Implémentation du jeu de bataille navale(https://fr.wikipedia.org/wiki/Bataille_navale_(jeu))
"""

# Importations
from copy import deepcopy   #Pour que les cartes des joueurs soient totalement indépendantes.
"""try:
    import tkinter as tk
    hasGraphics = True
except ImportError:
    hasGraphics = False"""

from display import displayMapPrep, displayMaps, clear
from logiccore import *

# Constantes

EMPTY_ROW = [0 for _ in range(10)] #Ligne vide, c'est à dire que avec des zéros.
COLUMN_IDENTIFIERS = ['A','B','C','D','E','F','G','H','I','J'] #Identifiants des colonnes.
EMPTY_MAP = {}
for i in COLUMN_IDENTIFIERS:
    EMPTY_MAP[i] = EMPTY_ROW.copy()     #On crée la carte vide, identifiant:ligne vide.
BOATS = {2:[1], 3:[2], 4:[1], 5:[1]}    #Les bateaux organisés sous la forme taille:nombre

# Fonctions

'''def graphical():
    """Demande à l'utlisateur si il veut lancer en interface graphique"""
    answer = input("Voulez-vous lancer en interface graphique? (o/n) ")
    if answer in ('O', 'o'):
        return True
    else:
        return False'''

def squareInput(mapP):
    """Fonction qui demande une case à l'utilisateur, et convertit la chaine de caractères en tuple.\n"""
    while True:
        try:
            square = input("Donner la case(ligne, colonne): ")
            row = square[0].upper()   #row prend le premier caractère, converti en majuscule.
            if square[1] == '-':
                print("Erreur! Pas de nombres négatifs.")
            column = int(square[1:])  #column prend le reste des caractères, convertis en entier.
            test_squ = mapP[row][column-1]  #Si la case n'est pas sur la carte, il y a KeyError
            return (row, column-1)
        except ValueError:
            print("Erreur! Plus ou moins de deux caractères, ou colonne qui n'est pas un nombre.\n")
        except KeyError:
            print("Erreur! La case {} n'est pas sur la grille.\n".format(square))
        except IndexError:
            print("Erreur! La case {} n'est pas sur la grille.\n".format(square))

def wantsReset():
    """Demande à l'utilisateur si il veut enlever son bateau."""
    reset = input("Confirmez-vous le placement du bateau?(o/n) ")
    if reset in ('o', 'O'):
        return False
    else:
        return True

def screenClean():
    """Demande à l'utilisateur si il veut effacer la carte,
    après avoir placé tous ses bateaux."""
    screenClean = ""
    while screenClean not in ('o', 'O'):
        screenClean = input("Voulez-vous passer au joueur suivant? (o/n)")
        print("\n")
    return True

## Fonctions d'exécution

def placeOrReset(mapP, lign, begin, end, boats):
    """Place le bateau demandé par l'utilisateur et lui demande si
    il veut l'enlever."""
    try:
        diff = difference(begin, end)
        placeBoat(mapP, lign, begin, end, diff, boats)
        displayMapPrep(mapP)
        if wantsReset():
            resetBoat(mapP, lign, begin, end, diff, boats)
        else:
            boats[diff].append((lign, begin, end))
    except KeyError:
        print("Erreur! Le bateau n'est pas d'une taille existante.\n")
    except OverlapError:
        print("Erreur! Il y a un déjà un bateau sur une des cases.\n")
    except NoMoreBoatsError:
        print("Erreur! Il n'y a plus de bateaux de cette taille.\n")

def attackSquare(mapP, row, column, boats):
    """Attaque d'une case par un joueur. Cela modifie l'état de cette case."""
    value = mapP[row][column]
    if value == 0:
        print("Plouf! C'est raté.\n")
        mapP[row][column] = 1
    elif value == 2:
        print("Touché! C'est réussi.\n")
        mapP[row][column] = 3
        message = checkSinkedAndSink(mapP, row, column, boats)
        print(message)
    else:
        raise AttackedError

##Fonctions principales

def prepPhase(mapP, boats):
    """Prépare la carte pour un des joueurs.
    C'est la phase de placement des bateaux."""
    displayMapPrep(mapP)
    while True:
        number_boats = 0    #Il s'agit du nombre de bateaux qu'il reste à placer.
        for boat in boats.values():
            number_boats += boat[0] #Le nombre de bateaux d'une certaine taille est stocké au premier index de la liste.
        if number_boats == 0:
            for boat in boats.values():
                del boat[0]     #On enlève le nombre de bateaux à placer, qui n'est plus nécessaire par la suite.
            break
        boatsLeft = "Il vous reste : \n"
        for taille, nombre in boats.items():
            boatsLeft += "{} bateau(x) de taille {}\n".format(nombre[0], taille)
        print(boatsLeft)
        print("Donner les cases de début et de fin de votre bateau.")
        row1, column1 = squareInput(mapP)
        row2, column2 = squareInput(mapP)
#        clear()
        if row1 == row2:    
            if isBigger(column1, column2):
                placeOrReset(mapP, row1, column2, column1, boats)                  
            else:
                placeOrReset(mapP, row1, column1, column2, boats)
        elif column1 == column2:
            if isBigger(row1, row2):
                placeOrReset(mapP, column1, row2, row1, boats)
            else:
                placeOrReset(mapP, column1, row1, row2, boats)
        elif row1 != row2 and column1 != column2:   #Par exemple A1 et E5 ne sont pas alignées.
            print("Erreur! Les cases {}{} et {}{} ne sont pas alignées.\n".format(
                row1,column1+1,row2,column2+1))
    displayMapPrep(mapP)
    if screenClean():
        clear()

def play_turn(name, player_map, boats):
    turn_ongoing = True
    victory = False
    while turn_ongoing:    #Tour joueur 1
        """Pour éviter que le tour se finisse prématurément quand il y a une erreur,
        on fait une boucle while."""
        try:
            row, column = squareInput(player_map)
#            clear()
            attackSquare(player_map, row, column, boats)
            boatsDestroyed = hasNoBoats(boats)
            if boatsDestroyed:
                print(f"{name} a gagné !")
                victory = True
            turn_ongoing = False
        except AttackedError:
            print("Vous avez déjà attaqué cette case.")
    return victory

def battlePhase(map1, map2, boats1, boats2):
    """Les joueurs choississent à tour de rôle les cases qu'ils veulent attaquer."""
    battle_ongoing = True
    name1 = "Joueur 1"
    name2 = "Joueur 2"
    while battle_ongoing:
        displayMaps(map1,map2)
        victory = play_turn(name1, map2, boats2)
        if not victory:
            displayMaps(map1,map2)
            victory = play_turn(name2, map1, boats1)
        if victory:
            battle_ongoing = False
# Main

if __name__ == "__main__":
    try:
        mapP1 = deepcopy(EMPTY_MAP)
        mapP2 = deepcopy(EMPTY_MAP)

        boatsP1 = deepcopy(BOATS)
        boatsP2 = deepcopy(BOATS)

        """if hasGraphics:
            wantsGraphics = graphical()
        else:
            wantsGraphics = hasGraphics

        if wantsGraphics:
            window = tk.Tk()
            window.title("Bataille navale")
            window.geometry("1080x720")
            window.minsize(480,360)
            window.config(background="#607c8e")
            
            window.mainloop()"""

        print("C'est au tour du joueur 1 de placer ses bateaux.\n")
        prepPhase(mapP1, boatsP1)

        print("C'est au tour du joueur 2 de placer ses bateaux.\n")
        prepPhase(mapP2, boatsP2)

        battlePhase(mapP1, mapP2, boatsP1, boatsP2)
    except KeyboardInterrupt:
        print("\n\nControl-C, exiting.")