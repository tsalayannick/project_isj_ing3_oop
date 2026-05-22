
from datetime import datetime


# ─── Authentification ───────────────────────────────────────────

UTILISATEURS = {
    "admin": "1234",
    "root":  "simnet"
}

def authentifier():

    print("\n-- Authentification requise --")
    login = input("Login : ")
    mdp   = input("Mot de passe : ")
    if login in UTILISATEURS and UTILISATEURS[login] == mdp:
        print("Authentification réussie.")
        return True
    print("Erreur : login ou mot de passe incorrect.")
    return False


# ─── Gestionnaire du Firewall ───────────────────────────────────

class GestionnaireFirewall:


    def __init__(self, firewall):
        self.firewall = firewall  # objet Firewall du Module 1

    # Ajouter une règle
    def ajouter_regle(self, action, ip_source=None,
                      protocole=None, port=None, plage=None):
        regle = {
            "action":    action,
            "ip_source": ip_source,
            "protocole": protocole,
            "port":      port,
            "plage":     plage
        }
        self.firewall.regles.append(regle)
        print(f"Règle ajoutée : {action} | IP={ip_source} | "
              f"Proto={protocole} | Port={port} | Plage={plage}")

    # Supprimer une règle par index
    def supprimer_regle(self, index):
        if 0 <= index < len(self.firewall.regles):
            regle = self.firewall.regles.pop(index)
            print(f"Règle {index} supprimée : {regle}")
        else:
            print("Erreur : index invalide.")

    # Afficher toutes les règles
    def afficher_regles(self):
        print(f"\n-- Règles du Firewall {self.firewall.nom} --")
        if not self.firewall.regles:
            print("  Aucune règle définie.")
        else:
            for i, r in enumerate(self.firewall.regles):
                print(f"  [{i}] Action={r['action']} | "
                      f"IP={r['ip_source']} | "
                      f"Proto={r['protocole']} | "
                      f"Port={r['port']} | "
                      f"Plage={r['plage']}")

    # Filtrer un paquet selon les règles
    def filtrer(self, paquet):
        for regle in self.firewall.regles:

            # Vérification IP source
            ip_ok = (regle["ip_source"] is None or regle["ip_source"] == paquet.ip_source)

            # Vérification protocole
            proto_ok = (regle["protocole"] is None or regle["protocole"] == paquet.protocole)

            # Vérification port
            port_ok = (regle["port"] is None or regle["port"] == paquet.port)

            # Vérification plage réseau
            plage_ok = (regle["plage"] is None or paquet.ip_source.startswith(regle["plage"]))

            # Si tous les critères correspondent
            if ip_ok and proto_ok and port_ok and plage_ok:
                decision = regle["action"]
                self._journaliser(paquet, decision)
                print(f"[FIREWALL] Paquet {decision} "
                      f"(IP={paquet.ip_source} | "
                      f"Proto={paquet.protocole})")
                return decision

        # Aucune règle ne correspond : autoriser par défaut
        self._journaliser(paquet, "ALLOW")
        print("[FIREWALL] Paquet autorisé (aucune règle applicable)")
        return "ALLOW"

    # Enregistrer une décision dans le journal
    def _journaliser(self, paquet, decision):
        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entree = (f"[{horodatage}] {decision} | "
                  f"{paquet.ip_source} -> {paquet.ip_destination} | "
                  f"Proto={paquet.protocole}")
        self.firewall.journal.append(entree)


    def afficher_journal(self):
        print(f"\n-- Journal du Firewall {self.firewall.nom} --")
        if not self.firewall.journal:
            print("  Journal vide.")
        else:
            for entree in self.firewall.journal:
                print(f"  {entree}")


    def vider_journal(self):
        self.firewall.journal.clear()
        print(f"Journal du firewall {self.firewall.nom} vidé.")

    def inspecter(self, paquet, nom_equipement):
        heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for regle in self.firewall.regles:
            if regle.correspond(paquet):
                decision = regle.action
                raison   = f"[{decision}] sur {nom_equipement}"
                entree   = f"[{heure}] {raison} | {paquet}"                  
                self.firewall.journal.append(entree)
            if decision == "BLOCK":
                return False, raison
            else:
                return True, raison
        raison = f"ALLOW par defaut sur {nom_equipement}"
        entree = f"[{heure}] {raison} | {paquet}"
        self.firewall.journal.append(entree)
        return True, raison