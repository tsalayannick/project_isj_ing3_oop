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

moniteur = MoniteurReseau()

moniteur.ajouter_paquet("paquet 1")
moniteur.ajouter_paquet("paquet 2")
moniteur.ajouter_paquet("paquet 3")

print(moniteur.historique)
