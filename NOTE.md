A faire :


1. Principal :
   - Paramètres (contenu : fps, volume dans le jeu, plein écran, ...) (bouton dans le jeu)
   - Documenter (Docstring, README, ...)

2. Visuel :
   - animations, mettre la musique, ...
   - Voir les TODOs

3. Bug : 
   - Quitter pendant que l'on décide de si l'on doit charger ou non une ancienne sauvegarde fait crash l'adversaire
   - Si le port est déjà utilisé, le jeu n'indique par l'erreur à l'hôte
   - Les champs invalides n'empêchent pas de faire l'action
   - (incertain) Dans de rare cas (souvent en fermant brutalement la fenêtre) le processus ne s'arrête pas
   - Si la fenêtre est fermée, l'erreur "delete_vao AttributeError: 'NoneType' object has no attribute 'current_context'" apparait parfois

4. Vérification :
   - Tester sur Linux
   - test avec "assert" (cahier des charges)
   - mode d'emploi (video + pdf) expliquant le fonctionnement
