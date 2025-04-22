import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

class PricePredictor:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.model = None
    
    def prepare_data(self, data, lookback=60):
        """
        Prépare les données pour l'entraînement du modèle.
        
        Args:
            data (pandas.DataFrame): Les données boursières
            lookback (int): Le nombre de jours à utiliser pour la prédiction
        
        Returns:
            tuple: (X, y) les données préparées
        """
        # Normalisation des données
        scaled_data = self.scaler.fit_transform(data['Close'].values.reshape(-1, 1))
        
        X, y = [], []
        for i in range(len(scaled_data) - lookback):
            X.append(scaled_data[i:(i + lookback), 0])
            y.append(scaled_data[i + lookback, 0])
        
        return np.array(X), np.array(y)
    
    def build_lstm_model(self, input_shape):
        """
        Construit un modèle LSTM pour la prédiction de prix.
        
        Args:
            input_shape (tuple): La forme des données d'entrée
        
        Returns:
            tensorflow.keras.Model: Le modèle LSTM
        """
        model = Sequential([
            LSTM(units=50, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(units=50, return_sequences=False),
            Dropout(0.2),
            Dense(units=1)
        ])
        
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model
    
    def train(self, data, epochs=50, batch_size=32):
        """
        Entraîne le modèle sur les données fournies.
        
        Args:
            data (pandas.DataFrame): Les données boursières
            epochs (int): Le nombre d'époques d'entraînement
            batch_size (int): La taille du lot d'entraînement
        """
        X, y = self.prepare_data(data)
        X = X.reshape((X.shape[0], X.shape[1], 1))
        
        self.model = self.build_lstm_model((X.shape[1], 1))
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=1)
    
    def predict(self, data, days=30):
        """
        Prédit les prix futurs.
        
        Args:
            data (pandas.DataFrame): Les données boursières
            days (int): Le nombre de jours à prédire
        
        Returns:
            numpy.ndarray: Les prix prédits
        """
        if self.model is None:
            raise ValueError("Le modèle n'a pas été entraîné")
        
        last_sequence = self.scaler.transform(data['Close'].values[-60:].reshape(-1, 1))
        predictions = []
        
        for _ in range(days):
            pred = self.model.predict(last_sequence.reshape(1, -1, 1))
            predictions.append(pred[0, 0])
            last_sequence = np.append(last_sequence[1:], pred)
        
        return self.scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

class MarketAnalyzer:
    def __init__(self):
        self.regression_model = LinearRegression()
    
    def analyze_trend(self, data):
        """
        Analyse la tendance du marché.
        
        Args:
            data (pandas.DataFrame): Les données boursières
        
        Returns:
            dict: Les résultats de l'analyse
        """
        if data is None or data.empty:
            return None
        
        # Calcul des indicateurs
        returns = data['Close'].pct_change()
        volatility = returns.std() * np.sqrt(252)  # Volatilité annualisée
        trend = (data['Close'][-1] / data['Close'][0] - 1) * 100  # Variation en pourcentage
        
        # Analyse de la tendance
        X = np.arange(len(data)).reshape(-1, 1)
        y = data['Close'].values
        self.regression_model.fit(X, y)
        slope = self.regression_model.coef_[0]
        
        return {
            'trend': 'haussière' if slope > 0 else 'baissière',
            'volatility': volatility,
            'returns': trend,
            'slope': slope
        }
    
    def generate_signals(self, data):
        """
        Génère des signaux de trading basés sur l'analyse technique.
        
        Args:
            data (pandas.DataFrame): Les données boursières
        
        Returns:
            pandas.DataFrame: Les signaux de trading
        """
        if data is None or data.empty:
            return None
        
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0
        
        # Signaux basés sur les moyennes mobiles
        signals['ma20'] = data['Close'].rolling(window=20).mean()
        signals['ma50'] = data['Close'].rolling(window=50).mean()
        
        # Génération des signaux
        signals['signal'][20:] = np.where(signals['ma20'][20:] > signals['ma50'][20:], 1.0, 0.0)
        signals['positions'] = signals['signal'].diff()
        
        return signals 