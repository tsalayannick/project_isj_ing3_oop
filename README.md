# SIMNet — Simulateur de Réseau Intelligent en Python

> Projet de groupe — Programmation Orientée Objet en Python  
> INGÉNIEUR 3 SRT — Institut Saint Jean — Année académique 2025/2026

---

## Membres du groupe

| N° | Nom et Prénom            | Rôle                                  |
|----|----------------------    |---------------------------------------|
| 1  | Tsala Yannick            | Chef de projet — Module 1 (Modélisation réseau) |
| 2  | Selihe Emmanuel          | Module 2 (Simulation de trafic)       |
| 3  | Ngassa Bradley           | Module 3 (Sécurité & Filtrage)        |
| 4  | Aissatou Bintou          | Module 4 (Surveillance & Rapports)    |
| 5  | Sarr Salif               | Module 5 (Interface console)          |

---

## Description du projet

SIMNet est un **simulateur de réseau d'entreprise entièrement orienté objet**, développé en Python 3.  
Il permet de modéliser une infrastructure réseau, d'y faire circuler des données, d'en assurer la sécurité et d'en superviser le fonctionnement.

---

## Structure du projet

```
project_isj_ing3_oop/
│
├── src/
│   ├── equipements.py   # Classes des équipements réseau
│   ├── topologie.py     # Topologie et liens entre équipements
│   ├── paquets.py       # Paquet et simulation de trafic
│   ├── securite.py      # Firewall, règles de filtrage, journal
│   ├── moniteur.py      # Moniteur réseau et génération de rapport
│   └── main.py          # Point d'entrée — menu interactif
│
├── rapport.pdf          # Rapport technique du groupe
└── README.md            # Ce fichier
```

---

## Instructions de lancement

### Prérequis

- **Python 3.x** installé sur votre machine
- Aucune bibliothèque externe requise (uniquement la bibliothèque standard Python)

### Lancer le simulateur

```bash
# 1. Cloner le dépôt
git clone https://github.com/tsalayannick/project_isj_ing3_oop.git
cd project_isj_ing3_oop

# 2. Lancer le simulateur
python src/main.py
```

Le menu interactif s'affiche automatiquement dans le terminal.

---

## Fonctionnalités implémentées

### Module 1 — Modélisation du réseau ✅

- Classe mère `Equipement` avec validation d'adresse IPv4
- 6 types d'équipements : `Routeur`, `Switch`, `Serveur`, `Firewall`, `PointAccesWifi`, `Terminal`
- Classe `Lien` avec bande passante (Mbps) et latence (ms)
- Classe `Topologie` : conteneur central du réseau
  - Ajout / suppression d'équipements
  - Ajout de liens entre équipements
  - Recherche d'équipement par nom
  - Affichage complet de la topologie

### Module 2 — Simulation de trafic ✅

- Classe `Paquet` avec adresse source/destination, protocole (TCP/UDP/ICMP), taille et priorité
- Algorithme de routage **BFS** (Breadth First Search) pour trouver le chemin optimal
- Transmission saut par saut à travers les équipements intermédiaires
- Détection des destinations inatteignables
- Statistiques : paquets envoyés, perdus, débit cumulé, temps de transit simulé

### Module 3 — Sécurité et filtrage ✅

- Règles de filtrage par IP source, protocole et port destination
- Journalisation de chaque décision avec horodatage (`datetime`)
- Authentification login / mot de passe pour accéder à la configuration du firewall
- Affichage du journal complet

### Module 4 — Surveillance et rapports ✅

- Classe `Moniteur` collectant les statistiques du réseau
- Suivi des paquets transmis / perdus par équipement
- Taux d'utilisation des liens
- Historique des 10 derniers paquets (`collections.deque`)
- Génération du rapport d'exploitation dans `rapport_simnet.txt`

### Module 5 — Interface console interactive ✅

- Menu interactif en boucle `while`
- Ajout / suppression d'équipements et de liens
- Envoi de paquets avec visualisation du parcours
- Consultation du journal du firewall
- Affichage des statistiques
- Génération du rapport
- Quitter proprement le simulateur

---

## Concepts POO utilisés

| Concept | Application dans SIMNet |
|---|---|
| **Héritage** | `Routeur`, `Switch`, `Serveur`... héritent de `Equipement` |
| **Encapsulation** | Chaque classe gère ses propres données via ses méthodes |
| **Abstraction** | `Equipement` modélise un équipement réseau générique |
| **Polymorphisme** | `afficher()` redéfinie différemment dans chaque sous-classe |

---

## Exemple d'utilisation

```
===== SIMNET — MENU PRINCIPAL =====
1. Ajouter un équipement
2. Supprimer un équipement
3. Ajouter un lien
4. Afficher la topologie
5. Envoyer un paquet
6. Consulter le journal du firewall
7. Afficher les statistiques
8. Générer le rapport
0. Quitter
====================================
Votre choix : 
```

---

## Modules Python utilisés

Uniquement des modules de la **bibliothèque standard Python 3** :

- `abc` — classes abstraites
- `datetime` — horodatage du journal firewall
- `collections` — `deque` pour l'historique des paquets
- `os` — gestion des fichiers pour le rapport

---

*Institut Saint Jean — Yaoundé, Cameroun — 2025/2026*
