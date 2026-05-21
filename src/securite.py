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
    

class Authentifiable:
    def __init__(self, login, mot_de_passe):
        self.__login = login
        self.__mot_de_passe = mot_de_passe
    
    def authentifier(self, login, mot_de_passe):
        return self.__login == login and self.__mot_de_passe == mot_de_passe
    

class Journalisable:
    def __init__(self):
        self.journal = []

    def logger(self, message):
        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entree = f"[{horodatage}] {message}"
        self.journal.append(entree)

    def afficher_journal(self):
        print("\n===Journal du firewall===")
        if not self.journal:
            print("(journal vide)")
        else:
            for entree in self.journal:
                print(f" {entree}")
        print("====================\n")
    

class RegleFiltrage:

    ACTIONS_VALIDES = ("BLOQUER", "AUTORISER")
    TYPES_VALIDES = ("ip", "protocole", "port", "reseau")

    def __init__(self, type_regle, valeur, action, description=""):
        if type_regle not in self.TYPES_VALIDES:
            raise ValueError(
                f"Type de regle invalide : '{type_regle}'."
                f"Types acceptes : {self.TYPES_VALIDES}"
            )
        
        action_upper = action.upper()
        if action_upper not in self.ACTIONS_VALIDES:
            raise ValueError(
                f"Action invalide : '{action}'."
                f"Actions acceptees : {self.ACTIONS_VALIDES}"
            )
        
        self.type_regle = type_regle
        self.valeur = str(valeur)
        self.action = action_upper
        self.description = description

    def correspond(self, paquet):
        if self.type_regle == "ip":
            return paquet.source == self.valeur
        
        elif self.type_regle == "protocole":
            return paquet.protocole.upper() == self.valeur.upper()
        
        elif self.type_regle == "port":
            return str(paquet.port_destination) == self.valeur
        
        elif self.type_regle == "reseau":
            return paquet.source.startswith(self.valeur)
        

        return False
    
    def __str__(self):
        desc = f" -- {self.description}" if self.description else ""
        return(
            f"[{self.action}] {self.type_regle.upper()} = {self.valeur} {desc}"
        )
    
    def __repr__(self):
        return(
            f"RegleFiltrage(type_regle={self.type_regle}),"
            f"valeur={self.valeur!r}, action={self.action!r}"
        )
    
    class PaquetSimple:
        def __init__(self, source, destination, protocole, port_destination, taille=0, priorite=0):

            self.source = source
            self.destination = destination
            self.protocole = protocole
            self.port_destination = port_destination
            self.taille = taille
            self.priorite = priorite

        def __str__(self):
            return (
                f"Paquet({self.source} -> {self.destination} | " f"{self.protocole}:{self.port_destination})"
            )
        
        def __repr__(self):
            return (
                f"PaquetSimple(source={self.source!r}, destination = {self.destination!r},"
                f"protocole={self.protocole!r}, port_destination={self.port_destination!r})"
            )

    class Firewall(equipement, Authentifiable, Journalisable):
        def __init__(self, nom, adresse_ip, login, mot_de_passe):

            equipement.__init__(self, nom, adresse_ip)
            Authentifiable.__init__(self, login, mot_de_passe)
            Journalisable.__init__(self)

            
            self.regles = []
            self.nb_paquets_bloques = 0
            self.nb_paquets_autorises = 0
            self._config_verrouillee = True


            self.logger(f"Firewall '{self.nom}' initialise a l'adresse {self.adresse_ip}")

        def deverouiller(self, login, mot_de_passe):
            if self.authentifier(login, mot_de_passe):
                self._config_verrouillee = False
                self.logger(f"Access a la configuration deverrouille (login : {login}).")
                print(f"[AUTH] acces accorde pour '{login}'.")
                return True
            else:
                self.logger(f"Tentative d'access echouee (login : '{login}').")
                print(f"[AUTH] Access refuse pour '{login}'.")
                return False
            
        def verrouiller(self):
            self._config_verrouillee = True
            self.logger("configuration verrouillee.")
            print("[AUTH] Configuration verrouillee.")

        def _verifier_access(self):
            if self._config_verrouillee:
                raise PermissionError(
                    "Configuration verrouillee."
                    "Appelez deverouiller (login, mot_de_passe) d'abord."
                )
        
        def ajouter_regle(self, type_regle, valeur, action, description=""):
            self._verifier_access()
            regle = RegleFiltrage(type_regle, valeur, action, description)
            self.regles.append(regle)

            self.logger(f"Regle ajoutee : {regle}")
            print(f"[REGLE] Ajoutee -> {regle}")

        def supprimer_regle(self, index):
            self._verifier_access()
            if index < 0 or index >= len(self.regles):
                raise IndexError(
                    f"index {index} invalide."
                    f"Le firewall a {len(self.regles)} regle(s) (indices 0 a {len(self.regles)-1})"
                )
            
            regle_supprime = self.regles.pop(index)
            self.logger(f"Regle supprime : {regle_supprime}")
            print(f"[REGLE] supprime -> {regle_supprime}")


        def afficher_regles(self):
            print("\n=== Regle de filtrage ===")
            if not self.regles:
                print(" (aucune regle definie)")
            else:
                for i, regle in enumerate(self.regles):
                    print(f" [{i}] {regle}")
            print("=================\n")

        
        def filtrer_paquet(self, paquet):
            for regle in self.regles:
                if regle.corresponf(paquet):
                    if regle.action == "BLOQUER":
                       self.nb_paquets_bloques += 1
                       message = (
                           f"BLOQUE -- {paquet} "
                           f"(regle : {regle})"
                       )

                       self.logger(message)
                       print(f"[FIREWALL] {message}")
                       return False
                    
                    else:
                        self.nb_paquets_autorises += 1
                        message = (
                            f"AUTORISE (regle explicite) -- {paquet} "
                            f"(regle : {regle})"
                        )

                        self.logger(message)
                        print(f"[FIREWALL] {message}")
                        return True
                    
            self.nb_paquets_autorises += 1
            message = f"AUTORISE (defaut) - {paquet}"
            self.logger(message)
            print(f"[FIREWALL] {message}")
            return True


        def afficher_infos(self):
            print("\n======================================")
            print(f"|| FIREWALL : {self.nom:<26} ||")
            print(f"===================================")
            print(f"|| IP    : {self.adresse_ip:<20} ||")
            verrou = "verrouillee" if self._config_verrouillee else "Deverouille"
            print(f"|| configuration : {verrou:<20}||")
            print(f"|| Regle : {len(self.regles):<20}||")
            print(f"|| Paquets OK  : {self.nb_paquets_autorises:<20}||")
            print(f"|| paquets KO  :{self.nb_paquets_bloques:<20}||")
            print(f"|| entrees log  : {len(self.journal):<20}||")
            print("=========================================\n")
        
        def __str__(self):
            return (
                f"Firewall '{self.mom}' | IP : {self.adresse_ip} |"
                f"Regles : {len(self.regles)} |"
                f"Bloques : {self.nb_paquets_bloques} |"
                f"Autorises ; {self.nb_paquets_autorises}"
            )
        
        def __repr__(self):
            return (
                f"Firewall (nom={self.nom!r}, adresse_ip={self.adresse_ip!r}, "f"nb_regles={len(self.regles)!r})"
            )
        
        




