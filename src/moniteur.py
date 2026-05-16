class MoniteurReseau:

    def __init__(self):

        self.paquets_transmis = 0
        self.paquets_perdus = 0
        self.historique = []

    def paquet_transmis(self):

        self.paquets_transmis += 1

    def paquet_perdu(self):

        self.paquets_perdus += 1

    def ajouter_paquet(self, paquet):

        self.historique.append(paquet)

        if len(self.historique) > 10:

            self.historique.pop(0)

    def afficher_statistiques(self):

        print(" STATISTIQUES RÉSEAU ")
        print("Paquets transmis :", self.paquets_transmis)
        print("Paquets perdus :", self.paquets_perdus)
        print("Nombre de paquets dans l'historique :", len(self.historique))

moniteur = MoniteurReseau()

moniteur.paquet_transmis()
moniteur.paquet_transmis()
moniteur.paquet_perdu()
moniteur.afficher_statistiques()