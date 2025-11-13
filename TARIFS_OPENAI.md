# 💰 Tarifs OpenAI - Coach LoL

## Modèles disponibles et prix

### GPT-4o-mini (PAR DÉFAUT - RECOMMANDÉ)
**Le plus économique et performant pour ce cas d'usage**

- **Input** : $0.150 / 1M tokens (~$0.00015 par 1000 tokens)
- **Output** : $0.600 / 1M tokens (~$0.0006 par 1000 tokens)

#### Estimation de coût par utilisation :
- **Analyse d'historique** : ~2000 tokens → **~$0.0015** (~0.15 centimes)
- **Analyse pré-game** : ~2500 tokens → **~$0.002** (~0.2 centimes)
- **Analyse de matchup** : ~1500 tokens → **~$0.001** (~0.1 centime)

**💡 Avec $5 de crédit gratuit : environ 2000-3000 analyses !**

---

### GPT-4o (PREMIUM)
**Plus puissant mais plus cher**

- **Input** : $2.50 / 1M tokens
- **Output** : $10.00 / 1M tokens

#### Estimation de coût :
- **Analyse d'historique** : ~$0.025 (~2.5 centimes)
- **Analyse pré-game** : ~$0.03 (~3 centimes)

**Avec $5 : environ 150-200 analyses**

---

### GPT-4 (ANCIEN)
**Ancien modèle, moins recommandé**

- **Input** : $30.00 / 1M tokens
- **Output** : $60.00 / 1M tokens

❌ **Non recommandé** - GPT-4o-mini est meilleur et 200x moins cher

---

## 💵 Offre gratuite OpenAI

OpenAI offre **$5 de crédit gratuit** pour les nouveaux comptes.

### Avec GPT-4o-mini (par défaut) :
- ✅ **2000-3000 analyses complètes**
- ✅ Largement suffisant pour plusieurs mois d'utilisation
- ✅ Excellente qualité d'analyse

### Utilisation typique d'un joueur actif :
- 5 analyses d'historique par semaine : ~$0.0075/semaine (~0.75 centime)
- 10 analyses pré-game ranked : ~$0.02/semaine (~2 centimes)
- **Total : ~$0.03/semaine** (~3 centimes)

**→ $5 vous donne environ 150-170 semaines = 3+ ANS d'utilisation !**

---

## 🔧 Comment changer de modèle ?

Éditez le fichier `llm_coach.py` ligne 221 :

```python
model="gpt-4o-mini",  # Par défaut, très économique
```

### Options :
- `"gpt-4o-mini"` → Le moins cher, excellent (défaut) ⭐
- `"gpt-4o"` → Plus puissant, 15x plus cher
- `"gpt-4-turbo"` → Alternative à GPT-4o
- `"gpt-3.5-turbo"` → Ancien, pas recommandé

---

## 📊 Comparaison des coûts

| Action | GPT-4o-mini | GPT-4o | Économie |
|--------|-------------|---------|----------|
| Analyse historique | $0.0015 | $0.025 | 16x moins cher |
| Analyse pré-game | $0.002 | $0.03 | 15x moins cher |
| 100 analyses | $0.15 | $2.50 | 16x moins cher |
| Utilisation 1 an | $1.50 | $25 | 16x moins cher |

---

## 🎯 Recommandations

### Pour la plupart des utilisateurs :
✅ **GPT-4o-mini** (par défaut)
- Excellent rapport qualité/prix
- Analyses détaillées et pertinentes
- $5 = plusieurs années d'utilisation

### Si vous voulez la meilleure qualité possible :
⚡ **GPT-4o**
- Analyses encore plus détaillées
- Meilleure compréhension du contexte
- $5 = plusieurs mois d'utilisation

### Budget serré ?
💰 **GPT-4o-mini reste le meilleur choix**
- Qualité largement suffisante
- Coût dérisoire
- Vous pouvez faire 3000 analyses avec $5

---

## 🔗 Liens utiles

- [Tarifs officiels OpenAI](https://openai.com/api/pricing/)
- [Obtenir une clé API](https://platform.openai.com/api-keys)
- [Crédit gratuit $5](https://platform.openai.com/signup)
- [Tableau de bord usage](https://platform.openai.com/usage)

---

## ❓ FAQ

### "C'est vraiment si peu cher ?"
Oui ! GPT-4o-mini est incroyablement économique. Une analyse coûte moins d'un centime.

### "Les $5 gratuits, c'est vraiment gratuit ?"
Oui, OpenAI offre $5 de crédit à tous les nouveaux comptes. Pas de carte bancaire nécessaire pour commencer.

### "Que se passe-t-il après les $5 ?"
Vous devrez ajouter une carte bancaire et payer à l'utilisation. Mais avec GPT-4o-mini, ça reste très bon marché.

### "Je peux suivre ma consommation ?"
Oui, sur https://platform.openai.com/usage vous voyez exactement combien vous dépensez.

---

**Conclusion : OpenAI + GPT-4o-mini = parfait pour Coach LoL ! 🎮💰**
