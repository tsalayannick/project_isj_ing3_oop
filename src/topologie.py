# Un lien représente la connexion entre deux équipements
class Lien:
    def __init__(self, equipement_a, equipement_b, bande_passante, latence):
        self.equipement_a = equipement_a      # premier équipement
        self.equipement_b = equipement_b      # deuxième équipement
        self.bande_passante = bande_passante  # en Mbps
        self.latence = latence                # en ms

    def afficher(self):
        print(f"Lien : {self.equipement_a.nom} <---> {self.equipement_b.nom} "
              f"| Bande passante : {self.bande_passante} Mbps "
              f"| Latence : {self.latence} ms")