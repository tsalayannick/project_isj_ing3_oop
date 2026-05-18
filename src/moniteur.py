class MoniteurReseau:

    def __init__(self):

        self.paquets_transmis = 0
        self.paquets_perdus = 0
        self.historique = []
        self.stats_liens = {}
        self.equipements_actifs = []
        self.equipements_inactifs = []

    def paquet_transmis(self):

        self.paquets_transmis += 1

    def paquet_perdu(self):

        self.paquets_perdus += 1

    def ajouter_paquet(self, paquet):

        self.historique.append(paquet)

        if len(self.historique) > 10:

            self.historique.pop(0)

    def enregistrer_lien(self, nom_lien, octets):

        if nom_lien not in self.stats_liens:
            self.stats_liens[nom_lien] = 0
        self.stats_liens[nom_lien] += octets

    def mettre_a_jour_equipements(self, liste_equipements):

        self.equipements_actifs = [e for e in liste_equipements if e.statut == "actif"]
        self.equipements_inactifs = [e for e in liste_equipements if e.statut == "inactif"]

    def afficher_statistiques(self):

        print(" STATISTIQUES RÉSEAU ")
        print("Paquets transmis :", self.paquets_transmis)
        print("Paquets perdus :", self.paquets_perdus)
        print("Nombre de paquets dans l'historique :", len(self.historique))
        print("Équipements actifs :", len(self.equipements_actifs))
        print("Équipements inactifs :", len(self.equipements_inactifs))

moniteur = MoniteurReseau()
moniteur.paquet_transmis()
moniteur.paquet_transmis()
moniteur.paquet_transmis()
moniteur.paquet_perdu()
moniteur.ajouter_paquet("paquet1")
moniteur.ajouter_paquet("paquet2")
moniteur.afficher_statistiques()