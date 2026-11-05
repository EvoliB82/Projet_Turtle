"""
app_graphique.py - Interface Tkinter du « Générateur de bâtiments »

Fichiers nécessaires dans le MÊME dossier :
    projet_turtle.py   (ton fichier, NON modifié)
    app_graphique.py   (ce fichier)
    musiques/          (dossier où tu déposes tes .mp3, créé automatiquement)

Installation :  pip install pygame        (sert uniquement à lire les MP3)
Lancement    :  python app_graphique.py
"""

import os
import math
import colorsys
import tkinter as tk
from tkinter import ttk

import pygame          # lecture des MP3
import turtle          # pour régler la fenêtre de dessin
import projet_turtle   # tes fonctions de dessin (voir la remarque plus bas)


# ============================================================
# 1. DONNÉES : la configuration de tous les bâtiments
# ============================================================

NB_BAT_MAX = 10
NB_ETAGES_MAX = 3
DOSSIER_MUSIQUES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musiques")


def creer_etage():
    """Retourne un NOUVEAU dictionnaire avec les réglages par défaut d'un étage.
    Les couleurs sont des tuples RGB (rouge, vert, bleu) entre 0 et 255."""
    return {
        "mur": (230, 230, 230),
        "porte": (139, 69, 19),
        "fenetre": (135, 206, 235),
        "toit_type": "triangle",
        "toit_couleur": (200, 30, 30),
    }


def creer_batiment():
    """Un bâtiment = son nombre d'étages + une liste de 3 étages (un dictionnaire chacun).
    On crée toujours 3 étages : si on passe de 3 à 2 étages puis de nouveau à 3,
    l'étage 3 garde ses réglages."""
    etages = []
    for i in range(NB_ETAGES_MAX):
        etages.append(creer_etage())   # un dictionnaire DIFFÉRENT à chaque tour
    return {"nb_etages": 1, "etages": etages}


# La liste de tous les bâtiments : batiments[0] est "Bat 1", batiments[1] est "Bat 2"...
batiments = []
for i in range(NB_BAT_MAX):
    batiments.append(creer_batiment())

# Ce qui est affiché en ce moment (None = rien). On utilise un dictionnaire
# pour pouvoir le modifier dans les fonctions sans écrire "global".
selection = {"batiment": None, "etage": None}


# ============================================================
# 2. COULEURS : du cercle chromatique vers un tuple RGB
# ============================================================

def hsv_vers_rgb(teinte, saturation, luminosite):
    """teinte : 0 à 360 (angle sur le cercle), saturation et luminosité : 0 à 100.
    Retourne un tuple (r, g, b) avec des entiers de 0 à 255."""
    r, g, b = colorsys.hsv_to_rgb(teinte / 360, saturation / 100, luminosite / 100)
    return (round(r * 255), round(g * 255), round(b * 255))


def rgb_vers_hex(rgb):
    """(255, 0, 0) -> '#ff0000' : Tkinter a besoin de ce format pour colorer ses widgets."""
    r, g, b = rgb
    return f"#{r:02x}{g:02x}{b:02x}"


# ============================================================
# 3. DESSIN : on utilise les fonctions de projet_turtle
# ============================================================
# Remarque : importer projet_turtle exécute sa ligne `setup(width=2000, height=2000)`,
# ce qui ouvre une fenêtre Turtle géante. On la redimensionne puis on la cache
# tant qu'on n'a rien à dessiner.

turtle.setup(900, 700)
turtle.screensize(2000, 3400)   # zone de dessin plus grande que la fenêtre (barres de défilement)
turtle.colormode(255)           # IMPORTANT : permet de donner des couleurs en (r, g, b) de 0 à 255
turtle.title("Rue générée")

fenetre_turtle = turtle.getcanvas().winfo_toplevel()
# Si on ferme la fenêtre Turtle, on la cache seulement (pour pouvoir la ré-ouvrir).
fenetre_turtle.protocol("WM_DELETE_WINDOW", fenetre_turtle.withdraw)
fenetre_turtle.withdraw()


def toit_plat_colore(x, y, couleur):
    """toit_plat() de projet_turtle n'accepte pas de couleur (il trace toujours en noir).
    On trace donc la même ligne ici, mais colorée et plus épaisse."""
    projet_turtle.setup(x, y)        # on réutilise le setup de projet_turtle
    turtle.color(couleur, couleur)
    turtle.pensize(8)
    turtle.forward(projet_turtle.d)
    turtle.pensize(1)


