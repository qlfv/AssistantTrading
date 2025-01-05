import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('PERPLEXITY_API_KEY')

class TradingBot:
    def __init__(self):
        self.secret_key = os.getenv('SECRET_KEY')
        self.conversation_history = []

    def display_welcome_message(self):
        print("""
   ___ _      _____          _       ___                  _       _     _   
  / __(_)_ __/__   \___  ___| |__   / _____  _ __ ___ ___(_) __ _| |__ | |_ 
 / _\ | | '_ \ / /\/ _ \/ __| '_ \ / _\/ _ \| '__/ _ / __| |/ _` | '_ \| __|
/ /   | | | | / / |  __| (__| | | / / | (_) | | |  __\__ | | (_| | | | | |_ 
\/    |_|_| |_\/   \___|\___|_| |_\/   \___/|_|  \___|___|_|\__, |_| |_|\__|
                                                            |___/           
        """)
        print("\n🚀 Bienvenue sur **FinTechForesight**, votre assistant intelligent pour le trading et les cryptomonnaies ! 🚀\n")
        print("📊 Posez vos questions sur les marchés boursiers, les cryptomonnaies ou demandez des analyses techniques.")
        print("💡 Tapez 'quitter' à tout moment pour mettre fin à la session.")
        print("____________________________________________________________________________________\n")

    def handle_chat(self, user_message):
        """Gérer la conversation avec l'IA."""
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
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            content = response.json()['choices'][0]['message']['content']
            self.conversation_history.append({"role": "assistant", "content": content})
            return content
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                return "Désolé, je n'ai pas pu comprendre votre demande. Pourriez-vous la reformuler?"
            else:
                return f"Une erreur s'est produite : {str(e)}"
        except requests.exceptions.RequestException as e:
            return f"Erreur de connexion : {str(e)}"

def main():
    bot = TradingBot()
    bot.display_welcome_message()

    while True:
        user_message = input("Votre question : ")
        if user_message.lower() == 'quitter':
            print("Merci d'avoir utilisé FinTechForesight. À bientôt !")
            break
        response = bot.handle_chat(user_message)
        print("\nAssistant IA :", response)
        print("____________________________________________________________________________________\n")

if __name__ == '__main__':
    main()