# FinTechForesight - Assistant IA pour le Trading et les Cryptomonnaies

Un assistant intelligent avancé qui combine l'analyse technique, l'apprentissage automatique et l'intelligence artificielle pour fournir des insights précieux sur les marchés financiers et les cryptomonnaies.

## 🌟 Fonctionnalités principales :
- 🤖 Assistant IA conversationnel spécialisé en trading
- 📊 Analyse technique avancée (RSI, moyennes mobiles, etc.)
- 📈 Prédiction des prix avec modèles LSTM
- 💹 Génération de signaux de trading
- 📉 Visualisation des données en temps réel
- 🔍 Analyse fondamentale des actifs

## 🚀 Prérequis :
- Python 3.8 ou supérieur
- Une clé API valide pour Perplexity AI
- Les dépendances listées dans `.requirement`

## ⚙️ Installation :

1. Clonez ce dépôt :

```bash
git clone https://github.com/Wiminds/FinTechForesight.git
cd FinTechForesight
```

2. Installez les dépendances :

```bash
pip install -r .requirement
```

3. Configurez vos variables d'environnement :

   - Créez un fichier `.env` à la racine du projet
   - Copiez-y les clés nécessaires en suivant le modèle fourni dans `.env.example` :
     ```
     PERPLEXITY_API_KEY=VotreCléAPIIci
     SECRET_KEY=VotreCléSecrèteIci
     ```

4. Lancez l'assistant :

```bash
python main.py
```

## 📁 Structure du projet :
```
FinTechForesight/
├── app/
│   ├── __init__.py
│   └── .requirement
├── data/
│   └── (stockage des données et graphiques)
├── models/
│   └── models.py
├── utils/
│   └── utils.py
├── main.py
├── .requirement
├── LICENSE
└── README.md
```

## 💡 Fonctionnalités détaillées :

### Analyse de marché
- Analyse technique avec indicateurs (RSI, moyennes mobiles)
- Visualisation des tendances
- Génération de signaux de trading
- Analyse des volumes et de la liquidité

### Prédiction de prix
- Modèle LSTM pour la prédiction des prix
- Analyse des tendances à court et long terme
- Visualisation des prédictions
- Évaluation de la précision des prédictions

### Gestion des données
- Récupération des données boursières en temps réel
- Stockage et analyse des données historiques
- Génération de rapports et graphiques
- Export des données au format CSV

## 🛠️ Développement :

Pour contribuer au projet :

1. Créez une nouvelle branche :

```bash
git checkout -b feature/nom-de-la-fonctionnalite
```

2. Effectuez vos modifications et testez localement.

3. Soumettez une pull request sur GitHub.

## 📚 Dépendances :

Le projet utilise les bibliothèques suivantes :

- `requests` : Requêtes HTTP vers l'API Perplexity AI
- `python-dotenv` : Gestion des variables d'environnement
- `pandas` : Analyse de données
- `numpy` : Calculs mathématiques
- `matplotlib` : Visualisation des données
- `yfinance` : Accès aux données de marché
- `scikit-learn` : Apprentissage automatique
- `tensorflow` : Modèles de deep learning

## 🤝 Contribution :

Les contributions sont les bienvenues ! Si vous avez des idées ou trouvez des bugs, ouvrez une issue ou soumettez une pull request.

## 📄 Licence :

Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus d'informations.
