# solarcast

☀️ SolarCast : Solution Intelligente de Prédiction Solaire
SolarCast est une application web Full-Stack conçue pour démocratiser l'accès aux prévisions de production d'énergie photovoltaïque. En combinant le Machine Learning et des données météorologiques de haute précision, l'outil permet aux utilisateurs d'optimiser leur consommation énergétique.

🏗️ Architecture du Système
L'écosystème SolarCast repose sur une communication fluide entre trois piliers technologiques :

Le Frontend (Angular) : Une interface réactive et typée qui permet de configurer les caractéristiques de l'installation (puissance, localisation, inclinaison).

Le Backend (FastAPI) : Un moteur de calcul ultra-rapide qui orchestre l'entraînement des modèles IA et la récupération des données externes.

L'Infrastructure de Données (Redis) : Une couche de persistance haute performance utilisée pour le cache des prévisions et la gestion de la sécurité (Rate Limiting).

🧠 Le Moteur d'Intelligence Artificielle
Au cœur du projet se trouve un modèle XGBoost (Extreme Gradient Boosting). Contrairement à une simple estimation statistique, SolarCast :

Récupère l'historique d'ensoleillement de la NASA sur les dernières années.

Entraîne dynamiquement un modèle spécifique aux coordonnées GPS fournies.

Applique ce modèle sur les prévisions de Visual Crossing pour obtenir une estimation de production heure par heure.

🚀 Optimisations Techniques
⚡ Performance & Coût (Caching)
Pour limiter les appels coûteux aux APIs météo et accélérer le temps de réponse, les résultats sont stockés dans Redis.

Une même recherche dans une zone géographique identique est servie instantanément depuis le cache.

Les données sont versionnées (v2:predict:...) pour garantir une cohabitation saine entre les environnements.

🛡️ Sécurité (Rate Limiting)
Afin de protéger l'infrastructure contre les abus ou les attaques par déni de service, un limiteur de débit est intégré via Redis. Chaque utilisateur est limité à 60 requêtes par minute, identifiées par adresse IP (v2:rate:...).

🌍 Impact Environnemental
SolarCast ne se contente pas de chiffres bruts. Pour chaque prédiction, l'application calcule :

Économies financières : Estimation du gain en euros selon les tarifs actuels.

Empreinte Carbone : Calcul du CO2 évité grâce à l'énergie propre produite.

🛠️ Stack Technique Récapitulative
Frontend : Angular (TypeScript)

Backend : Python (FastAPI)

IA : XGBoost, Scikit-learn, Pandas

Data : NASA Power API, Visual Crossing

DevOps : Docker, Redis, Render