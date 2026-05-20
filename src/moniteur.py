import datetime
import collections

class MoniteurReseau:

    def __init__(self):
        self.paquets_transmis = 0
        self.paquets_perdus = 0
        self.historique = collections.deque(maxlen=10)
        self.stats_equipements = {}
        self.stats_liens = {}
        self.equipements_actifs = []
        self.equipements_inactifs = []

    def paquet_transmis(self, nom_equipement):
        self.paquets_transmis += 1
        if nom_equipement not in self.stats_equipements:
            self.stats_equipements[nom_equipement] = {"transmis": 0, "perdus": 0}
        self.stats_equipements[nom_equipement]["transmis"] += 1

    def paquet_perdu(self, nom_equipement):
        self.paquets_perdus += 1
        if nom_equipement not in self.stats_equipements:
            self.stats_equipements[nom_equipement] = {"transmis": 0, "perdus": 0}
        self.stats_equipements[nom_equipement]["perdus"] += 1

    def ajouter_paquet(self, paquet):
        self.historique.append(paquet)

    def enregistrer_lien(self, nom_lien, octets):
        if nom_lien not in self.stats_liens:
            self.stats_liens[nom_lien] = 0
        self.stats_liens[nom_lien] += octets

    def mettre_a_jour_equipements(self, liste_equipements):
        self.equipements_actifs = [e for e in liste_equipements if e.statut == "actif"]
        self.equipements_inactifs = [e for e in liste_equipements if e.statut == "inactif"]

    def afficher_statistiques(self):
        print("STATISTIQUES RÉSEAU ")
        print("Paquets transmis (total) :", self.paquets_transmis)
        print("Paquets perdus (total)   :", self.paquets_perdus)
        print("Historique               :", len(self.historique), "paquet(s)")
        print("\n Stats par équipement ")
        for nom, stats in self.stats_equipements.items():
            print(f"  {nom} → transmis: {stats['transmis']}, perdus: {stats['perdus']}")
        print("\nÉquipements actifs   :", len(self.equipements_actifs))
        print("Équipements inactifs :", len(self.equipements_inactifs))