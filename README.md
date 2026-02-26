Jeu d'Action Interstellaire
Ce projet est un jeu d'action développé en Python avec la bibliothèque Pygame. Il met en œuvre des concepts avancés d'algorithmique et d'architecture logicielle pour offrir une expérience de jeu fluide et dynamique.

1. Architecture Événementielle (Game Loop)
Le moteur du jeu repose sur une Game Loop rigoureuse qui assure la synchronisation entre:
La capture des entrées utilisateur (clavier/manette).
Le joueur pilote un vaisseau spatial et doit survivre dans un environnement hostile tout en gérant ses ressources.
Déplacement : Utilisation des touches directionnelles (Haut, Bas, Gauche, Droite).
Attaque : Le vaisseau est équipé d'un système de tir laser pour éliminer les menaces(La touche espace permet de tirer ces lasers).
Défense : La touche Shift permet d'activer un bouclier protecteur contre les tirs ennemis.
Bonus : La collecte de diamants permet au joueur de regagner des points de vie en plein vol.
La mise à jour de l'état logique du jeu (physique, collisions, scores).

3. Algorithmique Avancée & Difficulté Adaptative
Pour garantir une rejouabilité constante, le jeu propose un environnement dynamique:
Trajectoires aléatoires : Les ennemis et obstacles suivent des motifs de déplacement imprévisibles.
Équilibrage dynamique : La difficulté s'adapte en temps réel aux performances du joueur, ajustant la vitesse et la fréquence d'apparition des entités.

4. Gestion Optimisée des Entités
Le cycle de vie des objets complexes (Intelligence Artificielle des ennemis, projectiles) est géré via des structures de données optimisées (listes de dictionnaires).
Cette approche permet de manipuler un grand nombre d'entités simultanément sans perte de performance.

Gestion des Ressources via JSON
L'une des particularités techniques du projet est la gestion des boucliers :
Le stock de boucliers est sérialisé et stocké dans un fichier JSON.
Cette architecture impose au joueur une utilisation stratégique de ses ressources, car le stock est limité et persistant.
Dans le fichier JSON le score estaussi stocké pour ammener de la competitivité dans le jeu.

💻 Technologies Utilisées
Langage : Python 
Bibliothèque Graphique : Pygame 
Logique : Algorithmique avancée et programmation événementielle 

Comment Lancer le Jeu ?
Assurez-vous d'avoir Python installé sur votre machine.
Installez la bibliothèque Pygame :
pip install pygame
Lancez le script principal :
Interstellaire_AMDE_ABBA_ADJI.py