def dessiner_rue(nombre, avec_espace):
    """Dessine la rue avec les fonctions de projet_turtle
    et la configuration stockée dans la liste `batiments`."""

    # d = taille d'un bâtiment (même calcul que dans ton programme en console).
    # Les fonctions de projet_turtle lisent SA variable d, donc on la modifie là-bas.
    if avec_espace:
        projet_turtle.d = 500 // (nombre * 2 - 1)
    else:
        projet_turtle.d = 500 // nombre
    d = projet_turtle.d

    if avec_espace:
        pas = 2 * d     # un bâtiment + un espace
    else:
        pas = d

    turtle.tracer(0)    # on dessine sans animation (beaucoup plus rapide)...
    turtle.end_fill()   # termine un remplissage resté en cours (le toit plat en laisse un)
    turtle.clear()      # efface l'ancien dessin

    # Le sol : sol() trace depuis la position actuelle, on se place donc d'abord à gauche.
    turtle.pencolor("black")
    turtle.pensize(1)
    projet_turtle.setup(-300, -300)
    projet_turtle.sol()

    for numero in range(nombre):
        bat = batiments[numero]
        x = -300 + pas * numero

        # Les étages, de bas en haut
        for j in range(bat["nb_etages"]):
            e = bat["etages"][j]
            y = -300 + d * j
            projet_turtle.etage(x, y, e["mur"])
            projet_turtle.fenetre(x + d // 8, y + d // 2, e["fenetre"])
            projet_turtle.fenetre(x + 5 * d // 8, y + d // 2, e["fenetre"])
            if j == 0:   # la porte n'existe qu'au rez-de-chaussée
                projet_turtle.porte(x + 3 * d // 8, y, e["porte"])

        # Le toit : celui du dernier étage
        haut = bat["etages"][bat["nb_etages"] - 1]
        y_toit = -300 + d * bat["nb_etages"]
        if haut["toit_type"] == "triangle":
            projet_turtle.toit_triangulaire(x, y_toit, haut["toit_couleur"])
        elif haut["toit_type"] == "demi-cercle":
            projet_turtle.toit_circulaire(x + d, y_toit, haut["toit_couleur"])
        else:
            toit_plat_colore(x, y_toit, haut["toit_couleur"])

    turtle.update()     # ...et on affiche tout d'un coup


# ============================================================
# 4. MUSIQUE
# ============================================================

audio_disponible = True
try:
    pygame.mixer.init()
except pygame.error:
    audio_disponible = False

lecture = {"en_pause": False}


def chercher_musiques():
    """Parcourt le dossier `musiques` et retourne la liste des fichiers .mp3."""
    os.makedirs(DOSSIER_MUSIQUES, exist_ok=True)   # crée le dossier s'il n'existe pas
    liste = []
    for nom_fichier in os.listdir(DOSSIER_MUSIQUES):
        if nom_fichier.lower().endswith(".mp3"):
            liste.append(nom_fichier)
    liste.sort()
    return liste


def actualiser_musiques():
    liste = chercher_musiques()
    liste_deroulante["values"] = liste
    if len(liste) > 0:
        if var_musique.get() not in liste:
            var_musique.set(liste[0])
    else:
        var_musique.set("")
        var_info_musique.set("Aucun fichier .mp3 trouvé dans le dossier « musiques »")


def lire_musique():
    if not audio_disponible:
        return
    nom = var_musique.get()
    if nom == "":
        return
    if lecture["en_pause"]:
        pygame.mixer.music.unpause()
        lecture["en_pause"] = False
    else:
        try:
            pygame.mixer.music.load(os.path.join(DOSSIER_MUSIQUES, nom))
            pygame.mixer.music.set_volume(var_volume.get() / 100)
            pygame.mixer.music.play(loops = -1)
        except pygame.error:
            var_info_musique.set("Impossible de lire ce fichier")
            return
    var_info_musique.set("Lecture : " + nom)


def pause_musique():
    if not audio_disponible:
        return
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        lecture["en_pause"] = True
        var_info_musique.set("Pause")


def arreter_musique():
    if not audio_disponible:
        return
    pygame.mixer.music.stop()
    lecture["en_pause"] = False
    var_info_musique.set("Arrêté")


def musique_choisie(event):
    arreter_musique()   # on change de morceau : on arrête l'ancien


def changer_volume(valeur):
    if audio_disponible:
        pygame.mixer.music.set_volume(int(float(valeur)) / 100)


# ============================================================
# 5. FONCTIONS DE L'INTERFACE (appelées par les boutons)
# ============================================================
# Ces fonctions utilisent des widgets créés plus bas dans le fichier :
# ce n'est pas un problème, car elles ne s'exécutent qu'après leur création.

def montrer(cadre):
    """Affiche un seul cadre à la fois dans la zone de configuration."""
    for c in (message_accueil, cadre_batiment, cadre_musique):
        c.pack_forget()
    cadre.pack(fill="both", expand=True)


def config_etage():
    """Le dictionnaire de l'étage actuellement affiché."""
    return batiments[selection["batiment"]]["etages"][selection["etage"]]


def maj_boutons_batiments(valeur=None):
    """Affiche Bat 1 ... Bat N selon le curseur (valeur est envoyée par le curseur, on l'ignore)."""
    nombre = var_nb_bat.get()
    for bouton in boutons_bat:
        bouton.pack_forget()
    for i in range(nombre):
        boutons_bat[i].pack(side="left", padx=2)
    # Si le bâtiment affiché n'existe plus, on revient à l'accueil
    if selection["batiment"] is not None and selection["batiment"] >= nombre:
        selection["batiment"] = None
        selection["etage"] = None
        montrer(message_accueil)


def afficher_batiment(i):
    selection["batiment"] = i
    selection["etage"] = None
    titre_batiment.config(text=f"Bâtiment {i + 1}")
    var_nb_etages.set(batiments[i]["nb_etages"])   # on affiche la config de CE bâtiment
    maj_boutons_etages()
    cadre_etage.pack_forget()
    montrer(cadre_batiment)


def maj_boutons_etages():
    nombre = batiments[selection["batiment"]]["nb_etages"]
    for bouton in boutons_etage:
        bouton.pack_forget()
    for i in range(nombre):
        boutons_etage[i].pack(side="left", padx=2)


def changer_nb_etages():
    bat = batiments[selection["batiment"]]
    bat["nb_etages"] = var_nb_etages.get()         # stocké dans CE bâtiment seulement
    maj_boutons_etages()
    if selection["etage"] is not None and selection["etage"] >= bat["nb_etages"]:
        selection["etage"] = None
        cadre_etage.pack_forget()


def afficher_etage(i):
    selection["etage"] = i
    titre_etage.config(text=f"Bâtiment {selection['batiment'] + 1} - Étage {i + 1}")
    var_toit_type.set(config_etage()["toit_type"])
    afficher_apercus()
    cadre_etage.pack(fill="both", expand=True, pady=5)


def afficher_apercus():
    """Colore les petits carrés avec les couleurs de l'étage affiché."""
    config = config_etage()
    for cle in apercus:
        apercus[cle].config(bg=rgb_vers_hex(config[cle]))


def choisir_toit():
    config_etage()["toit_type"] = var_toit_type.get()


def clic_cercle(event):
    """Clic (ou glissement) sur le cercle chromatique : angle = teinte."""
    dx = event.x - CENTRE
    dy = CENTRE - event.y          # l'axe y de l'écran descend, celui des maths monte
    if dx * dx + dy * dy > RAYON * RAYON:
        return                     # clic en dehors du cercle
    teinte = math.degrees(math.atan2(dy, dx)) % 360
    couleur = hsv_vers_rgb(teinte, var_saturation.get(), var_luminosite.get())
    config_etage()[var_partie.get()] = couleur    # le tuple RGB est stocké dans l'étage
    afficher_apercus()


def dessiner_cercle():
    """Dessine le cercle chromatique : 360 petites parts de 1 degré, une couleur chacune."""
    for angle in range(360):
        couleur = rgb_vers_hex(hsv_vers_rgb(angle, 100, 100))
        canvas_cercle.create_arc(CENTRE - RAYON, CENTRE - RAYON,
                                 CENTRE + RAYON, CENTRE + RAYON,
                                 start=angle, extent=2, fill=couleur, outline=couleur)


def lancer_generation():
    fenetre_turtle.deiconify()
    fenetre_turtle.lift()
    dessiner_rue(var_nb_bat.get(), var_espace.get())


def quitter():
    if audio_disponible:
        pygame.mixer.quit()
    turtle.bye()        # ferme la fenêtre Turtle (sinon le programme ne s'arrête pas)
    fenetre.destroy()


# ============================================================
# 6. CONSTRUCTION DE LA FENÊTRE
# ============================================================

fenetre = tk.Tk()
fenetre.title("Générateur de bâtiments")
fenetre.geometry("800x600")
fenetre.protocol("WM_DELETE_WINDOW", quitter)

# master=fenetre est obligatoire ici : Turtle a déjà créé sa propre fenêtre Tk,
# il faut préciser à quelle fenêtre appartiennent nos variables.
var_nb_bat = tk.IntVar(master=fenetre, value=3)
var_nb_etages = tk.IntVar(master=fenetre, value=1)
var_espace = tk.BooleanVar(master=fenetre, value=True)
var_partie = tk.StringVar(master=fenetre, value="mur")
var_toit_type = tk.StringVar(master=fenetre, value="triangle")
var_saturation = tk.IntVar(master=fenetre, value=100)
var_luminosite = tk.IntVar(master=fenetre, value=100)
var_musique = tk.StringVar(master=fenetre)
var_volume = tk.IntVar(master=fenetre, value=50)
var_info_musique = tk.StringVar(master=fenetre)

# ---------- Zone du haut : curseur + boutons ----------
cadre_haut = ttk.Frame(fenetre)
cadre_haut.pack(fill="x", padx=10, pady=(8, 0))
ttk.Label(cadre_haut, text="Nombre de bâtiments :").pack(side="left")
tk.Scale(cadre_haut, from_=1, to=NB_BAT_MAX, orient="horizontal", length=250,
         variable=var_nb_bat, command=maj_boutons_batiments).pack(side="left", padx=8)

cadre_boutons = ttk.Frame(fenetre)
cadre_boutons.pack(fill="x", padx=10, pady=5)

cadre_bat = ttk.Frame(cadre_boutons)
cadre_bat.pack(side="left")
boutons_bat = []
for i in range(NB_BAT_MAX):
    # i=i : sans cela, tous les boutons utiliseraient la dernière valeur de i
    bouton = ttk.Button(cadre_bat, text=f"Bat {i + 1}", width=6,
                        command=lambda i=i: afficher_batiment(i))
    boutons_bat.append(bouton)

ttk.Button(cadre_boutons, text="Musique",
           command=lambda: montrer(cadre_musique)).pack(side="right")

ttk.Separator(fenetre, orient="horizontal").pack(fill="x", pady=5)

# ---------- Zone du bas : espacement + génération ----------
# (packée avant la zone de configuration pour rester toujours visible)
cadre_bas = ttk.Frame(fenetre)
cadre_bas.pack(side="bottom", fill="x", padx=10, pady=8)
ttk.Checkbutton(cadre_bas, text="Espacer les bâtiments", variable=var_espace).pack(side="left")
ttk.Button(cadre_bas, text="Générer la rue", command=lancer_generation).pack(side="right")

# ---------- Zone de configuration ----------
zone_config = ttk.Frame(fenetre)
zone_config.pack(fill="both", expand=True, padx=10)

message_accueil = ttk.Label(zone_config, text="Clique sur un bâtiment (Bat 1, Bat 2...) ou sur Musique.")
cadre_batiment = ttk.Frame(zone_config)
cadre_musique = ttk.Frame(zone_config)
message_accueil.pack(pady=30)

# ---------- Configuration d'un bâtiment ----------
titre_batiment = ttk.Label(cadre_batiment, font=("Arial", 13, "bold"))
titre_batiment.pack(anchor="w")

ligne_nb = ttk.Frame(cadre_batiment)
ligne_nb.pack(anchor="w", pady=3)
ttk.Label(ligne_nb, text="Nombre d'étages :").pack(side="left")
for n in range(1, NB_ETAGES_MAX + 1):
    ttk.Radiobutton(ligne_nb, text=str(n), value=n, variable=var_nb_etages,
                    command=changer_nb_etages).pack(side="left", padx=5)

cadre_boutons_etages = ttk.Frame(cadre_batiment)
cadre_boutons_etages.pack(anchor="w", pady=3)
boutons_etage = []
for i in range(NB_ETAGES_MAX):
    bouton = ttk.Button(cadre_boutons_etages, text=f"Etage {i + 1}",
                        command=lambda i=i: afficher_etage(i))
    boutons_etage.append(bouton)

# ---------- Configuration d'un étage ----------
cadre_etage = ttk.Frame(cadre_batiment)   # affiché quand on clique sur "Etage X"
titre_etage = ttk.Label(cadre_etage, font=("Arial", 11, "bold"))
titre_etage.pack(anchor="w")

cadre_reglages = ttk.Frame(cadre_etage)
cadre_reglages.pack(fill="both", expand=True)

# Colonne de gauche : quelle partie colorer + type de toit
cadre_gauche = ttk.Frame(cadre_reglages)
cadre_gauche.pack(side="left", anchor="n", padx=(0, 30))

ttk.Label(cadre_gauche, text="Colorer :").grid(row=0, column=0, columnspan=2, sticky="w")
PARTIES = [("mur", "Murs"), ("porte", "Porte"), ("fenetre", "Fenêtres"), ("toit_couleur", "Toit")]
apercus = {}    # clé -> petit carré qui montre la couleur actuelle
for ligne, (cle, nom) in enumerate(PARTIES, start=1):
    ttk.Radiobutton(cadre_gauche, text=nom, value=cle, variable=var_partie).grid(row=ligne, column=0, sticky="w")
    carre = tk.Label(cadre_gauche, width=4, relief="solid", bd=1)
    carre.grid(row=ligne, column=1, padx=8, pady=2)
    apercus[cle] = carre

ttk.Label(cadre_gauche, text="Type de toit :").grid(row=6, column=0, columnspan=2, sticky="w", pady=(10, 0))
ligne_toit = 7
for nom_forme in projet_turtle.forme:     # la liste ["triangle", "demi-cercle", "plat"] vient de projet_turtle
    ttk.Radiobutton(cadre_gauche, text=nom_forme, value=nom_forme, variable=var_toit_type,
                    command=choisir_toit).grid(row=ligne_toit, column=0, columnspan=2, sticky="w")
    ligne_toit += 1
ttk.Label(cadre_gauche, text="(seul le toit du dernier étage est dessiné)",
          foreground="gray").grid(row=ligne_toit, column=0, columnspan=2, sticky="w", pady=(4, 0))

# Colonne de droite : cercle chromatique + réglages
cadre_droite = ttk.Frame(cadre_reglages)
cadre_droite.pack(side="left", anchor="n")

CENTRE = 80
RAYON = 75
canvas_cercle = tk.Canvas(cadre_droite, width=2 * CENTRE, height=2 * CENTRE, highlightthickness=0)
canvas_cercle.pack()
dessiner_cercle()
canvas_cercle.bind("<Button-1>", clic_cercle)
canvas_cercle.bind("<B1-Motion>", clic_cercle)    # fonctionne aussi en glissant

tk.Scale(cadre_droite, from_=0, to=100, orient="horizontal", label="Saturation",
         variable=var_saturation, length=2 * CENTRE).pack()
tk.Scale(cadre_droite, from_=0, to=100, orient="horizontal", label="Luminosité",
         variable=var_luminosite, length=2 * CENTRE).pack()
ttk.Label(cadre_droite, text="Règle puis clique sur le cercle", foreground="gray").pack()

# ---------- Section musique ----------
ttk.Label(cadre_musique, text="Musique", font=("Arial", 13, "bold")).pack(anchor="w")

ligne_choix = ttk.Frame(cadre_musique)
ligne_choix.pack(anchor="w", pady=8)
liste_deroulante = ttk.Combobox(ligne_choix, textvariable=var_musique, state="readonly", width=45)
liste_deroulante.pack(side="left")
liste_deroulante.bind("<<ComboboxSelected>>", musique_choisie)
ttk.Button(ligne_choix, text="Actualiser", command=actualiser_musiques).pack(side="left", padx=8)

tk.Scale(cadre_musique, from_=0, to=100, orient="horizontal", label="Volume", length=250,
         variable=var_volume, command=changer_volume).pack(anchor="w")

ligne_boutons = ttk.Frame(cadre_musique)
ligne_boutons.pack(anchor="w", pady=8)
ttk.Button(ligne_boutons, text="Lecture", command=lire_musique).pack(side="left", padx=2)
ttk.Button(ligne_boutons, text="Pause", command=pause_musique).pack(side="left", padx=2)
ttk.Button(ligne_boutons, text="Stop", command=arreter_musique).pack(side="left", padx=2)

ttk.Label(cadre_musique, textvariable=var_info_musique).pack(anchor="w")
if not audio_disponible:
    var_info_musique.set("Audio indisponible (aucune carte son détectée par pygame)")

# ============================================================
# 7. DÉMARRAGE
# ============================================================
maj_boutons_batiments()
actualiser_musiques()
changer_volume(var_volume.get())
fenetre.mainloop()
