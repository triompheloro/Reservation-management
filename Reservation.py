import sqlite3
import tkinter as tk
from tkinter import simpledialog, messagebox

class Voyageur:
    def __init__(self, nom, prenom, place):
        self.nom = nom
        self.prenom = prenom
        self.place = place

    def modifier_place(self, nouvelle_place):
        self.place = nouvelle_place

class Voiture:
    def __init__(self, nombre_places):
        self.nombre_places = nombre_places

# Fonction pour mettre à jour la liste des places disponibles
def mettre_a_jour_places_disponibles():
    places_occupees = data.execute("SELECT place FROM Voyageurs")
    places_occupees = [place[0] for place in places_occupees]
    places_disponibles = [i for i in range(1, voiture.nombre_places + 1) if i not in places_occupees]
    return places_disponibles

# Fonction pour gérer le clic sur le bouton de réservation
def reserver_place():
    places_disponibles = mettre_a_jour_places_disponibles()

    if not places_disponibles:
        messagebox.showinfo("Voiture Pleine", "La voiture est pleine. Aucune réservation supplémentaire autorisée.")
        return

    nom = entry_nom.get()
    prenom = entry_prenom.get()

    # Check if the selected place is not already reserved
    selected_place = choisir_place(places_disponibles)
    place_occupant = data.execute("SELECT * FROM Voyageurs WHERE place=?", (selected_place,)).fetchone()
    if place_occupant:
        messagebox.showinfo("Place Occupée", f"La place {selected_place} est déjà réservée. Veuillez choisir une autre place.")
        return

    # Vérifier si le nom saisi est déjà dans la base de données
    voyageur_existant = data.execute("SELECT * FROM Voyageurs WHERE nom=? AND prenom=?", (nom, prenom)).fetchone()
    if voyageur_existant:
        messagebox.showinfo("Voyageur Existante", f"{nom} {prenom} a déjà une réservation.")
        return

    voyageur = Voyageur(nom, prenom, selected_place)

    data.execute("INSERT INTO Voyageurs(nom, prenom, place) VALUES (?, ?, ?)",
                 (voyageur.nom, voyageur.prenom, voyageur.place))
    data.commit()

    messagebox.showinfo("Réservation Réussie", f"Réservation pour {nom} {prenom} à la place {selected_place} réussie.")
    mettre_a_jour_interface()

# Fonction pour gérer le clic sur le bouton de changement de réservation
def changer_reservation():
    places_disponibles = mettre_a_jour_places_disponibles()

    if not places_disponibles:
        messagebox.showinfo("Voiture Pleine", "La voiture est pleine. Aucune réservation supplémentaire autorisée.")
        return

    nom = entry_nom.get()
    prenom = entry_prenom.get()

    voyageur = data.execute("SELECT * FROM Voyageurs WHERE nom=? AND prenom=?", (nom, prenom)).fetchone()

    if not voyageur:
        messagebox.showinfo("Voyageur Non Trouvé", f"Aucune réservation trouvée pour {nom} {prenom}.")
        return

    place_choisie = choisir_place(places_disponibles)

    data.execute("UPDATE Voyageurs SET place=? WHERE nom=? AND prenom=?", (place_choisie, nom, prenom))
    data.commit()

    messagebox.showinfo("Changer Réservation", f"Réservation pour {nom} {prenom} changée à la place {place_choisie}.")
    mettre_a_jour_interface()

# Fonction pour annuler une réservation
def annuler_reservation():
    nom = entry_nom.get()
    prenom = entry_prenom.get()

    voyageur = data.execute("SELECT * FROM Voyageurs WHERE nom=? AND prenom=?", (nom, prenom)).fetchone()

    if not voyageur:
        messagebox.showinfo("Voyageur Non Trouvé", f"Aucune réservation trouvée pour {nom} {prenom}.")
        return

    data.execute("DELETE FROM Voyageurs WHERE nom=? AND prenom=?", (nom, prenom))
    data.commit()

    messagebox.showinfo("Annuler Réservation", f"Réservation pour {nom} {prenom} annulée avec succès.")
    mettre_a_jour_interface()

# Fonction pour choisir une place parmi les places disponibles
def choisir_place(places_disponibles):
    return simpledialog.askinteger("Choisir une Place", f"Places Disponibles: {places_disponibles}", minvalue=1, maxvalue=voiture.nombre_places)

# Fonction pour mettre à jour les informations affichées des voyageurs
def mettre_a_jour_interface():
    info_text.delete(1.0, tk.END)
    informations_des_voyageurs = data.execute("SELECT * FROM Voyageurs ORDER BY nom, prenom")
    for voyageur in informations_des_voyageurs:
        info_text.insert(tk.END, f"{voyageur[0]} {voyageur[1]} - Place {voyageur[2]}\n")
    info_text.insert(tk.END, "______________________________\n")

# Créer une connexion à la base de données SQLite
with sqlite3.connect("ListeDesPassager.db") as data:
    data.execute("CREATE TABLE IF NOT EXISTS Voyageurs(nom TEXT, prenom TEXT, place INTEGER)")

    # Créer une voiture avec 5 places
    voiture = Voiture(16)

    # Créer une fenêtre Tkinter
    fenetre = tk.Tk()
    fenetre.title("Système de Réservation de Voyage")

    # Créer des éléments de l'interface graphique (GUI)
    label_nom = tk.Label(fenetre, text="Nom:")
    label_prenom = tk.Label(fenetre, text="Prénom:")
    entry_nom = tk.Entry(fenetre)
    entry_prenom = tk.Entry(fenetre)
    bouton_reserver = tk.Button(fenetre, text="Réserver", command=reserver_place)
    bouton_changer = tk.Button(fenetre, text="Changer Réservation", command=changer_reservation)
    bouton_annuler = tk.Button(fenetre, text="Annuler Réservation", command=annuler_reservation)
    info_text = tk.Text(fenetre, height=10, width=50)
    info_text.insert(tk.END, "Informations des Voyageurs:\n")

    # Mise en page en grille
    label_nom.grid(row=0, column=0)
    entry_nom.grid(row=0, column=1)
    label_prenom.grid(row=1, column=0)
    entry_prenom.grid(row=1, column=1)
    bouton_reserver.grid(row=2, column=0, columnspan=2, pady=10)
    bouton_changer.grid(row=3, column=0, columnspan=2, pady=10)
    bouton_annuler.grid(row=4, column=0, columnspan=2, pady=10)
    info_text.grid(row=5, column=0, columnspan=2)

    # Mettre à jour l'interface avec les informations des voyageurs existantes
    mettre_a_jour_interface()

    # Démarrer la boucle des événements Tkinter
    fenetre.mainloop()
