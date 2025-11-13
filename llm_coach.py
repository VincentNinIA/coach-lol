"""
Module d'intégration LLM pour l'analyse intelligente avec OpenAI (GPT)
Vous pouvez aussi utiliser Anthropic Claude en modifiant ce module
"""
import os
import json
from typing import Dict, List, Optional

class LLMCoach:
    def __init__(self, api_key: str = None, provider: str = "openai"):
        """
        Initialize le coach LLM
        provider: "openai" pour GPT (défaut), "anthropic" pour Claude
        """
        self.provider = provider

        if provider == "openai":
            # Pour OpenAI (par défaut)
            try:
                from openai import OpenAI
                self.api_key = api_key or os.getenv('OPENAI_API_KEY')
                if self.api_key:
                    self.client = OpenAI(api_key=self.api_key)
                else:
                    self.client = None
                    print("⚠️  Clé API OpenAI non configurée. L'analyse LLM sera désactivée.")
            except ImportError:
                print("⚠️  Module openai non installé. Installez-le avec : pip install openai")
                self.client = None

        elif provider == "anthropic":
            # Pour Anthropic (optionnel)
            try:
                import anthropic
                self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
                if self.api_key:
                    self.client = anthropic.Anthropic(api_key=self.api_key)
                else:
                    self.client = None
                    print("⚠️  Clé API Anthropic non configurée. L'analyse LLM sera désactivée.")
            except ImportError:
                print("⚠️  Module anthropic non installé. Installez-le avec : pip install anthropic")
                self.client = None

    def is_available(self) -> bool:
        """Vérifie si le LLM est disponible"""
        return self.client is not None

    def analyze_player_performance(self, stats: Dict, player_name: str) -> str:
        """
        Analyse les statistiques d'un joueur avec le LLM
        Retourne une analyse détaillée et des conseils personnalisés
        """
        if not self.is_available():
            return "❌ Analyse LLM non disponible (clé API manquante)"

        # Préparer les données pour le LLM
        prompt = self._build_performance_prompt(stats, player_name)

        try:
            if self.provider == "openai":
                return self._call_gpt(prompt)
            elif self.provider == "anthropic":
                return self._call_claude(prompt)
        except Exception as e:
            return f"❌ Erreur lors de l'analyse LLM : {str(e)}"

    def analyze_pregame(self, analysis: Dict, player_name: str, your_rank: str = None) -> str:
        """
        Analyse la situation pré-game avec le LLM
        Donne des conseils stratégiques personnalisés
        """
        if not self.is_available():
            return "❌ Analyse LLM non disponible (clé API manquante)"

        prompt = self._build_pregame_prompt(analysis, player_name, your_rank)

        try:
            if self.provider == "openai":
                return self._call_gpt(prompt)
            elif self.provider == "anthropic":
                return self._call_claude(prompt)
        except Exception as e:
            return f"❌ Erreur lors de l'analyse LLM : {str(e)}"

    def analyze_champion_matchup(self, your_champ: str, enemy_champ: str,
                                  your_rank: str, matchup_history: Dict = None) -> str:
        """
        Analyse un matchup spécifique avec le LLM
        """
        if not self.is_available():
            return "❌ Analyse LLM non disponible (clé API manquante)"

        prompt = self._build_matchup_prompt(your_champ, enemy_champ, your_rank, matchup_history)

        try:
            if self.provider == "openai":
                return self._call_gpt(prompt)
            elif self.provider == "anthropic":
                return self._call_claude(prompt)
        except Exception as e:
            return f"❌ Erreur lors de l'analyse LLM : {str(e)}"

    def _build_performance_prompt(self, stats: Dict, player_name: str) -> str:
        """Construit le prompt pour l'analyse de performance"""
        prompt = f"""ANALYSE DE PERFORMANCE - {player_name}
=====================================

📊 DONNÉES BRUTES ({stats.get('total_games', 0)} parties analysées) :

PERFORMANCE GLOBALE :
- Record: {stats.get('wins', 0)}W - {stats.get('losses', 0)}L ({stats.get('winrate', 0):.1f}% WR)
- KDA: {stats.get('avg_kills', 0):.1f} / {stats.get('avg_deaths', 0):.1f} / {stats.get('avg_assists', 0):.1f} = {stats.get('kda_avg', 0):.2f} KDA
- Farm: {stats.get('cs_per_min_avg', 0):.1f} CS/min
- Vision Score: {stats.get('vision_score_avg', 0):.1f} par game
- Participation aux kills: {stats.get('kill_participation', 0):.1f}%

CHAMPION POOL (Top 5 par nombre de games) :"""

        # Ajouter les stats détaillées des champions
        if stats.get('champions'):
            top_champs = sorted(stats['champions'].items(), key=lambda x: x[1]['games'], reverse=True)[:5]
            for champ, champ_stats in top_champs:
                games = champ_stats['games']
                winrate = (champ_stats['wins'] / games * 100) if games > 0 else 0
                kda = (champ_stats['kills'] + champ_stats['assists']) / max(champ_stats['deaths'], 1)
                avg_kills = champ_stats['kills'] / games
                avg_deaths = champ_stats['deaths'] / games
                avg_assists = champ_stats['assists'] / games
                prompt += f"\n  {champ}:"
                prompt += f"\n    - {games} games | {winrate:.1f}% WR"
                prompt += f"\n    - {avg_kills:.1f}/{avg_deaths:.1f}/{avg_assists:.1f} = {kda:.2f} KDA"

        prompt += """

🎯 TON RÔLE EN TANT QUE COACH PRO :

Analyse ces données avec un œil d'expert Challenger/Master. Identifie les VRAIES forces et faiblesses, pas les généralités.

Structure ton analyse en 5 sections :

## 1. 🔍 DIAGNOSTIC INSTANTANÉ
Un paragraphe direct qui résume le profil du joueur (style de jeu, niveau estimé, tendances principales).

## 2. ✅ POINTS FORTS (2-3 éléments)
Identifie ce qui fonctionne VRAIMENT. Sois spécifique avec les chiffres.
Exemple: "CS/min à 7.2 → bon farm, tu connais tes matchups en lane"

## 3. ⚠️ POINTS CRITIQUES À FIX (3-4 éléments prioritaires)
Les problèmes qui coûtent des games. Pour chaque point :
- Le problème identifié (avec les stats qui le prouvent)
- Pourquoi ça te coûte des victoires
- Impact sur ton MMR/LP

## 4. 💡 PLAN D'ACTION CONCRET (3-5 conseils)
Des conseils ACTIONNABLES, pas de généralités. Format :
- Quoi faire exactement
- Comment le faire
- Comment mesurer si ça marche

## 5. 🎮 STRATÉGIE CHAMPION POOL
- Quels champions one-trick/main pour monter
- Lesquels drop ou limiter
- Pourquoi (basé sur tes stats)

IMPORTANT :
- Utilise le vocabulaire technique LoL (macro, micro, wave management, etc.)
- Sois direct et constructif, pas gentil pour être gentil
- Compare aux benchmarks de l'elo quand c'est pertinent
- Donne des objectifs chiffrés quand possible
"""
        return prompt

    def _build_pregame_prompt(self, analysis: Dict, player_name: str, your_rank: str = None) -> str:
        """Construit le prompt pour l'analyse pré-game"""
        enemy_analysis = analysis.get('enemy_analysis', {})

        prompt = f"""🎯 BRIEFING PRÉ-GAME - {player_name}"""

        if your_rank:
            prompt += f" [{your_rank}]"

        prompt += "\n" + "="*50 + "\n\n"
        prompt += "📋 SCOUTING ÉQUIPE ADVERSE :\n\n"

        # Ajouter les infos détaillées sur chaque adversaire
        for i, (summoner_name, data) in enumerate(enemy_analysis.items(), 1):
            prompt += f"{i}. {summoner_name}\n"
            prompt += f"   Rang: {data.get('rank', 'Unknown')}\n"

            if data.get('wins') and data.get('losses'):
                total = data['wins'] + data['losses']
                prompt += f"   Form: {data['wins']}W-{data['losses']}L ({data.get('winrate', 0):.1f}% WR sur {total} games)\n"

            threat = data.get('threat_level', 'UNKNOWN')
            threat_emoji = {'TRÈS ÉLEVÉ': '🔴', 'ÉLEVÉ': '🟠', 'MOYEN': '🟡', 'FAIBLE': '🟢'}.get(threat, '⚪')
            prompt += f"   Menace: {threat_emoji} {threat}\n"

            stats = data.get('stats', {})
            if stats:
                prompt += f"   Stats: {stats.get('kda_avg', 0):.2f} KDA"
                if stats.get('wins', 0) + stats.get('losses', 0) > 0:
                    recent_wr = (stats['wins'] / (stats['wins'] + stats['losses']) * 100)
                    prompt += f" | {stats.get('wins', 0)}W-{stats.get('losses', 0)}L récent ({recent_wr:.0f}%)\n"

            # Ajouter les mains champions si disponibles
            if data.get('main_champions'):
                mains = data['main_champions'][:3]
                prompt += f"   Mains: {', '.join(mains)}\n"

            prompt += "\n"

        prompt += """
🎮 TON RÔLE EN TANT QUE COACH :

Tu dois donner un gameplan tactique PRO pour cette partie spécifique. Pas de conseils génériques.

Structure ton briefing en 5 sections :

## 1. 🔴 ANALYSE THREAT LEVEL
Pour CHAQUE adversaire :
- Son niveau de danger réel (1-5)
- Pourquoi il est dangereux (ou pas)
- Comment le contrer spécifiquement

## 2. 🎯 WIN CONDITIONS PRINCIPALES
Identifie les 2-3 conditions de victoire prioritaires pour cette game :
- Que faire dans les 15 premières minutes
- Quel joueur carry/faire snowball
- Quel objectif prioriser (Drake soul? Baron? Split?)

## 3. ⚠️ LOSE CONDITIONS (pièges à éviter)
Les 2-3 choses qui peuvent vous faire perdre :
- Erreurs fatales à ne pas commettre
- Picks/plays dangereux de l'équipe adverse
- Timings critiques

## 4. 💡 GAMEPLAN PHASE PAR PHASE
Stratégie concrète :
- EARLY (0-15min): Focus principal et rotations
- MID (15-25min): Objectifs et teamfight approach
- LATE (25min+): Win condition et macro calls

## 5. 🗣️ CALLS PRIORITAIRES
3-5 micro-calls tactiques spécifiques à cette game :
- Invades possibles
- Gank paths vulnérables
- Vision key spots
- Target priority en teamfight

STYLE :
- Sois ULTRA spécifique à cette game
- Vocabulaire technique LoL (tracking jungler, dive windows, tempo, etc.)
- Direct et assertif comme un coach IRL
- Objectifs chiffrés quand possible (ex: "GG si vous êtes 3 drakes à 20min")
"""
        return prompt

    def _build_matchup_prompt(self, your_champ: str, enemy_champ: str,
                              your_rank: str, matchup_history: Dict = None) -> str:
        """Construit le prompt pour l'analyse de matchup"""
        prompt = f"""Tu es un coach professionnel de League of Legends spécialisé dans les matchups.

MATCHUP :
=========
Ton champion : {your_champ}
Champion adverse : {enemy_champ}
Ton rang : {your_rank}
"""

        if matchup_history:
            prompt += f"\nHistorique sur ce matchup : {matchup_history.get('games', 0)} parties, {matchup_history.get('winrate', 0):.1f}% WR\n"

        prompt += """

DEMANDE :
=========
Fournis une analyse du matchup en 5 sections :

1. **Vue d'ensemble** : Qui a l'avantage dans ce matchup et pourquoi ?
2. **Phase de lane** : Conseils pour les 15 premières minutes
3. **Power spikes** : Quand tu es fort, quand l'adversaire est fort
4. **Combos et pièges** : Ce qu'il faut éviter et comment le punir
5. **Build et runes** : Recommandations d'adaptation

Sois très spécifique et actionnable. Utilise des emojis.
"""
        return prompt

    def _call_gpt(self, prompt: str) -> str:
        """Appelle l'API OpenAI GPT"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-5",  # GPT-5 pour une analyse de qualité professionnelle optimale
                messages=[
                    {"role": "system", "content": """Tu es un coach professionnel de League of Legends de haut niveau (Challenger/Master).
