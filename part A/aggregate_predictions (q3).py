import requests

# Liste des URL ngrok des serveurs de modèles du groupe
model_urls = [
    'https://c95f-46-193-3-62.ngrok-free.app/predict/logistic', # vérifier à chauqe démarrage les bons urls
    'https://c95f-46-193-3-62.ngrok-free.app/predict/predict/decision_tree'
    
]

# Exemple de données à prédire
data = {
    "sepal_length": "5.1",
    "sepal_width": "3.5",
    "petal_length": "1.4",
    "petal_width": "0.2"
}

# Collecter les prédictions de chaque modèle
predictions = []
for url in model_urls:
    try: 
        response = requests.get(url, params=data)
        if response.ok:
            prediction = response.json()['prediction']
            predictions.append(prediction[0])
        else:
            print(f"Erreur lors de la requête : {response.status_code} pour l'URL {url}")
    except Exception as e:
        print(f"Erreur lors de l'accès à l'URL {url}: {e}")

# Calculer la prédiction moyenne (pour un problème de classification, cela pourrait nécessiter une logique supplémentaire)
if predictions:
    consensus_prediction = sum(predictions) / len(predictions)
    print("Prédiction consensuelle :", consensus_prediction)
else:
    print("Aucune prédiction reçue.")


## avec des poids pour chaque modèle
# Poids initiaux
# weights = [1.0 for _ in range(nombre_de_modeles)]

# # Pour chaque lot de données
# for data_batch in data_batches:
#     predictions = []
#     # Collecter les prédictions de chaque modèle
#     for i, model_url in enumerate(model_urls):
#         prediction = make_prediction(model_url, data_batch)
#         predictions.append(prediction)
    
#     # Calculer la prédiction consensuelle (moyenne pondérée)
#     consensus_prediction = sum(weight * prediction for weight, prediction in zip(weights, predictions)) / sum(weights)
    
#     # Évaluer chaque modèle et ajuster les poids
#     for i, prediction in enumerate(predictions):
#         if abs(prediction - consensus_prediction) > seuil_d_erreur_acceptable:
#             weights[i] *= facteur_de_reduction  # Slashing pour les prédictions inexactes
#         else:
#             weights[i] *= facteur_d_augmentation  # Renforcement pour les bonnes prédictions

#     # Utiliser `consensus_prediction` comme prédiction finale pour ce lot

