# IMPORTATIONS

import turtle
from random import randint

# CONFIGURATION
turtle.setup(width=1000, height=800)
turtle.speed(0) # Vmax
turtle.hideturtle() # Evite de montrer les tracés

x_depart = -480 # 20 px du bord gauche
y_depart = -300 # 200 px au dessus du sol

COULEURS_FACADE = ["yellow", "beige", "orange", "cyan", "lightgray", "white", "pink"]
COULEURS_PORTE = ["brown", "red", "black", "darkgray", "blue"]
COULEURS_TOIT = ["red", "darkgray", "blue", "black", "green"]

# NUAGES

# Creation du type Nuages
class Nuages:
    def __init__(self, width : int, height : int) -> None:
        """
        Initialise la classe Nuages (creation d'un nouveau type comme
        <int> ou <str>, en prenant la hauteur et la largeur en argument)
        """
        self.x = -580 # Commence toujours hors de l'ecran
        self.y = randint(300, 350) # Hauteur aléatoire
        self.speed = randint(5, 10) # Vitesse aléatoire
        self.width = width # Largeur
        self.height = height # Hauteur
 
        self.crayon = turtle.Turtle() # Cree une nouvelle couche sur laquelle le crayon "crayon" seul écrit
        self.crayon.hideturtle()
        self.crayon.speed(0)

    def draw(self) -> None:
        """
        On dessine le nuage
        """
        self.crayon.penup()
        self.crayon.goto(self.x, self.y)
        self.crayon.pendown()

        self.crayon.color("black", "white")
        self.crayon.begin_fill()

        for i in range(2):
            self.crayon.forward(self.width)
            self.crayon.left(90)
            self.crayon.forward(self.height)
            self.crayon.left(90)

        self.crayon.end_fill()
        self.crayon.penup()

    def effacer(self) -> None:
        """
        On efface toute la couche  sur laquelle le crayon "crayon" écrit, soit tous les nuages 
        """
        self.crayon.clear()

# Trace des nuages
def animation() -> None:
    """
    On cree une animation du déplacement des nuages
    """
    global nuages

    # Création aléatoire d'un nouveau nuage avec 1/5 chance de "naître"
    if randint(1, 5) == 2:
        nuages.append(Nuages(randint(20, 30), randint(20, 30)))

    # Déplacement et suppression des nuages
    for nuage_actuel in nuages.copy(): # On conserve la liste originale aussi précieusement qu'on utilise l'ArM ou lieu du vrai ADN
        nuage_actuel.effacer() # On efface tous les nuages
        nuage_actuel.x += nuage_actuel.speed # On avance en fonction de la vitesse du nuage

        if nuage_actuel.x > 1020: # Quand le nuage n'est plus visible, on le supprime
            nuages.remove(nuage_actuel)
        else:
            nuage_actuel.draw()

    # Programmer la prochaine mise à jour
    turtle.ontimer(animation, 50)


# SOL
def sol() -> None:
    """
    Trace le sol
    """
    turtle.up()
    turtle.goto(x_depart, y_depart)
    turtle.down()
    turtle.pensize(3)
    turtle.forward(950)
    turtle.pensize(1)


# FENETRES
def rectangle(x : int, y : int, largeur : int, hauteur : int, couleur : str) -> None:
    """
    Trace un rectangle qui sera la base de plusieurs autres fonctions
    """
    turtle.up()
    turtle.goto(x, y)
    turtle.setheading(0)
    turtle.down()
    turtle.color("black", couleur)
    turtle.begin_fill()
    for _ in range(2):
        turtle.forward(largeur)
        turtle.left(90)
        turtle.forward(hauteur)
        turtle.left(90)
    turtle.end_fill()


def fenetre_rdc(x : int, y : int) -> None:
    """
    On trace la fenêtre du rez-de-chaussée
    """
    rectangle(x + 20, y + 35, 40, 35, "lightblue")


def fenetre_etage(x : int, y : int) -> None:
    """
    On trace les fenêtres des étages supérieurs
    """
    rectangle(x + 20, y + 20, 40, 60, "lightblue")
    rectangle(x + 90, y + 20, 40, 60, "lightblue")


# BALCON
def balcon_dessin(x : int, y : int) -> None:
    """
    On trace un balcon
    """
    turtle.color("black", "darkgray")

    # Base du balcon
    turtle.up()
    turtle.goto(x, y)
    turtle.setheading(0)
    turtle.down()
    turtle.begin_fill()
    for _ in range(2):
        turtle.forward(40)
        turtle.left(90)
        turtle.forward(4)
        turtle.left(90)
    turtle.end_fill()

    # Barres horizontales
    turtle.up()
    turtle.goto(x, y + 4)
    turtle.setheading(0)
    turtle.down()
    turtle.forward(40)

    turtle.up()
    turtle.goto(x, y + 20)
    turtle.down()
    turtle.forward(40)

    # Barres verticales
    for i in range(5, 40, 10):
        turtle.up()
        turtle.goto(x + i, y + 4)
        turtle.setheading(90)
        turtle.down()
        turtle.forward(16)

    turtle.up()


