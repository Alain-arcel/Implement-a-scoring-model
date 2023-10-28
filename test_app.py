import dash
from dash.dependencies import Input, Output
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service  # Importez le module Service pour Edge

# Importez votre application Dash ici
from app import app

# Spécifiez le chemin vers le Microsoft Edge WebDriver que vous avez téléchargé
edge_driver_path = r"C:\Users\alain\Documents\edgedriver_win64\msedgedriver.exe"

# Configuration du driver Edge
edge_options = webdriver.EdgeOptions()
# Initialisation du driver Edge
driver = webdriver.Edge(executable_path=edge_driver_path, options=edge_options)

try:
    # Fonction pour attendre que l'élément Dash se charge
    def wait_for_element(driver, element_id):
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.ID, element_id)))
        return element

    # Fonction de test pour vérifier si le tableau de bord s'affiche correctement
    def test_dashboard():
        driver.get("https://ancient-cove-92425-1e6b4c347760.herokuapp.com/")  # Assurez-vous d'utiliser l'URL correcte

        # Attendez que l'élément de titre s'affiche
        title_element = wait_for_element(driver, "title")

        # Vérifiez le contenu du titre
        assert title_element.text == "Tableau de bord de gestion des risques"

        # Vous pouvez ajouter d'autres vérifications ici en fonction de vos besoins

finally:
    # Fermez le navigateur après les tests, même en cas d'exception
    driver.quit()
