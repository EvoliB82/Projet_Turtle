from turtle import *
import math

setup(width = 2000, height = 2000)

d = 500 # Cette variable définit la longueur des immeubles et la distance entre les immeubles
couleurs = [ "red","green","blue","yellow","orange","purple","pink","brown","black","white","gray","cyan",
"magenta","lime","navy","teal","gold","silver","violet", "indigo","turquoise","coral","salmon","maroon", "olive"] #Une liste qui contient les couleurs que l'utilisateur peux demander
forme = ["triangle", "demi-cercle", "plat"] #Une liste qui contient les formes de toit possibles
nb_bat = 0 #Le nombre de batiment est 0 par défaut
espace = True # On met des espaces entre les batiments par défaut
nb_etages = [] # On rentre le nombre d'éléments d'étage

def setup(x : int, y : int, pensize : int = 1) -> None:
    """
    Initialise toutes les fonctions de tracé avec pour coordonnées (x,y)
    """
    penup()
    goto(x,y)
    pendown()
    speed(0)
    begin_fill()
    setheading(0)

def etage(x : int, y : int, clr : str) -> None:
    """
    Trace un etage de coordonnées (x,y) et de couleur clr
    """
    global d
    setup(x,y)
    color("black",clr)
    for i in range(4):
        forward(d)
        left(90)
    end_fill()

