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
│       └── pizza_router.py
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

### Test de l'API avec Bruno ou Postman

Les collections de requêtes HTTP pour tester l'API sont disponibles dans ./Bruno et ./Postman.

### Documentation Swagger générée automatiquement par FastAPI

<http://localhost:8080/docs>

### Endpoint pizzas

#### Lecture de tous les items

```sh
curl --request GET \
  --url http://localhost:8080/pizzas
```

```http
GET /pizzas HTTP/1.1
Host: localhost:8080
```

```json
[
  {
    "id": 1,
    "name": "Margherita",
    "created_at": "2024-12-12T13:25:25.162192",
    "updated_at": null
  }
]
```

#### Lecture d'un item sélectionné par son id

```sh
curl --request GET \
  --url http://localhost:8080/pizzas/1
```

```http
GET /pizzas/1 HTTP/1.1
Host: localhost:8080
```

```json
{
  "id": 1,
  "name": "Margherita",
  "created_at": "2024-12-12T13:25:25.162192",
  "updated_at": null
}
```

## Adminer (interface web d'administration de base de données)

Pour des raisons de sécurité, __désactiver ce service en production__.

<http://localhost:8181>

- Interface d'administration web [Adminer](http://localhost:8181/?pgsql=db&username=pizzas&db=pizzas&ns=public)
- Sélectionner Système : __postgresql__
- Serveur : __db__ (= nom du service Docker)
- Utilisateur : voir valeur définie dans ./db/.env
- Mot de passe : voir valeur définie dans ./db/.env
- Base de données : voir valeur définie dans ./db/.env

## Base de données PostgreSQL

```SQL

DROP TABLE IF EXISTS "pizzas";
DROP SEQUENCE IF EXISTS pizzas_id_seq;
CREATE SEQUENCE pizzas_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."pizzas" (
    "id" integer DEFAULT nextval('pizzas_id_seq') NOT NULL,
    "name" character varying NOT NULL,
    "created_at" timestamp NOT NULL,
    "updated_at" timestamp,
    CONSTRAINT "pizzas_name_key" UNIQUE ("name"),
    CONSTRAINT "pizzas_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

CREATE INDEX "ix_pizzas_id" ON "public"."pizzas" USING btree ("id");

INSERT INTO "pizzas" ("id", "name", "created_at", "updated_at") VALUES
(1, 'Margherita', '2024-12-12 13:25:25.162192', NULL);
```

--

!["Logotype Shrp"](https://sherpa.one/images/sherpa-logotype.png)

__Alexandre Leroux__  
_Enseignant / Formateur_  
_Développeur logiciel web & mobile_

Nancy (Grand Est, France)

<https://shrp.dev>
