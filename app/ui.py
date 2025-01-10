from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class PriceGraph(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)
        
        self.setParent(parent)
        
        self.ax.set_title("Évolution du Prix de Solana (USD)")
        self.ax.set_xlabel("Temps")
        self.ax.set_ylabel("Prix (USD)")
        
        self.data = []

    def update_graph(self, new_price):
        self.data.append(new_price)
        
        if len(self.data) > 20:  # Limiter à 20 points pour éviter un graphique trop chargé
            self.data.pop(0)
        
        self.ax.clear()
        
        self.ax.plot(self.data, marker="o", color="#88C0D0")
        
        self.ax.set_title("Évolution du Prix de Solana (USD)")
        
        self.draw()

def create_ui(parent_widget, check_balance_func, get_price_func, check_connection_func):
    """
    Crée l'interface utilisateur principale.
    
    Args:
        parent_widget: Le widget parent.
        check_balance_func: Fonction pour récupérer le solde.
        get_price_func: Fonction pour récupérer le prix de Solana.
        check_connection_func: Fonction pour vérifier la connexion au compte Phantom.
    """
    layout = QVBoxLayout(parent_widget)
    layout.setAlignment(Qt.AlignTop)

    # Graphique pour afficher l'évolution du prix
    price_graph = PriceGraph(parent_widget)
    layout.addWidget(price_graph)

    # Résultat du solde
    result_label = QLabel("Solde : Chargement...")
    result_label.setStyleSheet("""
        font-size: 18px;
        font-weight: bold;
        color: #A3BE8C;
    """)
    layout.addWidget(result_label)

    # Label pour afficher le prix actuel de Solana
    price_label = QLabel("Prix SOL : Chargement...")
    price_label.setStyleSheet("""
        font-size: 18px;
        font-weight: bold;
        color: #88C0D0;
    """)
    layout.addWidget(price_label)

    # Label pour afficher l'état de connexion au compte Phantom
    connection_status_label = QLabel("Connexion : Vérification en cours...")
    connection_status_label.setStyleSheet("""
        font-size: 16px;
        font-weight: bold;
        color: #FFD700;  # Jaune pour indiquer une vérification en cours
    """)
    layout.addWidget(connection_status_label)

    def update_data():
        """
        Met à jour le solde et le prix SOL en temps réel.
        """
        balance = check_balance_func()
        price = get_price_func()
        
        if balance is not None:
            result_label.setText(f"Solde : {balance:.2f} SOL")
        
        if price is not None:
            price_label.setText(f"Prix SOL : {price:.2f} USD")
            price_graph.update_graph(price)

        # Vérification de la connexion au compte Phantom
        is_connected = check_connection_func()
        if is_connected:
            connection_status_label.setText("Connexion : Réussie ✅")
            connection_status_label.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                color: #32CD32;  # Vert pour indiquer une connexion réussie
            """)
        else:
            connection_status_label.setText("Connexion : Échouée ❌")
            connection_status_label.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                color: #FF4500;  # Rouge pour indiquer une erreur de connexion
            """)

    # Rafraîchissement automatique avec QTimer
    timer = QTimer(parent_widget)
    timer.timeout.connect(update_data)  # Appelle la fonction update_data périodiquement
    timer.start(5000)  # Rafraîchit toutes les 5 secondes

    # Bouton pour rafraîchir manuellement les données
    refresh_button = QPushButton("Rafraîchir Manuellement")
    refresh_button.setStyleSheet("""
        QPushButton {
            background-color: #5E81AC;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px;
            margin-top: 15px;
        }
        QPushButton:hover {
            background-color: #81A1C1;
        }
        QPushButton:pressed {
            background-color: #4C566A;
        }
    """)
    
    refresh_button.clicked.connect(update_data)
    
    layout.addWidget(refresh_button)
