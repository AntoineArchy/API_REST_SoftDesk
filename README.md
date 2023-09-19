# Présentation
Le but de l'exercice est de développer une API REST permettant à des utilisateurs de créer des projets, définir des tâches et features de ces projets (issue) ainsi que d'ajouter des commentaires à ces issues.
Cette application est développée en utilisant le framework Django et Django REST framework.

# Fonctionnement 
Le projet repose sur quatres ressources principales : Project, Issue, Comments et Users.

Project (Projets): Les projets sont la resource de base de l'application. C'est autours d'un projet que se construiront les autres ressources.  
Issue (Tâches): Les issues sont liées à un projet et permettent de définir des problèmes ou axes d'améliorations des projets. Une issue peut avoir un statut, une prioritée et un utilisateur assigné.  
Comments (Commentaires): Les comments permettent aux utilisateurs de discuter autours d'une issue.  
Users (Utilisateurs): Les utilisateurs de l'API. 

# Fonctionnalités
Depuis l'application, il est possible pour un utilisateur de : 
- Se connecter ou créer un autre utilisateur.
- Créer des projets ou s'abonner à un projet existant
- Créer des tâches, les assignées a un utilisateur et en modifier les détails
- Ajouter des commentaires aux tâches
- Modifier ou supprimer le contenu créé par l'utilisateur authentifié 
- Modifier ou supprimer les informations concernant l'utilisateur authentifié

# Mise en place

### Récupération du dépot 
- Téléchargez le contenu de ce dépot via le bouton dédié ou, dans un terminal : $ git clone https://github.com/AntoineArchy/API_REST_SoftDesk.git

### Création de l'environnement virtuel
Ouvrez un terminal; 

- Pour ouvrir un terminal sur Windows, pressez les touches windows + r et entrez cmd.
- Sur Mac, pressez les touches command + espace et entrez "terminal".
- Sur Linux, vous pouvez ouvrir un terminal en pressant les touches Ctrl + Alt + T.

Placez-vous dans le dossier où vous souhaitez créer l'environnement (Pour plus de facilité aux étapes suivantes, il est recommandé de faire cette opération dans le dossier contenant le script à exécuter). Puis exécutez à présent la commande : 

`python -m venv env
`

Une fois fait, un nouveau dossier "env" devrait être créé dans le répertoire, il s'agit de votre environnement virtuel.


### Activation de l'environnement virtuel
Une fois la première étape réalisée, vous pouvez à présent activer votre environnement.

Pour ce faire, dans le dossier où l'environnement a été créé :


Ouvrez un terminal, rendez-vous au chemin d'installation de votre environnement puis exécutez la commande : 

- Windows (Cmd) : `env\Scripts\activate.bat`
- bash/zsh : `source venv/bin/activate`
- fish : `source venv/bin/activate.fish`
- csh/tcsh : `source venv/bin/activate.csh`
- PowerShell : `venv/bin/Activate.ps1`

Une fois fait, vous constatez que les lignes de votre cmd commencent à présent par "(env)", cela signifie que votre environnement est actif.

### Installation des dépendances
Dans le même terminal qu'à l'étape précédente :

`pip install -r requirements.txt`

#### Note : 
Il est également possible de monter l'environnement virtuel avec Pipenv, pour ce faire :

- Ouvrez un terminal puis où vous souhaitez créer l'environnement puis exécutez à présent les commandes : 

-`pipenv install`  
-`pipenv shell`

### Execution 
Lors du premier lancement, il est important de suivre les étapes l'une après l'autre. Lors des exécutions suivantes, il est possible de réutiliser l'environnement créé précédemment. Pour ce faire, ne suivez que l'étape 2 (Activer l'environnement virtuel), vous pouvez alors simplement contrôler que les dépendances sont bien installées via la commande : `pip freeze`. Si toutes les dépendances sont bien présentes, il est possible de passer directement à l'exécution du script.

- Dans le terminal ayant servi à l'activation de l'environnement virtuel, exécutez la commande :
`python3 manage.py runserver`
- Dans le navigateur de votre choix, se rendre à l'adresse http://127.0.0.1:8000/api (une fois la commande runserver exécutée, le terminal devrait vous afficher une confirmation du lancement ainsi que l'adresse pour joindre le serveur)


# Utilisation  

Dans un premier temps, il vous faudra créer un compte administrateur via la commande : 
`python manage.py createsuperuser` puis renseignez les informations demandées par le terminal.

Une fois ce compte en place, il vous sera alors possible de vous connecter et de naviguer l'API soit via une plateforme d'API (Postman, ...) ou via le
serveur localhost du Django REST Framework.

L'administration de la BDD est accessible via l'url http://127.0.0.1:8000/admin  
Les schémas sont accessibles via l'url http://127.0.0.1:8000/api/schema  
L'application utilisant drf-spectacular, il est possible d'accéder aux resources de l'api via les urls http://127.0.0.1:8000/api/schema/swagger-ui/  ou  http://127.0.0.1:8000/api/schema/redoc/  
Aucun front-end n'étant mis en place, assurez bien que vos requêtes commencent par <URL_de_votre_serveur>/api/