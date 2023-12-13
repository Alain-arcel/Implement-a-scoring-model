# Projet de scoring de crédit

## Introduction
Prêt à dépenser est une société financière qui propose des crédits à la consommation pour des personnes ayant peu ou pas du tout d'historique de prêt. L'entreprise souhaite développer un outil de "scoring crédit" pour calculer la probabilité qu'un client rembourse son crédit, puis classifie la demande en crédit accordé ou refusé.
Ce projet vise à construire un modèle de scoring qui répond aux objectifs suivants :
* Avoir une bonne précision, c'est-à-dire prédire correctement si un client remboursera ou non son crédit.
* Prendre en compte le déséquilibre entre les bons et les mauvais clients, qui est un problème courant dans les données de crédit.
* Minimiser le coût métier, c'est-à-dire minimiser le risque de perte en capital (faux négatifs) ou de manque à gagner en marge (faux positifs).

## Données
Les données utilisées dans ce projet sont issues d'une compétition Kaggle sur le crédit à la consommation. Ces données comprennent des informations sur les clients, telles que leur âge, leur revenu, leur historique de crédit, etc.
https://www.kaggle.com/c/home-credit-default-risk/data

## Spécifications du dashboard
Le dashboard interactif devra contenir les fonctionnalités suivantes :
* Visualisation du score et de son interprétation pour chaque client.
* Visualisation des informations descriptives relatives à un client.
* Comparaison des informations descriptives relatives à un client à l'ensemble des clients ou à un groupe de clients similaires.
* Spécifications techniques

Le dashboard interactif sera réalisé en Python, en utilisant la bibliothèque **Dash**. L'application sera déployée sur une plateforme Cloud, telle qu'**Azure** et **Heroku**.

## Méthode
La méthode utilisée pour construire le modèle de scoring sera la suivante :
* Analyse exploratoire des données pour identifier les variables pertinentes et les problèmes potentiels.
* Préparation des données pour les rendre compatibles avec l'algorithme de modélisation.
* Feature engineering pour créer de nouvelles variables à partir des variables existantes.
* Sélection d'un algorithme de modélisation.
* Entraînement du modèle sur les données d'entraînement.
* Évaluation du modèle sur les données de test.
* Optimisation du modèle en ajustant les hyperparamètres.
* Déploiement du modèle en production.

## Résultats attendus
Les résultats attendus de ce projet sont les suivants :
* Un modèle de scoring performant, avec une bonne précision et une bonne prise en compte du déséquilibre entre les bons et les mauvais clients.
* Un dashboard interactif utile aux chargés de relation client, qui leur permet de comprendre les décisions d'octroi de crédit et d'améliorer la connaissance client.

## Spécifications contextuelles
Les spécifications contextuelles suivantes seront prises en compte dans l'élaboration du modèle :
* Le déséquilibre entre les bons et les mauvais clients sera pris en compte en utilisant la méthode du SMOTE.
* Le déséquilibre du coût métier entre les faux négatifs et les faux positifs sera pris en compte en créant un score métier personnalisé. Ce score sera calculé en fonction du coût d'un faux négatif et d'un faux positif.
* Le seuil qui détermine, à partir d'une probabilité, la classe 0 ou 1 sera optimisé pour minimiser le score métier.

## Outils et bibliothèques utilisés
Les outils et bibliothèques suivants seront utilisés dans ce projet :
* Python
* Pandas
* Scikit-learn
* FastAPI
* Dash
* Azure
* Heroku
* Docker
* Evidently
* Shap

## Conclusion
Ce projet est un défi intéressant, qui permettra de développer une solution innovante pour Prêt à dépenser. Les résultats de ce projet auront un impact positif sur l'entreprise, en lui permettant d'améliorer la précision de ses décisions d'octroi de crédit et d'offrir un meilleur service à ses clients.

