import unittest
from dashboard import app  

class TestDashApp(unittest.TestCase):

    def setUp(self):
        # Crée un client de test pour interagir avec l'application
        self.app = app.server.test_client()
        self.app.testing = True

    def test_index(self):
        # Vérifie si la page d'accueil renvoie un code 200 (succès)
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_client_dropdown(self):
        # Vérifie si la page avec le client-dropdown renvoie un code 200 (succès)
        response = self.app.get('/client-dropdown')
        self.assertEqual(response.status_code, 200)

    def test_variable_dropdown(self):
        # Vérifie si la page avec le variable-dropdown renvoie un code 200 (succès)
        response = self.app.get('/variable-dropdown')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()