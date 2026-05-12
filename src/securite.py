from datetime import datetime

class equipement:
    def __init__(self, nom, ip_adresse):
        self.nom = nom
        self.ip_adresse = ip_adresse
        
    def afficher_info(self):
        print(f"equipement: {self.nom}, IP Adresse: {self.ip_adresse}")

    def __str__(self):
        return f"{self.nom} ({self.ip_adresse})"
    
    def __repr__(self):
        return f"equipement(nom='{self.nom!r}', ip_adresse='{self.ip_adresse!r}')"
    
