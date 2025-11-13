"""
Module pour le coaching en temps réel pendant la sélection de champions
"""
import time
from typing import Dict, Optional
from riot_api import RiotAPI
from data_analyzer import DataAnalyzer

class LiveGameCoach:
    def __init__(self, api: RiotAPI):
        self.api = api
        self.analyzer = DataAnalyzer()

    def check_for_active_game(self, puuid: str) -> Optional[Dict]:
        """Vérifie si le joueur est en partie"""
        return self.api.get_current_game(puuid)

    def analyze_pregame(self, game_data: Dict, player_puuid: str) -> Dict:
        """
        Analyse la phase de sélection de champions
        Retourne des informations sur les adversaires et des conseils
        """
        if not game_data:
            return {}

        analysis = {
            'game_mode': game_data.get('gameMode'),
            'game_queue': game_data.get('gameQueueConfigId'),
            'your_team': [],
            'enemy_team': [],
            'recommendations': [],
            'threats': []
        }

        participants = game_data.get('participants', [])

        # Séparer les équipes
        player_team_id = None
        for participant in participants:
            if participant['puuid'] == player_puuid:
                player_team_id = participant['teamId']
                break

        if player_team_id is None:
            return analysis

        for participant in participants:
            player_info = {
                'summoner_name': participant.get('summonerName', 'Unknown'),
                'champion_id': participant.get('championId'),
                'puuid': participant.get('puuid'),
                'team_id': participant.get('teamId')
            }

            if participant['teamId'] == player_team_id:
                analysis['your_team'].append(player_info)
            else:
                analysis['enemy_team'].append(player_info)

        # Analyser l'équipe adverse
        print("\n🔍 Analyse de l'équipe adverse en cours...")
        enemy_analysis = self._analyze_enemy_players(analysis['enemy_team'])
        analysis['enemy_analysis'] = enemy_analysis

        # Générer des recommandations
        analysis['recommendations'] = self._generate_recommendations(
            analysis['your_team'],
            analysis['enemy_team'],
            enemy_analysis
        )

        return analysis

    def _analyze_enemy_players(self, enemy_team: list) -> Dict:
        """Analyse détaillée de chaque joueur adverse"""
        enemy_analysis = {}

        for i, enemy in enumerate(enemy_team, 1):
            print(f"  Analyse joueur {i}/{len(enemy_team)}...", end='\r')

            puuid = enemy.get('puuid')
            if not puuid:
                continue

            # Récupérer l'historique récent
            match_ids = self.api.get_match_history(puuid, count=20, queue=420)  # Ranked Solo

            player_data = {
                'summoner_name': enemy.get('summoner_name'),
                'champion_id': enemy.get('champion_id'),
                'recent_matches': [],
                'rank': 'Unknown',
                'winrate': 0,
                'main_champions': [],
                'threat_level': 'UNKNOWN'
            }

            # Récupérer le rang
            summoner = self.api.get_summoner_by_puuid(puuid)
            if summoner and 'id' in summoner:
                league_entries = self.api.get_league_entries(summoner['id'])
                if league_entries:
                    ranked_solo = next((e for e in league_entries if e['queueType'] == 'RANKED_SOLO_5x5'), None)
                    if ranked_solo:
                        player_data['rank'] = f"{ranked_solo['tier']} {ranked_solo['rank']} - {ranked_solo['leaguePoints']} LP"
                        player_data['winrate'] = (ranked_solo['wins'] / (ranked_solo['wins'] + ranked_solo['losses'])) * 100 if (ranked_solo['wins'] + ranked_solo['losses']) > 0 else 0
                        player_data['wins'] = ranked_solo['wins']
                        player_data['losses'] = ranked_solo['losses']

            # Analyser les matchs récents
            if match_ids:
                matches_data = []
                for match_id in match_ids[:10]:  # Limiter à 10 matchs pour la vitesse
                    match_detail = self.api.get_match_details(match_id)
                    if match_detail:
                        matches_data.append(match_detail)
                    time.sleep(0.1)  # Petit délai pour éviter le rate limit

                if matches_data:
                    stats = self.analyzer.analyze_match_history(matches_data, puuid)
                    player_data['stats'] = stats
                    player_data['threat_level'] = self._calculate_threat_level(player_data)

            # Récupérer les champions principaux depuis les stats analysées
            if player_data.get('stats') and player_data['stats'].get('champions'):
                # Extraire les noms des champions les plus joués
                champs = player_data['stats']['champions']
                top_champs = sorted(champs.items(), key=lambda x: x[1]['games'], reverse=True)[:3]
                player_data['main_champions'] = [champ_name for champ_name, _ in top_champs]
            else:
                # Fallback: utiliser les maîtrises (mais sans noms de champions disponibles)
                masteries = self.api.get_champion_masteries(puuid, count=3)
                if masteries:
                    # Stocker juste les niveaux de maîtrise comme info
                    player_data['main_champions'] = [f"Lvl{m['championLevel']}" for m in masteries]
                else:
                    player_data['main_champions'] = []

            enemy_analysis[enemy.get('summoner_name')] = player_data

        print("\n✓ Analyse terminée")
        return enemy_analysis

    def _calculate_threat_level(self, player_data: Dict) -> str:
        """Calcule le niveau de menace d'un joueur"""
        rank = player_data.get('rank', 'Unknown')
        winrate = player_data.get('winrate', 50)
        stats = player_data.get('stats', {})

        # Score de menace basé sur plusieurs facteurs
        threat_score = 0

        # Facteur de rang
        if 'CHALLENGER' in rank or 'GRANDMASTER' in rank:
            threat_score += 5
        elif 'MASTER' in rank:
            threat_score += 4
        elif 'DIAMOND' in rank or 'EMERALD' in rank:
            threat_score += 3
        elif 'PLATINUM' in rank:
            threat_score += 2
        elif 'GOLD' in rank:
            threat_score += 1

        # Facteur de winrate
        if winrate >= 60:
            threat_score += 2
        elif winrate >= 55:
            threat_score += 1
        elif winrate < 45:
            threat_score -= 1

        # Facteur de KDA
        kda = stats.get('kda_avg', 0)
        if kda >= 4:
            threat_score += 2
        elif kda >= 3:
            threat_score += 1

        # Déterminer le niveau de menace
        if threat_score >= 7:
            return "🔴 TRÈS ÉLEVÉ"
        elif threat_score >= 5:
            return "🟠 ÉLEVÉ"
        elif threat_score >= 3:
            return "🟡 MOYEN"
        else:
            return "🟢 FAIBLE"

    def _generate_recommendations(self, your_team: list, enemy_team: list, enemy_analysis: Dict) -> list:
        """Génère des recommandations basées sur l'analyse"""
        recommendations = []

        # Identifier les plus grandes menaces
        threats = []
        for summoner_name, data in enemy_analysis.items():
            if '🔴' in data.get('threat_level', '') or '🟠' in data.get('threat_level', ''):
                threats.append({
                    'name': summoner_name,
                    'rank': data.get('rank'),
                    'threat_level': data.get('threat_level'),
                    'winrate': data.get('winrate', 0)
                })

        if threats:
            recommendations.append("⚠️  MENACES IDENTIFIÉES :")
            for threat in threats:
                recommendations.append(f"   • {threat['name']} ({threat['rank']}) - {threat['threat_level']} - WR: {threat['winrate']:.1f}%")

        # Conseils généraux
        recommendations.append("\n💡 CONSEILS STRATÉGIQUES :")
        recommendations.append("   • Communiquez avec votre équipe dès la phase de picks")
        recommendations.append("   • Placez des wards défensifs si vous êtes contre des joueurs expérimentés")
        recommendations.append("   • Adaptez votre style de jeu en fonction du niveau de vos adversaires")

        if len(threats) >= 2:
            recommendations.append("   • ⚠️  Plusieurs menaces détectées : jouez prudemment et attendez les erreurs")

        return recommendations

    def format_pregame_report(self, analysis: Dict) -> str:
        """Formate le rapport pré-game de manière lisible"""
        if not analysis:
            return "Aucune analyse disponible"

        report = []
        report.append("\n" + "=" * 80)
        report.append("🎮 ANALYSE PRÉ-GAME - COACH LOL")
        report.append("=" * 80)

        report.append(f"\nMode de jeu : {analysis.get('game_mode', 'Unknown')}")

        # Équipe adverse
        if analysis.get('enemy_analysis'):
            report.append("\n" + "-" * 80)
            report.append("👥 ÉQUIPE ADVERSE :")
            report.append("-" * 80)

            for summoner_name, data in analysis['enemy_analysis'].items():
                report.append(f"\n🔹 {summoner_name}")
                report.append(f"   Rang : {data.get('rank', 'Unknown')}")

                if data.get('wins') and data.get('losses'):
                    report.append(f"   Record : {data['wins']}W - {data['losses']}L ({data.get('winrate', 0):.1f}% WR)")

                report.append(f"   Niveau de menace : {data.get('threat_level', 'UNKNOWN')}")

                stats = data.get('stats', {})
                if stats:
                    report.append(f"   KDA moyen : {stats.get('kda_avg', 0):.2f}")
                    report.append(f"   Performance récente : {stats.get('wins', 0)}W - {stats.get('losses', 0)}L sur les {stats.get('total_games', 0)} dernières parties")

                # Champions principaux
                if data.get('main_champions'):
                    report.append(f"   Champions mains : ", end='')
                    champ_info = [f"Level {m['level']} ({m['points']:,} pts)" for m in data['main_champions'][:3]]
                    report.append(", ".join(champ_info))

        # Recommandations
        if analysis.get('recommendations'):
            report.append("\n" + "-" * 80)
            for rec in analysis['recommendations']:
                report.append(rec)

        report.append("\n" + "=" * 80)
        report.append("Bonne chance sur la Faille de l'invocateur ! 🏆")
        report.append("=" * 80 + "\n")

        return "\n".join(report)

    def monitor_game_start(self, puuid: str, check_interval: int = 10):
        """
        Surveille le démarrage d'une partie et lance l'analyse automatiquement
        """
        print("🔍 Surveillance du démarrage de partie...")
        print(f"Vérification toutes les {check_interval} secondes")
        print("Appuyez sur Ctrl+C pour arrêter\n")

        try:
            while True:
                game = self.check_for_active_game(puuid)

                if game:
                    print("🎮 Partie détectée ! Lancement de l'analyse...\n")
                    analysis = self.analyze_pregame(game, puuid)
                    report = self.format_pregame_report(analysis)
                    print(report)
                    return analysis

                print("⏳ Aucune partie en cours...", end='\r')
                time.sleep(check_interval)

        except KeyboardInterrupt:
            print("\n\n❌ Surveillance interrompue")
            return None
