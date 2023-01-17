Ce module est une "surcouche" pour le module pyglet afin d'implémenter quelques éléments qui
ne sont pas déjà disponible nativement dans cette librairie, tel que :

- Les scènes (attachable à une fenêtre afin de changer rapidement de menu / d'interface)
- Les widgets (attachable à des scènes afin de rajouter des boutons, des textes, ...)

Ces éléments permettent de plus facilement gérer le redimentionnement de la fenêtre tout en
restant suffisament rapide pour ne pas causer de problème de ralentissement.