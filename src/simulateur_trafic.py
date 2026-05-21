# simulateur_trafic.py
# coeur du module 2 : calcule le chemin et envoie les paquets
from statistiques import Statistiques


class SimulateurTrafic:
    # on utilise Dijkstra pour trouver le chemin le plus rapide (latence minimale)

    def __init__(self, topologie):
        self.topologie = topologie
        self.statistiques = Statistiques()

    def _construire_graphe(self):
        # transforme la topologie en dictionnaire de voisins
        graphe = {}

        for lien in self.topologie.liens:
            eq_a = lien.equipement_a
            eq_b = lien.equipement_b

            # on ignore les equipements eteints
            if eq_a.statut == False or eq_b.statut == False:
                continue

            if eq_a.nom not in graphe:
                graphe[eq_a.nom] = []
            if eq_b.nom not in graphe:
                graphe[eq_b.nom] = []

            # lien dans les deux sens
            graphe[eq_a.nom].append((lien.latence, eq_b.nom, lien))
            graphe[eq_b.nom].append((lien.latence, eq_a.nom, lien))

        return graphe

    def calculer_chemin(self, nom_source, nom_destination):
        if nom_source == nom_destination:
            return [nom_source], 0.0, 999999.0

        graphe = self._construire_graphe()

        # initialisation : toutes les distances a l'infini sauf la source
        distances = {}
        predecesseurs = {}
        liens_utilises = {}

        for nom in graphe:
            distances[nom] = 999999.0
        distances[nom_source] = 0.0

        noeuds_non_visites = list(graphe.keys())

        while len(noeuds_non_visites) > 0:

            # on cherche le noeud non visite avec la plus petite distance
            noeud_actuel = None
            distance_min = 999999.0

            for noeud in noeuds_non_visites:
                if distances.get(noeud, 999999.0) < distance_min:
                    distance_min = distances[noeud]
                    noeud_actuel = noeud

            if noeud_actuel is None:
                break
            if noeud_actuel == nom_destination:
                break

            noeuds_non_visites.remove(noeud_actuel)

            for latence, nom_voisin, lien in graphe.get(noeud_actuel, []):
                nouveau_cout = distances[noeud_actuel] + latence

                # si on trouve un chemin plus court on met a jour
                if nouveau_cout < distances.get(nom_voisin, 999999.0):
                    distances[nom_voisin] = nouveau_cout
                    predecesseurs[nom_voisin] = noeud_actuel
                    liens_utilises[nom_voisin] = lien

        if distances.get(nom_destination, 999999.0) >= 999999.0:
            return [], 999999.0, 0.0

        # reconstruction du chemin en remontant les predecesseurs
        chemin = []
        noeud = nom_destination
        while noeud in predecesseurs:
            chemin.append(noeud)
            noeud = predecesseurs[noeud]
        chemin.append(nom_source)
        chemin.reverse()

        # bande passante du maillon le plus faible
        bande_passante_min = 999999.0
        for noeud in chemin[1:]:
            lien = liens_utilises.get(noeud)
            if lien is not None and lien.bande_passante < bande_passante_min:
                bande_passante_min = lien.bande_passante

        return chemin, distances[nom_destination], bande_passante_min

    def transmettre(self, paquet, firewall=None, afficher_details=True):
        if afficher_details:
            print("\n" + "-" * 50)
            print("  ENVOI D'UN PAQUET")
            print("-" * 50)
            paquet.afficher()

        # on cherche les equipements par leur IP
        eq_source = self._trouver_par_ip(paquet.adresse_source)
        eq_dest = self._trouver_par_ip(paquet.adresse_dest)

        if eq_source is None:
            print(f"  ERREUR : IP source inconnue : {paquet.adresse_source}")
            self.statistiques.enregistrer(paquet, False, 0.0, 0.0)
            return False

        if eq_dest is None:
            print(f"  ERREUR : IP destination inconnue : {paquet.adresse_dest}")
            self.statistiques.enregistrer(paquet, False, 0.0, 0.0)
            return False

        chemin, latence_totale, bande_passante_min = self.calculer_chemin(
            eq_source.nom, eq_dest.nom
        )

        if len(chemin) == 0:
            print(f"  ERREUR : {eq_source.nom} ne peut pas joindre {eq_dest.nom}")
            self.statistiques.enregistrer(paquet, False, 0.0, 0.0)
            return False

        if afficher_details:
            print(f"  Chemin ({len(chemin) - 1} saut(s)) :")

        # parcours saut par saut
        numero_saut = 0
        for nom_equipement in chemin:
            eq = self.topologie.trouver_equipement(nom_equipement)

            if afficher_details:
                if numero_saut == 0:
                    etiquette = "DEPART"
                elif numero_saut == len(chemin) - 1:
                    etiquette = "ARRIVE"
                else:
                    etiquette = f"Saut {numero_saut}"
                print(f"    [{etiquette}] {nom_equipement} ({eq.adresse_ip})")

            # verification firewall a chaque saut sauf a la source
            if firewall is not None and numero_saut > 0:
                autorise, raison = firewall.inspecter(paquet, nom_equipement)
                if not autorise:
                    print(f"  BLOQUE en [{nom_equipement}] : {raison}")
                    self.statistiques.enregistrer(paquet, False, latence_totale, 0.0)
                    return False

            numero_saut = numero_saut + 1

        # calcul du debit : taille en bits / temps en secondes
        taille_en_bits = paquet.taille * 8

        if latence_totale > 0:
            debit_calcule = (taille_en_bits / (latence_totale / 1000)) / 1_000_000
        else:
            debit_calcule = bande_passante_min

        # le debit ne peut pas depasser le maillon le plus faible
        if bande_passante_min < 999999.0:
            debit_final = min(debit_calcule, bande_passante_min)
        else:
            debit_final = debit_calcule

        if afficher_details:
            print(f"  Resultat : LIVRE !")
            print(f"  Latence  : {latence_totale:.2f} ms")
            print(f"  Debit    : {debit_final:.2f} Mbps")

        self.statistiques.enregistrer(paquet, True, latence_totale, debit_final)
        return True

    def _trouver_par_ip(self, adresse_ip):
        # cherche un equipement dans la liste par son adresse IP
        for eq in self.topologie.equipements:
            if eq.adresse_ip == adresse_ip:
                return eq
        return None

    def afficher_statistiques(self):
        self.statistiques.afficher()

    def afficher_historique(self):
        self.statistiques.afficher_historique()
