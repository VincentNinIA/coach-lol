# 💰 Tarifs OpenAI - Coach LoL

## Modèles disponibles et prix

### GPT-5 (PAR DÉFAUT - RECOMMANDÉ) ⭐
**Analyse de qualité professionnelle optimale**

- **Input** : $5.00 / 1M tokens
- **Output** : $20.00 / 1M tokens

#### Estimation de coût par utilisation :
- **Analyse d'historique complète** : ~4000 tokens → **~$0.08** (~8 centimes)
- **Analyse pré-game détaillée** : ~3500 tokens → **~$0.07** (~7 centimes)
- **Analyse de matchup** : ~2500 tokens → **~$0.05** (~5 centimes)

**💡 Avec $5 de crédit gratuit : environ 60-75 analyses professionnelles !**

**Pourquoi GPT-5 ?**
- 🎯 Analyse de niveau Challenger/Master supérieure
- 🧠 Meilleure compréhension de la méta et du vocabulaire technique LoL
- 💡 Conseils encore plus précis et actionnables
- 📊 Interprétation optimale des stats avancées
- ⚡ Raisonnement amélioré et réponses plus rapides

---

### GPT-4o-mini (ÉCONOMIQUE)
**Budget serré**

- **Input** : $0.150 / 1M tokens
- **Output** : $0.600 / 1M tokens

#### Estimation de coût :
- **Analyse d'historique** : ~2000 tokens → **~$0.0015** (~0.15 centimes)
- **Analyse pré-game** : ~2500 tokens → **~$0.002** (~0.2 centimes)

**Avec $5 : environ 2000-3000 analyses**

⚠️ Qualité inférieure pour l'analyse LoL (conseils moins précis)

---

### GPT-4o (ANCIEN)
**Ancien modèle, remplacé par GPT-5**

- **Input** : $2.50 / 1M tokens
- **Output** : $10.00 / 1M tokens

⚠️ **Remplacé par GPT-5** - GPT-5 offre une meilleure qualité d'analyse pour 2x le prix

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

Éditez le fichier `llm_coach.py` ligne 294 :

```python
model="gpt-5",  # Par défaut, qualité PRO optimale ⭐
```

### Options :
- `"gpt-5"` → Analyse professionnelle optimale (défaut recommandé) ⭐
- `"gpt-4o"` → Ancien modèle professionnel
- `"gpt-4o-mini"` → 10x moins cher mais qualité moindre
- `"gpt-3.5-turbo"` → Ancien, pas recommandé pour LoL

---

## 📊 Comparaison des coûts

| Action | GPT-5 (PRO) | GPT-4o | GPT-4o-mini |
|--------|-------------|--------|-------------|
| Analyse historique | $0.08 (8¢) | $0.04 (4¢) | $0.0015 (0.15¢) |
| Analyse pré-game | $0.07 (7¢) | $0.035 (3.5¢) | $0.002 (0.2¢) |
| 100 analyses | $8.00 | $4.00 | $0.15 |
| $5 de crédit | ~60 analyses PRO | ~125 analyses | ~3000 analyses basiques |

---

## 🎯 Recommandations

### Pour monter en elo sérieusement :
⭐ **GPT-5** (par défaut actuel)
- Analyse digne d'un coach Challenger avec raisonnement optimisé
- Vocabulaire technique et conseils ultra-précis
- Identifie les vrais problèmes dans votre gameplay
- $5 = ~60-75 analyses professionnelles
- **Coût : ~8 centimes par analyse** → Le prix d'un conseil pro premium !

### Alternative professionnelle :
💎 **GPT-4o** (ancien pro)
- Toujours excellent pour l'analyse LoL
- 2x moins cher que GPT-5
- $5 = ~125 analyses
- À modifier dans `llm_coach.py` ligne 294

### Budget très serré :
💰 **GPT-4o-mini** (économique)
- Coût dérisoire (~0.2 centime par analyse)
- $5 = ~3000 analyses
- Qualité correcte mais conseils plus génériques
- À modifier dans `llm_coach.py` ligne 294

### Notre avis :
✅ GPT-5 représente le top de l'analyse LoL si vous voulez VRAIMENT progresser
✅ 8 centimes pour une analyse pro ultra-détaillée, c'est donné
✅ $5 vous donnent 60-75 sessions de coaching de qualité supérieure

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

**Conclusion : OpenAI + GPT-5 = analyse LoL de niveau professionnel ! 🎮💰**
