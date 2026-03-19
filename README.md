\# 🏃 Garmin Connect API



Une API REST construite avec \*\*FastAPI\*\* pour récupérer vos données personnelles depuis Garmin Connect — pas, calories, distance, fréquence cardiaque et plus encore.



> ⚠️ Garmin ne dispose pas d'API publique officielle. Ce projet s'appuie sur la librairie \[`python-garminconnect`](https://github.com/cyberjunky/python-garminconnect) qui utilise l'API web non officielle de Garmin Connect.



\---



\## ✨ Fonctionnalités



\- 📊 Stats quotidiennes complètes (pas, calories, FC, stress, étages...)

\- 🗓️ Consultation par date ou par plage (jusqu'à 31 jours)

\- ⚡ Cache mémoire d'une minute pour limiter les appels à Garmin

\- 🔐 Authentification via `.env` ou Basic Auth dans Swagger

\- 📋 Logging structuré des requêtes et erreurs dans le terminal

\- 📖 Documentation Swagger interactive auto-générée



\---



\## 📁 Structure du projet



```

garmin\_api/

├── main.py              # Point d'entrée — app, middleware, routers

├── helpers.py           # Auth, dates, cache

├── config.py            # Lecture du fichier .env

├── .env                 # Credentials Garmin (non versionné)

├── requirements.txt

├── models/

│   ├── daily\_stats.py

│   ├── steps.py

│   ├── calories.py

│   └── heart\_rate.py

└── routers/

&#x20;   ├── stats.py

&#x20;   ├── steps.py

&#x20;   ├── calories.py

&#x20;   └── heart\_rate.py

```



\---



\## 🚀 Installation



\### 1. Cloner le repo



```bash

git clone https://github.com/ton-user/garmin-connect-api.git

cd garmin-connect-api

```



\### 2. Installer les dépendances



```bash

pip install -r requirements.txt

```



\### 3. Configurer les credentials



Remplis le fichier `.env` avec tes identifiants Garmin Connect :



```env

GARMIN\_EMAIL=ton@email.com

GARMIN\_PASSWORD=tonmotdepasse

```



> Si tu laisses le `.env` vide, l'API te demandera tes credentials via Basic Auth directement dans Swagger.



\### 4. Lancer le serveur



```bash

cd garmin\_api

python -m uvicorn main:app --reload --port 8000

```



La documentation Swagger est disponible sur : \*\*http://localhost:8000/docs\*\*



\---



\## 📡 Endpoints



| Méthode | Route | Description |

|---------|-------|-------------|

| `GET` | `/stats/today` | Toutes les stats du jour |

| `GET` | `/stats/{date}` | Toutes les stats d'une date |

| `GET` | `/stats/range/{start}/{end}` | Stats sur une plage (max 31 jours) |

| `GET` | `/steps/today` | Pas + distance du jour |

| `GET` | `/steps/{date}` | Pas + distance d'une date |

| `GET` | `/calories/today` | Calories du jour |

| `GET` | `/calories/{date}` | Calories d'une date |

| `GET` | `/heart-rate/today` | Fréquence cardiaque du jour |

| `GET` | `/heart-rate/{date}` | Fréquence cardiaque d'une date |



Les dates sont au format \*\*YYYY-MM-DD\*\* (ex: `2025-03-19`).



\---



\## 📦 Exemple de réponse — `/stats/today`



```json

{

&#x20; "date": "2025-03-19",

&#x20; "total\_steps": 8420,

&#x20; "step\_goal": 10000,

&#x20; "total\_distance\_meters": 6315.5,

&#x20; "total\_kilocalories": 2150.0,

&#x20; "active\_kilocalories": 450.0,

&#x20; "bmr\_kilocalories": 1700.0,

&#x20; "wellness\_active\_kilocalories": 430.0,

&#x20; "average\_heart\_rate": 68,

&#x20; "max\_heart\_rate": 142,

&#x20; "resting\_heart\_rate": 52,

&#x20; "average\_stress\_level": 28,

&#x20; "floor\_climbed": 4,

&#x20; "minutes\_sedentary": 480,

&#x20; "minutes\_lightly\_active": 210,

&#x20; "minutes\_moderately\_active": 45,

&#x20; "minutes\_highly\_active": 30

}

```



\---



\## 🔐 Authentification



\### Option 1 — Fichier `.env` (recommandé)



Remplis `GARMIN\_EMAIL` et `GARMIN\_PASSWORD` dans le `.env`. Les credentials sont chargés automatiquement au démarrage, aucune saisie requise dans Swagger.



\### Option 2 — Basic Auth via Swagger



Laisse le `.env` vide. Dans Swagger (`/docs`), clique sur le bouton \*\*🔒 Authorize\*\* en haut à droite et saisis tes identifiants Garmin. Ils seront utilisés pour toutes les requêtes de la session.



\### Option 3 — Basic Auth via curl / requests



```bash

curl -u "ton@email.com:motdepasse" http://localhost:8000/stats/today

```



```python

import requests



r = requests.get(

&#x20;   "http://localhost:8000/stats/today",

&#x20;   auth=("ton@email.com", "motdepasse")

)

print(r.json())

```



\---



\## 🛡️ Sécurité



\- Ne versionne \*\*jamais\*\* ton fichier `.env` — il est à ajouter dans ton `.gitignore`

\- Ce projet est conçu pour un usage \*\*local ou personnel\*\*. Si tu l'exposes sur Internet, ajoute une couche de sécurité supplémentaire (HTTPS, token API, etc.)



\---



\## 🧰 Stack technique



\- \[FastAPI](https://fastapi.tiangolo.com/) — framework web

\- \[python-garminconnect](https://github.com/cyberjunky/python-garminconnect) — client Garmin non officiel

\- \[Pydantic v2](https://docs.pydantic.dev/) — validation des données

\- \[pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic\_settings/) — gestion du `.env`

\- \[Uvicorn](https://www.uvicorn.org/) — serveur ASGI



\---



\## 📝 Licence



MIT



