"""
Interface Streamlit pour Coach LoL
Application web moderne avec analyse LLM
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

from riot_api import RiotAPI
from data_analyzer import DataAnalyzer
from live_game_coach import LiveGameCoach
from llm_coach import LLMCoach

# Configuration de la page
st.set_page_config(
    page_title="Coach LoL",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    .threat-high {
        color: #ff4444;
        font-weight: bold;
    }
    .threat-medium {
        color: #ffaa00;
        font-weight: bold;
    }
    .threat-low {
        color: #44ff44;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
        background-color: #667eea;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation de la session state
if 'api' not in st.session_state:
    st.session_state.api = None
if 'llm_coach' not in st.session_state:
    st.session_state.llm_coach = None
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = DataAnalyzer()
if 'current_player' not in st.session_state:
    st.session_state.current_player = None
if 'connected' not in st.session_state:
    st.session_state.connected = False

def init_apis():
    """Initialise les APIs"""
    if st.session_state.api is None:
        # Récupérer depuis les secrets Streamlit
        riot_key = st.secrets.get('RIOT_API_KEY', '')
        region = st.secrets.get('DEFAULT_REGION', 'EUW')
        st.session_state.api = RiotAPI(api_key=riot_key, region=region)

    if st.session_state.llm_coach is None:
        # Récupérer depuis les secrets Streamlit
        openai_key = st.secrets.get('OPENAI_API_KEY', None)
        st.session_state.llm_coach = LLMCoach(api_key=openai_key, provider="openai")

def sidebar_config():
    """Sidebar pour la configuration"""
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/667eea/ffffff?text=Coach+LoL", use_container_width=True)
        st.markdown("---")

        st.header("🔑 Configuration")

        # Afficher le statut des APIs
        with st.expander("📋 Statut des APIs", expanded=True):
            # Vérifier Riot API
            riot_key = st.secrets.get('RIOT_API_KEY', '')
            if riot_key and riot_key != "RGAPI-VOTRE-CLE-ICI":
                st.success("✓ API Riot configurée")
            else:
                st.error("❌ API Riot non configurée")
                st.caption("Éditez le fichier `.streamlit/secrets.toml`")

            # Vérifier OpenAI API
            openai_key = st.secrets.get('OPENAI_API_KEY', '')
            if openai_key and openai_key != "sk-VOTRE-CLE-ICI":
                st.success("✓ Analyse IA activée (OpenAI GPT)")
            else:
                st.warning("⚠️ Analyse IA désactivée (optionnel)")
                st.caption("Ajoutez OPENAI_API_KEY dans `.streamlit/secrets.toml`")

            # Afficher la région
            region = st.secrets.get('DEFAULT_REGION', 'EUW')
            st.info(f"🌍 Région : {region}")

            st.caption("💡 Modèle IA : GPT-4o (analyse professionnelle niveau Challenger)")
            st.caption("📝 Pour modifier la configuration, éditez `.streamlit/secrets.toml`")

        st.markdown("---")

        # Connexion joueur
        st.header("👤 Connexion")

        if not st.session_state.connected:
            game_name = st.text_input("Nom d'invocateur", placeholder="Faker")
            tag_line = st.text_input("Tag", placeholder="KR1")

            if st.button("🔌 Se connecter"):
                with st.spinner("Connexion en cours..."):
                    init_apis()
                    account = st.session_state.api.get_account_by_riot_id(game_name, tag_line)

                    if account:
                        st.session_state.current_player = account
                        st.session_state.connected = True
                        st.success(f"✓ Connecté : {account['gameName']}#{account['tagLine']}")
                        st.rerun()
                    else:
                        st.error("❌ Compte introuvable. Vérifiez votre clé API et vos identifiants.")
        else:
            player = st.session_state.current_player
            st.success(f"✓ Connecté")
            st.write(f"**{player['gameName']}#{player['tagLine']}**")

            if st.button("🚪 Déconnexion"):
                st.session_state.connected = False
                st.session_state.current_player = None
                st.rerun()

        st.markdown("---")
        st.markdown("### 📚 Liens utiles")
        st.markdown("[API Riot](https://developer.riotgames.com/)")
        st.markdown("[API OpenAI](https://platform.openai.com/api-keys)")
        st.markdown("[Tarifs OpenAI](https://openai.com/api/pricing/)")

def main_page():
    """Page principale"""
    st.markdown('<div class="main-header">🎮 Coach LoL - Analyseur IA</div>', unsafe_allow_html=True)

    if not st.session_state.connected:
        st.info("👈 Configurez vos API et connectez-vous pour commencer")
        st.markdown("---")

        # Guide de démarrage
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🚀 Démarrage rapide")
            st.markdown("""
            1. **Obtenez votre clé API Riot**
               - Allez sur [developer.riotgames.com](https://developer.riotgames.com/)
               - Connectez-vous et générez une clé (gratuit, 24h)

            2. **Configurez l'API IA (optionnel)**
               - Clé OpenAI pour l'analyse IA avec GPT
               - [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
               - Gratuit : $5 de crédit au début

            3. **Connectez-vous**
               - Entrez votre nom d'invocateur et tag
               - Exemple : Faker#KR1
            """)

        with col2:
            st.markdown("### ✨ Fonctionnalités")
            st.markdown("""
            **📊 Analyse d'historique**
            - Statistiques complètes
            - Performance par champion
            - Visualisations interactives

            **🎯 Analyse pré-game**
            - Infos sur les adversaires
            - Niveau de menace
            - Conseils stratégiques IA

            **🤖 Coach IA**
            - Analyse personnalisée
            - Conseils adaptés à votre niveau
            - Recommandations tactiques
            """)

        return

    # Onglets principaux
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Mon Historique",
        "🎯 Analyse Pré-Game",
        "🏆 Statistiques Champions",
        "💡 Conseils IA"
    ])

    with tab1:
        show_match_history()

    with tab2:
        show_pregame_analysis()

    with tab3:
        show_champion_stats()

    with tab4:
        show_llm_tips()

def show_match_history():
    """Onglet d'analyse d'historique"""
    st.header("📊 Analyse de votre historique")

    col1, col2 = st.columns([3, 1])

    with col1:
        nb_matches = st.slider("Nombre de parties à analyser", 5, 50, 20)

    with col2:
        analyze_btn = st.button("🔍 Analyser")

    if analyze_btn:
        with st.spinner("📥 Récupération des données..."):
            init_apis()
            puuid = st.session_state.current_player['puuid']

            # Récupérer les matchs
            match_ids = st.session_state.api.get_match_history(puuid, count=nb_matches)

            if not match_ids:
                st.error("Aucune partie trouvée")
                return

            # Récupérer les détails
            progress_bar = st.progress(0)
            matches = []

            for i, match_id in enumerate(match_ids):
                match_detail = st.session_state.api.get_match_details(match_id)
                if match_detail:
                    matches.append(match_detail)
                progress_bar.progress((i + 1) / len(match_ids))

            progress_bar.empty()

            # Analyser
            stats = st.session_state.analyzer.analyze_match_history(matches, puuid)
            st.session_state.stats = stats

            # Afficher les métriques
            st.markdown("### 📈 Statistiques Générales")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Parties", stats['total_games'])
                st.metric("Winrate", f"{stats.get('winrate', 0):.1f}%")

            with col2:
                st.metric("Victoires", stats['wins'], delta=f"+{stats['wins']}")
                st.metric("Défaites", stats['losses'], delta=f"-{stats['losses']}")

            with col3:
                st.metric("KDA Moyen", f"{stats.get('kda_avg', 0):.2f}")
                st.metric("CS/min", f"{stats.get('cs_per_min_avg', 0):.1f}")

            with col4:
                st.metric("Kills", f"{stats.get('avg_kills', 0):.1f}")
                st.metric("Deaths", f"{stats.get('avg_deaths', 0):.1f}")

            # Graphiques
            st.markdown("---")
            col1, col2 = st.columns(2)

            with col1:
                # Graphique Winrate
                fig_wr = go.Figure(data=[
                    go.Pie(
                        labels=['Victoires', 'Défaites'],
                        values=[stats['wins'], stats['losses']],
                        marker=dict(colors=['#44ff44', '#ff4444']),
                        hole=0.4
                    )
                ])
                fig_wr.update_layout(title="Répartition Victoires/Défaites")
                st.plotly_chart(fig_wr, use_container_width=True)

            with col2:
                # Top champions
                if stats.get('champions'):
                    top_champs = sorted(stats['champions'].items(),
                                      key=lambda x: x[1]['games'], reverse=True)[:5]
                    champ_names = [c[0] for c in top_champs]
                    champ_games = [c[1]['games'] for c in top_champs]

                    fig_champs = go.Figure(data=[
                        go.Bar(x=champ_names, y=champ_games, marker_color='#667eea')
                    ])
                    fig_champs.update_layout(title="Top 5 Champions (parties jouées)")
                    st.plotly_chart(fig_champs, use_container_width=True)

            # Analyse LLM
            if st.session_state.llm_coach and st.session_state.llm_coach.is_available():
                st.markdown("---")
                st.markdown("### 🤖 Analyse IA de vos performances")

                # Utiliser un hash des stats pour détecter les changements
                import json
                stats_hash = hash(json.dumps(stats, sort_keys=True, default=str))

                # Générer l'analyse si pas déjà en cache
                if 'performance_analysis' not in st.session_state or st.session_state.get('last_analysis_hash') != stats_hash:
                    with st.spinner("🧠 Analyse en cours par l'IA..."):
                        player_name = st.session_state.current_player['gameName']
                        analysis_result = st.session_state.llm_coach.analyze_player_performance(stats, player_name)

                        # Debug: afficher le type et la longueur
                        st.write(f"DEBUG - Type: {type(analysis_result)}, Longueur: {len(analysis_result) if analysis_result else 0}")
                        st.write(f"DEBUG - Début du contenu: {repr(analysis_result[:200]) if analysis_result else 'None'}")

                        if analysis_result and len(analysis_result) > 0:
                            st.session_state.performance_analysis = analysis_result
                            st.session_state.last_analysis_hash = stats_hash
                        else:
                            st.session_state.performance_analysis = f"❌ L'analyse a retourné un résultat vide (type={type(analysis_result)}, len={len(analysis_result) if analysis_result else 0})"

                # Afficher l'analyse
                if st.session_state.get('performance_analysis'):
                    # Vérifier si c'est une erreur
                    if st.session_state.performance_analysis.startswith("❌"):
                        st.error(st.session_state.performance_analysis)
                    else:
                        st.markdown(st.session_state.performance_analysis)
                else:
                    st.warning("⚠️ L'analyse n'a pas pu être générée")

def show_pregame_analysis():
    """Onglet d'analyse pré-game"""
    st.header("🎯 Analyse Pré-Game")

    st.info("📌 Cette fonctionnalité analyse vos adversaires lorsque vous êtes en partie")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Comment ça marche ?")
        st.markdown("""
        1. Lancez une partie dans League of Legends
        2. Pendant la sélection de champions, cliquez sur "Analyser"
        3. Le coach récupère les infos de vos adversaires
        4. Vous recevez une analyse détaillée avec l'IA
        """)

    with col2:
        if st.button("🔍 Analyser la partie en cours", use_container_width=True):
            with st.spinner("Recherche d'une partie active..."):
                init_apis()
                puuid = st.session_state.current_player['puuid']
                live_coach = LiveGameCoach(st.session_state.api)

                game = live_coach.check_for_active_game(puuid)

                if not game:
                    st.warning("❌ Vous n'êtes pas en partie actuellement")
                    st.info("💡 Lancez une partie dans LoL puis revenez ici")
                else:
                    st.success("✓ Partie détectée !")

                    with st.spinner("🔬 Analyse de l'équipe adverse..."):
                        analysis = live_coach.analyze_pregame(game, puuid)
                        st.session_state.pregame_analysis = analysis

                    # Afficher l'analyse
                    st.markdown("---")
                    st.markdown("### 👥 Équipe Adverse")

                    enemy_analysis = analysis.get('enemy_analysis', {})

                    for summoner_name, data in enemy_analysis.items():
                        with st.expander(f"🔹 {summoner_name}", expanded=True):
                            col1, col2, col3 = st.columns(3)

                            with col1:
                                st.markdown(f"**Rang:** {data.get('rank', 'Unknown')}")
                                threat = data.get('threat_level', 'UNKNOWN')
                                st.markdown(f"**Menace:** {threat}")

                            with col2:
                                if data.get('wins') and data.get('losses'):
                                    st.markdown(f"**Record:** {data['wins']}W - {data['losses']}L")
                                    st.markdown(f"**Winrate:** {data.get('winrate', 0):.1f}%")

                            with col3:
                                stats = data.get('stats', {})
                                if stats:
                                    st.markdown(f"**KDA:** {stats.get('kda_avg', 0):.2f}")
                                    st.markdown(f"**Forme:** {stats.get('wins', 0)}W - {stats.get('losses', 0)}L")

                    # Analyse LLM
                    if st.session_state.llm_coach and st.session_state.llm_coach.is_available():
                        st.markdown("---")
                        st.markdown("### 🤖 Analyse Stratégique IA")

                        # Générer l'analyse si pas déjà en cache pour cette game
                        if 'pregame_llm_analysis' not in st.session_state or st.session_state.get('last_pregame_analysis') != analysis:
                            with st.spinner("🧠 Génération des conseils..."):
                                player_name = st.session_state.current_player['gameName']
                                st.session_state.pregame_llm_analysis = st.session_state.llm_coach.analyze_pregame(
                                    analysis, player_name
                                )
                                st.session_state.last_pregame_analysis = analysis

                        # Afficher l'analyse
                        if st.session_state.get('pregame_llm_analysis'):
                            if st.session_state.pregame_llm_analysis.startswith("❌"):
                                st.error(st.session_state.pregame_llm_analysis)
                            else:
                                st.markdown(st.session_state.pregame_llm_analysis)
                        else:
                            st.warning("⚠️ L'analyse n'a pas pu être générée")

def show_champion_stats():
    """Onglet des statistiques par champion"""
    st.header("🏆 Statistiques par Champion")

    nb_matches = st.slider("Nombre de parties", 10, 100, 50, key="champ_matches")

    if st.button("📊 Analyser mes champions", use_container_width=True):
        with st.spinner("Analyse en cours..."):
            init_apis()
            puuid = st.session_state.current_player['puuid']

            # Récupérer les matchs
            match_ids = st.session_state.api.get_match_history(puuid, count=nb_matches)
            matches = []

            progress_bar = st.progress(0)
            for i, match_id in enumerate(match_ids):
                match_detail = st.session_state.api.get_match_details(match_id)
                if match_detail:
                    matches.append(match_detail)
                progress_bar.progress((i + 1) / len(match_ids))

            progress_bar.empty()

            # Analyser
            stats = st.session_state.analyzer.analyze_match_history(matches, puuid)
            champion_analysis = st.session_state.analyzer.analyze_champion_performance(
                stats['champions']
            )

            # Créer un DataFrame
            df_data = []
            for champ, champ_stats in champion_analysis.items():
                df_data.append({
                    'Champion': champ,
                    'Parties': champ_stats['games'],
                    'Winrate (%)': round(champ_stats['winrate'], 1),
                    'KDA': round(champ_stats['kda'], 2),
                    'Kills': round(champ_stats['avg_kills'], 1),
                    'Deaths': round(champ_stats['avg_deaths'], 1),
                    'Assists': round(champ_stats['avg_assists'], 1)
                })

            df = pd.DataFrame(df_data)

            # Afficher le tableau
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Winrate (%)": st.column_config.ProgressColumn(
                        "Winrate (%)",
                        format="%.1f%%",
                        min_value=0,
                        max_value=100,
                    ),
                }
            )

            # Graphiques
            col1, col2 = st.columns(2)

            with col1:
                # Winrate par champion
                fig_wr = px.bar(
                    df.head(10),
                    x='Champion',
                    y='Winrate (%)',
                    title='Winrate par Champion (Top 10)',
                    color='Winrate (%)',
                    color_continuous_scale='RdYlGn'
                )
                st.plotly_chart(fig_wr, use_container_width=True)

            with col2:
                # KDA par champion
                fig_kda = px.bar(
                    df.head(10),
                    x='Champion',
                    y='KDA',
                    title='KDA par Champion (Top 10)',
                    color='KDA',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_kda, use_container_width=True)

