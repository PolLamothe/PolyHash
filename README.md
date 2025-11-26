Projet Poly#
============

### Description du projet

-----
Ce projet implémente une solution au problème Traffic Signaling du concours Google Hash Code 2021.

L’objectif est de simuler la circulation dans une ville modélisée par des intersections, rues à sens unique et voitures, puis d’optimiser les schedules de feux tricolores afin de réduire les temps d’attente et maximiser le score obtenu.

La ville est décrite par un ensemble de rues (avec durée de traversée), d’intersections et de trajets prédéfinis pour chaque voiture.

Notre programme lit un fichier d’entrée, calcule un planning de feux optimal selon notre stratégie, puis génère un fichier de sortie conforme au format attendu.



### Notre Missions

---
Notre mission dans ce projet se compose de plusieurs étapes :
1. Lire et interpréter les fichiers d’entrée
   - Durée de simulation
   - Liste des intersections
   - Liste des rues (nom, début, fin, durée)
   - Chemin que chaque voiture doit parcourir 
   

2. Analyser le trafic
    - Compter combien de voitures passent par chaque rue
    - Identifier les intersections critiques / très fréquentées
    - Calculer la charge potentielle sur les feux


3. Générer un planning de feux (traffic light schedule)
    
    Pour chaque intersection :
    - Choisir quelles rues auront un feu vert (certaines rues peuvent rester toujours rouges)
    - Définir un ordre de passage
    - Déterminer une durée de feu vert adaptée au trafic 


4. Optimiser pour maximiser le score
    
    Un véhicule rapporte :
    - F points s’il termine à temps
    - D - T points supplémentaires, où T est le temps d’arrivée

    L’objectif est donc :
    - Faire passer un maximum de voitures à temps
    - Minimiser leur attente aux intersections 


5. Générer le fichier de sortie

    Selon le format requis :
    - Nombre d’intersections configurées
   
    - Pour chacune :
      - ID de l’intersection
      - Nombre de rues gérées
      - Les paires (rue, durée du feu vert)

   
### Résumé

---
En bref, ce projet vise à optimiser l’écoulement du trafic dans une simulation afin d’obtenir le meilleur score possible.
Nous développons un algorithme se basant sur la densité du trafic pour produire un schedule intelligent et efficace, tout en respectant les contraintes du problème Hash Code.


Fonctionnement du projet
========================

(Description du fonctionnement du projet, notamment comment le lancer (paramètres, etc).)

La syntaxe générale/minimale est

    polyhash.py ./challenges/challenge.in ./output/sortie.txt

L'équipe
========

À compléter par **chaque personne**: 1 ligne par personne, indiquant le nom et l'adresse mail de la personne, et chacun pousse ses informations.

L'objectif de cette manipulation est de provoquer des conflits d'édition, qui surviennent quand un même fichier est modifié au même endroit par plusieurs personnes, et de voir comment on les résout.

- LAMOTHE Pol - pol.lamothe--trebaol@etu.univ-nantes.fr
- Killian Guérin - killian.guerin1@etu.univ-nantes.fr
- Yves Maël Tchouassi - yves-mael.tchouassi@etu.univ-nantes.fr
- ARNAUD Kyllian - kyllian.arnaud@etu.univ-nantes.fr