# REZ-DE-CHAUSSEE
def etage0(couleur : str ="lightgray" ) -> None:
    """
    On trace les rez-de-chaussée, avec la couleur lightgray par défaut
    """
    rectangle(x_depart, y_depart, 150, 100, couleur)
    fenetre_rdc(x_depart, y_depart)


# PORTE
def porte(couleur_porte : str ="brown") -> None:
    """
    On trace la porte, avec la couleur brown par défaut
    """
    rectangle(x_depart + 80, y_depart, 50, 80, couleur_porte)


# ETAGES
def etage_X(num_etage : int, couleur : str ="lightgray") -> None:
    """
    Trace l'étage X, avec lightgray comme couleur par défaut
    """
    y_etage = y_depart + num_etage * 100 # On définit la hauteur
    rectangle(x_depart, y_etage, 150, 100, couleur) 
    fenetre_etage(x_depart, y_etage)
    balcon_dessin(x_depart + 20, y_etage + 20)
    balcon_dessin(x_depart + 90, y_etage + 20)


# TOITS
def toit_plat(nb_etages : int, couleur : str ="darkgray") -> None:
    """
    On trace un toit plat, avec la couleur darkgray par défaut
    """
    y_toit = y_depart + (nb_etages + 1) * 100 # On définit la hauteur
    turtle.up()
    turtle.goto(x_depart, y_toit)
    turtle.setheading(0)
    turtle.down()
    turtle.pensize(4)
    turtle.color(couleur)
    turtle.forward(150)
    turtle.pensize(1)


def toit_adc(nb_etages: int, couleur : str ="red") -> None:
    """
    On trace un toit arc de cercle avec comme couleur par défaut red
    """
    x_toit = x_depart # On définit la distance avec le debut de la rue 
    y_toit = y_depart + (nb_etages + 1) * 100 # On définit la hauteur
    turtle.setheading(0)
    turtle.up()
    turtle.goto(x_toit , y_toit)
    turtle.forward(150)
    turtle.setheading(90)
    turtle.down()
    turtle.pensize(2)
    turtle.color("black", couleur)
    turtle.begin_fill()
    turtle.circle(75, extent=180) # Un demi-cercle
    turtle.end_fill()
    turtle.pensize(1)


def toit_triangle(nb_etages : int, couleur : str ="red") -> None:
    """
    On trace un toit triangle avec la couleur red par défaut
    """
    y_toit = y_depart + (nb_etages + 1) * 100 # On définit la hauteur
    turtle.up()
    turtle.goto(x_depart, y_toit)
    turtle.setheading(0)
    turtle.down()
    turtle.pensize(2)
    turtle.color("black", couleur)
    turtle.begin_fill()
    for _ in range(3):
        turtle.forward(150)
        turtle.left(120)
    turtle.end_fill()
    turtle.pensize(1)


# PASSER A LA MAISON SUIVANTE
def nouvelle_maison() -> None:
    """
    On actualise la distance au bord gauche de la rue
    """
    global x_depart
    x_depart += 185


# PROGRAMME PRINCIPAL
sol() # On commence par tracer le sol

# Nombre de maisons
nb_maison = 0 # On commence sans maisons
while nb_maison < 1 or nb_maison > 4: # On attend un nombre de maison qui appratient à [1;4]
    try: # On execute le code...
        nb_maison = int(input("Nombre de maisons (1 à 4) : "))
    except ValueError:# ... et si ça plante on prend l'erreur en charge pour éviter l'arrêt du code et la perte de toute sauvegarde
        print("Veuillez entrer un nombre entier valide.")

# Dessin des maisons
for i in range(nb_maison): 
    print(f"\n--- Bâtiment N° {i + 1} ---")

    # Nombre d'étages
    nb_etage = -1
    while nb_etage < 0 or nb_etage > 4:
        try:
            nb_etage = int(input("Nombre d'étages (0 à 4) : "))
        except ValueError:
            print("Veuillez entrer un nombre entier valide.")

    # Couleurs
    couleur_facade = ""
    while couleur_facade not in COULEURS_FACADE:
        couleur_facade = input(f"Couleur de la façade {COULEURS_FACADE} : ").lower().strip()

    couleur_porte = ""
    while couleur_porte not in COULEURS_PORTE:
        couleur_porte = input(f"Couleur de la porte {COULEURS_PORTE} : ").lower().strip()

    # Dessin du bâtiment
    etage0(couleur_facade)
    porte(couleur_porte)

    for j in range(1, nb_etage + 1):
        etage_X(j, couleur_facade)

    # Choix du toit
    quel_toit = ""
    while quel_toit not in ["triangle", "plat", "ardc"]:
        quel_toit = input("Quel toit (triangle, plat, ardc) : ").lower().strip()

    couleur_toit = ""
    while couleur_toit not in COULEURS_TOIT:
        couleur_toit = input(f"Couleur du toit {COULEURS_TOIT} : ").lower().strip()

    if quel_toit == "triangle":
        toit_triangle(nb_etage, couleur_toit)
    elif quel_toit == "plat":
        toit_plat(nb_etage, couleur_toit)
    else:
        toit_adc(nb_etage, couleur_toit)

    nouvelle_maison()

print("Une super rue moderne !")

nuages = []
animation()
turtle.done()
