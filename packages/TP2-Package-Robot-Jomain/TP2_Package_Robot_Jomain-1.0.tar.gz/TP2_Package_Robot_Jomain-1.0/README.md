# TP2 Admin : projet robot

## Principe
Déplacer un robot qui est représenté par un 1 sur une grille où chaque case correspond à un 0 (voir image). Vous pouvez le déplacer en appelant les méthodes up,down,left ou right.

![Image de la grille](Images/grille.png)
## Installation
### Packages nécessaires au fonctionnement 
- numpy
- pytest
## Règles 
### Règles liées à la grille
Si vous rentrez un nombre inférieur à 2 ou plus grand que 30 pour les lignes ou les colonnes, il y a la création automatique d'une grille de taille 20x20.
Une erreur est renvoyée si l'utilisateur entre autre chose qu'un nombre entier.(exemple : un float ou une string)
Le robot se trouve au départ en haut à gauche de la grille c'est-à-dire à la position (0,0).
### Règles liées au déplacement du robot
Le robot peut être déplacer en appelant les différentes méthodes up,down,left et right. Le robot effectuera le déplacement à la condition qu'il ne sorte pas de la grille sinon une erreur est renvoyée.
## Packages
### Package_Robot
Il contient la classe deplacement qui contient les différentes méthodes nécessaires au déplacement du robot. Il y a aussi la méthode qui permet d'afficher la grille.

![Image de la classe deplacement](Images/class_deplacement.png)
### Packages_Test
Il contient plusieurs classes telles que :
- Test_Deplacement_Robot qui vérifie que chaque méthode up,right,down et left renvoie une errreur si le robot veut se déplacer en dehors de la grille.

![Image de la classe Test_Deplacement_Robot](Images/test_deplacement.png)
- Test_Grid qui vérifie que l'utilisateur a bient entré un nombre entier pour la taille de la grille, qu'il est bien plus grand que 2 et plus petit quee 30.

![Image de la classe Test_Grid](Images/test_grid.png)
## Améliorations futures
Générer des obstacles sur la grille.
Robot capable de pousser l'obstacle s'il n'est pas au bord de la grille.
