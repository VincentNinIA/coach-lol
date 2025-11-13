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
        prompt = f"""Tu es un coach professionnel de League of Legends. Analyse les statistiques suivantes du joueur {player_name} et fournis une analyse détaillée avec des conseils concrets pour s'améliorer.

STATISTIQUES DU JOUEUR :
=========================

Statistiques générales ({stats.get('total_games', 0)} parties) :
- Victoires / Défaites : {stats.get('wins', 0)}W - {stats.get('losses', 0)}L
- Winrate : {stats.get('winrate', 0):.1f}%
- KDA moyen : {stats.get('kda_avg', 0):.2f}
- K/D/A : {stats.get('avg_kills', 0):.1f} / {stats.get('avg_deaths', 0):.1f} / {stats.get('avg_assists', 0):.1f}
- CS/min moyen : {stats.get('cs_per_min_avg', 0):.1f}
- Vision score moyen : {stats.get('vision_score_avg', 0):.1f}

Champions les plus joués :
"""
        # Ajouter les stats des champions
        if stats.get('champions'):
            top_champs = sorted(stats['champions'].items(), key=lambda x: x[1]['games'], reverse=True)[:5]
            for champ, champ_stats in top_champs:
                games = champ_stats['games']
                winrate = (champ_stats['wins'] / games * 100) if games > 0 else 0
                kda = (champ_stats['kills'] + champ_stats['assists']) / max(champ_stats['deaths'], 1)
                prompt += f"\n- {champ} : {games} games, {winrate:.1f}% WR, {kda:.2f} KDA"

        prompt += """

DEMANDE :
=========
Fournis une analyse structurée en 4 sections :

1. **Points forts** : Identifie 2-3 points positifs basés sur les stats
2. **Points à améliorer** : Identifie 2-3 aspects qui nécessitent du travail
3. **Conseils prioritaires** : Donne 3-5 conseils concrets et actionnables
4. **Focus champions** : Recommande sur quels champions se concentrer et pourquoi

Sois direct, constructif et précis. Utilise des emojis pour rendre l'analyse plus lisible.
"""
        return prompt

    def _build_pregame_prompt(self, analysis: Dict, player_name: str, your_rank: str = None) -> str:
        """Construit le prompt pour l'analyse pré-game"""
        enemy_analysis = analysis.get('enemy_analysis', {})

        prompt = f"""Tu es un coach professionnel de League of Legends. Une partie va commencer et tu dois analyser l'équipe adverse pour donner des conseils stratégiques à {player_name}"""

        if your_rank:
            prompt += f" (rang: {your_rank})"

        prompt += ".\n\nANALYSE DE L'ÉQUIPE ADVERSE :\n=========================\n\n"

        # Ajouter les infos sur chaque adversaire
        for i, (summoner_name, data) in enumerate(enemy_analysis.items(), 1):
            prompt += f"\nJoueur {i} : {summoner_name}\n"
            prompt += f"- Rang : {data.get('rank', 'Unknown')}\n"

            if data.get('wins') and data.get('losses'):
                prompt += f"- Record : {data['wins']}W - {data['losses']}L ({data.get('winrate', 0):.1f}% WR)\n"

            prompt += f"- Niveau de menace : {data.get('threat_level', 'UNKNOWN')}\n"

            stats = data.get('stats', {})
            if stats:
                prompt += f"- KDA moyen : {stats.get('kda_avg', 0):.2f}\n"
                prompt += f"- Performance récente : {stats.get('wins', 0)}W - {stats.get('losses', 0)}L (dernières parties)\n"

        prompt += """

DEMANDE :
=========
Fournis une analyse stratégique en 4 sections :

1. **Évaluation de la menace** : Classe les adversaires du plus dangereux au moins dangereux
2. **Points faibles à exploiter** : Identifie les faiblesses de l'équipe adverse
3. **Stratégie de game** : Donne une stratégie globale pour cette partie
4. **Conseils individuels** : 3-5 conseils spécifiques pour bien jouer cette game

Sois tactique, précis et motive le joueur. Utilise des emojis.
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
                model="gpt-4o-mini",  # gpt-4o-mini est moins cher, vous pouvez utiliser "gpt-4o" ou "gpt-4" pour plus de qualité
                messages=[
                    {"role": "system", "content": "Tu es un coach professionnel de League of Legends."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
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