def show_llm_tips():
    """Onglet des conseils IA"""
    st.header("💡 Coach IA Personnel")

    if not st.session_state.llm_coach or not st.session_state.llm_coach.is_available():
        st.warning("⚠️ Configurez votre clé API OpenAI dans la sidebar pour activer cette fonctionnalité")
        st.info("💰 OpenAI offre $5 de crédit gratuit = ~125 analyses PRO avec GPT-4o (~4¢/analyse)")
        return

    st.markdown("### 🎯 Obtenez des conseils personnalisés")

    # Sélection du type de conseil
    tip_type = st.selectbox(
        "Type de conseil",
        ["Conseil général", "Analyse de matchup", "Conseil rapide"]
    )

    if tip_type == "Analyse de matchup":
        col1, col2 = st.columns(2)

        with col1:
            your_champ = st.text_input("Votre champion", placeholder="Yasuo")

        with col2:
            enemy_champ = st.text_input("Champion adverse", placeholder="Zed")

        your_rank = st.text_input("Votre rang", placeholder="Gold II")

        if st.button("🧠 Analyser le matchup"):
            with st.spinner("Analyse du matchup..."):
                st.session_state.matchup_analysis = st.session_state.llm_coach.analyze_champion_matchup(
                    your_champ, enemy_champ, your_rank
                )

        # Afficher l'analyse si elle existe
        if 'matchup_analysis' in st.session_state and st.session_state.matchup_analysis:
            if st.session_state.matchup_analysis.startswith("❌"):
                st.error(st.session_state.matchup_analysis)
            else:
                st.markdown(st.session_state.matchup_analysis)

    elif tip_type == "Conseil rapide":
        context = st.text_area(
            "Décrivez votre situation",
            placeholder="Je suis en lane contre un Darius, je joue Teemo..."
        )

        if st.button("💡 Obtenir un conseil"):
            with st.spinner("Génération du conseil..."):
                tip = st.session_state.llm_coach.get_quick_tip(context)
                st.info(tip)

    else:
        st.markdown("""
        ### 📚 Conseils Généraux

        Utilisez les autres onglets pour obtenir des analyses détaillées :
        - **Mon Historique** : Analyse complète de vos performances
        - **Analyse Pré-Game** : Conseils pour votre prochaine partie
        - **Statistiques Champions** : Identifiez vos points forts

        Le Coach IA vous donnera des conseils personnalisés basés sur vos données réelles !
        """)

# Lancer l'application
if __name__ == "__main__":
    sidebar_config()
    main_page()
