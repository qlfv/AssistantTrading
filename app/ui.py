from PyQt5.QtWidgets import QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

def create_ui(parent_widget, account_selector_values, check_balance_func, reload_accounts_func, get_price_func):
    layout = QVBoxLayout(parent_widget)
    layout.setAlignment(Qt.AlignTop)

    # Titre principal
    title_label = QLabel("Phantom Balance Checker")
    title_label.setStyleSheet("""
        font-size: 28px;
        font-weight: bold;
        color: #ECEFF4;
        margin-bottom: 20px;
    """)
    layout.addWidget(title_label)

    # Sélection du compte
    account_label = QLabel("Sélectionnez un compte :")
    account_label.setStyleSheet("font-size: 16px; color: #D8DEE9;")
    layout.addWidget(account_label)

    account_selector = QComboBox()
    account_selector.addItems(account_selector_values)
    account_selector.setStyleSheet("""
        QComboBox {
            background-color: #3B4252;
            color: #ECEFF4;
            border: 1px solid #D8DEE9;
            border-radius: 5px;
            padding: 5px;
        }
        QComboBox:hover {
            border-color: #81A1C1;
        }
        QComboBox::drop-down {
            border: none;
        }
    """)
    layout.addWidget(account_selector)

    # Résultat du solde
    result_label = QLabel("Solde : N/A")
    result_label.setStyleSheet("""
        font-size: 18px;
        font-weight: bold;
        color: #A3BE8C;
        margin-top: 10px;
        padding: 10px;
        background-color: #2E3440;
        border-radius: 5px;
    """)
    layout.addWidget(result_label)

    # Label pour afficher le prix du Solana
    price_label = QLabel("Prix SOL : Chargement...")
    price_label.setStyleSheet("""
        font-size: 18px;
        font-weight: bold;
        color: #88C0D0;
        margin-top: 10px;
        padding: 10px;
        background-color: #2E3440;
        border-radius: 5px;
    """)
    layout.addWidget(price_label)

    def update_price():
        price = get_price_func()
        if price is not None:
            price_label.setText(f"Prix SOL : {price:.2f} USD")
        else:
            price_label.setText("Erreur lors de la récupération du prix.")

    # Notifications (initialisation correcte ici)
    notifications = []

    def add_notification(message):
        notifications.append(message)
        QMessageBox.information(parent_widget, "Notification", message)

    def remove_notification_by_message(message):
        if message in notifications:
            notifications.remove(message)

    # Bouton pour vérifier le solde
    def on_check_balance():
        selected_account_text = account_selector.currentText()
        check_balance_func(selected_account_text, result_label,
                           add_notification, remove_notification_by_message)

    check_button = QPushButton("Vérifier le Solde")
    check_button.setStyleSheet("""
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
    check_button.clicked.connect(on_check_balance)
    layout.addWidget(check_button)

    # Bouton pour rafraîchir les comptes
    def on_reload_accounts():
        new_accounts = reload_accounts_func()
        account_selector.clear()
        account_selector.addItems(new_accounts)

    reload_button = QPushButton("Rafraîchir Comptes")
    reload_button.setStyleSheet("""
        QPushButton {
            background-color: #88C0D0;
            color: black;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px;
            margin-top: 10px;
        }
        QPushButton:hover {
            background-color: #8FBCBB;
        }
        QPushButton:pressed {
            background-color: #81A1C1;
        }
    """)
    reload_button.clicked.connect(on_reload_accounts)
    layout.addWidget(reload_button)

    # Bouton pour rafraîchir le prix du Solana
    refresh_price_button = QPushButton("Rafraîchir Prix SOL")
    refresh_price_button.setStyleSheet("""
        QPushButton {
            background-color: #88C0D0;
            color: black;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px;
            margin-top: 10px;
        }
        QPushButton:hover {
            background-color: #8FBCBB;
        }
        QPushButton:pressed {
            background-color: #81A1C1;
        }
    """)
    refresh_price_button.clicked.connect(update_price)
    layout.addWidget(refresh_price_button)

    return account_selector, result_label, notifications, add_notification, remove_notification_by_message, update_price
