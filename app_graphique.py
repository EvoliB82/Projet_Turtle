import tkinter as tk
from tkinter import ttk

fenetre = tk.Tk()
fenetre.title("Générateur de bâtiments")
fenetre.geometry("800x600")

d = 50


# =========================
# NOMBRE DE BÂTIMENTS
# =========================

nb_bat = tk.IntVar(value=1)

slider_bat = tk.Scale(
    fenetre,
    from_=1,
    to=10,
    orient="horizontal",
    variable=nb_bat,
    command=lambda valeur: afficher_batiments()
)
slider_bat.place(x=15, y=20)

titre_nb_bat = tk.Label(fenetre, text="Nombre de bâtiments")
titre_nb_bat.place(x=15, y=5)


ligne = tk.Frame(fenetre, height=2, bg="black")
ligne.place(x=0, y=75, relwidth=1)


# =========================
# ZONE DE CONFIGURATION
# =========================

zone_configuration = tk.Frame(fenetre)
zone_configuration.place(x=15, y=90)


# =========================
# MUSIQUE
# =========================

musiques = ["Musique 1", "Musique 2", "Musique 3"]

volume = tk.IntVar(value=50)


def lecture():
    print("Lecture")


def pause():
    print("Pause")


def stop():
    print("Stop")


def configuration_musique():
    for widget in zone_configuration.winfo_children():
        widget.destroy()

    titre = tk.Label(
        zone_configuration,
        text="Configuration de la musique"
    )
    titre.pack()

    liste_musiques = ttk.Combobox(
        zone_configuration,
        values=musiques,
        state="readonly"
    )
    liste_musiques.pack()
    liste_musiques.current(0)

    slider_volume = tk.Scale(
        zone_configuration,
        from_=0,
        to=100,
        orient="horizontal",
        variable=volume
    )
    slider_volume.pack()

    bouton_lecture = tk.Button(
        zone_configuration,
        text="▶ Lecture",
        command=lecture
    )
    bouton_lecture.pack()

    bouton_pause = tk.Button(
        zone_configuration,
        text="⏸ Pause",
        command=pause
    )
    bouton_pause.pack()

    bouton_stop = tk.Button(
        zone_configuration,
        text="⏹ Stop",
        command=stop
    )
    bouton_stop.pack()


musique = tk.Button(
    fenetre,
    text="Musique",
    command=configuration_musique
)
musique.place(x=700, y=20)


# =========================
# ÉTAGES
# =========================

nb_etages = []

for i in range(10):
    nb_etages.append(tk.IntVar(value=1))

# Nombre d'étages de chaque bâtiment

boutons_etage = []

# Zone dans laquelle on affichera la configuration
# de l'étage sélectionné


def selection_etage(numero):
    global zone_etage
    
    for widget in zone_etage.winfo_children():
        widget.destroy()

    titre = tk.Label(
        zone_etage,
        text=f"Configuration de l'étage {numero}"
    )
    titre.pack()


def afficher_etages():
    nombre = nb_etages[batiment_selectionne - 1].get()

    for i, bouton in enumerate(boutons_etage):
        if i < nombre:
            bouton.place(
                x=130 + d * (i + 1),
                y=150
            )
        else:
            bouton.place_forget()


# =========================
# BÂTIMENTS
# =========================

boutons_batiments = []

# Bâtiment actuellement sélectionné
batiment_selectionne = None

def sauvegarder_etages():
    afficher_etages()

def selection_batiment(numero):
    global batiment_selectionne

    batiment_selectionne = numero

    for widget in zone_configuration.winfo_children():
        widget.destroy()

    titre = tk.Label(
        zone_configuration,
        text=f"Configuration de Bat{numero}"
    )
    titre.pack()
    
    zone_etage = tk.Frame(zone_configuration)


    # On récupère le nombre d'étages déjà sauvegardé

    slider_etages = tk.Scale(
        zone_configuration,
        from_=1,
        to=3,
        orient="horizontal",
        variable=nb_etages[numero - 1],
        command=lambda valeur: sauvegarder_etages()
    )
    slider_etages.pack()

    # Création des boutons d'étage
    boutons_etage.clear()

    for i in range(3):
        bouton = tk.Button(
            fenetre,
            text=f"Etage {i + 1}",
            command=lambda numero=i + 1: selection_etage(numero)
        )
        boutons_etage.append(bouton)

    afficher_etages()

    zone_etage.place(x=0, y=100)



        


for i in range(10):
    bouton = tk.Button(
        fenetre,
        text=f"Bat {i + 1}",
        command=lambda numero=i + 1: selection_batiment(numero)
    )
    bouton.place(
        x=130 + d * (i + 1),
        y=30
    )
    boutons_batiments.append(bouton)


def afficher_batiments():
    nombre = nb_bat.get()

    for i, bouton in enumerate(boutons_batiments):
        if i < nombre:
            bouton.place(
                x=130 + d * (i + 1),
                y=30
            )
        else:
            bouton.place_forget()


# =========================
# INITIALISATION
# =========================

afficher_batiments()

fenetre.mainloop()