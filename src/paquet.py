
# paquet.py
# Ce fichier représente un paquet réseau.
# Un paquet c'est comme une lettre qu'on envoie
# d'un ordinateur à un autre.

from datetime import datetime
from protocole import Protocole

class Paquet:
    """
    Un paquet réseau, c'est comme une enveloppe
    qu'on envoie sur le réseau.
    Elle contient :
    - l'adresse de celui qui envoie (source)
    - l'adresse de celui qui reçoit (destination)
    - le protocole utilisé (TCP, UDP ou ICMP)
    - la taille en octets
    - la priorité (1 = basse, 5 = haute)
    """
    # Ce compteur augmente à chaque nouveau paquet
    # pour donner un numéro unique à chaque paquet
    nombre_total_paquets = 0

    def __init__(self, adresse_source, adresse_destination,
                 protocole, taille_en_octets, niveau_priorite):
        """
        On crée un nouveau paquet.
        Si les infos sont mauvaises, on arrête avec une erreur.
        """

        # Vérification du protocole
        if not Protocole.est_valide(protocole):
            print("ERREUR : Protocole invalide !")
            print("Choisir parmi : TCP, UDP ou ICMP")
            raise ValueError("Protocole invalide")

        # Vérification de la taille
        if taille_en_octets <= 0:
            print("ERREUR : La taille doit être supérieure à 0 !")
            raise ValueError("Taille invalide")

        # Vérification de la priorité
        if niveau_priorite < 1 or niveau_priorite > 5:
            print("ERREUR : La priorité doit être entre 1 et 5 !")
            raise ValueError("Priorité invalide")

        #On incrémente le compteur global
        Paquet.nombre_total_paquets = Paquet.nombre_total_paquets + 1

        #On enregistre toutes les infos du paquet
        self.numero          = Paquet.nombre_total_paquets
        self.adresse_source  = adresse_source
        self.adresse_dest    = adresse_destination
        self.protocole       = protocole.upper()
        self.taille          = taille_en_octets
        self.priorite        = niveau_priorite
        self.heure_creation  = datetime.now()

    def afficher(self):
        """Affiche les informations du paquet dans la console."""
        print(f"Paquet n°{self.numero}")
        print(f" De  : {self.adresse_source}")
        print(f" Ver   : {self.adresse_dest}")
        print(f" Protocole: {self.protocole}")
        print(f"  Taille  : {self.taille} octets")
        print(f" Priorité : {self.priorite}/5")
        print(f"Créé à   : {self.heure_creation.strftime('%H:%M:%S')}")

    def __str__(self):
        """Affichage court du paquet (utilisé par print())."""
        return (f"[Paquet #{self.numero}] "
                f"{self.adresse_source} -> {self.adresse_dest} "
                f"| {self.protocole} | {self.taille} octets "
                f"| Priorité {self.priorite}")
