"""
Module pour interagir avec l'API Riot Games
"""
import requests
import time
import os
from typing import Dict, List, Optional

# Constantes définies dans le module (indépendant de config.py)
REGIONS = {
    'EUW': 'euw1',
    'EUN': 'eun1',
    'NA': 'na1',
    'KR': 'kr',
    'BR': 'br1',
    'JP': 'jp1',
    'LA1': 'la1',
    'LA2': 'la2',
    'OC': 'oc1',
    'TR': 'tr1',
    'RU': 'ru'
}

ROUTING = {
    'EUW': 'europe',
    'EUN': 'europe',
    'NA': 'americas',
    'BR': 'americas',
    'LA1': 'americas',
    'LA2': 'americas',
    'KR': 'asia',
    'JP': 'asia',
    'OC': 'sea',
    'TR': 'europe',
    'RU': 'europe'
}

API_BASE_URL = 'https://{region}.api.riotgames.com'
CONTINENTAL_BASE_URL = 'https://{routing}.api.riotgames.com'

class RiotAPI:
    def __init__(self, api_key: str = None, region: str = 'EUW'):
        self.api_key = api_key or os.getenv('RIOT_API_KEY', '')
        self.region = REGIONS.get(region, REGIONS['EUW'])
        self.routing = ROUTING.get(region, 'europe')
        self.headers = {
            'X-Riot-Token': self.api_key
        }

    def _make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """Effectue une requête à l'API avec gestion des erreurs"""
        try:
            response = requests.get(url, headers=self.headers, params=params)

            # Gestion du rate limiting
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 1))
                print(f"Rate limit atteint. Attente de {retry_after} secondes...")
                time.sleep(retry_after)
                return self._make_request(url, params)

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête : {e}")
            return None

    def get_summoner_by_name(self, summoner_name: str, tag: str = None) -> Optional[Dict]:
        """
        Récupère les informations d'un invocateur par son nom
        Note: Depuis 2023, il faut utiliser Riot ID (nom#tag)
        """
        # Nouvelle API avec Riot ID
        if tag:
            url = f"{CONTINENTAL_BASE_URL.format(routing=self.routing)}/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag}"
            account = self._make_request(url)

            if account:
                # Récupère les infos du summoner avec le PUUID
                return self.get_summoner_by_puuid(account['puuid'])

        return None

    def get_summoner_by_puuid(self, puuid: str) -> Optional[Dict]:
        """Récupère les informations d'un invocateur par son PUUID"""
        url = f"{API_BASE_URL.format(region=self.region)}/lol/summoner/v4/summoners/by-puuid/{puuid}"
        return self._make_request(url)

    def get_account_by_riot_id(self, game_name: str, tag_line: str) -> Optional[Dict]:
        """Récupère le compte Riot par Riot ID (nom#tag)"""
        url = f"{CONTINENTAL_BASE_URL.format(routing=self.routing)}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        return self._make_request(url)

    def get_match_history(self, puuid: str, count: int = 20, queue: int = None) -> Optional[List[str]]:
        """
        Récupère l'historique des matchs d'un joueur
        queue: 420 = Ranked Solo, 440 = Ranked Flex, 400 = Normal Draft, etc.
        """
        url = f"{CONTINENTAL_BASE_URL.format(routing=self.routing)}/lol/match/v5/matches/by-puuid/{puuid}/ids"
        params = {'count': count}
        if queue:
            params['queue'] = queue

        return self._make_request(url, params)

    def get_match_details(self, match_id: str) -> Optional[Dict]:
        """Récupère les détails d'un match spécifique"""
        url = f"{CONTINENTAL_BASE_URL.format(routing=self.routing)}/lol/match/v5/matches/{match_id}"
        return self._make_request(url)

    def get_league_entries(self, summoner_id: str) -> Optional[List[Dict]]:
        """Récupère les entrées de classement d'un joueur"""
        url = f"{API_BASE_URL.format(region=self.region)}/lol/league/v4/entries/by-summoner/{summoner_id}"
        return self._make_request(url)

    def get_current_game(self, puuid: str) -> Optional[Dict]:
        """Récupère les informations de la partie en cours"""
        # D'abord récupérer le summoner ID
        summoner = self.get_summoner_by_puuid(puuid)
        if not summoner:
            return None

        url = f"{API_BASE_URL.format(region=self.region)}/lol/spectator/v5/active-games/by-summoner/{puuid}"
        return self._make_request(url)

    def get_champion_masteries(self, puuid: str, count: int = None) -> Optional[List[Dict]]:
        """Récupère les maîtrises de champion d'un joueur"""
        url = f"{API_BASE_URL.format(region=self.region)}/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}"
        params = {}
        if count:
            params['count'] = count

        return self._make_request(url, params)


if __name__ == "__main__":
    # Test de l'API
    api = RiotAPI()

    # Exemple d'utilisation
    print("Test de l'API Riot Games")
    print("=" * 50)

    # Remplacez par votre Riot ID
    game_name = "VOTRE_NOM"
    tag_line = "EUW"  # ou votre tag

    print(f"Recherche du compte : {game_name}#{tag_line}")
    account = api.get_account_by_riot_id(game_name, tag_line)

    if account:
        print(f"✓ Compte trouvé : {account['gameName']}#{account['tagLine']}")
        print(f"  PUUID : {account['puuid']}")
    else:
        print("✗ Compte non trouvé. Vérifiez votre clé API et vos identifiants.")
