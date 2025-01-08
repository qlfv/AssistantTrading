import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStatusBar
from PyQt5.QtCore import QTimer
from ui import create_ui
from logic import check_balance, reload_accounts, get_solana_price

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Initialisation de l'application...")  # Debug
        self.setWindowTitle("Phantom Balance Checker")
        self.setGeometry(100, 100, 1000, 600)

        # Charger les comptes au démarrage
        print("Chargement des comptes...")
        self.account_selector_values = reload_accounts()
        print(f"Comptes chargés : {self.account_selector_values}")

        # Créer l'interface utilisateur et récupérer les éléments nécessaires
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        print("Création de l'interface utilisateur...")
        self.ui_elements = create_ui(
            self.central_widget,
            self.account_selector_values,
            check_balance,
            reload_accounts,
            get_solana_price
        )

        # Déballer les éléments retournés par create_ui
        (self.account_selector, self.result_label,
         self.notification_list, self.add_notification_func,
         self.remove_notification_func, self.update_price_func) = self.ui_elements

        # Barre de statut
        print("Ajout de la barre de statut...")
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Connecté au réseau Mainnet-Beta")
        self.setStatusBar(self.status_bar)

        # Démarrer le rafraîchissement automatique du solde et du prix SOL
        print("Démarrage du rafraîchissement automatique...")
        self.start_auto_refresh()
        self.start_price_refresh()

    def start_auto_refresh(self):
        """
        Rafraîchit le solde automatiquement toutes les 5 secondes.
        """
        print("Rafraîchissement automatique du solde...")
        check_balance(self.account_selector.currentText(), self.result_label,
                      self.add_notification_func, self.remove_notification_func)
        QTimer.singleShot(5000, self.start_auto_refresh)  # Relance après 5 secondes

    def start_price_refresh(self):
        """
        Rafraîchit le prix de Solana automatiquement toutes les 10 secondes.
        """
        print("Rafraîchissement automatique du prix SOL...")
        self.update_price_func()
        QTimer.singleShot(10000, self.start_price_refresh)  # Relance après 10 secondes


if __name__ == "__main__":
    print("Lancement de l'application...")
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    print("Application en cours d'exécution...")
    sys.exit(app.exec_())
