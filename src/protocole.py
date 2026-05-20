
# protocole.py
# Ce fichier contient les protocoles réseaux
# autorisés dans notre simulateur.

class Protocole:
    """  Cette classe contient les noms des protocoles
    qu'on accepte dans notre simulateur.
    Un protocole c'est juste la "langue" que
    les paquets utilisent pour voyager.
    """

    # Les trois protocoles qu'on accepte
    TCP  = "TCP"
    UDP  = "UDP"
    ICMP = "ICMP"

    # On les met dans une liste pour vérifier facilement
    LISTE_VALIDES = ["TCP", "UDP", "ICMP"]

    @staticmethod
    def est_valide(protocole):
        """   Vérifie si le protocole donné est dans notre liste.
        Retourne True si oui, False si non.
        """
        # On met en majuscule pour éviter les erreurs de casse
        protocole_en_majuscule = protocole.upper()

        if protocole_en_majuscule in Protocole.LISTE_VALIDES:
            return True
        else:
            return False
