# TP2 Admin : projet robot

## Principe
Déplacer un robot qui est représenté par un 1 sur une grille où chaque case correspond à un 0 (voir image). Vous pouvez le déplacer en appelant les méthodes up,down,left ou right.

![Image de la grille](Images/grille.png)

Vous pouvez aussi décider d'ajouter le nombres d'obstacles que vous désirez sur la grille qui son représentés par des 7. (voir image ci-dessous). Les obstacles sont fixes et le robot ne peut donc pas se rendre sur une case qui possède un obstacle.

![Image de la grille avec obstacle](Images/grille_Obstacle.png)
## Jouer
Une fois le package installé, 
## Règles 
### Règles liées à la grille
Si vous rentrez un nombre inférieur à 3 ou plus grand que 30 pour les lignes ou les colonnes, il y a la création automatique d'une grille de taille 20x20.
Une erreur est renvoyée si l'utilisateur entre autre chose qu'un nombre entier.(exemple : un float ou une string)
Le robot se trouve au départ à la position (1,1) (au centre de la grille si celle-ci est de taille 3x3).
### Règles liées au déplacement du robot
Le robot peut être déplacer en appelant les différentes méthodes up,down,left et right. Le robot effectuera le déplacement à condition que :
- qu'il ne sorte pas de la grille sinon une erreur est renvoyée.
- qu'il n'y pas un obstacle sur son chemin sinon une erreur est renvoyée.
### Règles liées à la génération des obstacles
Les obstacles sont générés aléatoirements sur la grille.
Si vous rentrez un nombre d'obstacles cohérents par rapport à la taille de la grille (pas trop grand sinon voir sections Problèmes), alors vous aurez exactement ce nombre d'obstacles sur la grille car il y a une gestion des éventuels doublons.
Si vous rentrez un nombre qui dépasse le nombre de cases de la grille pour le nombre d'obstacles; alors vous n'aurez qu'un obstacle présent sur la grille qui sera en position (2,0).
## Packages
### Package_Robot
Il contient la classe deplacement qui contient les différentes méthodes nécessaires au déplacement du robot. Il y a aussi la méthode qui permet d'afficher la grille. La classe prend en paramètre d'entrée : 
- Le nombre de lignes que vous souhaitez pour la grille.
- Le nombre de colonnes que vous souhaitez pour la grille.
- Le nombre d'obstacles que vous souhaitez mettre sur la grille.

![Image de la classe deplacement](Images/class_deplacement.png)
### Packages_Test
Il contient plusieurs classes de tests telles que :
- Test_Deplacement_Robot qui vérifie que chaque méthode up,right,down et left renvoie une errreur si le robot veut se déplacer en dehors de la grille.

![Image de la classe Test_Deplacement_Robot](Images/test_deplacement.png)
- Test_Grid qui vérifie que l'utilisateur a bient entré un nombre entier pour la taille de la grille, qu'il est bien plus grand que 2 et plus petit quee 30.

![Image de la classe Test_Grid](Images/test_grid.png)
- Test_obstacle qui vérifie que pour chaque méthode de déplacements quelorsque le robot rencontre un obstacle alors on renvoie une erreur.

![Image de la classe Test_obstacle](Images/test_obstacle.png)
#### Tests
Avec l'utilisation de pytest, on voit que nos tests sont passés avec succès : 

![Image montrant le succès des tests](Images/test_OK.png)

2 tests ont été enlevé, il s'agit des tests qui vérifiait si l'utilisateur avait entré des nombres inférieurs à 3 ou supérieur à 30 pour la grille car ces erreurs ont été géré en créant une grille 20x20 si l'utilisateur est en dehors de ces limites.
## Améliorations futures
Robot capable de pousser l'obstacle s'il n'est pas au bord de la grille.
Mettre plusieurs robots sur la grille.
Approfondir notre classe de test en rajoutant d'autres cas.
## Problèmes liés à la génération d'obstacles
En théorie, on est censé pouvoir générer (ligne x colonne -1) obstacles sur la grille. Cependant, dès qu'on se rapproche de cette limite, le programme tourne à l'infini car il cherche toutes les combinaisons possibles pour mettre les obstacles sur la grille. On ne peut donc pas remplir la grille d'obstacles avec le robot présent (par exemple pour la grille 3x3, le maximum d'obstacle est 7 car il trouve jamais la combinaison (2,1) pour le dernier obstacle).


