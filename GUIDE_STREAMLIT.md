# 🎮 Guide d'utilisation - Coach LoL avec Interface Streamlit

## 🚀 Installation et Configuration

### 1. Installation des dépendances

```bash
pip install -r requirements.txt
```

Cela installera :
- `requests` : Pour les appels API Riot
- `streamlit` : Framework de l'interface web
- `pandas` : Manipulation de données
- `plotly` : Visualisations interactives
- `anthropic` : API Claude pour l'analyse IA

### 2. Configuration des clés API avec Streamlit Secrets

**Méthode recommandée pour Streamlit** : Utiliser le fichier `secrets.toml`

```bash
# Copiez le fichier template
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Éditez le fichier `.streamlit/secrets.toml` :
```toml
RIOT_API_KEY = "RGAPI-votre-cle-ici"
OPENAI_API_KEY = "sk-votre-cle-ici"
DEFAULT_REGION = "EUW"
```

**Avantages** :
- ✅ Pas besoin de saisir les clés à chaque démarrage
- ✅ Sécurisé (le fichier est automatiquement gitignored)
- ✅ Configuration centralisée

### 3. Obtenir les clés API

#### Clé API Riot (OBLIGATOIRE)
1. Allez sur [https://developer.riotgames.com/](https://developer.riotgames.com/)
2. Connectez-vous avec votre compte Riot
3. Cliquez sur "REGENERATE API KEY"
4. Copiez votre clé (valable 24h)
5. Collez-la dans `.streamlit/secrets.toml`
6. **Gratuit et sans limitation majeure**

#### Clé API OpenAI (OPTIONNEL - pour l'IA)
1. Allez sur [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Créez un compte
3. Obtenez votre clé API
4. Collez-la dans `.streamlit/secrets.toml`
5. **$5 de crédit gratuit** = ~3000 analyses !

## 🎯 Lancement de l'application

### Interface Streamlit (recommandé)
```bash
streamlit run app_streamlit.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse :
`http://localhost:8501`

### Interface CLI (alternative)
```bash
python coach_lol.py
```

## 📖 Guide d'utilisation de l'interface Streamlit

### 🔧 Configuration initiale (Sidebar)

1. **Vérification des APIs**
   - La sidebar affiche le statut de vos clés API
   - ✓ API Riot configurée (vert) = OK
   - ❌ API Riot non configurée (rouge) = Éditez `.streamlit/secrets.toml`
   - ⚠️ Analyse IA désactivée (orange) = Optionnel

2. **Connexion**
   - Entrez votre nom d'invocateur
   - Entrez votre tag (ex: EUW, 1234, etc.)
   - Cliquez sur "🔌 Se connecter"

**Note** : Les clés API sont maintenant gérées via `.streamlit/secrets.toml`, vous n'avez plus à les saisir dans l'interface !

### 📊 Onglet 1 : Mon Historique

**Fonctionnalités :**
- Analyse de vos X dernières parties (5-50)
- Statistiques détaillées : winrate, KDA, CS/min, vision score
- Graphiques interactifs :
  - Répartition victoires/défaites
  - Top 5 champions joués
- **Analyse IA** : Conseils personnalisés basés sur vos performances

**Comment utiliser :**
1. Ajustez le slider pour choisir le nombre de parties
2. Cliquez sur "🔍 Analyser"
3. Attendez le chargement (30-60 secondes pour 20 parties)
4. Consultez les statistiques et graphiques
5. Lisez l'analyse IA en bas de page

**Ce que vous obtenez :**
- ✅ Points forts identifiés
- ⚠️ Points à améliorer
- 💡 Conseils prioritaires actionnables
- 🎮 Recommandations de champions

### 🎯 Onglet 2 : Analyse Pré-Game

**Fonctionnalités :**
- Détection automatique de partie en cours
- Analyse complète de l'équipe adverse :
  - Rang et LP de chaque adversaire
  - Winrate et record récent
  - KDA moyen
  - Niveau de menace (🔴 Très élevé, 🟠 Élevé, 🟡 Moyen, 🟢 Faible)
- **Analyse stratégique IA** : Plan de jeu personnalisé

**Comment utiliser :**
1. Lancez une partie dans League of Legends
2. Pendant la sélection de champions, revenez sur l'app
3. Cliquez sur "🔍 Analyser la partie en cours"
4. Attendez l'analyse (15-30 secondes)
5. Consultez les infos sur chaque adversaire
6. Lisez l'analyse stratégique IA

**Ce que vous obtenez :**
- 🎯 Évaluation de la menace par joueur
- 💥 Points faibles à exploiter
- 📋 Stratégie de game recommandée
- 💡 Conseils individuels pour la partie

### 🏆 Onglet 3 : Statistiques Champions

**Fonctionnalités :**
- Vue d'ensemble de tous vos champions
- Tableau interactif avec :
  - Nombre de parties
  - Winrate
  - KDA moyen
  - K/D/A détaillés
- Graphiques :
  - Winrate par champion
  - KDA par champion

**Comment utiliser :**
1. Choisissez le nombre de parties à analyser (10-100)
2. Cliquez sur "📊 Analyser mes champions"
3. Explorez le tableau (triable par colonne)
4. Identifiez vos mains et vos points faibles

