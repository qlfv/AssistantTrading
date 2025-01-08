import os
import base58
import requests
from dotenv import load_dotenv
from solana.rpc.api import Client
from solders.keypair import Keypair  # type: ignore

load_dotenv()

# Configuration du client Solana (Mainnet)
client = Client("https://api.mainnet-beta.solana.com")


def reload_accounts():
    """
    Recharge les comptes depuis le fichier .env.
    
    Returns:
        list: Liste des comptes disponibles sous forme de chaînes.
    """
    accounts = []
    for key in os.environ.keys():
        if key.startswith("ACCOUNT_"):
            private_key_base58 = os.getenv(key)
            try:
                private_key_bytes = base58.b58decode(private_key_base58)
                public_key = Keypair.from_bytes(private_key_bytes).pubkey()
                accounts.append(f"{key} ({public_key})")
            except ValueError:
                print(f"Clé invalide détectée pour {key}. Veuillez vérifier votre fichier .env.")
    return accounts


def check_balance(selected_account_text, result_label, add_notification_func, remove_notification_func):
    """
    Vérifie le solde du compte sélectionné.
    
    Args:
        selected_account_text (str): Texte du compte sélectionné.
        result_label (QLabel): Label où afficher le solde.
        add_notification_func (callable): Fonction pour ajouter une notification.
        remove_notification_func (callable): Fonction pour supprimer une notification spécifique.
    """
    # Supprimer les notifications "Veuillez sélectionner un compte" existantes
    remove_notification_func("Veuillez sélectionner un compte")

    if not selected_account_text:
        add_notification_func("Veuillez sélectionner un compte.")
        return

    try:
        # Extraire la clé privée de .env
        account_key = selected_account_text.split()[0]  # Obtenir la clé avant l'espace
        private_key_base58 = os.getenv(account_key)
        
        if not private_key_base58:
            raise ValueError(f"Clé privée introuvable pour {account_key}")

        private_key_bytes = base58.b58decode(private_key_base58)
        public_key = Keypair.from_bytes(private_key_bytes).pubkey()

        # Appel API pour obtenir le solde
        balance_response = client.get_balance(public_key)

        # Accéder à la valeur du solde via l'attribut `value`
        balance_lamports = balance_response.value
        
        if balance_lamports is None:
            add_notification_func(f"Erreur dans la réponse : {balance_response}")
            return

        # Affichage du solde en SOL (1 SOL = 10^9 lamports)
        result_label.setText(f"Solde : {balance_lamports / 10**9:.2f} SOL")

    except Exception as e:
        add_notification_func(f"Erreur : {e}")


def get_solana_price():
    """
    Récupère le prix actuel de Solana en USD à partir de l'API CoinGecko.
    
    Returns:
        float: Le prix de Solana en USD, ou None si une erreur survient.
    """
    url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['solana']['usd']
        else:
            print(f"Erreur API: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erreur lors de la récupération du prix : {e}")
        return None