# Un lien représente la connexion entre deux équipements
class Lien:
    def __init__(self, equipement_a, equipement_b, bande_passante, latence):
        self.equipement_a = equipement_a      # premier équipement
        self.equipement_b = equipement_b      # deuxième équipement
        self.bande_passante = bande_passante  # en Mbps
        self.latence = latence                # en ms

    def afficher(self):
        print(f"Lien : {self.equipement_a.nom} -----> {self.equipement_b.nom} "
              f"| Bande passante : {self.bande_passante} Mbps "
              f"| Latence : {self.latence} ms")

# topologie.py
# Module 1 - Topologie du réseau


class Lien:
    def __init__(self, equipement_a, equipement_b, bande_passante, latence):
        self.equipement_a = equipement_a
        self.equipement_b = equipement_b
        self.bande_passante = bande_passante
        self.latence = latence

    def afficher(self):
        print(f"Lien : {self.equipement_a.nom} <---> {self.equipement_b.nom}"
              f" | Bande passante : {self.bande_passante} Mbps"
              f" | Latence : {self.latence} ms")


class Topologie:
    def __init__(self):
        self.equipements = []
        self.liens = []

    def ajouter_equipement(self, equipement):
        self.equipements.append(equipement)
        print(f"Equipement '{equipement.nom}' ajouté au réseau.")

    def supprimer_equipement(self, nom):
        for equipement in self.equipements:
            if equipement.nom == nom:
                self.equipements.remove(equipement)
                print(f"Equipement '{nom}' supprimé du réseau.")
                return
        print(f"Equipement '{nom}' introuvable.")

    def ajouter_lien(self, equipement_a, equipement_b, bande_passante, latence):
        lien = Lien(equipement_a, equipement_b, bande_passante, latence)
        self.liens.append(lien)
        print(f"Lien ajouté entre '{equipement_a.nom}' et '{equipement_b.nom}'.")


    def trouver_equipement(self, nom):
            for equipement in self.equipements:
                if equipement.nom == nom:
                    print(f"Equipement '{nom}' trouvé.")
                    return equipement
            print(f"Equipement '{nom}' introuvable.")
            return None

    def afficher(self):
        print("\n===== TOPOLOGIE DU RÉSEAU =====")

        print(f"\n-- Equipements ({len(self.equipements)}) --")
        if len(self.equipements) == 0:
            print("  Aucun équipement.")
        else:
            for equipement in self.equipements:
                equipement.afficher()

        print(f"\n-- Liens ({len(self.liens)}) --")
        if len(self.liens) == 0:
            print("  Aucun lien.")
        else:
            for lien in self.liens:
                lien.afficher()

        print("================================\n")