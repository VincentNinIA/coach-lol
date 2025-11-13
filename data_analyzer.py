"""
Module d'analyse des données de match et de joueur
"""
from typing import Dict, List, Optional
from collections import defaultdict, Counter
import statistics

class DataAnalyzer:
    def __init__(self):
        self.champion_data = {}

    def analyze_match_history(self, matches: List[Dict], player_puuid: str) -> Dict:
        """
        Analyse l'historique de matchs d'un joueur
        Retourne des statistiques détaillées
        """
        if not matches:
            return {}

        stats = {
            'total_games': len(matches),
            'wins': 0,
            'losses': 0,
            'kills': [],
            'deaths': [],
            'assists': [],
            'champions': defaultdict(lambda: {'games': 0, 'wins': 0, 'kills': 0, 'deaths': 0, 'assists': 0}),
            'roles': defaultdict(int),
            'recent_performance': [],
            'kda_avg': 0.0,
            'vision_score_avg': 0.0,
            'cs_per_min_avg': 0.0
        }

        for match in matches:
            info = match.get('info', {})
            participants = info.get('participants', [])

            # Trouver le joueur dans les participants
            player = next((p for p in participants if p['puuid'] == player_puuid), None)

            if not player:
                continue

            # Stats de base
            win = player['win']
            stats['wins' if win else 'losses'] += 1
            stats['kills'].append(player['kills'])
            stats['deaths'].append(player['deaths'])
            stats['assists'].append(player['assists'])

            # Stats par champion
            champ_name = player['championName']
            stats['champions'][champ_name]['games'] += 1
            stats['champions'][champ_name]['wins'] += 1 if win else 0
            stats['champions'][champ_name]['kills'] += player['kills']
            stats['champions'][champ_name]['deaths'] += player['deaths']
            stats['champions'][champ_name]['assists'] += player['assists']

            # Rôle
            stats['roles'][player.get('teamPosition', 'UNKNOWN')] += 1

            # Performance récente
            game_duration_min = info['gameDuration'] / 60
            stats['recent_performance'].append({
                'champion': champ_name,
                'win': win,
                'kda': f"{player['kills']}/{player['deaths']}/{player['assists']}",
                'cs': player['totalMinionsKilled'] + player.get('neutralMinionsKilled', 0),
                'cs_per_min': (player['totalMinionsKilled'] + player.get('neutralMinionsKilled', 0)) / game_duration_min,
                'vision_score': player.get('visionScore', 0),
                'damage': player['totalDamageDealtToChampions'],
                'gold': player['goldEarned']
            })

            # Moyennes
            stats['vision_score_avg'] += player.get('visionScore', 0)
            stats['cs_per_min_avg'] += (player['totalMinionsKilled'] + player.get('neutralMinionsKilled', 0)) / game_duration_min

        # Calcul des moyennes
        if stats['total_games'] > 0:
            stats['winrate'] = (stats['wins'] / stats['total_games']) * 100
            stats['avg_kills'] = statistics.mean(stats['kills'])
            stats['avg_deaths'] = statistics.mean(stats['deaths'])
            stats['avg_assists'] = statistics.mean(stats['assists'])
            stats['kda_avg'] = (stats['avg_kills'] + stats['avg_assists']) / max(stats['avg_deaths'], 1)
            stats['vision_score_avg'] /= stats['total_games']
            stats['cs_per_min_avg'] /= stats['total_games']

        return stats

    def analyze_champion_performance(self, champion_stats: Dict) -> Dict:
        """Analyse la performance sur un champion spécifique"""
        analysis = {}

        for champ, stats in champion_stats.items():
            games = stats['games']
            if games == 0:
                continue

            analysis[champ] = {
                'games': games,
                'winrate': (stats['wins'] / games) * 100,
                'avg_kills': stats['kills'] / games,
                'avg_deaths': stats['deaths'] / games,
                'avg_assists': stats['assists'] / games,
                'kda': (stats['kills'] + stats['assists']) / max(stats['deaths'], 1)
            }

        # Trier par nombre de games
        analysis = dict(sorted(analysis.items(), key=lambda x: x[1]['games'], reverse=True))

        return analysis

    def analyze_enemy_team(self, enemy_players: List[Dict], api) -> Dict:
        """
        Analyse l'équipe adverse pour donner des insights
        """
        analysis = {
            'players': [],
            'threat_level': {},
            'recommendations': []
        }

        for enemy in enemy_players:
            puuid = enemy.get('puuid')
            champion = enemy.get('championName', 'Unknown')

            if not puuid:
                continue

            # Récupérer les infos du joueur
            summoner = api.get_summoner_by_puuid(puuid)
            if not summoner:
                continue

            # Récupérer le rang
            league_entries = api.get_league_entries(summoner['id'])
            rank_info = "Unranked"
            if league_entries:
                ranked_solo = next((e for e in league_entries if e['queueType'] == 'RANKED_SOLO_5x5'), None)
                if ranked_solo:
                    rank_info = f"{ranked_solo['tier']} {ranked_solo['rank']} ({ranked_solo['leaguePoints']} LP)"

            # Récupérer la maîtrise du champion
            masteries = api.get_champion_masteries(puuid, count=10)

            player_analysis = {
                'summoner_name': summoner['name'],
                'champion': champion,
                'rank': rank_info,
                'masteries': []
            }

            if masteries:
                for mastery in masteries[:5]:
                    player_analysis['masteries'].append({
                        'champion_id': mastery['championId'],
                        'level': mastery['championLevel'],
                        'points': mastery['championPoints']
                    })

            analysis['players'].append(player_analysis)

        return analysis

    def get_matchup_advice(self, your_champion: str, enemy_champion: str, your_rank: str) -> List[str]:
        """
        Génère des conseils pour un matchup spécifique
        (À enrichir avec une base de données de matchups)
        """
        advice = [
            f"Matchup : {your_champion} vs {enemy_champion}",
            f"Votre niveau : {your_rank}",
        ]

        # Conseils génériques (à personnaliser avec une vraie DB)
        generic_advice = [
            "Surveillez les cooldowns clés de votre adversaire",
            "Placez des wards pour éviter les ganks",
            "Adaptez votre build en fonction de la composition ennemie",
            "Communiquez avec votre équipe pour les objectifs",
            "Gardez un œil sur la minimap"
        ]

        advice.extend(generic_advice)

        return advice

    def calculate_threat_level(self, player_stats: Dict) -> str:
        """
        Calcule le niveau de menace d'un joueur adverse
        """
        # Logique de calcul basée sur le rang, winrate, etc.
        rank = player_stats.get('rank', 'Unranked')

        if 'CHALLENGER' in rank or 'GRANDMASTER' in rank or 'MASTER' in rank:
            return "TRÈS ÉLEVÉ"
        elif 'DIAMOND' in rank or 'EMERALD' in rank:
            return "ÉLEVÉ"
        elif 'PLATINUM' in rank or 'GOLD' in rank:
            return "MOYEN"
        elif 'SILVER' in rank or 'BRONZE' in rank:
            return "FAIBLE"
        else:
            return "INCONNU"

    def format_performance_report(self, stats: Dict) -> str:
        """Formate un rapport de performance lisible"""
        if not stats:
            return "Aucune donnée disponible"

        report = []
        report.append("\n" + "=" * 60)
        report.append("RAPPORT DE PERFORMANCE")
        report.append("=" * 60)

        report.append(f"\nStatistiques générales ({stats['total_games']} parties) :")
        report.append(f"  • Victoires / Défaites : {stats['wins']}W - {stats['losses']}L")
        report.append(f"  • Winrate : {stats.get('winrate', 0):.1f}%")
        report.append(f"  • KDA moyen : {stats.get('kda_avg', 0):.2f}")
        report.append(f"  • K/D/A : {stats.get('avg_kills', 0):.1f} / {stats.get('avg_deaths', 0):.1f} / {stats.get('avg_assists', 0):.1f}")
        report.append(f"  • CS/min moyen : {stats.get('cs_per_min_avg', 0):.1f}")
        report.append(f"  • Vision score moyen : {stats.get('vision_score_avg', 0):.1f}")

        # Champions les plus joués
        if stats['champions']:
            report.append("\nChampions les plus joués :")
            top_champs = sorted(stats['champions'].items(), key=lambda x: x[1]['games'], reverse=True)[:5]

            for champ, champ_stats in top_champs:
                games = champ_stats['games']
                winrate = (champ_stats['wins'] / games * 100) if games > 0 else 0
                kda = (champ_stats['kills'] + champ_stats['assists']) / max(champ_stats['deaths'], 1)
                report.append(f"  • {champ}: {games} games - {winrate:.1f}% WR - {kda:.2f} KDA")

        # Rôles préférés
        if stats['roles']:
            report.append("\nRôles joués :")
            for role, count in sorted(stats['roles'].items(), key=lambda x: x[1], reverse=True):
                if role and role != 'UNKNOWN':
                    report.append(f"  • {role}: {count} games")

        report.append("=" * 60)

        return "\n".join(report)
