"""Module pour l'affichage du programme."""

import os

def clear():
    """Enlève tout ce qui est à l'écran."""
    if os.name =='nt':
        os.system('cls')
    else:
        os.system('clear') 

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
        return 'C'

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