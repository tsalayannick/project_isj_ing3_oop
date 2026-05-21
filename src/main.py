# main.py — Interface console de SIMNet

from equipements import Routeur, Switch, Serveur, Firewall, PointAccesWifi, Terminal, saisir_ip
from topologie import Topologie
from paquet import Paquet
from simulateur_trafic import SimulateurTrafic
from moniteur import MoniteurReseau

# Creation des objets principaux
topologie = Topologie()
simulateur = SimulateurTrafic(topologie)
moniteur = MoniteurReseau()

while True:
    print("\n===== SIMNet =====")
    print("1. Ajouter un equipement")
    print("2. Supprimer un equipement")
    print("3. Ajouter un lien")
    print("4. Supprimer un lien")
    print("5. Afficher la topologie")
    print("6. Envoyer un paquet")
    print("7. Journal du Firewall")
    print("8. Statistiques")
    print("9. Historique des paquets")
    print("10. Generer un rapport")
    print("0. Quitter")

    choix = input("Choix : ")

    match choix:

        case "1":
            while True:
                print("\n-- Ajouter un equipement --")
                print("1-Routeur 2-Switch 3-Serveur 4-Firewall 5-Wifi 6-Terminal")
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
                encore = input("\nVoulez-vous ajouter un autre equipement ? (o/n) : ")
                if encore.lower() != "o":
                    break
            input("\nAppuyez sur Entree pour continuer...")

        case "2":
            while True:
                print("\n-- Supprimer un equipement --")
                if len(topologie.equipements) == 0:
                    print("Erreur : aucun equipement dans le reseau.")
                    break
                print("Equipements disponibles :")
                for eq in topologie.equipements:
                    print(f"  - {eq.nom} ({eq.adresse_ip})")
                nom = input("Nom de l'equipement a supprimer : ")
                topologie.supprimer_equipement(nom)
                if len(topologie.equipements) == 0:
                    print("Plus aucun equipement dans le reseau.")
                    break
                encore = input("\nVoulez-vous supprimer un autre equipement ? (o/n) : ")
                if encore.lower() != "o":
                    break
            input("\nAppuyez sur Entree pour continuer...")

        case "3":
            while True:
                print("\n-- Ajouter un lien --")
                if len(topologie.equipements) < 2:
                    print("Erreur : il faut au moins 2 equipements pour creer un lien.")
                    break
                print("Equipements disponibles :")
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
                                    print("Erreur : la bande passante et la latence doivent etre positives.")
                                else:
                                    topologie.ajouter_lien(eq_a, eq_b, bp, lat)
                            except ValueError:
                                print("Erreur : veuillez entrer des nombres valides.")
                encore = input("\nVoulez-vous ajouter un autre lien ? (o/n) : ")
                if encore.lower() != "o":
                    break
            input("\nAppuyez sur Entree pour continuer...")

        case "4":
            while True:
                print("\n-- Supprimer un lien --")
                if len(topologie.liens) == 0:
                    print("Erreur : aucun lien dans le reseau.")
                    break
                print("Liens disponibles :")
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
                encore = input("\nVoulez-vous supprimer un autre lien ? (o/n) : ")
                if encore.lower() != "o":
                    break
            input("\nAppuyez sur Entree pour continuer...")

        case "5":
            topologie.afficher()
            input("\nAppuyez sur Entree pour continuer...")

        case "6":
            print("\n-- Envoyer un paquet --")
            if len(topologie.equipements) < 2:
                print("Erreur : il faut au moins 2 equipements pour envoyer un paquet.")
            else:
                print("Equipements disponibles :")
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
                        simulateur.transmettre(paquet)
                    except ValueError as e:
                        print(f"Erreur : {e}")
            input("\nAppuyez sur Entree pour continuer...")

        case "7":
            print("\n-- Journal du Firewall --")
            firewalls = [eq for eq in topologie.equipements if isinstance(eq, Firewall)]
            if not firewalls:
                print("Erreur : aucun firewall dans le reseau.")
            else:
                for fw in firewalls:
                    print(f"\n--- Firewall : {fw.nom} ---")
                    if len(fw.journal) == 0:
                        print("  Journal vide.")
                    else:
                        for entree in fw.journal:
                            print(f"  {entree}")
            input("\nAppuyez sur Entree pour continuer...")

        case "8":
            simulateur.afficher_statistiques()
            input("\nAppuyez sur Entree pour continuer...")

        case "9":
            simulateur.afficher_historique()
            input("\nAppuyez sur Entree pour continuer...")

        case "10":
            moniteur.generer_rapport()
            input("\nAppuyez sur Entree pour continuer...")

        case "0":
            print("Au revoir !")
            break

        case _:
            print("Erreur : choix invalide. Entrez un numero entre 0 et 10.")
            input("\nAppuyez sur Entree pour continuer...")