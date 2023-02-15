A faire :  
Widgets:  
- Slider   
- Checkbox
- Grille (bataille navale)



Réseau :

- Connexion entre les joueurs
- Envoie des paramètres à l'autre joueur (largeur longueur du plateau, nombre de bateau et leur taille, ...)
- Phase de placement des bateaux
- Confirmer l'emplacement des bateaux (envoie des données signalant la confirmation)

- Joueur 1 sélectionne une case (envoie des données à l'autre joueur)
- Joueur 2 envoie la valeur de retour de board.bomb après les données de joueur 1
- Joueur 2 sélectionne une case 
- Joueur 1 envoie la valeur de retour également
...

- Joueur 1 gagne (envoie des données de victoire à l'autre joueur)
- Joueur 1 et Joueur 2 s'envoie mutuellement leurs plateaux pour voir les cases restantes de l'autre
- Proposition de rejouer ?