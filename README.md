# Projet Poly# - Google Hash Code 2021

## Description du projet
Ce projet implémente une solution au problème "Traffic Signaling" du concours Google Hash Code 2021. L’objectif est de simuler la circulation dans une ville modélisée par des intersections, des rues à sens unique et des voitures, afin d'optimiser les plans de feux tricolores (schedules). Le but est de réduire les temps d’attente et de maximiser le score global en faisant arriver le maximum de voitures à destination dans le temps imparti.

Le programme lit un fichier d’entrée, applique une stratégie algorithmique pour générer un planning de feux, simule le trafic pour évaluer le score via un module dédié, et produit un fichier de sortie conforme au format attendu.

## Équipe et Répartition des tâches

**LAMOTHE Pol** - pol.lamothe--trebaol@etu.univ-nantes.fr
> **Tâches :** Architecture des données (`Polystructure`), implémentation de la stratégie avancée (`AdvancedSolver`) et stratégie de nettoyage (`Unused`).

**GUÉRIN Killian** - killian.guerin1@etu.univ-nantes.fr
> **Tâches :** Implémentation du moteur de simulation et de scoring (`Polyscorer`) et gestion des tickets.

**TCHOUASSI Yves Maël** - yves-mael.tchouassi@etu.univ-nantes.fr
> **Tâches :** Lecture et parsing des fichiers d'entrée (`Polyparser`) et implémentation de l'heuristique statistique (`MostUsed`).

**ARNAUD Kyllian** - kyllian.arnaud@etu.univ-nantes.fr
> **Tâches :** Génération des fichiers de sortie (`Polyexport`), implémentation de l'heuristique équilibrée (`IntersectionSolver`) et rédaction de la documentation.

## Procédure d'installation

Le projet nécessite **Python 3**.

1. **Cloner le dépôt** :
```bash
git clone https://gitlab.univ-nantes.fr/E239555L/polyhash-2025.git
```

2. **Installer les dépendances** :
Le projet utilise `ruff` pour le linting.
```bash
pip install -r requirements.txt
```



## Procédure d'exécution

Le point d'entrée du programme est le script `polyhash.py`.

### Syntaxe de base

```bash
python3 polyhash.py [fichier_challenge] [nom_stratégie] -o [fichier_sortie]
```

### Arguments

* `challenge` : Le nom du fichier d'entrée (sans l'extension `.in`, ex: `a_example`).
* `solution` : La stratégie à utiliser (par défaut `empty`). Valeurs disponibles :
* `mostused`
* `intersectionsolver`
* `advanced`
* `unused`
* `empty`


* `-o`, `--output` : Chemin du fichier de sortie (ex: `a` -> solutions/CHALLENGE/a.txt).
* `-v` : Mode verbeux.
* `-d` : Mode diagnostic (génère un fichier CSV d'analyse dans le dossier `diagnose/`).

### Exemple

Pour exécuter la stratégie avancée sur le challenge "a_example" et sauvegarder le résultat :

```bash
python3 polyhash.py a_example advanced -o a
```

## Détail des stratégies mises en œuvre

### 1. Stratégie `MostUsed` (Heuristique simple)

* **Principe :** Cette stratégie compte le nombre de passages de voitures dans chaque rue. Le temps de feu vert attribué est calculé proportionnellement à la fréquentation de la rue (fréquence divisée par 6, avec un minimum de 1 seconde).
* **Performances :** Très rapide (complexité linéaire par rapport au nombre de voitures), peu gourmande en mémoire.

### 2. Stratégie `IntersectionSolver` (Heuristique par budget)

* **Principe :** Chaque intersection dispose d'un "budget" de temps fixe (10 secondes). Ce temps est réparti entre les rues entrantes au prorata du trafic global observé sur chacune d'elles.
* **Performances :** Exécution rapide. Permet d'équilibrer le trafic mieux que `MostUsed` sur des intersections complexes.

### 3. Stratégie `Advanced` (Algorithme itératif)

C'est notre stratégie la plus performante. Elle fonctionne par itérations successives :

1. **Filtrage initial :** Élimination des voitures qui n'ont mathématiquement pas le temps d'arriver à destination.
2. **Initialisation :** Attribution d'un temps de 1 seconde à toutes les rues utilisées.
3. **Optimisation des conflits :** Analyse des bouchons via une simulation intermédiaire (`scorer`). Si une rue verte est vide alors qu'une rue rouge est bouchée, l'ordre de passage est modifié.
4. **Gestion de la densité :** Augmentation itérative du temps de feu vert pour les rues où s'accumulent le plus de voitures.
5. **Nettoyage final :** Les voitures n'ayant toujours pas fini leur trajet après optimisation sont retirées du calcul pour libérer les rues.

* **Performances :** Temps d'exécution plus long car elle nécessite plusieurs appels au simulateur (`scorer`) pour ajuster les paramètres, mais offre les meilleurs scores.

## Organisation du code

Le projet est structuré en modules pour séparer les responsabilités :

* **`polyhash.py`** : Programme principal. Gère les arguments en ligne de commande et orchestre les étapes (parsing -> solving -> scoring -> export).
* **`polystructure.py`** : Contient les classes de données (`Challenge`, `Intersection`, `Street`, `Car`, `Schedule`). C'est le cœur du modèle objet.
* **`polyparser.py`** : Chargé de lire les fichiers `.in` et de créer les objets du `DataManager`.
* **`polyexport.py`** : Génère le fichier de sortie conforme au format attendu par Hash Code.
* **`polyscorer.py`** : Simule le déroulement du trafic seconde par seconde pour calculer le score et fournir des métriques utilisées par la stratégie `Advanced`.
* **`solvers/`** : Package contenant les différentes stratégies (`advanced.py`, `mostused.py`, `intersectionsolver.py`, `unused.py`).

## Bugs et limitations connus

* **Limitations de l'approche `Advanced` :** L'optimisation est locale et itérative. Elle peut tomber dans des optimums locaux. De plus, la simulation complète (`scorer`) à chaque itération peut être coûteuse en temps pour les très gros fichiers.
* **Gestion de la mémoire :** Pour les très gros challenges, la création d'objets pour chaque rue et voiture peut consommer une quantité importante de RAM.

## Autres fonctionnalitées :

**Diagnostic :** L'option `-d` exporte un fichier CSV avec l'état détaillé des intersections, utile pour le débogage.