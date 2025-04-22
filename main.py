import requests
import os
import logging
from dotenv import load_dotenv
from datetime import datetime
from utils.utils import get_stock_data, get_crypto_data, calculate_technical_indicators, plot_stock_data
from models.models import PricePredictor, MarketAnalyzer

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

load_dotenv()
api_key = os.getenv('PERPLEXITY_API_KEY')

class TradingBot:
    def __init__(self):
        self.secret_key = os.getenv('SECRET_KEY')
        self.conversation_history = []
        self.price_predictor = PricePredictor()
        self.market_analyzer = MarketAnalyzer()
        logging.info("Initialisation du TradingBot")

    def display_welcome_message(self):
        print("""
   ___ _      _____          _       ___                  _       _     _   
  / __(_)_ __/__   \\___  ___| |__   / _____  _ __ ___ ___(_) __ _| |__ | |_ 
 / _\\ | | '_ \\ / /\\/ _ \\/ __| '_ \\ / _\\/ _ \\| '__/ _ / __| |/ _` | '_ \\| __|
/ /   | | | | / / |  __| (__| | | / / | (_) | | |  __\\__ | | (_| | | | | |_ 
\\/    |_|_| |_\\/   \\___|\\___|_| |_\\/   \\___/|_|  \\___|___|_|\\__, |_| |_|\\__|
                                                            |___/           
        """)
        print("\n🚀 Bienvenue sur **FinTechForesight**, votre assistant intelligent pour le trading et les cryptomonnaies ! 🚀\n")
        print("📊 Posez vos questions sur les marchés boursiers, les cryptomonnaies ou demandez des analyses techniques.")
        print("💡 Tapez 'quitter' à tout moment pour mettre fin à la session.")
        print("____________________________________________________________________________________\n")
        logging.info("Message de bienvenue affiché")

    def analyze_asset(self, symbol, is_crypto=True):
        """Analyse un actif (crypto ou action) et génère un rapport."""
        try:
            # Récupération des données
            if is_crypto:
                data = get_crypto_data(symbol)
            else:
                data = get_stock_data(symbol)
            
            if data is None or data.empty:
                return "Impossible de récupérer les données pour cet actif."
            
            # Calcul des indicateurs techniques
            data = calculate_technical_indicators(data)
            
            # Analyse de la tendance
            trend_analysis = self.market_analyzer.analyze_trend(data)
            
            # Génération des signaux
            signals = self.market_analyzer.generate_signals(data)
            
            # Création du graphique
            plot_stock_data(data, symbol)
            
            # Entraînement du modèle de prédiction
            self.price_predictor.train(data)
            predictions = self.price_predictor.predict(data)
            
            # Construction du rapport
            report = f"""
Analyse de {symbol} :

📈 Tendance : {trend_analysis['trend']}
💰 Variation : {trend_analysis['returns']:.2f}%
📊 Volatilité : {trend_analysis['volatility']:.2f}%

Indicateurs techniques :
- RSI actuel : {data['RSI'].iloc[-1]:.2f}
- MA20 : {data['MA20'].iloc[-1]:.2f}
- MA50 : {data['MA50'].iloc[-1]:.2f}

Dernier signal : {'Achat' if signals['signal'].iloc[-1] == 1 else 'Vente'}

Un graphique d'analyse a été généré dans le dossier data/
"""
            return report
        except Exception as e:
            logging.error(f"Erreur lors de l'analyse de {symbol}: {str(e)}")
            return f"Une erreur s'est produite lors de l'analyse de {symbol}."

    def validate_user_input(self, user_message):
        """Valide l'entrée utilisateur."""
        if not user_message or len(user_message.strip()) == 0:
            logging.warning("Entrée utilisateur vide")
            return False
        return True

    def handle_chat(self, user_message):
        """Gérer la conversation avec l'IA."""
        if not self.validate_user_input(user_message):
            return "Veuillez entrer une question valide."

        # Vérification si c'est une demande d'analyse
        if user_message.lower() in ['btc', 'eth', 'xrp', 'ada', 'sol']:
            return self.analyze_asset(user_message.upper(), is_crypto=True)
        elif user_message.lower() in ['aapl', 'msft', 'googl', 'amzn', 'meta']:
            return self.analyze_asset(user_message.upper(), is_crypto=False)

        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        expert_context = """
        Vous êtes un expert en intelligence artificielle spécialisé dans les cryptomonnaies et les marchés boursiers. 
        Vous possédez une connaissance approfondie de la technologie blockchain, des stratégies de trading, de l'analyse de marché et des instruments financiers. 
        Votre expertise couvre toutes les cryptomonnaies, collections d'NFTs ainsi que les marchés boursiers traditionnels. 
        Vous pouvez fournir des avis sur les tendances de marché, l'analyse technique, l'analyse fondamentale et les stratégies d'investissement. 
        """

        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history = self.conversation_history[-5:]  # Conserver les 5 derniers messages

        payload = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [{"role": "system", "content": expert_context}] + self.conversation_history,
            "temperature": 0.2,
            "max_tokens": 1000,
        }

        try:
            logging.info(f"Envoi de la requête à l'API Perplexity: {user_message[:50]}...")
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            content = response.json()['choices'][0]['message']['content']
            self.conversation_history.append({"role": "assistant", "content": content})
            logging.info("Réponse reçue avec succès")
            return content
        except requests.exceptions.HTTPError as e:
            logging.error(f"Erreur HTTP: {str(e)}")
            if e.response.status_code == 400:
                return "Désolé, je n'ai pas pu comprendre votre demande. Pourriez-vous la reformuler?"
            else:
                return f"Une erreur s'est produite : {str(e)}"
        except requests.exceptions.RequestException as e:
            logging.error(f"Erreur de connexion: {str(e)}")
            return f"Erreur de connexion : {str(e)}"
        except Exception as e:
            logging.error(f"Erreur inattendue: {str(e)}")
            return "Une erreur inattendue s'est produite. Veuillez réessayer."

def main():
    try:
        bot = TradingBot()
        bot.display_welcome_message()

        while True:
            user_message = input("Votre question : ")
            if user_message.lower() == 'quitter':
                print("Merci d'avoir utilisé FinTechForesight. À bientôt !")
                logging.info("Session terminée par l'utilisateur")
                break
            response = bot.handle_chat(user_message)
            print("\nAssistant IA :", response)
            print("____________________________________________________________________________________\n")
    except KeyboardInterrupt:
        print("\n\nSession interrompue par l'utilisateur. Au revoir!")
        logging.info("Session interrompue par l'utilisateur")
    except Exception as e:
        logging.error(f"Erreur dans la fonction main: {str(e)}")
        print("Une erreur inattendue s'est produite. Veuillez réessayer.")

if __name__ == '__main__':
    main()