# 🚀 Guide de démarrage rapide - Coach LoL

## En 3 minutes chrono ! ⏱️

### 1. Installation (1 minute)

```bash
# Installez les dépendances
pip install -r requirements.txt
```

### 2. Obtenez votre clé API Riot (1 minute)

1. Allez sur **https://developer.riotgames.com/**
2. Connectez-vous avec votre compte Riot
3. Cliquez sur **"REGENERATE API KEY"**
4. Copiez la clé (commence par `RGAPI-`)

### 3. Lancez l'application (30 secondes)

```bash
streamlit run app_streamlit.py
```

L'application s'ouvre dans votre navigateur !

### 4. Configuration dans l'app (30 secondes)

1. **Sidebar gauche** → Cliquez sur "API Riot Games"
2. Collez votre clé API
3. Sélectionnez votre région (EUW par défaut)
4. Entrez votre **nom d'invocateur** et votre **tag**
   - Exemple : `Faker` et `KR1`
5. Cliquez sur **"🔌 Se connecter"**

✅ **C'est tout ! Vous êtes prêt !**

---

## 🎮 Premiers pas

### Analysez votre historique
1. Allez dans l'onglet **"📊 Mon Historique"**
2. Ajustez le nombre de parties (20 par défaut)
3. Cliquez sur **"🔍 Analyser"**
4. Consultez vos stats !

### Analysez vos adversaires (avant une ranked)
1. **Lancez une partie** dans League of Legends
2. Pendant la sélection, allez dans l'onglet **"🎯 Analyse Pré-Game"**
3. Cliquez sur **"🔍 Analyser la partie en cours"**
4. Lisez les infos sur vos adversaires
5. Profit ! 🏆

---

## 🤖 Activer l'analyse IA (OPTIONNEL)

L'analyse IA vous donne des **conseils personnalisés** ultra précis.

### Obtenir une clé OpenAI (gratuit pour commencer)
1. Allez sur **https://platform.openai.com/api-keys**
2. Créez un compte
3. Obtenez votre clé API
4. **$5 de crédit gratuit** offert = ~3000 analyses !

💰 Une analyse coûte ~0.2 centime avec GPT-4o-mini

### Configurer dans l'app
1. **Sidebar** → "API LLM (Analyse IA)"
2. Collez votre clé
3. ✅ "Analyse IA activée" s'affiche

**Maintenant vos analyses incluent des conseils IA personnalisés !**

---

## 💡 Tips rapides

### Vous avez peu de temps ?
- Analysez seulement **5-10 parties** pour des résultats rapides
- L'analyse pré-game prend **15-30 secondes**

### Vous voulez progresser ?
- Analysez **20-50 parties** pour des stats précises
- Utilisez l'**analyse IA** pour des conseils ciblés
- Consultez vos **stats par champion** pour identifier vos mains

### En ranked ?
- Gardez l'app ouverte en **2ème écran**
- Analysez vos adversaires **à chaque partie**
- Lisez la **stratégie IA** pendant le chargement

---

## ❓ Problèmes ?

### "403 Forbidden" / "Compte introuvable"
→ Vérifiez votre **clé API** (valable 24h seulement)
→ Vérifiez votre **nom + tag** (ex: Faker#KR1)

### "Aucune partie en cours"
→ Normal si vous n'êtes pas en game
→ Lancez une partie dans LoL puis réessayez

### L'app ne démarre pas
```bash
# Réinstallez les dépendances
pip install -r requirements.txt --upgrade
```

---

## 📚 Pour aller plus loin

- **[README complet](README.md)** : Toutes les fonctionnalités
- **[Guide Streamlit](GUIDE_STREAMLIT.md)** : Guide détaillé de l'interface
- **[API Riot Docs](https://developer.riotgames.com/docs/lol)** : Documentation officielle

---

**Bon coaching et montez ce MMR ! 🚀🏆**
