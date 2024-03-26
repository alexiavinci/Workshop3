from flask import Flask, request, jsonify
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import numpy as np

app = Flask(__name__)

# Chargement du dataset et entraînement du modèle (peut être fait à l'avance)
iris = load_iris()
X, y = iris.data, iris.target
model = LogisticRegression(max_iter=200)
model.fit(X, y)

@app.route('/predict', methods=['GET'])
def predict():
    # Extrait les paramètres de la requête
    sepal_length = request.args.get('sepal_length', type=float)
    sepal_width = request.args.get('sepal_width', type=float)
    petal_length = request.args.get('petal_length', type=float)
    petal_width = request.args.get('petal_width', type=float)
    
    # Prédiction
    prediction = model.predict(np.array([[sepal_length, sepal_width, petal_length, petal_width]]))
    species = iris.target_names[prediction][0]
    
    # Réponse
    return jsonify(species=species)

if __name__ == '__main__':
    app.run(debug=True)
