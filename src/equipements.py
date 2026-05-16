
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

class Routeur(Equipement):
    def __init__(self, nom, adresse_ip, marque, statut=True):
        super().__init__(nom, adresse_ip, marque, statut)
        self.table_routage = {}  # exemple : {"192.168.1.0": "192.168.0.1"}

    def ajouter_route(self, destination, prochain_saut):
        self.table_routage[destination] = prochain_saut
        print(f"Route ajoutée : {destination} -> {prochain_saut}")

    def afficher(self):
        super().afficher()
        print(f"  Table de routage : {self.table_routage}")



class Switch(Equipement):
    def __init__(self, nom, adresse_ip, marque, statut=True):
        super().__init__(nom, adresse_ip, marque, statut)
        self.vlans = []  # exemple : [10, 20, 30]

    def ajouter_vlan(self, vlan_id):
        self.vlans.append(vlan_id)
        print(f"VLAN {vlan_id} ajouté au switch {self.nom}.")

    def afficher(self):
        super().afficher()
        print(f"  VLANs : {self.vlans}")



class Serveur(Equipement):
    def __init__(self, nom, adresse_ip, marque, statut=True):
        super().__init__(nom, adresse_ip, marque, statut)
        self.services = []  # exemple : ["HTTP:80", "SSH:22"]

    def ajouter_service(self, service):
        self.services.append(service)
        print(f"Service '{service}' ajouté au serveur {self.nom}.")

    def afficher(self):
        super().afficher()
        print(f"  Services : {self.services}")



class Firewall(Equipement):
    def __init__(self, nom, adresse_ip, marque, statut=True):
        super().__init__(nom, adresse_ip, marque, statut)
        self.regles = []  # sera utilisé dans le Module 3
        self.journal = [] # sera utlisé dans le Module 3
    def afficher(self):
        super().afficher()
        print(f"  Règles de filtrage : {len(self.regles)} /")
        print(f"  Journal d'actualisation du reseau après filtrage : {len(self.journal)} /")


class PointAccesWifi(Equipement):
    def __init__(self, nom, adresse_ip, marque, ssid, canal, statut=True):
        super().__init__(nom, adresse_ip, marque, statut)
        self.ssid = ssid    # nom du réseau wifi
        self.canal = canal  # canal utilisé (1 à 13)

    def afficher(self):
        super().afficher()
        print(f"  SSID : {self.ssid} | Canal : {self.canal}")



class Terminal(Equipement):
    def __init__(self, nom, adresse_ip, marque, statut=True):
        super().__init__(nom, adresse_ip, marque, statut)

    def afficher(self):
        super().afficher()
        print(f"  Type : terminal client")