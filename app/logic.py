import os
import base58
import requests
from dotenv import load_dotenv
from solana.rpc.api import Client
from solders.keypair import Keypair  # type: ignore
from bs4 import BeautifulSoup

load_dotenv()

# Configuration du client Solana
SOLANA_ENDPOINT = os.getenv("SOLANA_ENDPOINT", "https://api.mainnet-beta.solana.com")
client = Client(SOLANA_ENDPOINT)

# Charger la clé privée depuis .env avec validation
private_key_base58 = os.getenv("PRIVATE_KEY")

if not private_key_base58:
    raise ValueError("La clé privée (PRIVATE_KEY) n'est pas définie dans le fichier .env.")

try:
    private_key_bytes = base58.b58decode(private_key_base58)
    keypair = Keypair.from_bytes(private_key_bytes)
    public_key = keypair.pubkey()
except Exception as e:
    raise ValueError(f"Erreur lors du décodage de la clé privée : {e}")


def check_connection():
    """
    Vérifie si la connexion au compte Phantom est réussie.
    """
    try:
        balance_response = client.get_balance(public_key)
        if balance_response.value is not None:
            return True
        else:
            return False
    except Exception as e:
        print(f"Erreur lors de la vérification de la connexion : {e}")
        return False


def get_balance():
    """
    Récupère le solde du portefeuille Phantom en SOL.
    """
    try:
        balance_response = client.get_balance(public_key)
        balance_lamports = balance_response.value
        return balance_lamports / 10**9  # Convertir les lamports en SOL
    except Exception as e:
        print(f"Erreur lors de la récupération du solde : {e}")
        return None


def get_solana_price_from_coinmarketcap():
    """
    Récupère le prix actuel de Solana en USD via l'API CoinMarketCap.
    """
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": os.getenv("COINMARKETCAP_API_KEY"),
    }
    parameters = {
        "symbol": "SOL",
        "convert": "USD"
    }
    
    try:
        response = requests.get(url, headers=headers, params=parameters)
        response.raise_for_status()
        data = response.json()
        return data["data"]["SOL"]["quote"]["USD"]["price"]
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération du prix : {e}")
        return None


def execute_trade(input_token, output_token, amount):
    """
    Exécute un swap via l'API Jupiter.
    
    Args:
        input_token (str): Mint du token d'entrée (ex: "SOL").
        output_token (str): Mint du token de sortie (ex: "USDC").
        amount (float): Montant à échanger.
    """
    url = f"https://quote-api.jup.ag/v4/swap"
    payload = {
        "inputMint": input_token,
        "outputMint": output_token,
        "amount": int(amount * 10**9),  # Convertir SOL en lamports
        "slippage": 1,  # Tolérance au slippage (1%)
        "userPublicKey": str(public_key)
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"Trade exécuté avec succès : {data}")
            return data["transaction"]
        else:
            print(f"Erreur lors de l'exécution du trade : {response.status_code}")
            return None
    except Exception as e:
        print(f"Erreur lors de l'exécution du trade : {e}")
        return None


def get_solana_price_scraper():
    """
    Récupère le prix actuel de Solana en USD en scrappant CoinMarketCap.
    """
    url = "https://coinmarketcap.com/currencies/solana/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Rechercher l'élément contenant le prix (peut varier selon la structure HTML)
        price_tag = soup.find("div", class_="priceValue")
        
        if price_tag:
            price_text = price_tag.text.replace("$", "").replace(",", "")
            return float(price_text)
        else:
            print("Impossible de trouver le prix sur la page.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du scraping : {e}")
        return None

def check_connection():
    """
    Vérifie si la connexion au compte Phantom est réussie.
    """
    try:
        balance_response = client.get_balance(public_key)
        if balance_response.value is not None:
            return True
        else:
            return False
    except Exception as e:
        print(f"Erreur lors de la vérification de la connexion : {e}")
        return False
