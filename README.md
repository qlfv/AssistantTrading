# FinTechForesight 🚀

**FinTechForesight** est un assistant intelligent conçu pour fournir des analyses de marché, des stratégies de trading, et répondre aux questions sur les cryptomonnaies et les marchés boursiers.

## Fonctionnalités principales :
- 📉 Analyse des tendances de marché.
- 🤖 Interaction avec une IA experte en trading.
- 🔒 Gestion sécurisée des conversations.

## Prérequis :
- Python 3.8 ou supérieur
- Une clé API valide pour Perplexity AI.

## Installation :

1. Clonez ce dépôt :

```bash
git clone https://github.com/Wiminds/FinTechForesight.git
cd FinTechForesight
```

2. Installez les dépendances nécessaires :

```bash
pip install -r requirements.txt
```

3. Configurez vos variables d'environnement :

   - Créez un fichier `.env` à la racine du projet.
   - Copiez-y les clés nécessaires en suivant le modèle fourni dans `.env.example` :
     ```
     PERPLEXITY_API_KEY=VotreCléAPIIci
     SECRET_KEY=VotreCléSecrèteIci
     ```

4. Lancez le bot :

```bash
python main.py
```

---

## Développement :

Si vous souhaitez contribuer ou modifier le projet, voici quelques étapes utiles :

1. **Créer une nouvelle branche** :

```bash
git checkout -b feature/nom-de-la-fonctionnalite
```

2. **Effectuer vos modifications** et tester localement.

3. **Soumettre une pull request** sur GitHub.

---

## Dépendances :

Le projet utilise les bibliothèques suivantes :

- `requests` : Pour effectuer des requêtes HTTP vers l'API Perplexity AI.
- `python-dotenv` : Pour gérer les variables d'environnement.

Installez-les via `requirements.txt` :

```bash
pip install -r requirements.txt
```

---

## Contribution :

Les contributions sont ouvertes à tous ! Si vous avez des idées ou trouvez des bugs, ouvrez une issue ou soumettez une pull request.

---

## Licence :

Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus d'informations.
