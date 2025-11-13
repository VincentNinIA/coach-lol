"""
Coach LoL - Application principale
Interface en ligne de commande pour analyser vos performances et obtenir des conseils
"""
import sys
from riot_api import RiotAPI
from data_analyzer import DataAnalyzer
from live_game_coach import LiveGameCoach

class CoachLoL:
    def __init__(self):
        self.api = None
        self.analyzer = DataAnalyzer()
        self.live_coach = None
        self.current_player = None

    def display_menu(self):
        """Affiche le menu principal"""
        print("\n" + "=" * 60)
        print("🎮 COACH LOL - Menu Principal")
        print("=" * 60)
        print("\n1. 🔑 Configurer l'API et se connecter")
        print("2. 📊 Analyser mon historique de parties")
        print("3. 🏆 Voir mes statistiques par champion")
        print("4. 🎯 Surveillance de partie (analyse pré-game)")
        print("5. 🔍 Analyser une partie en cours")
        print("6. ❓ Aide")
        print("0. 🚪 Quitter")
        print("\n" + "=" * 60)

    def setup_api(self):
        """Configure l'API et authentifie le joueur"""
        print("\n🔑 Configuration de l'API Riot Games")
        print("-" * 60)

        api_key = input("Entrez votre clé API Riot (ou appuyez sur Entrée pour utiliser celle du config.py) : ").strip()

        if not api_key:
            # Utiliser la clé du config
            from config import RIOT_API_KEY
            api_key = RIOT_API_KEY

        region = input("Entrez votre région (EUW/NA/KR/etc.) [défaut: EUW] : ").strip().upper() or "EUW"

        self.api = RiotAPI(api_key=api_key, region=region)
        self.live_coach = LiveGameCoach(self.api)

        print("\n🎮 Connexion à votre compte...")
        print("-" * 60)

        game_name = input("Entrez votre nom d'invocateur : ").strip()
        tag_line = input("Entrez votre tag (ex: EUW, 1234, etc.) : ").strip()

        account = self.api.get_account_by_riot_id(game_name, tag_line)

        if account:
            self.current_player = account
            print(f"\n✓ Connecté en tant que : {account['gameName']}#{account['tagLine']}")
            print(f"  PUUID : {account['puuid'][:20]}...")
            return True
        else:
            print("\n✗ Erreur : Impossible de trouver le compte.")
            print("Vérifiez votre clé API, votre nom d'invocateur et votre tag.")
            return False

    def analyze_match_history(self):
        """Analyse l'historique de matchs du joueur"""
        if not self.current_player:
            print("\n⚠️  Vous devez d'abord vous connecter (option 1)")
            return

        print("\n📊 Analyse de l'historique de parties")
        print("-" * 60)

        count = input("Nombre de parties à analyser [défaut: 20] : ").strip()
        count = int(count) if count.isdigit() else 20

        print(f"\n🔍 Récupération de {count} parties...")
        match_ids = self.api.get_match_history(self.current_player['puuid'], count=count)

        if not match_ids:
            print("✗ Aucune partie trouvée")
            return

        print(f"✓ {len(match_ids)} parties trouvées")
        print("📥 Téléchargement des détails des matchs...")

        matches = []
        for i, match_id in enumerate(match_ids, 1):
            print(f"  Partie {i}/{len(match_ids)}...", end='\r')
            match_detail = self.api.get_match_details(match_id)
            if match_detail:
                matches.append(match_detail)

        print(f"\n✓ {len(matches)} parties analysées")
        print("\n🔬 Analyse des statistiques en cours...")

        stats = self.analyzer.analyze_match_history(matches, self.current_player['puuid'])
        report = self.analyzer.format_performance_report(stats)

        print(report)

        # Sauvegarder le rapport
        save = input("\n💾 Sauvegarder le rapport dans un fichier ? (o/n) : ").strip().lower()
        if save == 'o':
            filename = f"rapport_{self.current_player['gameName']}_{count}_parties.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✓ Rapport sauvegardé dans {filename}")

    def analyze_champion_stats(self):
        """Affiche les statistiques par champion"""
        if not self.current_player:
            print("\n⚠️  Vous devez d'abord vous connecter (option 1)")
            return

        print("\n🏆 Analyse des statistiques par champion")
        print("-" * 60)

        count = input("Nombre de parties à analyser [défaut: 50] : ").strip()
        count = int(count) if count.isdigit() else 50

        print(f"\n🔍 Récupération de {count} parties...")
        match_ids = self.api.get_match_history(self.current_player['puuid'], count=count)

        if not match_ids:
            print("✗ Aucune partie trouvée")
            return

        matches = []
        for i, match_id in enumerate(match_ids, 1):
            print(f"  Partie {i}/{len(match_ids)}...", end='\r')
            match_detail = self.api.get_match_details(match_id)
            if match_detail:
                matches.append(match_detail)

        print(f"\n✓ Analyse des champions...")

        stats = self.analyzer.analyze_match_history(matches, self.current_player['puuid'])
        champion_analysis = self.analyzer.analyze_champion_performance(stats['champions'])

        print("\n" + "=" * 60)
        print("🏆 STATISTIQUES PAR CHAMPION")
        print("=" * 60)

        for i, (champ, champ_stats) in enumerate(champion_analysis.items(), 1):
            print(f"\n{i}. {champ}")
            print(f"   Parties : {champ_stats['games']}")
            print(f"   Winrate : {champ_stats['winrate']:.1f}%")
            print(f"   KDA moyen : {champ_stats['kda']:.2f}")
            print(f"   K/D/A : {champ_stats['avg_kills']:.1f} / {champ_stats['avg_deaths']:.1f} / {champ_stats['avg_assists']:.1f}")

        print("\n" + "=" * 60)

    def monitor_game(self):
        """Surveille le démarrage d'une partie"""
        if not self.current_player:
            print("\n⚠️  Vous devez d'abord vous connecter (option 1)")
            return

        print("\n🎯 Mode surveillance de partie")
        print("-" * 60)
        print("Le coach va surveiller le début de votre prochaine partie")
        print("et analyser automatiquement l'équipe adverse.")

        self.live_coach.monitor_game_start(self.current_player['puuid'], check_interval=10)

    def analyze_current_game(self):
        """Analyse une partie en cours"""
        if not self.current_player:
            print("\n⚠️  Vous devez d'abord vous connecter (option 1)")
            return

        print("\n🔍 Analyse de la partie en cours")
        print("-" * 60)

        print("Recherche d'une partie active...")
        game = self.live_coach.check_for_active_game(self.current_player['puuid'])

        if not game:
            print("✗ Vous n'êtes pas en partie actuellement")
            print("💡 Utilisez l'option 4 pour surveiller le démarrage d'une partie")
            return

        print("✓ Partie active trouvée !")
        print("🔬 Analyse en cours...\n")

        analysis = self.live_coach.analyze_pregame(game, self.current_player['puuid'])
        report = self.live_coach.format_pregame_report(analysis)

        print(report)

    def show_help(self):
        """Affiche l'aide"""
        print("\n" + "=" * 60)
        print("❓ AIDE - COACH LOL")
        print("=" * 60)
        print("\n📋 Comment utiliser Coach LoL :")
        print("\n1. Obtenez une clé API Riot Games :")
        print("   → Allez sur https://developer.riotgames.com/")
        print("   → Connectez-vous avec votre compte Riot")
        print("   → Générez une clé de développement (valable 24h)")
        print("   → Copiez la clé dans config.py ou entrez-la au démarrage")

        print("\n2. Configurez votre connexion (option 1) :")
        print("   → Entrez votre clé API")
        print("   → Sélectionnez votre région (EUW, NA, KR, etc.)")
        print("   → Entrez votre nom d'invocateur et tag")

        print("\n3. Utilisez les fonctionnalités :")
        print("   → Option 2 : Analysez votre historique de parties")
        print("   → Option 3 : Consultez vos stats par champion")
        print("   → Option 4 : Surveillez le début d'une partie (analyse auto)")
        print("   → Option 5 : Analysez une partie déjà en cours")

        print("\n💡 Conseils :")
        print("   • La clé API de développement est gratuite mais limitée")
        print("   • Évitez de faire trop de requêtes trop rapidement")
        print("   • L'analyse pré-game prend 15-30 secondes")
        print("   • Plus vous analysez de parties, plus les stats sont précises")

        print("\n🔗 Liens utiles :")
        print("   • Documentation API Riot : https://developer.riotgames.com/docs/lol")
        print("   • Rate limits : https://developer.riotgames.com/docs/portal#web-apis_rate-limiting")

        print("\n" + "=" * 60)

    def run(self):
        """Lance l'application"""
        print("\n" + "🎮" * 20)
        print("\n   BIENVENUE SUR COACH LOL")
        print("   Améliorez votre gameplay avec l'analyse de données\n")
        print("🎮" * 20)

        while True:
            self.display_menu()
            choice = input("\nVotre choix : ").strip()

            if choice == '1':
                self.setup_api()
            elif choice == '2':
                self.analyze_match_history()
            elif choice == '3':
                self.analyze_champion_stats()
            elif choice == '4':
                self.monitor_game()
            elif choice == '5':
                self.analyze_current_game()
            elif choice == '6':
                self.show_help()
            elif choice == '0':
                print("\n👋 Merci d'avoir utilisé Coach LoL !")
                print("Bonne chance sur la Faille de l'invocateur ! 🏆\n")
                sys.exit(0)
            else:
                print("\n❌ Choix invalide. Veuillez réessayer.")

            input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    try:
        coach = CoachLoL()
        coach.run()
    except KeyboardInterrupt:
        print("\n\n👋 Programme interrompu. À bientôt !")
        sys.exit(0)
