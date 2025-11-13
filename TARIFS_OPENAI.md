# 💰 Tarifs OpenAI - Coach LoL

## Modèles disponibles et prix

### GPT-4o (PAR DÉFAUT - RECOMMANDÉ) ⭐
**Analyse de qualité professionnelle**

- **Input** : $2.50 / 1M tokens
- **Output** : $10.00 / 1M tokens

#### Estimation de coût par utilisation :
- **Analyse d'historique complète** : ~4000 tokens → **~$0.04** (~4 centimes)
- **Analyse pré-game détaillée** : ~3500 tokens → **~$0.035** (~3.5 centimes)
- **Analyse de matchup** : ~2500 tokens → **~$0.025** (~2.5 centimes)

**💡 Avec $5 de crédit gratuit : environ 100-150 analyses professionnelles !**

**Pourquoi GPT-4o ?**
- 🎯 Analyse de niveau Challenger/Master
- 🧠 Comprend la méta et le vocabulaire technique LoL
- 💡 Conseils beaucoup plus précis et actionnables
- 📊 Meilleure interprétation des stats avancées

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
model="gpt-4o",  # Par défaut, qualité PRO ⭐
```

### Options :
- `"gpt-4o"` → Analyse professionnelle (défaut recommandé) ⭐
- `"gpt-4o-mini"` → 10x moins cher mais qualité moindre
- `"gpt-4-turbo"` → Alternative à GPT-4o
- `"gpt-3.5-turbo"` → Ancien, pas recommandé pour LoL

---

## 📊 Comparaison des coûts

| Action | GPT-4o (PRO) | GPT-4o-mini | Différence |
|--------|--------------|-------------|------------|
| Analyse historique | $0.04 (4¢) | $0.0015 (0.15¢) | 27x plus cher |
| Analyse pré-game | $0.035 (3.5¢) | $0.002 (0.2¢) | 17x plus cher |
| 100 analyses | $4.00 | $0.15 | 27x plus cher |
| $5 de crédit | ~125 analyses PRO | ~3000 analyses basiques | 24x plus |

---

## 🎯 Recommandations

### Pour monter en elo sérieusement :
⭐ **GPT-4o** (par défaut actuel)
- Analyse digne d'un coach Challenger
- Vocabulaire technique et conseils précis
- Identifie les vrais problèmes dans votre gameplay
- $5 = ~125 analyses professionnelles
- **Coût : ~4 centimes par analyse** → Le prix d'un conseil pro !

### Budget très serré :
💰 **GPT-4o-mini** (économique)
- Coût dérisoire (~0.2 centime par analyse)
- $5 = ~3000 analyses
- Qualité correcte mais conseils plus génériques
- À modifier dans `llm_coach.py` ligne 221

### Notre avis :
✅ GPT-4o vaut largement son prix si vous voulez VRAIMENT progresser
✅ 4 centimes pour une analyse pro détaillée, c'est donné
✅ $5 vous donnent 125 sessions de coaching de qualité

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
