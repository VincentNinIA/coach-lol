# 🎮 Coach LoL - Analyseur de performance League of Legends avec IA

Un assistant de coaching intelligent pour League of Legends qui analyse vos performances, votre historique de parties, et vous donne des conseils personnalisés en temps réel avec l'IA.

## ✨ Fonctionnalités

### 🤖 Analyse IA (NEW!)
- **Coach IA personnel** : Analyse intelligente par GPT-4o-mini (OpenAI)
- **Conseils personnalisés** : Adaptés à votre niveau et style de jeu
- **Analyse de matchup** : Stratégies spécifiques champion vs champion
- **Recommandations tactiques** : Plan de jeu détaillé pour chaque partie
- **💰 Très économique** : ~0.2 centime par analyse avec GPT-4o-mini

### 🖥️ Interface moderne (NEW!)
- **Application web Streamlit** : Interface intuitive et élégante
- **Visualisations interactives** : Graphiques Plotly dynamiques
- **Tableaux de données** : Statistiques triables et filtrables
- **Responsive design** : Fonctionne sur tous les écrans

### 📊 Analyse d'historique
- Statistiques détaillées sur vos X dernières parties
- KDA moyen, winrate, CS/min, vision score
- Analyse par champion avec winrate et performance
- Identification de vos rôles préférés
- **+ Analyse IA de vos points forts/faibles**

### 🎯 Coaching en temps réel
- **Surveillance automatique** : détecte quand vous lancez une partie
- **Analyse pré-game** : analyse complète de l'équipe adverse
- **Niveau de menace** : identifie les joueurs dangereux (🔴🟠🟡🟢)
- **Conseils stratégiques IA** : plan de jeu personnalisé

### 🏆 Statistiques par champion
- Performance détaillée sur chaque champion
- Winrate, KDA, nombre de parties
- Identifiez vos mains et vos points faibles
- Graphiques de performance

## 🚀 Installation

### 1. Prérequis
- Python 3.8 ou supérieur
- Un compte League of Legends
- Une clé API Riot Games (gratuite)

### 2. Installation des dépendances
```bash
pip install -r requirements.txt
```

Cela installera :
- `requests` - API Riot
- `streamlit` - Interface web
- `pandas` - Manipulation de données
- `plotly` - Visualisations
- `openai` - API OpenAI pour l'IA (GPT)

### 3. Configuration des APIs

