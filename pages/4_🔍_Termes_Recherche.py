"""
Page Termes de Recherche - Mode Scripts (sans API)
"""

import streamlit as st
import pandas as pd
from datetime import datetime

from config.settings import STREAMLIT_CONFIG
from config.i18n import t, init_language
from modules.script_data_loader import script_loader
from utils.ui_helpers import load_custom_css, init_theme
from components.sidebar import render_custom_sidebar, hide_default_navigation
from components.topbar import render_topbar, TOPBAR_CSS


# ============================================================================
# CONFIGURATION
# ============================================================================

st.set_page_config(**STREAMLIT_CONFIG)
load_custom_css()
hide_default_navigation()
init_language()
init_theme()
st.markdown(TOPBAR_CSS, unsafe_allow_html=True)
render_topbar()


# ============================================================================
# FONCTIONS
# ============================================================================

def check_data():
    """Vérifie si des données sont disponibles"""
    if not script_loader.data_exists():
        st.error("❌ Aucune donnée disponible")
        if st.button("⚙️ Aller à la configuration"):
            st.switch_page("pages/0_⚙️_Configuration_Simple.py")
        st.stop()


# ============================================================================
# PAGE PRINCIPALE
# ============================================================================

def main():
    """Page principale"""

    check_data()

    st.title("Termes de recherche")

    st.info(
        "**Requêtes exactes déclenchées par vos annonces.** "
        "Utilisez cette vue pour identifier les opportunités et les mots-clés négatifs."
    )

    # Infos compte
    account_info = script_loader.get_account_info()
    currency = account_info.get('currency', 'EUR') if account_info else 'EUR'

    # Charger les termes de recherche
    search_terms = script_loader.get_search_terms()

    if not search_terms:
        st.warning("⚠️ Aucun terme de recherche disponible")
        st.info("Les termes de recherche s'accumulent au fil du temps. Revenez dans quelques jours.")
        return

    # Convertir en DataFrame
    df = pd.DataFrame(search_terms)

    st.subheader(f"{len(df)} termes de recherche (30 derniers jours)")

    # Statistiques globales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👁️ Impressions totales", f"{df['impressions'].sum():,.0f}")

    with col2:
        st.metric("🖱️ Clics totaux", f"{df['clicks'].sum():,.0f}")

    with col3:
        st.metric("💰 Coût total", f"{df['cost'].sum():,.2f} {currency}")

    with col4:
        st.metric("🎯 Conversions totales", f"{df['conversions'].sum():,.0f}")

    # Filtres
    st.subheader("Filtres")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Filtre par campagne
        campaigns = df['campaignName'].unique()
        selected_campaigns = st.multiselect(
            "Campagnes",
            options=campaigns,
            default=campaigns
        )

    with col2:
        # Filtre par nombre de clics minimum
        min_clicks = st.number_input(
            "Clics minimum",
            min_value=0,
            value=0,
            help="Afficher uniquement les termes ayant au moins X clics"
        )

    with col3:
        # Recherche textuelle
        search_query = st.text_input(
            "🔍 Rechercher un terme",
            placeholder="Ex: logiciel, formation, gratuit...",
            help="Recherche dans les termes de recherche"
        )

    # Appliquer les filtres
    df_filtered = df.copy()

    if selected_campaigns:
        df_filtered = df_filtered[df_filtered['campaignName'].isin(selected_campaigns)]

    if min_clicks > 0:
        df_filtered = df_filtered[df_filtered['clicks'] >= min_clicks]

    if search_query:
        df_filtered = df_filtered[
            df_filtered['query'].str.contains(search_query, case=False, na=False)
        ]

    # Trier par clics (desc)
    df_filtered = df_filtered.sort_values('clicks', ascending=False)

    st.write(f"**{len(df_filtered)} terme(s) affiché(s)**")

    # Options d'affichage
    view_mode = st.radio(
        "Mode d'affichage",
        options=["📋 Tableau détaillé", "📊 Top 20 termes"],
        horizontal=True
    )

    if view_mode == "📊 Top 20 termes":
        # Affichage Top 20
        df_top = df_filtered.head(20)

        for idx, term in df_top.iterrows():
            query = term['query']
            clicks = term['clicks']
            impressions = term['impressions']
            ctr = (clicks / impressions * 100) if impressions > 0 else 0
            cost = term['cost']
            conversions = term['conversions']

            # Déterminer la couleur selon les métriques
            if conversions > 0:
                color = "🟢"  # Vert = conversions
            elif clicks >= 5:
                color = "🟡"  # Jaune = beaucoup de clics
            else:
                color = "⚪"  # Blanc = peu de données

            # Détecter les mots suspects
            is_suspect = any(word in query.lower() for word in [
                'gratuit', 'free', 'emploi', 'job', 'formation', 'training',
                'stage', 'internship', 'cours', 'course', 'pdf', 'télécharger'
            ])

            with st.expander(
                f"{color} **{query}** - {clicks} clics • {cost:.2f} {currency}"
                + (" ⚠️" if is_suspect else "")
            ):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write("**Campagne**")
                    st.write(term['campaignName'])

                    st.write("**Volume**")
                    st.write(f"👁️ Impressions : {impressions:,.0f}")
                    st.write(f"🖱️ Clics : {clicks:,.0f}")
                    st.write(f"📊 CTR : {ctr:.2f}%")

                with col2:
                    st.write("**Coûts**")
                    st.write(f"💰 Coût : {cost:.2f} {currency}")

                    if clicks > 0:
                        cpc = cost / clicks
                        st.write(f"💵 CPC : {cpc:.2f} {currency}")

                with col3:
                    st.write("**Conversions**")
                    st.write(f"🎯 Conversions : {conversions:,.0f}")

                    if conversions > 0:
                        conv_rate = (conversions / clicks * 100) if clicks > 0 else 0
                        cpa = cost / conversions
                        st.write(f"📈 Taux : {conv_rate:.2f}%")
                        st.write(f"💰 CPA : {cpa:.2f} {currency}")

                # Alertes
                if is_suspect:
                    st.warning(
                        "⚠️ **Terme suspect** : Ce terme pourrait attirer du trafic non qualifié. "
                        "Envisagez de l'ajouter en mot-clé négatif si les performances sont mauvaises."
                    )

                if clicks >= 10 and conversions == 0:
                    st.error(
                        "🔴 **Aucune conversion** : Ce terme génère des clics mais aucune conversion. "
                        "Considérez l'ajout en négatif."
                    )

                if ctr < 1 and impressions > 100:
                    st.info(
                        "ℹ️ **CTR faible** : Ce terme a un faible taux de clic. "
                        "Vérifiez la pertinence avec votre annonce."
                    )

    else:
        # Affichage tableau
        # Préparer les colonnes à afficher
        display_df = df_filtered[[
            'query', 'campaignName', 'impressions', 'clicks',
            'ctr', 'cost', 'conversions'
        ]].copy()

        # Renommer les colonnes
        display_df.columns = [
            'Terme de recherche', 'Campagne', 'Impressions', 'Clics',
            'CTR (%)', f'Coût ({currency})', 'Conversions'
        ]

        # Formater les nombres
        display_df['Impressions'] = display_df['Impressions'].apply(lambda x: f"{x:,.0f}")
        display_df['Clics'] = display_df['Clics'].apply(lambda x: f"{x:,.0f}")
        display_df['CTR (%)'] = display_df['CTR (%)'].apply(lambda x: f"{x:.2f}")
        display_df[f'Coût ({currency})'] = display_df[f'Coût ({currency})'].apply(lambda x: f"{x:.2f}")
        display_df['Conversions'] = display_df['Conversions'].apply(lambda x: f"{x:.0f}")

        st.dataframe(display_df, use_container_width=True, height=600)

    st.markdown("---")

    # Actions
    st.subheader("📥 Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📥 Exporter en CSV", use_container_width=True):
            csv = df_filtered.to_csv(index=False)
            st.download_button(
                "Télécharger CSV",
                csv,
                "termes_recherche.csv",
                "text/csv"
            )

    with col2:
        if st.button("🔄 Actualiser", use_container_width=True):
            st.info("Actualisez les données depuis Configuration Simple")

    with col3:
        if st.button("📊 Retour vue d'ensemble", use_container_width=True):
            st.switch_page("pages/2_📊_Vue_Ensemble.py")

    # Conseils d'optimisation
    st.markdown("---")
    st.subheader("💡 Conseils d'optimisation")

    with st.expander("Comment utiliser les termes de recherche ?"):
        st.markdown("""
        **1. Identifier les termes hors-cible**
        - Cherchez les termes avec beaucoup de clics mais aucune conversion
        - Repérez les mots comme "gratuit", "emploi", "formation" qui attirent du trafic non qualifié

        **2. Ajouter des mots-clés négatifs**
        - Les termes hors-cible doivent être ajoutés en négatif dans Google Ads
        - Cela évitera de gaspiller votre budget sur du trafic non pertinent

        **3. Découvrir de nouveaux mots-clés**
        - Les termes avec de bonnes performances peuvent devenir de nouveaux mots-clés
        - Ajoutez-les en "Exact" ou "Expression" pour mieux contrôler

        **4. Ajuster les enchères**
        - Si un terme performe très bien, augmentez l'enchère pour obtenir plus de volume
        - Si un terme coûte cher sans résultat, ajoutez-le en négatif
        """)


# ============================================================================
# EXÉCUTION
# ============================================================================

if __name__ == "__main__":
    render_custom_sidebar("search")
    main()
