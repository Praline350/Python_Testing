import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from server import Server  # Assure-toi que c'est le bon chemin pour importer ton serveur
from threading import Thread
import time

@pytest.fixture(scope="module")
def server():
    # Lancer le serveur Flask dans un thread séparé
    server = Server()
    thread = Thread(target=server.run, kwargs={'host': '127.0.0.1', 'port': 5000, 'debug': False})
    thread.daemon = True
    thread.start()
    time.sleep(1)  # Attendre un moment pour s'assurer que le serveur est bien lancé
    yield server
    # Arrêter le serveur après les tests (si nécessaire)
    
@pytest.fixture(scope="module")
def browser():
    service = FirefoxService(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.implicitly_wait(10)  # Attente implicite pour les éléments

    yield driver

    driver.quit()

def test_index_page(server, browser):
    browser.get('http://127.0.0.1:5000/')
    assert "Welcome to the GUDLFT Registration Portal!" in browser.page_source  # Assure-toi que c'est le bon titre de ta page

def test_full_functionality_flow(server, browser):
    # Étape 1: Connexion
    browser.get('http://127.0.0.1:5000/')
    
    # Entrer l'email et soumettre le formulaire
    email_input = browser.find_element(By.NAME, 'email')
    email_input.send_keys('kate@shelifts.co.uk')  # Utilise un email valide dans ta base de données
    
    submit_button = browser.find_element(By.XPATH, "//button[text()='Enter']")
    submit_button.click()
    
    # Vérifier que la connexion a réussi
    assert "Welcome, kate@shelifts.co.uk" in browser.page_source
    
    # Étape 2: Réservation (Booking)
    # Cliquer sur le lien pour réserver une place
    booking_link = browser.find_element(By.LINK_TEXT, f"Book Places")
    booking_link.click()
    
    # Remplir le formulaire de réservation
    places_input = browser.find_element(By.NAME, 'places')
    places_input.send_keys('1')
    
    book_button = browser.find_element(By.XPATH, "//button[text()='Book']")
    book_button.click()
    
    # Vérifier que la réservation a réussi
    assert "Great-booking complete!" in browser.page_source
    
    # Étape 3: Accéder au tableau des points (Points Board)
    points_board_link = browser.find_element(By.LINK_TEXT, "Points Board")
    points_board_link.click()
    
    # Vérifier que le tableau des points est affiché
    assert "Points Board" in browser.page_source
    assert "She Lifts" in browser.page_source  # Vérifier que le club apparaît dans le tableau des points
