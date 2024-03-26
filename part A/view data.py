from sklearn.datasets import load_iris
import pandas as pd

# Chargement du dataset Iris
iris = load_iris()
iris_df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
iris_df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)

# Affichage des premières lignes pour l'analyse exploratoire
print(iris_df.head(), iris_df.describe(), iris_df['species'].value_counts())