#### Clé API Riot (OBLIGATOIRE)
1. Allez sur [https://developer.riotgames.com/](https://developer.riotgames.com/)
2. Connectez-vous avec votre compte Riot
3. Cliquez sur "REGENERATE API KEY"
4. Copiez votre clé (gratuite, valable 24h)

#### Clé API OpenAI (OPTIONNEL - pour l'IA)
1. Allez sur [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Créez un compte
3. Obtenez votre clé API
4. **$5 de crédit gratuit** = ~3000 analyses avec GPT-4o-mini !

📊 **[Voir les tarifs détaillés](TARIFS_OPENAI.md)** - Spoiler : c'est très économique !

#### Configuration

**Option A : Fichier .env (recommandé)**
```bash
cp .env.example .env
# Éditez .env avec vos clés
```

**Option B : Modifier config.py**
```python
# config.py
RIOT_API_KEY = 'RGAPI-VOTRE-CLE-ICI'
DEFAULT_REGION = 'EUW'
```

**Option C : Via l'interface**
Vous pouvez entrer les clés directement dans l'application.

## 📖 Utilisation

### Interface Streamlit (RECOMMANDÉ)
```bash
streamlit run app_streamlit.py
```

L'application s'ouvrira dans votre navigateur : `http://localhost:8501`

**📚 [Guide complet Streamlit](GUIDE_STREAMLIT.md)**

### Interface CLI (Alternative)
```bash
python coach_lol.py
```

### Menu principal
```
1. 🔑 Configurer l'API et se connecter
2. 📊 Analyser mon historique de parties
3. 🏆 Voir mes statistiques par champion
4. 🎯 Surveillance de partie (analyse pré-game)
5. 🔍 Analyser une partie en cours
```

### Exemples d'utilisation

#### 1. Première utilisation
```
1. Choisissez l'option 1 pour vous connecter
2. Entrez votre clé API (ou laissez vide si dans config.py)
3. Entrez votre région (EUW, NA, KR, etc.)
4. Entrez votre nom d'invocateur
5. Entrez votre tag (ex: EUW, 1234, etc.)
```

#### 2. Analyser votre historique
```
1. Choisissez l'option 2
2. Indiquez le nombre de parties (20 par défaut)
3. Consultez vos statistiques
4. Sauvegardez le rapport si besoin
```

#### 3. Mode surveillance (recommandé)
```
1. Choisissez l'option 4
2. Le programme surveille automatiquement
3. Lancez votre partie normalement
4. Dès que la partie démarre, l'analyse se lance !
5. Consultez les infos sur vos adversaires
```

#### 4. Analyser une partie en cours
```
1. Lancez votre partie
2. Pendant la sélection de champions, lancez le coach
3. Choisissez l'option 5
4. Obtenez l'analyse immédiatement
```

## 📊 Exemple de rapport

```
================================================================================
🎮 ANALYSE PRÉ-GAME - COACH LOL
================================================================================

Mode de jeu : CLASSIC

--------------------------------------------------------------------------------
👥 ÉQUIPE ADVERSE :
--------------------------------------------------------------------------------

🔹 Pseudo123
   Rang : DIAMOND II - 45 LP
   Record : 156W - 142L (52.3% WR)
   Niveau de menace : 🟠 ÉLEVÉ
   KDA moyen : 3.45
   Performance récente : 7W - 3L sur les 10 dernières parties
   Champions mains : Level 7 (234,567 pts), Level 7 (187,432 pts)

[...]

--------------------------------------------------------------------------------
⚠️  MENACES IDENTIFIÉES :
   • Pseudo123 (DIAMOND II - 45 LP) - 🟠 ÉLEVÉ - WR: 52.3%
   • TopLaner42 (DIAMOND I - 78 LP) - 🔴 TRÈS ÉLEVÉ - WR: 58.1%

💡 CONSEILS STRATÉGIQUES :
   • Communiquez avec votre équipe dès la phase de picks
   • Placez des wards défensifs si vous êtes contre des joueurs expérimentés
   • Adaptez votre style de jeu en fonction du niveau de vos adversaires
   • ⚠️  Plusieurs menaces détectées : jouez prudemment et attendez les erreurs
================================================================================
```

## 🔧 Configuration avancée

### Régions supportées
- **EUW** : Europe West
- **EUN** : Europe Nordic & East
- **NA** : North America
- **KR** : Korea
- **BR** : Brazil
- **JP** : Japan
- **LA1** : Latin America North
- **LA2** : Latin America South
- **OC** : Oceania
- **TR** : Turkey
- **RU** : Russia

### Modifier la région par défaut
```python
# config.py
DEFAULT_REGION = 'NA'  # Changez selon votre région
```

## ⚠️ Limitations

### Clé API de développement
- **Durée** : 24 heures
- **Rate limit** : 20 requêtes / seconde, 100 requêtes / 2 minutes
- **Gratuite** mais limitée

Pour une utilisation intensive, vous pouvez demander une clé API de production sur le portail développeur Riot.

### Délais d'analyse
- Analyse d'historique (20 parties) : ~30-60 secondes
- Analyse pré-game (5 adversaires) : ~15-30 secondes

## 🐛 Résolution de problèmes

### "403 Forbidden"
→ Votre clé API est invalide ou expirée. Régénérez-la sur le portail développeur.

### "429 Too Many Requests"
→ Vous avez dépassé le rate limit. Le programme attend automatiquement, mais évitez de lancer plusieurs analyses simultanément.

### "404 Not Found"
→ Le compte n'existe pas. Vérifiez votre nom d'invocateur et votre tag.

### "Aucune partie en cours"
→ Vous n'êtes pas en partie. Utilisez l'option 4 pour surveiller le démarrage.

## 🎯 Captures d'écran de l'interface Streamlit

### 📊 Analyse d'historique
![Analyse d'historique avec graphiques interactifs et analyse IA]

### 🎯 Analyse pré-game
![Détection de menace et conseils stratégiques]

### 🏆 Statistiques champions
![Tableaux et graphiques de performance par champion]

## 📚 Structure du projet

```
coach-lol/
├── app_streamlit.py      # 🌟 Application web Streamlit (NOUVEAU)
├── llm_coach.py          # 🤖 Module d'analyse IA avec Claude (NOUVEAU)
├── coach_lol.py          # Interface CLI alternative
├── riot_api.py           # Client API Riot Games
├── data_analyzer.py      # Analyse de données et statistiques
├── live_game_coach.py    # Analyse en temps réel pré-game
├── config.py             # Configuration (clés API, région)
├── requirements.txt      # Dépendances Python
├── .env.example          # Template de configuration
├── README.md            # Ce fichier
└── GUIDE_STREAMLIT.md   # Guide détaillé de l'interface web
```

## 🔐 Sécurité

- **Ne partagez jamais votre clé API**
- Ne commitez pas votre clé dans un repository public
- Utilisez des variables d'environnement pour la production
- La clé API de développement est limitée à votre compte

## 📝 Notes

### Riot ID (nom#tag)
Depuis 2023, Riot Games utilise un système de Riot ID (comme Discord).
Format : `NomDInvocateur#TAG`

Exemples :
- `Faker#KR1`
- `Caps#EUW`
- `NomJoueur#1234`

### Files d'attente (Queue IDs)
- 420 : Ranked Solo/Duo
- 440 : Ranked Flex
- 400 : Normal Draft
- 430 : Normal Blind
- 450 : ARAM

## 🤝 Contribution

Ce projet est un outil de coaching personnel. N'hésitez pas à l'adapter à vos besoins !

Améliorations possibles :
- Base de données de matchups
- Conseils spécifiques par champion
- Interface graphique (GUI)
- Analyse post-game automatique
- Tracking de progression sur plusieurs semaines
- Intégration avec Discord

## 📜 Licence

Ce projet utilise l'API Riot Games.
Respectez les [Terms of Service](https://developer.riotgames.com/terms) de Riot Games.

## 🔗 Liens utiles

- [Documentation API Riot](https://developer.riotgames.com/docs/lol)
- [Portail développeur](https://developer.riotgames.com/)
- [Community Discord](https://discord.gg/riotgamesdevrel)
- [Data Dragon (assets)](https://developer.riotgames.com/docs/lol#data-dragon)

---

**Bonne chance sur la Faille de l'invocateur ! 🏆**
