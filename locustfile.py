from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    def on_start(self):
        """Cette méthode est appelée lorsque l'utilisateur virtuel commence à exécuter des tâches."""
        self.login()

    def login(self):
        """Cette tâche simule la connexion de l'utilisateur."""
        response = self.client.post("/showSummary", data={"email": "john@simplylift.co"})
        if response.status_code == 200:
            print("Login successful")
        else:
            print("Login failed")

    
    @task
    def index(self):
        self.client.get("/")  # Envoie une requête GET à la route /

    @task
    def purchasePlaces(self):
        """Cette tâche simule l'achat de places."""
        response = self.client.post("/purchasePlaces", data={
            'competition': 'Spring Festival', 
            'club': 'Simply Lift', 
            'places': '1'
        })
        if response.status_code == 200:
            print("Purchase successful")
        else:
            print("Purchase failed")

    @task
    def PointsBoard(self):
        self.client.get("/PointsBoard")

    @task
    def book(self):
        self.client.get("/book/Spring Festival/Iron Temple")


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]  # Associe les tâches définies dans UserBehavior
    wait_time = between(1, 5)  # Temps d'attente aléatoire entre 1 et 5 secondes entre les tâches