# Mémoire de stage de Julien FENECH pour le Master 2 TNAH à l'Ecole nationale des Chartes.

Ce mémoire a pour cadre le projet de la reprise des données des instruments de recherche décrivants les versements issus du service Constance.
Le stage a été effectué du 1er avril au 31 juillet 2021 aux Archives nationales. Le but du projet est de récupérer les métadonnées descriptives d'instruments de recherche pour pouvoir créer des paquets d'informations à versées dans le Système d'archivage électronique ADAMANT.

## Le Mémoire
Se trouve dans le dépôt le Mémoire en deux format, PDF et une archive ZIP contenant les fichiers LaTeX.

## Les Livrables
Les livrables sont une sélection de certains travaux que j'ai pu effectuer durant le stage et décrits dans le mémoire.
L'ensemble de ces documents sont tels que produits durant le Stage aux Archives nationales, ils ont donc tous été créés sous Windows et ne sont donc principalements utilisables que sur ce système d'exploitation. Les seuls exceptions sont les programmes au format Python (.py) et les fichiers créés à l'origine sous Word et transformés en format PDF pour ce mémoire.

### Tableau d'analyse des producteurs
Un tableau d'analyse produit conjointement avec Jeanine GAILLARD des Archives nationales décrivant les producteurs de l'ensemble des instruments de recherche du projet, et qui ont été analysés pour observer leur homogénéité dans le cadre du projet. Certaines informations ont été supprimées du fichier proposé au jury, une colonne proposait des liens menant vers des extractions des biographies des producteurs stockés sur serveur de travail du DAEAA et qui ne seront donc pas disponible pour le jury.

### Projet synthèse DCSP
Pour le projet des synthèses de la DCSP se trouve l'analyse des fichiers que j'avais pu effectuer (format texte), l'article écrit pour le numéro d'"En direct" une lettre d'information interne des Archives nationales. Ainsi que le manifeste au format XML du SIP créé dans le cadre de ce projet.

### Le programme d'extraction des instruments de recherche vers le CSV
Programme en Python permettant l'extraction d'informations d'instruments de recherche en fonction de fichiers de configuration présent à la racine du programme.
Le programme se présente sous deux formats différents : un format python classique (.py) et un format exécutable sur Windows (.exe).
Le programme est parfaitement utilisable il suffit de fournir des instruments de recherche au format XML dans le dossier EAD et d'entrer les valeurs que l'on veut retrouver dans son tableau CSV dans le fichier colonnes.ini(par défaut le programme va créer un fichier CSV avec des noms de colonnes se référent à une table d'une base de données de Archives nationales)
Pour effectuer des tests vous pourrez trouver des instruments de recherche au format XML dans la Salle des inventaires virtuelles des Archives nationales (https://www.siv.archives-nationales.culture.gouv.fr/) Chercher n'importe quel inventaire puis dans les résultats cliquer sur "voir l'inventaire" enfin cliquer sur le bouton "Export XML de l'inventaire" une fois sur la page de l'inventaire.
Quelques instruments de recherche trouvable en SIV seront fournis pour simplification.

### Le programme de transformation d'instrument de recherche vers SIP
Programme en Python lui aussi qui permet la création automatisée d'un SIP avant ingestion dans le SAE des Archives nationales. Il accepte des instruments de recherche accompagnés des versements numériques qu'ils décrivent. Ces versements sont ceux du service Constance et sont non communicables.
Toutefois le programme est malgré tout utilisable, il ne crééra juste pas un SIP et un manifest complet, mais ceux-ci seront tout de même valide du point de vue du SEDA et de l'outil ReSIP (https://www.programmevitam.fr/pages/ressources/resip/) ce qui permet de tester de la validité des métadonnées descriptives, mais ne permettra pas de tester l'identification des fichiers via le programme Siegfried et la création des métadonnées techniques.
Ce programme n'est utilisable que sur un environnement Windows.
Pour l'utiliser il faut tout d'abord placer le dossier nommé "siegfried" et son contenu, fournit avec le programme, à la racine de son dossier utilisateur Windows (C:\Users\nom_utilisateur)
Il faut ensuite créer autant de dossier que d'instruments de recherche à transformer, dans ces dossier du nom de votre choix se trouvera l'instrument de recherche et un dossier nommé "content" (vide mais où devrait se trouver les fichiers à archiver). Un instrument de recherche trouvable en SIV sera fournit avec le programme pour exemple. 
Le programme se présente là aussi sous deux formats : Une version Python et un exécutable Windows.
Pour finir se trouvera aussi un manifeste complet issus d'un versement Constance et construit avec le programme.
