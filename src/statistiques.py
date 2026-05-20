# statistiques.py
# garde en memoire tout ce qui se passe sur le reseau

class Statistiques:

    TAILLE_HISTORIQUE = 10

    def __init__(self):
        # compteurs de base
        self.nombre_envoyes = 0
        self.nombre_perdus = 0
        self.debit_cumule = 0.0
        self.transit_cumule = 0.0
        self.historique = []

    def get_nombre_livres(self):
        return self.nombre_envoyes - self.nombre_perdus

    def get_taux_perte(self):
        # eviter division par zero
        if self.nombre_envoyes == 0:
            return 0.0
        return (self.nombre_perdus / self.nombre_envoyes) * 100

    def get_transit_moyen(self):
        if self.get_nombre_livres() == 0:
            return 0.0
        return self.transit_cumule / self.get_nombre_livres()

    def enregistrer(self, paquet, succes, temps_transit, debit):
        self.nombre_envoyes = self.nombre_envoyes + 1

        if succes:
            self.debit_cumule = self.debit_cumule + debit
            self.transit_cumule = self.transit_cumule + temps_transit
        else:
            # paquet perdu ou bloque
            self.nombre_perdus = self.nombre_perdus + 1

        self.historique.append((paquet, succes))

        # on garde seulement les 10 derniers
        if len(self.historique) > self.TAILLE_HISTORIQUE:
            self.historique.pop(0)

    def afficher(self):
        print("\n" + "=" * 45)
        print("     STATISTIQUES DU RESEAU")
        print("=" * 45)
        print(f"  Paquets envoyes : {self.nombre_envoyes}")
        print(f"  Paquets livres : {self.get_nombre_livres()}")
        print(f"  Paquets perdus : {self.nombre_perdus}")
        print(f"  Taux de perte : {self.get_taux_perte():.1f} %")
        print(f"  Debit cumule : {self.debit_cumule:.2f} Mbps")
        print(f"  Transit moyen : {self.get_transit_moyen():.2f} ms")
        print("=" * 45)

    def afficher_historique(self):
        print("\n" + "-" * 45)
        print(f"  HISTORIQUE DES {len(self.historique)} DERNIERS PAQUETS")
        print("-" * 45)
        if len(self.historique) == 0:
            print("  Aucun paquet transmis.")
        for paquet, succes in self.historique:
            if succes:
                print(f"  [OK]    {paquet}")
            else:
                print(f"  [PERDU] {paquet}")
        print("-" * 45)

    def vers_texte(self):
        # utilise par moniteur.py pour ecrire le rapport
        texte = "STATISTIQUES DU RESEAU\n"
        texte += f"  Paquets envoyes : {self.nombre_envoyes}\n"
        texte += f"  Paquets livres : {self.get_nombre_livres()}\n"
        texte += f"  Paquets perdus : {self.nombre_perdus}\n"
        texte += f"  Taux de perte : {self.get_taux_perte():.1f} %\n"
        texte += f"  Debit cumule : {self.debit_cumule:.2f} Mbps\n"
        texte += f"  Transit moyen : {self.get_transit_moyen():.2f} ms\n"
        return texte
