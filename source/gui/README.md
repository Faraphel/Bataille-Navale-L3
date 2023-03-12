Ce module est une "surcouche" pour le module pyglet afin d'implémenter quelques éléments qui
ne sont pas déjà disponibles nativement dans cette librairie, tel que :

- Les scènes (attachable à une fenêtre afin de changer rapidement de menu / d'interface)
- Les widgets (attachable à des scènes afin de rajouter des boutons, des textes, ...)

Ces éléments permettent de plus facilement gérer le redimensionnement de la fenêtre tout en
restant suffisamment rapide pour ne pas causer de problème de ralentissement.