**Ce que vous obtenez :**
- 📈 Classement de vos champions par performance
- 🎯 Identification de vos mains
- 📊 Visualisation de vos forces

### 💡 Onglet 4 : Conseils IA

**Fonctionnalités :**
- **Analyse de matchup** : Conseils spécifiques pour un 1v1
- **Conseil rapide** : Réponse à une question spécifique
- Conseils personnalisés par l'IA

**Comment utiliser :**

#### Analyse de matchup
1. Sélectionnez "Analyse de matchup"
2. Entrez votre champion (ex: Yasuo)
3. Entrez le champion adverse (ex: Zed)
4. Entrez votre rang (ex: Gold II)
5. Cliquez sur "🧠 Analyser le matchup"

**Ce que vous obtenez :**
- Vue d'ensemble du matchup
- Conseils pour la phase de lane
- Power spikes (quand vous êtes fort/faible)
- Combos à éviter et opportunités
- Recommandations de build et runes

#### Conseil rapide
1. Sélectionnez "Conseil rapide"
2. Décrivez votre situation
3. Obtenez un conseil ciblé instantanément

## 🎨 Fonctionnalités avancées

### Visualisations interactives
- **Hover** : Survolez les graphiques pour voir les détails
- **Zoom** : Cliquez et glissez pour zoomer
- **Filtrage** : Cliquez sur la légende pour masquer/afficher des données

### Export de données
- Les tableaux peuvent être copiés (clic droit)
- Les graphiques peuvent être exportés en image (icône caméra)

### Personnalisation
- Thème clair/sombre : Menu hamburger > Settings > Theme
- Plein écran : Menu hamburger > Settings > Wide mode

## 🔧 Dépannage

### "Erreur 403 Forbidden"
→ Votre clé API Riot est invalide ou expirée
- Régénérez-la sur le portail développeur
- Mettez à jour `.streamlit/secrets.toml` avec la nouvelle clé
- Relancez l'application

### "Aucune partie en cours"
→ Vous n'êtes pas actuellement en partie
- Lancez une partie dans LoL
- Attendez d'être en sélection de champions
- Réessayez

### "Analyse IA désactivée"
→ Vous n'avez pas configuré la clé OpenAI
- C'est normal ! L'analyse IA est optionnelle
- L'application fonctionne sans, mais sans les conseils IA
- Ajoutez `OPENAI_API_KEY` dans `.streamlit/secrets.toml` si vous voulez l'analyse intelligente
- Relancez l'application après modification

### "Rate limit dépassé"
→ Trop de requêtes API en peu de temps
- Attendez quelques secondes
- Évitez de lancer plusieurs analyses simultanément
- L'application gère automatiquement les limites

### L'application ne démarre pas
```bash
# Vérifiez l'installation des dépendances
pip install -r requirements.txt --upgrade

# Vérifiez la version de Python (3.8+)
python --version

# Relancez avec des logs détaillés
streamlit run app_streamlit.py --logger.level=debug
```

## 📊 Performances et optimisations

### Temps de chargement typiques
- Connexion au compte : 1-2 secondes
- Analyse de 20 parties : 30-60 secondes
- Analyse pré-game : 15-30 secondes
- Analyse IA : 5-10 secondes

### Conseils pour optimiser
- Commencez avec peu de parties (10-20)
- Augmentez progressivement si nécessaire
- L'analyse IA est cachée jusqu'à utilisation
- Les données sont mises en cache pendant la session

## 🎯 Cas d'usage recommandés

### 1. Analyse après session de jeu
1. Jouez 5-10 parties
2. Ouvrez l'app
3. Analysez votre historique
4. Consultez l'analyse IA
5. Identifiez vos erreurs récurrentes

### 2. Préparation avant une partie ranked
1. Ouvrez l'app en deuxième écran
2. Lancez votre ranked
3. Dès la sélection : analysez l'équipe adverse
4. Ajustez votre pick/ban en fonction
5. Lisez la stratégie IA

### 3. Amélioration sur un champion
1. Filtrez vos parties sur ce champion
2. Étudiez votre winrate et KDA
3. Comparez avec vos autres champions
4. Demandez un conseil IA spécifique

### 4. Analyse de matchup avant ranked
1. Allez dans "Conseils IA"
2. Analysez le matchup que vous craignez
3. Notez les conseils clés
4. Appliquez en game !

## 🔐 Sécurité et confidentialité

- ✅ Vos clés API restent locales (jamais envoyées ailleurs que vers Riot/Anthropic)
- ✅ Aucune donnée personnelle stockée
- ✅ Les analyses IA sont privées
- ✅ Code open source et auditable

## 🚀 Prochaines étapes

Après avoir pris en main l'application :
1. Testez toutes les fonctionnalités
2. Analysez plusieurs sessions de jeu
3. Utilisez les conseils IA régulièrement
4. Adaptez votre gameplay en fonction
5. Progressez sur la faille ! 🏆

## 📞 Support

- Problème avec l'API Riot : [developer.riotgames.com](https://developer.riotgames.com/)
- Problème avec Anthropic : [docs.anthropic.com](https://docs.anthropic.com/)
- Bugs de l'app : Consultez le code source et les logs

---

**Bon coaching et bonne montée en ranked ! 🎮🏆**