Tu analyses les performances avec un œil expert, tu identifies les patterns de jeu, les erreurs récurrentes et tu donnes des conseils précis et actionnables.
Tu utilises le vocabulaire technique de LoL (macro, micro, wave management, trading, recall timing, etc.).
Tu es direct, constructif et tu te concentres sur ce qui fait vraiment la différence pour progresser."""},
                    {"role": "user", "content": prompt}
                ],
                max_completion_tokens=3000  # GPT-5 utilise max_completion_tokens (temperature=1 par défaut uniquement)
            )

            # Diagnostiquer pourquoi la réponse est vide
            choice = response.choices[0]
            content = choice.message.content
            finish_reason = choice.finish_reason

            if content is None or len(content) == 0:
                return f"❌ GPT-5 a retourné une réponse vide (finish_reason={finish_reason}, content={'None' if content is None else 'empty string'})"

            return content
        except Exception as e:
            return f"❌ Erreur OpenAI API : {str(e)}"

    def _call_claude(self, prompt: str) -> str:
        """Appelle l'API Claude d'Anthropic"""
        try:
            import anthropic
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"❌ Erreur Claude API : {str(e)}"

    def get_quick_tip(self, context: str) -> str:
        """Génère un conseil rapide basé sur le contexte"""
        if not self.is_available():
            return "💡 Astuce : Communiquez avec votre équipe et placez des wards !"

        prompt = f"""Tu es un coach League of Legends. Donne UN conseil court (1-2 phrases max) pour cette situation :

{context}

Sois concis, direct et actionnable."""

        try:
            if self.provider == "anthropic":
                return self._call_claude(prompt)
            elif self.provider == "openai":
                return self._call_gpt(prompt)
        except:
            return "💡 Astuce : Restez focus et adaptez-vous à la situation !"


# Test du module
if __name__ == "__main__":
    coach = LLMCoach()

    if coach.is_available():
        print("✓ LLM Coach initialisé")

        # Test avec des stats fictives
        test_stats = {
            'total_games': 20,
            'wins': 12,
            'losses': 8,
            'winrate': 60.0,
            'kda_avg': 3.5,
            'avg_kills': 8.2,
            'avg_deaths': 4.1,
            'avg_assists': 10.1,
            'cs_per_min_avg': 6.8,
            'vision_score_avg': 25.5,
            'champions': {
                'Yasuo': {'games': 10, 'wins': 6, 'kills': 82, 'deaths': 41, 'assists': 101}
            }
        }

        print("\nTest d'analyse de performance...")
        analysis = coach.analyze_player_performance(test_stats, "TestPlayer")
        print(analysis)
    else:
        print("❌ LLM Coach non disponible (configurez votre clé API)")
