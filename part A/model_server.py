from flask import Flask, request, jsonify
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from aggregate_predictions_q4 import collect_predictions, adjust_weights_and_deposits, calculate_consensus_prediction

app = Flask(__name__)

# Chargement du dataset Iris
iris = load_iris()
X, y = iris.data, iris.target

# Entraînement du modèle de Régression Logistique
logistic_model = LogisticRegression(max_iter=200)
logistic_model.fit(X, y)

# Entraînement du modèle d'Arbre de Décision
decision_tree_model = DecisionTreeClassifier(random_state=42)
decision_tree_model.fit(X, y)

@app.route('/predict/logistic', methods=['GET'])
def predict_logistic():
    features = request.args
    features_array = np.array([[features.get("sepal_length"), features.get("sepal_width"), features.get("petal_length"), features.get("petal_width")]], dtype=float)
    prediction = logistic_model.predict(features_array)
    return jsonify({'prediction': prediction.tolist()})

@app.route('/predict/decision_tree', methods=['GET'])
def predict_decision_tree():
    features = request.args
    features_array = np.array([[features.get("sepal_length"), features.get("sepal_width"), features.get("petal_length"), features.get("petal_width")]], dtype=float)
    prediction = decision_tree_model.predict(features_array)
    return jsonify({'prediction': prediction.tolist()})

@app.route('/test_prediction', methods=['GET'])
def test_prediction():
    # Extraire les paramètres de la requête et les passer aux fonctions
    data_test = {
        "sepal_length": request.args.get('sepal_length'),
        "sepal_width": request.args.get('sepal_width'),
        "petal_length": request.args.get('petal_length'),
        "petal_width": request.args.get('petal_width')
    }
    true_value = int(request.args.get('true_value'))
    
    # Utilise les fonctions importées pour le traitement
    predictions = collect_predictions(data_test)
    adjust_weights_and_deposits(predictions, true_value)
    consensus_prediction = calculate_consensus_prediction(predictions)

    # Retourner la réponse
    return jsonify({
        "consensus_prediction": consensus_prediction
        # Ajoute d'autres informations si nécessaire
    })

if __name__ == '__main__':
    app.run(debug=True)

