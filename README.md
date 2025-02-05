# Docker + FastAPI (Python) + PostgreSQL

Projet modèle pour la mise en place d'une __API REST__ avec le langage __Python__ et le framework __FastAPI__ (<https://fastapi.tiangolo.com/>) et Docker.

Ce projet est fourni à des fins pédagogiques.

## Stack technologique

- Langage de programmation : Python (3.13.1)
- Framework : FastAPI
- Validateur : Pydantic
- Base de données : PostgreSQL
- ORM : SQLAlchemy
- Architecture d'API : REST

## Installation

Créer les fichiers :

- ./api/.env (reprendre le contenu du fichier ./api/.env.example)
- ./db/.env (reprendre le contenu du fichier ./db/.env.example)

## Arborescence du projet

```text
api
├── Dockerfile
├── README.md
├── app
│   ├── __init__.py
│   ├── db.py
│   ├── internal
│   │   ├── __init__.py
│   │   └── admin.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   └── task.py
│   └── routers
│       ├── __init__.py
│       └── task_router.py
└── requirements.txt
```

## Commandes Docker utiles

- Démarrage des services Docker :

`docker compose up`

- Rénitialisation des services Docker (suppression des données) :

`docker compose down`

- Démarrage des services Docker en mode détaché (reprise de la main dans le terminal) :

`docker compose up -d`

- Démarrage des services Docker avec reconstruction de l'image Docker associé à chaque service :

`docker compose up --build`

- Démarrage des services Docker avec activation du mode watch (= hot reloading) :

`docker compose up --watch`

- Consultation des services Docker actifs :

`docker compose ps`

- Arrêt des services Docker :

`docker compose stop`

- Création d'une image Docker à partir du fichier Dockerfile et des sources :

`docker build -t <image-name> .`

- Création d'un container à partir de l'image `<image-name>` précédemment créée :

`docker run -d --name <image-name> -p 8080:80 <image-name>`

### Volumes Docker

Les lignes suivantes du fichier __docker-compose.yml__ sont commentées par défaut :

```YAML
# volumes:
#   - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
#   - ./db/data:/var/lib/postgresql/data/
```

L'activation de la ligne `- ./db/init.sql:/docker-entrypoint-initdb.d/init.sql` permet d'injecter des données dans la base de données.

L'activation de la ligne `- ./db/data:/var/lib/postgresql/data/` permet de conserver une sauvegarde du contenu de la base de données dans le dossier local ./db/data

## Routes de l'API

### Test de l'API avec Bruno

Les collections de requêtes HTTP pour tester l'API sont disponibles dans ./Todolist API Python

### Documentation Swagger générée automatiquement par FastAPI

<http://localhost:8080/docs>

--

!["Logotype Shrp"](https://sherpa.one/images/sherpa-logotype.png)

__Alexandre Leroux__  
_Enseignant / Formateur_  
_Développeur logiciel web & mobile_

Nancy (Grand Est, France)

<https://shrp.dev>
