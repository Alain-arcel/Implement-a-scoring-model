import pytest
from fastapi.testclient import TestClient
from API import app  

client = TestClient(app)

# Test de la route principale
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to my FastAPI API!"}

# Test de la route pour obtenir la liste des identifiants clients
def test_get_client_ids():
    response = client.get("/client_ids")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test de la route pour obtenir la liste des features
def test_get_features():
    response = client.get("/features")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test de la route de prédiction de crédit
def test_predict_credit():
    client_id = 369780
    response = client.get(f"/credit/{client_id}")
    assert response.status_code == 200
    assert "Prédiction" in response.json()
    assert "Probabilité" in response.json()
    assert "Conclusion" in response.json()

# Test de la route pour récupérer les données d'un client spécifique
def test_get_client_data():
    client_id = 369780
    response = client.get(f"/client_data/{client_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test de la route pour récupérer les données de l'ensemble des clients
def test_get_all_clients_data():
    response = client.get("/all_clients_data")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test de la route pour calculer les plus proches voisins du client_id
def test_get_nearest_neighbors():
    client_id = 369780
    response = client.get(f"/nearest_neighbors/{client_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test de la route pour récupérer les valeurs SHAP par client
def test_get_shap_values_by_client():
    client_id = 369780
    response = client.get(f"/shap_values/{client_id}")
    assert response.status_code == 200
    assert "features" in response.json()
    assert "values" in response.json()

# Test de la route pour obtenir les valeurs SHAP de l'ensemble des données
def test_get_shap_values():
    response = client.get("/shap")
    assert response.status_code == 200
    assert "features" in response.json()
    assert "values" in response.json()

# Test de la route pour évaluer le data drift
def test_evaluate_data_drift():
    response = client.get("/data_drift")
    assert response.status_code == 200
    assert "timestamp" in response.json()
    assert "data" in response.json()
    assert "metrics" in response.json()

if __name__ == "__main__":
    pytest.main()
