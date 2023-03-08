A faire :


1. Principal :
   - Paramètres (contenu : fps, volume dans le jeu, plein écran, ...) (bouton dans le jeu)
   - Documenter (Docstring, README, ...)

2. Visuel :
   - animations, mettre la musique, ...
   - le replay devrait commencer par la fin ? (évite un bug visuel et les fonctions clears)
   - Voir les TODOs

3. Autre : 
   - test avec "assert" (cahier des charges)
   - mode d'emploi (video + pdf) expliquant le fonctionnement

Bug : 
   - Quitter pendant que l'on décide de si l'on doit charger ou non une ancienne sauvegarde fait crash l'adversaire
   - Si le port est déjà utilisé, le jeu n'indique par l'erreur à l'hote
   - Les champs invalides n'empêchent pas de faire l'action
   - (incertain) Dans de rare cas (souvent en fermant brutalement la fenêtre) le processus ne s'arrête pas
   - Si la fenêtre est fermé, l'erreur "delete_vao AttributeError: 'NoneType' object has no attribute 'current_context'" apparait parfois

   - Autre :
    - Tester sur Linux
