# Importation des bibliothèques
from fastapi import FastAPI, Path
from pydantic import BaseModel
import joblib
import pandas as pd
import shap
from sklearn.neighbors import NearestNeighbors
from sklearn.impute import SimpleImputer
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset


# Initialisation d'une instance de l'API
app = FastAPI()

# Chargement du modèle de prédiction de crédit
load_clf = joblib.load("LGBMClassifier.pkl")

# Chargement du dataframe de données
df = pd.read_parquet("test_df.parquet")

# Identification des colonnes avec des valeurs manquantes
columns_with_nan = df.columns[df.isna().any()].tolist()

# Création de l'instance SimpleImputer avec la stratégie de la médiane
imputer = SimpleImputer(strategy='median')

# Remplacement des valeurs manquantes par la médiane de chaque colonne
df[columns_with_nan] = imputer.fit_transform(df[columns_with_nan])

# Définition des caractéristiques pertinentes (isolement des features non utilisées)
ignore_features = ['Unnamed: 0', 'SK_ID_CURR', 'INDEX', 'TARGET']
relevant_features = [col for col in df.columns if col not in ignore_features]

# Création de l'explainer shap
explainer = shap.TreeExplainer(load_clf)

# Création d'une classe Pydantic pour les paramètres d'entrée
class ClientRequest(BaseModel):
    id_client: int

# Définition d'une route vers la racine de l'API
@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI API!"}

# Définition de la route pour obtenir la liste des identifiants clients
@app.get("/client_ids")
async def get_client_ids():
    clients_ids =  df['SK_ID_CURR'].tolist()
    return clients_ids

# Défintion d'une route pour obtenir la liste des features
@app.get("/features")
async def get_features():
    features = relevant_features
    return features

# Définition de la route de prédiction de crédit ("/credit/{id_client}")
@app.get("/credit/{id_client}")
async def predict_credit(id_client: int = Path(..., title="Client ID")):
    # Filtre sur les données du client en question
    X = df[df['SK_ID_CURR'] == id_client]
    X = X[relevant_features]

    # Calcul de la prédiction et de la probabilité de prédiction
    proba = load_clf.predict_proba(X)
    prediction = load_clf.predict(X)

    # Afficher la probabilité avec 2 chiffres après la virgule
    proba_formatted = round(float(proba[0][0]), 2)
    
    # Interprétation
    interpretation = ""
    if prediction[0] == 0:
        interpretation = f"Client solvable avec une probabilité égale à {proba_formatted}"
    else:
        interpretation = f"Client non solvable avec une probabilité égale à {proba_formatted}"
    
    # Création de la réponse de la prédiction
    pred_proba = {
        'Prédiction': int(prediction[0]),
        'Probabilité': proba_formatted,
        'Conclusion': interpretation
    }

    # Retour de la réponse de la prédiction
    return pred_proba


# Définition de la route pour récupérer les données d'un client spécifique
@app.get("/client_data/{id_client}")
async def get_client_data(id_client: int = Path(..., title="Client ID")):
    # Filtrer les données du client en question
    client_data = df[df['SK_ID_CURR'] == id_client]

    return client_data.to_dict(orient="records")

# Définition de la route pour récupérer les données de 1000 clients choisis de manière aléatoire
@app.get("/all_clients_data")
async def get_all_clients_data():
   
   # Échantillon aléatoire de 1000 clients
   random_clients = df.sample(n=1000, random_state=42)
   
   return random_clients.to_dict(orient="records")


# Définition de la route pour calculer les plus proches voisins du client_id
@app.get("/nearest_neighbors/{id_client}")
async def get_nearest_neighbors(id_client: int = Path(..., title="Client ID"), n_neighbors: int = 10):
    # Extraction des features du client en question
    client_data = df[df['SK_ID_CURR'] == id_client][relevant_features]

    # Initialisation du modèle des plus proches voisins
    nn_model = NearestNeighbors(n_neighbors=n_neighbors)
    
    # Entraînement du modèle sur l'ensemble des données
    nn_model.fit(df[relevant_features])
    
    # Recherche des plus proches voisins du client
    _, indices = nn_model.kneighbors(client_data)
    
    # Récupération du dataframe des plus proches voisins
    nearest_neighbors_df = df.iloc[indices[0]]
    
    # S'assurer que la colonne 'SK_ID_CURR' est incluse dans la réponse
    nearest_neighbors_df = nearest_neighbors_df.reset_index(drop=True)
    
    return nearest_neighbors_df.to_dict(orient="records")


# Définition de la route pour récupérer les valeurs SHAP par client
@app.get("/shap_values/{id_client}")
async def get_shap_values_by_client(id_client: int = Path(..., title="Client ID")):
    # Filtre les données du client en question
    client_data = df[df['SK_ID_CURR'] == id_client]
    client_data = client_data[relevant_features]

    # Calcul des valeurs SHAP pour le client
    shap_values = explainer.shap_values(client_data)

    # Conversion des valeurs SHAP en un objet JSON
    shap_values_json = {
        "features": relevant_features,
        "values": shap_values[0].tolist()  
    }

    return shap_values_json



# Définition d'une route pour obtenir les valeurs Shap de l'ensemble des données
@app.get("/shap")
async def get_shap_values():
    # Définir la taille du sous-échantillon
    subsample_size = 1000

    # Sélectionner un sous-échantillon aléatoire du jeu de données
    subsample = df.sample(n=subsample_size, random_state=42)

    # Calculer les valeurs SHAP pour le sous-échantillon
    shap_values_all = explainer.shap_values(subsample[relevant_features])

    # Conversion des valeurs Shap en un objet JSON
    shap_values_json_all = {
        "features": relevant_features,
        "values": shap_values_all[0].tolist()
    }

    return shap_values_json_all




# Chargement des données anciennes et actuelles
old_data = pd.read_parquet("application_train.parquet")
current_data = pd.read_parquet("application_test.parquet")

# Trouver les colonnes communes aux deux jeux de données
common_columns = list(set(old_data.columns).intersection(current_data.columns))


# Filtrer les deux jeux de données pour ne conserver que les colonnes communes
old_data = old_data[common_columns].sample(frac=0.01, random_state=42)
current_data = current_data[common_columns].sample(frac=0.01, random_state=42)


# Définition de la route pour évaluer le data drift
@app.get("/data_drift")
async def evaluate_data_drift():
    # Assurez-vous que les deux jeux de données ont la même structure

    if set(old_data.columns) != set(current_data.columns):
        return {"error": "Les jeux de données n'ont pas la même structure."}

    # Sélectionnez les colonnes pertinentes pour l'analyse de data drift
    relevant_columns = [col for col in old_data.columns if col not in ignore_features]

    # Filtrer les données pour ne conserver que les colonnes pertinentes
    old_data_filtered = old_data[relevant_columns]
    current_data_filtered = current_data[relevant_columns]

    rapport = Report(metrics=[
    DataDriftPreset(),
    ])

    rapport.run(reference_data=old_data_filtered, current_data=current_data_filtered)
    

    return rapport.json()