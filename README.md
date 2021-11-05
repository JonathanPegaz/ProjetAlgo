# ProjetAlgo sujet long Jonathan PEGAZ

requirement : pygame python3
lancement : `python main.py` dans le répertoire du projet 

# Contraintes et règles communes respectées
- Réalisation graphiques sous pygame
- Données structurées (classe)
- proportions (recalculé)
- planètes différenciées (couleur, sprite...)
- vitesses proportionnelles (plus rapide à proximité du soleil)
- trajectoires elliptiques
- simulation réaliste (vitesse, accélération, force)
- représentation plusieurs niveaux (lunes limité volontairement à 1 par planetes pour le temps de démarrage de l'application, peut être changé)
- données récupérées (parsing de fichier, appel de service web...)

# Intéractions disponibles :
- Zoom : avec la molette de la souris (haut/bas). Change la distance en million de km par pixel. Par défaut 1 million de km par pixel.

- Mass souris : Clic molette pour que la souris soit soumis à la gravité. Vous pouvez changer la masse de la souris en cliquant dans l'encadré concerné en haut à gauche. (attention à la rapidité de la simulation)

- Changement affichage entre nom planete et lune (influence sur la sélection). Touche m du clavier pour changer.

- Changement paramètre planète. Cliquer sur une planète permet d'afficher ces données moyennes nom masse distance soleil vitesse. Vous pouvez cliquer dans les cases concernées, changer les valeurs et cliquer sur save. (attention la mass doit rester en exposant)

- Recommencer la simulation avec les valeurs par défaut. Touche f5 du clavier.

- Creation planete avec parametres modifiable. Clique droit souris pour créer la planète avec les paramètres modifiables (sprite compris) à la position de la souris recalculés en million de km par rapport aux soleil. 

- Changement vitesse de la simulation avec les touches F1/F2. ATTENTION impact le réalisme de la simulation fortement. Expliqué plus bas. Temps par défaut 1jour/seconde. Affiché en haut à gauche de l'écran. 

!!!Je vais parler du problème du temps ici car il est important par rapport à l'intéraction concerné. (pour résumé plus vous accélerez le temps moins la simulation est préçise).
La notion de temps dans les calculs impact l'accelération et donc la position de la planète. Dans ma simulation l'accélération est multiplié par une valeur de temps. Cela pose des problèmes. Le fonctionnement normal devrait être de calculer l'accélération de la planète x/sec en fonction de la vitesse de la simulation mais le programme a du mal à suivre quand on commence à mettre des grandes valeur d'ou ma solution actuelle. Le soucis est quand impactant mon accélération lors du changement de la vitesse j'impacte aussi tout mes orbites car les positions se décalent. Cela commence à se ressentir à 1 an/sec pour les planètes et très rapidement pour les lunes. Je n'ai pas eu le temps de tester d'autres formules de calcul pour palier à ce problèmes. Je vous laisse regarder en éspérant avoir été assez clair.!!!

# Informations personnelles
J'ai plein d'autres idées mais pas eu le temps de les mettres en places. C'est possible que des relicats soient présent dans le codes. Je n'ai pas eu le temps non plus de faire un refactoring propre et de corriger la tonne de bug. Je vais expliquer plus bas comment fonctionne le projet car ce n'est pas forcément pratique de naviguer dans toutes ces lignes.

# Fonctionnement résumé
`Global:` Les données utilisés pour la simulation sont les valeurs réelle du système solaire retranscrit sur un plan 2D. Les formules de calcul utilisent bien les valeurs réel des planètes.
Les vecteurs de positions réelles dépendent du centre de l'écran (soleil x 0, y 0) donc ces vecteurs peuvent être négatif.  les vecteurs de position 2D sont par l'écran, le x 0 y 0 sont le haut gauche de l'écran. (similaire pour les autres vecteurs ex: vitesse accél force peuvent être négatif)


`ressources:` Contient l'ensemble des sprites et le background. Les sprites numérotés de 1 à 22 sont utilisées par le bouton random de l'intéraction utilisateurs création de planète. La plupart des sprites sont redimensionné en fonction du rayon de l'objet concerné.


`Data.py :`  
    Gère la création des planètes/lune au démarrage et dans les intéractions.
    Pour le démarrage j'utilise l'api "api.le-systeme-solaire.net" pour récuperer les données concernant le projets. Je parse les données en Json et les passe dans une fonction qui va me crée des objets pour tout mes éléments et les lister. 
    les autres fonctions vont me servir à créer des objets en fonctions des intéraction utilisateur.
`variables :`
- `list_id_create_planet:` 
    Représente les sprites des planètes random de l'intéraction créer une planète.
- `params_planets:` 
    utilisé pour l'appel api afin de filtrer les résultats.

`fonctions :`
- `def createObj(NomObjet, NomClass, params):`
    retourne la création d'un objet en fonction des paramètres. Utilisés par les autres fonctions.
- `def createSourisPlanete(current_distance_pixel, x, y, massSouris):`
    crée un objet souris avec des valeurs similaire à une planète en fonction des paramètres.
- `def createUserPlanete(create_input_boxes, x, y, create_planete_img, current_distance_pixel):`
    Créer une planètes en fonction des paramètres de l'intéraction utilisateurs. le x et y sont des positions du plan 2D de la souris qui sont retranscrit sur le plan réelle en fonction de la distance par pixel au moment de la création.
- `def createMoons(moon, planete_speed, planet_distance, central_planet):`
    Permet la création des lunes au moment du setup. peut etre appelé x fois par planètes pour récupérer toutes les lunes. Dans la simulation actuelle seulement 1 fois par planète car cla quantité impact le temps de démarrage de l'application.
- `def setUp():`
    Appel de l'api, traitement des données reçu, création des objets et retourne la liste de ces objets.


`Model.py:`


`display.py`


`main.py`


