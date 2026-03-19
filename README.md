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

│   ├── stats.py

│   ├── steps.py

│   ├── calories.py

│   └── heart\_rate.py


```

\## 🚀 Installation



\### 1. Cloner le repo



```bash

git clone https://github.com/cecehh/garmin_api


```



\### 2. Configurer les credentials



Remplis le fichier `.env` avec tes identifiants Garmin Connect :



```env

GARMIN\_EMAIL=ton@email.com

GARMIN\_PASSWORD=tonmotdepasse

```



> Si tu laisses le `.env` vide, l'API te demandera tes credentials via Basic Auth directement dans Swagger.



\### 3. Lancer le serveur


Utilisez le fichier launch.bat



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

  "date": "2025-03-19",
  
  "total_steps": 8420,
  
  "step_goal": 10000,
  
  "total_distance_meters": 6315.5,
  
  "total_kilocalories": 2150.0,
  
  "active\_kilocalories": 450.0,
  
  "bmr_kilocalories": 1700.0,
  
  "wellness_active_kilocalories": 430.0,
  
  "average_heart_rate": 68,
  
  "max_heart_rate": 142,
  
  "resting_heart_rate": 52,
  
  "average_stress_level": 28,
  
  "floor_climbed": 4,
  
  "minutes_sedentary": 480,
  
  "minutes_lightly_active": 210,
  
  "minutes_moderately_active": 45,
  
  "minutes_highly_active": 30

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

   "http://localhost:8000/stats/today",

   auth=("ton@email.com", "motdepasse")

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



