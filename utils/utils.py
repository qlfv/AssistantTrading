import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_stock_data(symbol, period='1y'):
    """
    Récupère les données boursières pour un symbole donné.
    
    Args:
        symbol (str): Le symbole de l'action
        period (str): La période de données à récupérer (par défaut: 1 an)
    
    Returns:
        pandas.DataFrame: Les données boursières
    """
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period=period)
        return data
    except Exception as e:
        print(f"Erreur lors de la récupération des données pour {symbol}: {str(e)}")
        return None

def calculate_technical_indicators(data):
    """
    Calcule les indicateurs techniques pour les données boursières.
    
    Args:
        data (pandas.DataFrame): Les données boursières
    
    Returns:
        pandas.DataFrame: Les données avec les indicateurs techniques
    """
    if data is None or data.empty:
        return None
    
    # Calcul des moyennes mobiles
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()
    
    # Calcul du RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    return data

def plot_stock_data(data, symbol):
    """
    Crée un graphique des données boursières avec les indicateurs techniques.
    
    Args:
        data (pandas.DataFrame): Les données boursières
        symbol (str): Le symbole de l'action
    """
    if data is None or data.empty:
        return
    
    plt.figure(figsize=(12, 6))
    
    # Tracé du prix de clôture
    plt.plot(data.index, data['Close'], label='Prix de clôture', color='blue')
    
    # Tracé des moyennes mobiles
    plt.plot(data.index, data['MA20'], label='MA20', color='orange')
    plt.plot(data.index, data['MA50'], label='MA50', color='red')
    
    plt.title(f'Analyse technique de {symbol}')
    plt.xlabel('Date')
    plt.ylabel('Prix')
    plt.legend()
    plt.grid(True)
    
    # Sauvegarde du graphique
    plt.savefig(f'data/{symbol}_analysis.png')
    plt.close()

def get_crypto_data(symbol, period='1y'):
    """
    Récupère les données de cryptomonnaie pour un symbole donné.
    
    Args:
        symbol (str): Le symbole de la cryptomonnaie
        period (str): La période de données à récupérer (par défaut: 1 an)
    
    Returns:
        pandas.DataFrame: Les données de cryptomonnaie
    """
    try:
        crypto = yf.Ticker(f"{symbol}-USD")
        data = crypto.history(period=period)
        return data
    except Exception as e:
        print(f"Erreur lors de la récupération des données pour {symbol}: {str(e)}")
        return None 