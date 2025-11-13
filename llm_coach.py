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

        # Déterminer le rôle principal
        main_role = "Unknown"
        if stats.get('roles'):
            main_role = max(stats['roles'].items(), key=lambda x: x[1])[0]
            # Traduire les codes Riot en noms lisibles
            role_names = {
                'TOP': 'Top', 'JUNGLE': 'Jungle', 'MIDDLE': 'Mid',
                'BOTTOM': 'ADC', 'UTILITY': 'Support', 'UNKNOWN': 'Flex'
            }
            main_role = role_names.get(main_role, main_role)

        prompt = f"""Coach LoL - Analyse {player_name} ({stats.get('total_games', 0)} games)

Rôle principal: {main_role}

Stats globales:
- {stats.get('wins', 0)}W-{stats.get('losses', 0)}L ({stats.get('winrate', 0):.1f}% WR)
- {stats.get('kda_avg', 0):.2f} KDA ({stats.get('avg_kills', 0):.1f}/{stats.get('avg_deaths', 0):.1f}/{stats.get('avg_assists', 0):.1f})
- {stats.get('cs_per_min_avg', 0):.1f} CS/min
- {stats.get('vision_score_avg', 0):.1f} Vision
- {stats.get('kill_participation', 0):.1f}% KP

Top champions:"""

        # Limiter à top 3 champions pour réduire la taille
        if stats.get('champions'):
            role_names = {
                'TOP': 'Top', 'JUNGLE': 'Jgl', 'MIDDLE': 'Mid',
                'BOTTOM': 'ADC', 'UTILITY': 'Sup', 'UNKNOWN': 'Flex'
            }
            top_champs = sorted(stats['champions'].items(), key=lambda x: x[1]['games'], reverse=True)[:3]
            for champ, cs in top_champs:
                wr = (cs['wins'] / cs['games'] * 100) if cs['games'] > 0 else 0
                kda = (cs['kills'] + cs['assists']) / max(cs['deaths'], 1)

                # Déterminer le rôle principal pour ce champion
                champ_role = "?"
                if 'roles' in cs and cs['roles']:
                    main_champ_role = max(cs['roles'].items(), key=lambda x: x[1])[0]
                    champ_role = role_names.get(main_champ_role, main_champ_role)

                prompt += f"\n{champ} ({champ_role}): {cs['games']}g, {wr:.0f}%WR, {kda:.1f}KDA"

        prompt += f"""

Analyse ce joueur {main_role} en 5 sections:
1. Diagnostic (1 para)
2. Points forts (2-3)
3. Points critiques (3-4)
4. Plan d'action (3-5 conseils précis pour {main_role})
5. Champion pool (lesquels garder/drop pour {main_role})

Adapte tes conseils au rôle {main_role}. Sois direct, technique, avec chiffres."""
        return prompt

    def _build_pregame_prompt(self, analysis: Dict, player_name: str, your_rank: str = None) -> str:
        """Construit le prompt pour l'analyse pré-game"""
        from champion_names import get_champion_name
        enemy_analysis = analysis.get('enemy_analysis', {})

        # Traduire le rôle du joueur
        your_role = analysis.get('your_role', 'UNKNOWN')
        role_names = {
            'TOP': 'Top', 'JUNGLE': 'Jungle', 'MIDDLE': 'Mid',
            'BOTTOM': 'ADC', 'UTILITY': 'Support', 'UNKNOWN': '?'
        }
        your_role_display = role_names.get(your_role, your_role)

        prompt = f"""Briefing pré-game {player_name} - Rôle: {your_role_display}"""
        if your_rank:
            prompt += f" [{your_rank}]"
        prompt += "\n\nEnnemis:\n"

        # Infos compactes sur adversaires
        for i, (name, data) in enumerate(enemy_analysis.items(), 1):
            threat = data.get('threat_level', 'UNKNOWN')
            champion_id = data.get('champion_id', '?')
            champion_name = get_champion_name(champion_id)

            # Afficher le champion actuel en premier
            prompt += f"{i}. {name} [{champion_name}] ({data.get('rank', '?')})"

            if data.get('wins') and data.get('losses'):
                prompt += f" - {data['wins']}W-{data['losses']}L ({data.get('winrate', 0):.0f}%)"

            stats = data.get('stats', {})
            if stats:
                prompt += f" - {stats.get('kda_avg', 0):.1f}KDA"

            prompt += f" - Menace: {threat}"

            if data.get('main_champions') and len(data['main_champions']) > 0:
                # main_champions est maintenant une liste de noms de champions
                mains = ', '.join(data['main_champions'][:2])
                prompt += f" - Mains habituels: {mains}"

            prompt += "\n"

        prompt += f"""
Analyse pro en 5 sections (adapté au rôle {your_role_display}):
1. Threat level (chaque ennemi 1-5, pourquoi, comment contrer depuis {your_role_display})
2. Win conditions (2-3 priorités pour {your_role_display})
3. Lose conditions (2-3 pièges à éviter en {your_role_display})
4. Gameplan (Early/Mid/Late spécifique {your_role_display})
5. Calls prioritaires (3-5 tactiques {your_role_display})

Direct, technique, spécifique au rôle {your_role_display}."""
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
                model="gpt-4o",  # Retour à GPT-4o - GPT-5 a des limites de tokens trop strictes
                messages=[
                    {"role": "system", "content": "Coach LoL pro (Challenger/Master). Analyse technique, directe, avec vocabulaire LoL (macro, micro, wave management). Sois précis et actionnable."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3000,
                temperature=0.7
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
