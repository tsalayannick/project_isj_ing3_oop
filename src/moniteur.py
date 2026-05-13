class MoniteurReseau:
    def __init__(self):
        
        self.paquets_transmis = 0
        self.paquets_perdus = 0
        self.historique = []

moniteur = MoniteurReseau()

print(moniteur.paquets_transmis)
print(moniteur.paquets_perdus)        
print(moniteur.historique)