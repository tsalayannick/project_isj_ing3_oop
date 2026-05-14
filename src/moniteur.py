class MoniteurReseau:
    def __init__(self):
        
        self.paquets_transmis = 0
        self.paquets_perdus = 0
        self.historique = []
  
    def paquet_transmis(self):
        self.paquets_transmis += 1
  
    def paquet_perdu(self):
        self.paquets_perdus += 1

moniteur = MoniteurReseau()

moniteur.paquet_transmis()
moniteur.paquet_transmis()
moniteur.paquet_perdu()

print(moniteur.paquets_transmis)
print(moniteur.paquets_perdus)