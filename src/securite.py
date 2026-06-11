from datetime import datetime


UTILISATEURS = {
    "admin": "1234",
    "root": "simnet"
}


def authentifier():
    print("\n-- Authentification requise --")
    login = input("Login : ")
    mdp = input("Mot de passe : ")

    if login in UTILISATEURS and UTILISATEURS[login] == mdp:
        print("Authentification réussie.")
        return True

    print("Erreur : login ou mot de passe incorrect.")
    return False


class GestionnaireFirewall:
    """Gère les règles de filtrage, l'inspection des paquets et le journal du firewall."""

    def __init__(self, firewall):
        self.firewall = firewall

    def ajouter_regle(self, action, ip_source=None, protocole=None, port=None, plage=None):
        action = action.upper()

        if action not in ["ALLOW", "BLOCK"]:
            print("Erreur : action invalide. Utilisez ALLOW ou BLOCK.")
            return

        if protocole is not None:
            protocole = protocole.upper()

        regle = {
            "action": action,
            "ip_source": ip_source,
            "protocole": protocole,
            "port": port,
            "plage": plage
        }

        self.firewall.regles.append(regle)

        print(
            f"Règle ajoutée : {action} | "
            f"IP={ip_source} | Proto={protocole} | "
            f"Port={port} | Plage={plage}"
        )

    def supprimer_regle(self, index):
        if 0 <= index < len(self.firewall.regles):
            regle = self.firewall.regles.pop(index)
            print(f"Règle {index} supprimée : {regle}")
        else:
            print("Erreur : index invalide.")

    def afficher_regles(self):
        print(f"\n-- Règles du Firewall {self.firewall.nom} --")

        if not self.firewall.regles:
            print("  Aucune règle définie.")
            return

        for i, regle in enumerate(self.firewall.regles):
            print(
                f"  [{i}] Action={regle['action']} | "
                f"IP={regle['ip_source']} | "
                f"Proto={regle['protocole']} | "
                f"Port={regle['port']} | "
                f"Plage={regle['plage']}"
            )

    def inspecter(self, paquet, nom_equipement):
        """
        Inspecte un paquet pendant son passage sur un équipement.
        Retourne :
        - True si le paquet est autorisé
        - False si le paquet est bloqué
        """

        for regle in self.firewall.regles:
            ip_ok = (
                regle["ip_source"] is None
                or regle["ip_source"] == paquet.adresse_source
            )

            proto_ok = (
                regle["protocole"] is None
                or regle["protocole"] == paquet.protocole
            )

            plage_ok = (
                regle["plage"] is None
                or paquet.adresse_source.startswith(regle["plage"])
            )

            # La classe Paquet actuelle ne contient pas encore d'attribut port.
            # Donc on garde ce critère pour évolution future, mais il ne bloque pas.
            port_ok = True

            if ip_ok and proto_ok and port_ok and plage_ok:
                decision = regle["action"]
                raison = f"{decision} sur {nom_equipement}"

                self._journaliser(paquet, raison)

                if decision == "BLOCK":
                    return False, raison

                return True, raison

        raison = f"ALLOW par défaut sur {nom_equipement}"
        self._journaliser(paquet, raison)
        return True, raison

    def filtrer(self, paquet):
        """
        Filtre directement un paquet selon les règles du firewall.
        Cette méthode retourne ALLOW ou BLOCK.
        """

        for regle in self.firewall.regles:
            ip_ok = (
                regle["ip_source"] is None
                or regle["ip_source"] == paquet.adresse_source
            )

            proto_ok = (
                regle["protocole"] is None
                or regle["protocole"] == paquet.protocole
            )

            plage_ok = (
                regle["plage"] is None
                or paquet.adresse_source.startswith(regle["plage"])
            )

            port_ok = True

            if ip_ok and proto_ok and port_ok and plage_ok:
                decision = regle["action"]
                self._journaliser(paquet, decision)
                print(f"[FIREWALL] Paquet {decision}")
                return decision

        self._journaliser(paquet, "ALLOW par défaut")
        print("[FIREWALL] Paquet autorisé par défaut")
        return "ALLOW"

    def _journaliser(self, paquet, raison):
        heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        entree = (
            f"[{heure}] {raison} | "
            f"{paquet.adresse_source} -> {paquet.adresse_dest} | "
            f"Proto={paquet.protocole}"
        )

        self.firewall.journal.append(entree)

    def afficher_journal(self):
        print(f"\n-- Journal du Firewall {self.firewall.nom} --")

        if not self.firewall.journal:
            print("  Journal vide.")
            return

        for entree in self.firewall.journal:
            print(f"  {entree}")

    def vider_journal(self):
        self.firewall.journal.clear()
        print(f"Journal du firewall {self.firewall.nom} vidé.")