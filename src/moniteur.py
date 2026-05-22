import datetime
import collections

from statistiques import Statistiques

class MoniteurReseau:
    """Surveille l'activité du réseau et génère des rapports d'exploitation."""

    def __init__(self):
        self.paquets_transmis = 0
        self.paquets_perdus = 0
        self.historique = collections.deque(maxlen=10)
        self.stats_equipements = {}
        self.stats_liens = {}
        self.equipements_actifs = []
        self.equipements_inactifs = []
        self.statistiques = Statistiques()

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

    def enregistrer_liens_topologie(self, topologie):
        for lien in topologie.liens:
            nom_lien = f"{lien.equipement_a.nom}-{lien.equipement_b.nom}"
            if nom_lien not in self.stats_liens:
                self.stats_liens[nom_lien] = 0

    def mettre_a_jour_equipements(self, topologie):
        self.equipements_actifs = [e for e in topologie.equipements if e.statut == "actif"]
        self.equipements_inactifs = [e for e in topologie.equipements if e.statut == "inactif"]

    def afficher_statistiques(self):
        print("=== STATISTIQUES RÉSEAU ===")
        print("Paquets transmis (total) :", self.paquets_transmis)
        print("Paquets perdus (total)   :", self.paquets_perdus)
        print("Historique               :", len(self.historique), "paquet(s)")
        print("\n--- Stats par équipement ---")
        if self.stats_equipements:
            for nom, stats in self.stats_equipements.items():
                print(f"  {nom} → transmis: {stats['transmis']}, perdus: {stats['perdus']}")
        else:
            print("  Aucune statistique disponible.")
        print("\nÉquipements actifs   :", len(self.equipements_actifs))
        print("Équipements inactifs :", len(self.equipements_inactifs))
        print()
        self.statistiques.afficher()

    def generer_rapport(self):
        maintenant = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("rapport_simnet.txt", "w", encoding="utf-8") as fichier:

            fichier.write("=== RAPPORT SIMNET ===\n")
            fichier.write(f"Généré le : {maintenant}\n\n")

            fichier.write(self.statistiques.vers_texte())

            fichier.write("\n--- Paquets par équipement ---\n")
            if self.stats_equipements:
                for nom, stats in self.stats_equipements.items():
                    fichier.write(f"  {nom} → transmis: {stats['transmis']}, perdus: {stats['perdus']}\n")
            else:
                fichier.write("  Aucune statistique disponible.\n")

            fichier.write("\n--- Taux d'utilisation des liens ---\n")
            if self.stats_liens:
                for lien, octets in self.stats_liens.items():
                    fichier.write(f"  {lien} : {octets} octets\n")
            else:
                fichier.write("  Aucun lien enregistré.\n")

            fichier.write("\n--- Historique des 10 derniers paquets ---\n")
            if self.historique:
                for i, paquet in enumerate(self.historique, 1):
                    fichier.write(f"  {i}. {paquet}\n")
            else:
                fichier.write("  Aucun paquet dans l'historique.\n")

            fichier.write("\n--- Équipements ---\n")
            fichier.write(f"  Actifs   : {len(self.equipements_actifs)}\n")
            fichier.write(f"  Inactifs : {len(self.equipements_inactifs)}\n")

        print("Rapport généré avec succès → rapport_simnet.txt")
