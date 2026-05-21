from equipements import Routeur, Switch, Serveur, Firewall, PointAccesWifi, Terminal, saisir_ip
from topologie import Topologie
from paquet import Paquet
from simulateur_trafic import SimulateurTrafic
from moniteur import MoniteurReseau
from securite import authentifier, GestionnaireFirewall

# Creation des objets principaux
topologie = Topologie()
simulateur = SimulateurTrafic(topologie)
moniteur   = MoniteurReseau()

while True:
    print("\n========== SIMNet — Menu Principal ==========")
    print("-- Equipements --")
    print("  1.  Ajouter un equipement")
    print("  2.  Supprimer un equipement")
    print("  3.  Activer / Desactiver un equipement")
    print("  4.  Gerer un equipement (routes / vlans / services)")
    print("-- Reseau --")
    print("  5.  Ajouter un lien")
    print("  6.  Supprimer un lien")
    print("  7.  Afficher la topologie")
    print("-- Trafic --")
    print("  8.  Envoyer un paquet")
    print("  9.  Afficher les statistiques")
    print("  10. Afficher l historique des paquets")
    print("-- Securite --")
    print("  11. Configurer le Firewall")
    print("  12. Journal du Firewall")
    print("-- Rapports --")
    print("  13. Generer un rapport")
    print("  0.  Quitter")
    print("=============================================")

    choix = input("Choix : ")

    match choix:

        # ===== AJOUTER UN EQUIPEMENT =====
        case "1":
            while True:
                print("\n-- Ajouter un equipement --")
                print("1-Routeur  2-Switch  3-Serveur  4-Firewall  5-Wifi  6-Terminal")
                t = input("Type : ")
                if t not in ["1","2","3","4","5","6"]:
                    print("Erreur : type invalide.")
                else:
                    nom    = input("Nom : ")
                    ip     = saisir_ip(topologie.equipements)
                    marque = input("Marque : ")
                    match t:
                        case "1":
                            topologie.ajouter_equipement(Routeur(nom, ip, marque))
                        case "2":
                            topologie.ajouter_equipement(Switch(nom, ip, marque))
                        case "3":
                            topologie.ajouter_equipement(Serveur(nom, ip, marque))
                        case "4":
                            topologie.ajouter_equipement(Firewall(nom, ip, marque))
                        case "5":
                            ssid  = input("SSID : ")
                            canal = int(input("Canal (1-13) : "))
                            topologie.ajouter_equipement(PointAccesWifi(nom, ip, marque, ssid, canal))
                        case "6":
                            topologie.ajouter_equipement(Terminal(nom, ip, marque))
                encore = input("Voulez-vous ajouter un autre equipement ? (o/n) : ")
                if encore.lower() != "o":
                    break
            input("\nAppuyez sur Entree pour continuer...")

        # ===== SUPPRIMER UN EQUIPEMENT =====
        case "2":
            while True:
                print("\n-- Supprimer un equipement --")
                if len(topologie.equipements) == 0:
                    print("Erreur : aucun equipement dans le reseau.")
                    break
                for eq in topologie.equipements:
                    print(f"  - {eq.nom} ({eq.adresse_ip})")
                nom = input("Nom de l equipement a supprimer : ")
                topologie.supprimer_equipement(nom)
                if len(topologie.equipements) == 0:
                    print("Plus aucun equipement dans le reseau.")
                    break
                encore = input("Voulez-vous supprimer un autre equipement ? (o/n) : ")
                if encore.lower() != "o":
                    break
            input("\nAppuyez sur Entree pour continuer...")

        # ===== ACTIVER / DESACTIVER =====
        case "3":
            print("\n-- Activer / Desactiver un equipement --")
            if len(topologie.equipements) == 0:
                print("Erreur : aucun equipement dans le reseau.")
            else:
                for eq in topologie.equipements:
                    etat = "actif" if eq.statut else "inactif"
                    print(f"  - {eq.nom} ({etat})")
                nom = input("Nom de l equipement : ")
                eq  = topologie.trouver_equipement(nom)
                if eq is None:
                    print("Erreur : equipement introuvable.")
                else:
                    print("1. Activer   2. Desactiver")
                    action = input("Choix : ")
                    match action:
                        case "1":
                            eq.activer()
                        case "2":
                            eq.desactiver()
                        case _:
                            print("Erreur : choix invalide.")
            input("\nAppuyez sur Entree pour continuer...")

        # ===== GERER UN EQUIPEMENT =====
        case "4":
            print("\n-- Gerer un equipement --")
            if len(topologie.equipements) == 0:
                print("Erreur : aucun equipement dans le reseau.")
            else:
                for eq in topologie.equipements:
                    print(f"  - {eq.nom} | {type(eq).__name__} ({eq.adresse_ip})")
                nom = input("Nom de l equipement : ")
                eq  = topologie.trouver_equipement(nom)
                if eq is None:
                    print("Erreur : equipement introuvable.")
                elif isinstance(eq, Routeur):
                    print("1. Ajouter une route   2. Afficher les routes")
                    action = input("Choix : ")
                    match action:
                        case "1":
                            dest = input("Destination (ex: 192.168.1.0) : ")
                            saut = input("Prochain saut (ex: 192.168.0.1) : ")
                            eq.ajouter_route(dest, saut)
                        case "2":
                            eq.afficher()
                        case _:
                            print("Erreur : choix invalide.")
                elif isinstance(eq, Switch):
                    print("1. Ajouter un VLAN   2. Afficher les VLANs")
                    action = input("Choix : ")
                    match action:
                        case "1":
                            vlan_id = int(input("ID du VLAN : "))
                            eq.ajouter_vlan(vlan_id)
                        case "2":
                            eq.afficher()
                        case _:
                            print("Erreur : choix invalide.")
                elif isinstance(eq, Serveur):
                    print("1. Ajouter un service   2. Afficher les services")
                    action = input("Choix : ")
                    match action:
                        case "1":
                            service = input("Service (ex: HTTP:80) : ")
                            eq.ajouter_service(service)
                        case "2":
                            eq.afficher()
                        case _:
                            print("Erreur : choix invalide.")
                else:
                    eq.afficher()
            input("\nAppuyez sur Entree pour continuer...")

        # ===== AJOUTER UN LIEN =====
        case "5":
            while True:
                print("\n-- Ajouter un lien --")
                if len(topologie.equipements) < 2:
                    print("Erreur : il faut au moins 2 equipements pour creer un lien.")
                    break
                for eq in topologie.equipements:
                    print(f"  - {eq.nom} ({eq.adresse_ip})")
                nom_a = input("Nom equipement A : ")
                nom_b = input("Nom equipement B : ")
                if nom_a == nom_b:
                    print("Erreur : vous ne pouvez pas relier un equipement a lui-meme.")
                else:
                    eq_a = topologie.trouver_equipement(nom_a)
                    eq_b = topologie.trouver_equipement(nom_b)
                    if eq_a is None or eq_b is None:
                        print("Erreur : un des equipements est introuvable.")
                    else:
                        lien_existant = False
                        for lien in topologie.liens:
                            if (lien.equipement_a.nom == nom_a and lien.equipement_b.nom == nom_b) or \
                               (lien.equipement_a.nom == nom_b and lien.equipement_b.nom == nom_a):
                                lien_existant = True
                                break
                        if lien_existant:
                            print("Erreur : un lien existe deja entre ces deux equipements.")
                        else:
                            try:
                                bp  = float(input("Bande passante (Mbps) : "))
                                lat = float(input("Latence (ms) : "))
                                if bp <= 0 or lat <= 0:
                                    print("Erreur : valeurs doivent etre positives.")
                                else:
                                    topologie.ajouter_lien(eq_a, eq_b, bp, lat)
                            except ValueError:
                                print("Erreur : veuillez entrer des nombres valides.")
                encore = input("Voulez-vous ajouter un autre lien ? (o/n) : ")
                if encore.lower() != "o":
                    break
            input("\nAppuyez sur Entree pour continuer...")

        # ===== SUPPRIMER UN LIEN =====
        case "6":
            while True:
                print("\n-- Supprimer un lien --")
                if len(topologie.liens) == 0:
                    print("Erreur : aucun lien dans le reseau.")
                    break
                for lien in topologie.liens:
                    print(f"  - {lien.equipement_a.nom} <-> {lien.equipement_b.nom}")
                nom_a = input("Nom equipement A : ")
                nom_b = input("Nom equipement B : ")
                lien_trouve = None
                for lien in topologie.liens:
                    if (lien.equipement_a.nom == nom_a and lien.equipement_b.nom == nom_b) or \
                       (lien.equipement_a.nom == nom_b and lien.equipement_b.nom == nom_a):
                        lien_trouve = lien
                        break
                if lien_trouve:
                    topologie.liens.remove(lien_trouve)
                    print(f"Lien entre '{nom_a}' et '{nom_b}' supprime.")
                else:
                    print("Erreur : lien introuvable.")
                if len(topologie.liens) == 0:
                    print("Plus aucun lien dans le reseau.")
                    break
                encore = input("Voulez-vous supprimer un autre lien ? (o/n) : ")
                if encore.lower() != "o":
                    break
            input("\nAppuyez sur Entree pour continuer...")

        # ===== AFFICHER LA TOPOLOGIE =====
        case "7":
            topologie.afficher()
            input("\nAppuyez sur Entree pour continuer...")

        # ===== ENVOYER UN PAQUET =====
        case "8":
            print("\n-- Envoyer un paquet --")
            if len(topologie.equipements) < 2:
                print("Erreur : il faut au moins 2 equipements pour envoyer un paquet.")
            else:
                for eq in topologie.equipements:
                    print(f"  - {eq.nom} ({eq.adresse_ip})")
                src = saisir_ip()
                dst = saisir_ip()
                if src == dst:
                    print("Erreur : la source et la destination ne peuvent pas etre identiques.")
                else:
                    proto = input("Protocole (TCP/UDP/ICMP) : ").upper()
                    try:
                        taille = int(input("Taille en octets : "))
                        prio   = int(input("Priorite (1-5) : "))
                        paquet = Paquet(src, dst, proto, taille, prio)
                        # On passe le firewall au simulateur si il y en a un
                        fw_obj = None
                        for eq in topologie.equipements:
                            if isinstance(eq, Firewall):
                                fw_obj = GestionnaireFirewall(eq)
                                break
                        simulateur.transmettre(paquet, firewall=fw_obj)
                    except ValueError as e:
                        print(f"Erreur : {e}")
            input("\nAppuyez sur Entree pour continuer...")

        # ===== STATISTIQUES =====
        case "9":
            simulateur.afficher_statistiques()
            input("\nAppuyez sur Entree pour continuer...")

        # ===== HISTORIQUE =====
        case "10":
            simulateur.afficher_historique()
            input("\nAppuyez sur Entree pour continuer...")

        # ===== CONFIGURER LE FIREWALL =====
        case "11":
            print("\n-- Configuration du Firewall --")
            firewalls = []
            for eq in topologie.equipements:
                if isinstance(eq, Firewall):
                    firewalls.append(eq)
            if not firewalls:
                print("Erreur : aucun firewall dans le reseau.")
            elif authentifier():
                for eq in firewalls:
                    print(f"  - {eq.nom}")
                nom = input("Nom du firewall a configurer : ")
                fw_eq = topologie.trouver_equipement(nom)
                if fw_eq is None or not isinstance(fw_eq, Firewall):
                    print("Erreur : firewall introuvable.")
                else:
                    gestionnaire = GestionnaireFirewall(fw_eq)
                    print("\n1. Ajouter une regle")
                    print("2. Supprimer une regle")
                    print("3. Afficher les regles")
                    print("4. Vider le journal")
                    action = input("Choix : ")
                    match action:
                        case "1":
                            print("Action : BLOCK ou ALLOW")
                            act        = input("Action : ").upper()
                            ip_source  = input("IP source (laisser vide si aucune) : ") or None
                            protocole  = input("Protocole TCP/UDP/ICMP (laisser vide si aucun) : ") or None
                            port_str   = input("Port destination (laisser vide si aucun) : ")
                            port       = int(port_str) if port_str else None
                            plage      = input("Plage reseau ex:192.168.1 (laisser vide si aucune) : ") or None
                            gestionnaire.ajouter_regle(act, ip_source, protocole, port, plage)
                        case "2":
                            gestionnaire.afficher_regles()
                            try:
                                index = int(input("Index de la regle a supprimer : "))
                                gestionnaire.supprimer_regle(index)
                            except ValueError:
                                print("Erreur : entrez un nombre valide.")
                        case "3":
                            gestionnaire.afficher_regles()
                        case "4":
                            gestionnaire.vider_journal()
                        case _:
                            print("Erreur : choix invalide.")
            input("\nAppuyez sur Entree pour continuer...")

        # ===== JOURNAL FIREWALL =====
        case "12":
            print("\n-- Journal du Firewall --")
            firewalls = []
            for eq in topologie.equipements:
                if isinstance(eq, Firewall):
                    firewalls.append(eq)
            if not firewalls:
                print("Erreur : aucun firewall dans le reseau.")
            elif authentifier():
                for fw in firewalls:
                    gestionnaire = GestionnaireFirewall(fw)
                    gestionnaire.afficher_journal()
            input("\nAppuyez sur Entree pour continuer...")

        # ===== RAPPORT =====
        case "13":
            moniteur.generer_rapport()
            input("\nAppuyez sur Entree pour continuer...")

        # ===== QUITTER =====
        case "0":
            print("Au revoir !")
            break

        case _:
            print("Erreur : choix invalide.")
            input("\nAppuyez sur Entree pour continuer...")