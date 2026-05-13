
def valider_ipv4(ip):
    parties = ip.split(".")
    if len(parties) != 4:
        return False
    for partie in parties:
        if not partie.isdigit():
            return False
        if not (0 <= int(partie) <= 255):
            return False
    return True


# Classe mère (abstraite) de tous les équipements
class Equipement:
    def __init__(self, nom, adresse_ip, marque, statut=True):
        if not valider_ipv4(adresse_ip):
            print(f"Erreur : adresse IP invalide -> {adresse_ip}")
            return
        self.nom = nom
        self.adresse_ip = adresse_ip
        self.marque = marque
        self.statut = statut  # True = actif, False = inactif

    def activer(self):
        self.statut = True
        print(f"{self.nom} est maintenant actif.")

    def desactiver(self):
        self.statut = False
        print(f"{self.nom} est maintenant inactif.")

    def afficher(self):
        if self.statut:
            etat = "actif"
        else:
            etat = "inactif"
        print(f"Nom: {self.nom} | IP: {self.adresse_ip} | Marque: {self.marque} | Statut: {etat}")

