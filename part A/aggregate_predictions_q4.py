import requests
from collections import Counter

SEUIL_ERREUR = 0.1
penalty_amount = 50

# Liste des URL ngrok des serveurs de modèles du groupe
# model_urls = [
#     'https://c95f-46-193-3-62.ngrok-free.app/predict/logistic', # vérifier à chauqe démarrage les bons urls
#     'https://c95f-46-193-3-62.ngrok-free.app/predict/predict/decision_tree'
    
# ]

# data test we know is Virginica label 2
# data = {
#     "sepal_length": "6.7",
#     "sepal_width": "3.0",
#     "petal_length": "5.2",
#     "petal_width": "2.3"
# }


# virginica is label 2
#true_value = 2 


# on a besoin de changer à chaque fois le nouvel url car compte gratuit sur ngrok :(
models = {
    "model1": {"deposit": 1000, "weight": 1.0, "url": "https://c00e-46-193-3-62.ngrok-free.app/predict/logistic"},
    "model2": {"deposit": 1000, "weight": 1.0, "url": "https://c00e-46-193-3-62.ngrok-free.app/predict/decision_tree"},
    
}

def collect_predictions(data):
    predictions = {}
    for model_id, model_info in models.items():
        try:
            response = requests.get(model_info["url"], params=data)
            if response.ok:
                prediction = response.json()['prediction']
                predictions[model_id] = prediction[0]
                print(f"Modèle {model_id} prédit: {prediction[0]}") 
            else:
                print(f"Erreur lors de la requête : {response.status_code} pour l'URL {model_info['url']}")
        except Exception as e:
            print(f"Erreur lors de l'accès à l'URL {model_info['url']}: {e}")
    return predictions



def distribute_penalty_among_accurate_models(penalty_pool, predictions, true_value):
    reward_per_accurate_model = penalty_pool / sum(1 for prediction in predictions.values() if prediction == true_value)  # Récompense à distribuer à chaque modèle précis
    for model_id, model in models.items():
        if predictions[model_id] == true_value:  # Vérifier si le modèle était précis
            model["deposit"] += reward_per_accurate_model  # Ajouter la récompense au dépôt du modèle précis



def adjust_weights_and_deposits(predictions, true_value):
    penalty_pool = 0

    for model_id, prediction in predictions.items():
        model = models[model_id]

        # Vérifier si la prédiction est correcte
        is_accurate = prediction == true_value

        if is_accurate:
            # Si le modèle est précis, augmenter son poids
            model["weight"] *= 1.1
        else:
            # Si le modèle est inexact, appliquer une pénalité
            model["deposit"] -= penalty_amount
            model["weight"] *= 0.9
            penalty_pool += penalty_amount

    # Répartir la pénalité parmi les modèles précis
    if penalty_pool > 0:
        distribute_penalty_among_accurate_models(penalty_pool, predictions, true_value)


def calculate_consensus_prediction(predictions):
    # Utiliser un vote majoritaire pour déterminer la prédiction consensuelle
    if predictions:
        # On extrait les prédictions de chaque modèle
        prediction_values = list(predictions.values())
        # On compte les occurrences de chaque prédiction
        prediction_counts = Counter(prediction_values)
        # Afficher la répartition des votes
        print(f"Répartition des votes: {prediction_counts}")
        # On détermine la prédiction la plus fréquente
        consensus_prediction, _ = prediction_counts.most_common(1)[0]
        return consensus_prediction
    else:
        return None