def porte(x :int, y : int, clr : str) -> None:
    """
    Trace une porte de coordonnées (x,y) et de couleur clr
    """
    global d
    setup(x,y)
    color(clr, clr)
    for i in range(2):
        forward(d//4)
        left(90)
        forward(d//2)
        left(90)
    end_fill()

def fenetre( x : int, y : int, clr : str) -> None:
    """
    Trace une fentre de coordonnées (x,y) et de couleur clr
    """
    global d
    setup(x,y)
    color(clr, clr)
    for i in range(4):
        forward(d//4)
        left(90)
    end_fill()

def toit_triangulaire(x : int, y : int, clr : str) -> None:
    """
    Trace un toit triangulaire de coordonnées (x,y) et de couleur clr
    """
    global d
    setup(x,y)
    color(clr, clr)
    begin_fill()
    for i in range(3):
        forward(d)
        left(120)
    end_fill()

def toit_circulaire(x :int, y : int, clr : str) -> None:
    """
    Trace un toit circulaire de coordonnées (x,y) et de couleur clr
    """
    global d
    setup(x, y)
    setheading(90)
    begin_fill()
    color(clr, clr)
    circle(d//2, 180)
    end_fill()

def toit_plat(x : int, y :int) -> None:
    """
    Trace un toit plat de coordonnées (x,y)
    """
    setup(x, y, 10)
    pencolor("black")
    forward(d)

def sol():
    taille = pensize()
    pensize(1)
    forward(950)
    up()
    goto(-300, -300)
    down()
    pensize(taille)

hideturtle()



if (__name__ == "__main__"):
    nb_bat = int(input("Bonjour, combien de maisons / immeuble voulez vous construire aujourd'hui (entre 1 et 10) ? ")) #Demande à l'utilisateur de rentrer le nombre de bâtiments à construire
    while (nb_bat <= 0 or nb_bat > 10 ):
        print("La valeur est incorrecte veuillez choisir un nombre de maisons / immeubles copris entre 1 et 10 inclus ")
        nb_bat = int(input())
    demande_espace = input("Voulez vous des espaces entre vos batiments ? (O/N) ")

    if (demande_espace.lower() == "n"):
        espace = False

    if (espace == True):
        d //= (nb_bat*2 - 1)
    else:
        d //= nb_bat

    sol()
    nb_etages.clear()
    for i in range(nb_bat):
        nb_etage = int(input(f"Combien d'étage voulez vous pour le batiment n° {i + 1}  ? "))
        while (nb_etage <= 0 or nb_etage > 3):
            print("La valeur est incorrecte veuillez choisir un nombre d'étges copris entre 1 et 3 inclus ")
            nb_etage = int(input())
        nb_etages.append(nb_etage)

    for batiment in range(nb_bat):
            couleur_etage = ""
            couleur_fenetre = ""
            couleur_porte = ""
            couleur_autorisees = couleurs.copy()
            couleur = " | ".join(couleurs)
            couleurs_aut = " | ".join(couleur_autorisees)


            couleur_etage = input(f"De quelle couleur souhaitez vous que l'étage n° 1 soit ? ({couleur}) ")
            while (couleur_etage.lower() not in couleurs):
                print(f"Votre couleur est invalide. Voici les couleurs : \n {couleur}")
                couleur_etage = input()       
            couleur_autorisees.remove(couleur_etage)
            if (couleur_etage.lower() in couleurs):
                etage(-300 + d * (1 + int(espace)) * batiment, -300 , couleur_etage)
            
            couleur_porte = input(f"De quelle couleur souhaitez vous que la porte soit (une couleur différente de l'étage)? ({couleurs_aut}) ")
            while(couleur_porte.lower() not in couleur_autorisees):
                    print(f"Votre couleur est invalide. Voici les couleurs : \n {couleurs_aut} ")
                    couleur_porte = input()
            if (couleur_porte.lower() in couleurs and couleur_porte != couleur_etage):
                porte(-300 + d * (1 + int(espace)) * batiment + d//2, -300, couleur_porte)    
        
            if (nb_etages[batiment] != 1):
                
                for etages in range(1, nb_etages[batiment]):
                    
                    couleur_etage = input(f"De quelle couleur souhaitez vous que l'étage n° {etages + 1} soit ? ({couleur}) ")
                    while (couleur_etage.lower() not in couleurs):
                        print(f"Votre couleur est invalide. Voici les couleurs : \n {couleur} ")
                        couleur_etage = input()       
                
                    if (couleur_etage.lower() in couleurs):
                        etage(-300 + d * (1 + int(espace)) * batiment, -300 + d*etages, couleur_etage)
                    
                    couleur_fenetre = input(f"De quelle couleur souhaitez vous que la fenêtre soit (une couleur différente de celle de l'étage)? ({couleurs_aut}) ")
                    while(couleur_fenetre.lower() not in couleur_autorisees):
                            print(f"Votre couleur est invalide. Voici les couleurs : \n {couleurs_aut} ")
                            couleur_fenetre = input()  
                
                    if (couleur_fenetre.lower() in couleurs and couleur_fenetre != couleur_etage):
                        fenetre(-300 + d * (1 + int(espace)) * batiment+ d//2, -300 + d*etages + d//2, couleur_fenetre)
            
            forme_toit = input(f"Quelle est la forme de toit que vous souhaitez pour le bâtiment N ° {batiment + 1} (triangle | demi-cercle | plat) ")
            while(forme_toit.lower() not in forme):
                print("La forme ne convient pas, choisissez entre triangle | demi-cercle | plat ")
                forme_toit = input()
            
            if (forme_toit in forme):
            
                if (forme_toit.lower() == "triangle"):            
                    couleur_toit = input(f"De quelle couleur souhaitez vous que le toit soit (une couleur différente de celle de l'étage)? ({couleur}) ")
                
                    while(couleur_toit.lower() not in couleurs or couleur_toit.lower() == couleur_etage):
                            print(f"Votre couleur est invalide. Voici les couleurs : \n {couleur} ")
                            couleur_toit = input()
                    if (nb_etages[batiment] != 1):        
                        toit_triangulaire(-300 + d * (1 + int(espace)) * batiment , -300 + d*(etages + 1), couleur_toit)
                    else:
                        toit_triangulaire(-300 + d * (1 + int(espace) * batiment) , -300 + d , couleur_toit)
                
                elif (forme_toit.lower() == "demi-cercle"):   
                    couleur_toit = input(f"De quelle couleur souhaitez vous que le soit (une couleur différente de celle de l'étage)? ({couleur}) ")
                    
                    while(couleur_toit.lower() not in couleurs or couleur_toit.lower() == couleur_etage):
                            print(f"Votre couleur est invalide. Voici les couleurs : \n {couleur} ")
                            couleur_toit = input()

                    if (nb_etages[batiment] != 1):                        
                        toit_circulaire(-300 + d * (1 + int(espace)) * batiment + d//2 + d//2, -300 + d*(etages+1), couleur_toit)
                    else:
                        toit_circulaire(-300 + d * (1 + int(espace)) * batiment + d//2 + d//2, -300 + d , couleur_toit)
                
                else:
                    if (nb_etages[batiment] != 1):
                        toit_plat(-300 + d * (1 + int(espace)) * batiment, -300 + d*(etages+1))
                    else:
                        toit_plat(-300 + d * (1 + int(espace)) * batiment, -300 + d)

    done()