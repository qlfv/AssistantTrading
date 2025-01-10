import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from ui import create_ui
from logic import get_balance, get_solana_price_from_coinmarketcap, check_connection

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Phantom Trading Bot")
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Appel de create_ui avec tous les arguments requis
        create_ui(
            self.central_widget,
            get_balance,
            get_solana_price_from_coinmarketcap,
            check_connection  # Ajout de la fonction manquante
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    main_app = MainApp()
    
    main_app.show()
    
    sys.exit(app.exec_())
