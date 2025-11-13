# 🌐 Déploiement sur Streamlit Cloud

## Configuration des secrets sur Streamlit Cloud

Lorsque vous déployez votre application sur Streamlit Cloud, vous devez configurer vos secrets (clés API) de manière sécurisée.

### 1. Déployez votre application

1. Allez sur [share.streamlit.io](https://share.streamlit.io)
2. Connectez-vous avec votre compte GitHub
3. Cliquez sur **"New app"**
4. Sélectionnez votre repository : `coach-lol`
5. Branch : `main`
6. Main file path : `app_streamlit.py`

### 2. Configurez les secrets

1. Dans l'interface de déploiement, cliquez sur **"Advanced settings"**
2. Allez dans l'onglet **"Secrets"**
3. Copiez-collez le contenu suivant (avec vos vraies clés) :

```toml
# Clé API Riot Games (obligatoire)
RIOT_API_KEY = "RGAPI-votre-cle-ici"

# Clé API OpenAI pour GPT (optionnel - pour l'analyse IA)
OPENAI_API_KEY = "sk-votre-cle-ici"

# Configuration par défaut
DEFAULT_REGION = "EUW"
```

4. Cliquez sur **"Save"**
5. Cliquez sur **"Deploy"**

### 3. C'est tout !

Votre application sera déployée et accessible publiquement via une URL du type :
`https://votre-app-coach-lol.streamlit.app`

## ⚠️ Important

### Limites de la clé API Riot

- Les clés API de développement sont valables **24h seulement**
- Vous devrez les régénérer chaque jour sur [developer.riotgames.com](https://developer.riotgames.com/)
- Pour une application en production, demandez une clé API de production

### Pour renouveler la clé API sur Streamlit Cloud

1. Allez sur votre application déployée
2. Cliquez sur **"Settings"** (roue dentée en bas à droite)
3. Allez dans **"Secrets"**
4. Mettez à jour `RIOT_API_KEY` avec la nouvelle clé
5. Sauvegardez

L'application redémarrera automatiquement avec la nouvelle clé.

## 🔐 Sécurité

- ✅ Les secrets ne sont **jamais** exposés publiquement
- ✅ Ils sont chiffrés par Streamlit Cloud
- ✅ Seule votre application y a accès
- ✅ Ne partagez jamais vos clés API publiquement

## 📝 Notes

- Streamlit Cloud offre un tier gratuit pour les applications publiques
- Votre application redémarre automatiquement en cas de changement de code (via git push)
- Les logs sont disponibles dans l'interface de gestion

---

**Bon déploiement ! 🚀**
