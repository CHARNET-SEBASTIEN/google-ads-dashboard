"""
Page Détail Campagne - Mode Scripts (sans API)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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


def get_campaign_by_id(campaign_id):
    """Récupère une campagne par son ID"""
    campaigns = script_loader.get_campaigns()
    for campaign in campaigns:
        if str(campaign.get('id')) == str(campaign_id):
            return campaign
    return None


# ============================================================================
# PAGE PRINCIPALE
# ============================================================================

def main():
    """Page principale"""

    check_data()

    st.title("Détail de la campagne")

    # Sélection de la campagne
    campaigns = script_loader.get_campaigns()

    if not campaigns:
        st.warning("⚠️ Aucune campagne trouvée")
        return

    # Sélecteur de campagne
    campaign_names = {str(c['id']): c['name'] for c in campaigns}

    # Utiliser la campagne sélectionnée ou la première par défaut
    default_id = st.session_state.get('selected_campaign_id', campaigns[0]['id'])

    selected_id = st.selectbox(
        "Sélectionnez une campagne",
        options=list(campaign_names.keys()),
        format_func=lambda x: campaign_names[x],
        index=list(campaign_names.keys()).index(str(default_id)) if str(default_id) in campaign_names else 0
    )

    campaign = get_campaign_by_id(selected_id)

    if not campaign:
        st.error("❌ Campagne introuvable")
        return

    # Infos compte
    account_info = script_loader.get_account_info()
    currency = account_info.get('currency', 'EUR') if account_info else 'EUR'

    # Header campagne
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.subheader(campaign['name'])

    with col2:
        status = campaign.get('status', 'UNKNOWN')
        if status == 'ENABLED':
            st.success("✅ Active")
        elif status == 'PAUSED':
            st.warning("⏸️ En pause")
        else:
            st.error("❌ Suspendue")

    with col3:
        st.metric("ID", campaign['id'])

    # Onglets
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Vue d'ensemble",
        "🔑 Mots-clés",
        "📈 Performances",
        "⚙️ Configuration"
    ])

    # ========================================================================
    # ONGLET 1 : VUE D'ENSEMBLE
    # ========================================================================

    with tab1:
        st.subheader("Métriques principales (30 derniers jours)")

        metrics = campaign.get('metrics', {})

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("👁️ Impressions", f"{metrics.get('impressions', 0):,.0f}")

        with col2:
            st.metric("🖱️ Clics", f"{metrics.get('clicks', 0):,.0f}")

        with col3:
            st.metric("💰 Coût", f"{metrics.get('cost', 0):,.2f} {currency}")

        with col4:
            st.metric("🎯 Conversions", f"{metrics.get('conversions', 0):,.0f}")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            ctr = metrics.get('ctr', 0)
            st.metric("📊 CTR", f"{ctr:.2f}%")

        with col2:
            avg_cpc = metrics.get('averageCpc', 0)
            st.metric("💵 CPC moyen", f"{avg_cpc:.2f} {currency}")

        with col3:
            conv_rate = metrics.get('conversionRate', 0)
            st.metric("🎯 Taux conv.", f"{conv_rate:.2f}%")

        with col4:
            cpa = metrics.get('costPerConversion', 0)
            st.metric("💰 CPA", f"{cpa:.2f} {currency}")

        # Budget et enchères
        st.subheader("Budget et enchères")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Budget journalier** : {campaign.get('budget', 0):.2f} {currency}")

        with col2:
            st.write(f"**Stratégie d'enchères** : {campaign.get('biddingStrategy', 'N/A')}")

    # ========================================================================
    # ONGLET 2 : MOTS-CLÉS
    # ========================================================================

    with tab2:
        st.subheader("Mots-clés de la campagne")

        keywords = script_loader.get_keywords(campaign_id=int(selected_id))

        if not keywords:
            st.info("ℹ️ Aucun mot-clé trouvé pour cette campagne")
        else:
            st.write(f"**{len(keywords)} mot(s)-clé(s)**")

            # Convertir en DataFrame
            df_keywords = pd.DataFrame(keywords)

            # Extraire les métriques
            if 'metrics' in df_keywords.columns:
                metrics_df = pd.json_normalize(df_keywords['metrics'])
                df_keywords = pd.concat([df_keywords.drop('metrics', axis=1), metrics_df], axis=1)

            # Statistiques
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total impressions", f"{df_keywords.get('impressions', pd.Series([0])).sum():,.0f}")
            with col2:
                st.metric("Total clics", f"{df_keywords.get('clicks', pd.Series([0])).sum():,.0f}")
            with col3:
                st.metric("Total coût", f"{df_keywords.get('cost', pd.Series([0])).sum():,.2f} {currency}")
            with col4:
                st.metric("Total conversions", f"{df_keywords.get('conversions', pd.Series([0])).sum():,.0f}")

            st.markdown("---")

            # Filtres
            col1, col2 = st.columns(2)

            with col1:
                match_types = df_keywords['matchType'].unique() if 'matchType' in df_keywords else []
                selected_match = st.multiselect(
                    "Type de correspondance",
                    options=match_types,
                    default=match_types
                )

            with col2:
                search_kw = st.text_input("🔍 Rechercher un mot-clé", "")

            # Filtrer
            df_filtered = df_keywords.copy()
            if selected_match and 'matchType' in df_filtered:
                df_filtered = df_filtered[df_filtered['matchType'].isin(selected_match)]
            if search_kw:
                df_filtered = df_filtered[df_filtered['text'].str.contains(search_kw, case=False, na=False)]

            # Trier par clics
            if 'clicks' in df_filtered:
                df_filtered = df_filtered.sort_values('clicks', ascending=False)

            # Afficher
            for idx, kw in df_filtered.iterrows():
                with st.expander(f"**{kw['text']}** ({kw.get('matchType', 'N/A')})"):
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.write("**Informations**")
                        st.write(f"Groupe d'annonces : {kw.get('adGroupName', 'N/A')}")
                        st.write(f"Type : {kw.get('matchType', 'N/A')}")
                        st.write(f"Statut : {kw.get('status', 'N/A')}")

                    with col2:
                        st.write("**Volume**")
                        st.write(f"👁️ Impressions : {kw.get('impressions', 0):,.0f}")
                        st.write(f"🖱️ Clics : {kw.get('clicks', 0):,.0f}")
                        st.write(f"📊 CTR : {kw.get('ctr', 0):.2f}%")

                    with col3:
                        st.write("**Coûts**")
                        st.write(f"💰 Coût : {kw.get('cost', 0):,.2f} {currency}")
                        st.write(f"💵 CPC moy. : {kw.get('averageCpc', 0):.2f} {currency}")
                        st.write(f"🎯 Conversions : {kw.get('conversions', 0):,.0f}")

                    # Alertes
                    text_lower = kw.get('text', '').lower()
                    if any(word in text_lower for word in ['gratuit', 'free', 'emploi', 'job', 'formation', 'stage']):
                        st.warning("⚠️ Ce mot-clé pourrait attirer du trafic non qualifié")

    # ========================================================================
    # ONGLET 3 : PERFORMANCES
    # ========================================================================

    with tab3:
        st.subheader("📈 Évolution des performances (30 derniers jours)")

        performance = script_loader.get_performance(campaign_id=int(selected_id))

        if not performance:
            st.info("ℹ️ Aucune donnée de performance disponible")
        else:
            df_perf = pd.DataFrame(performance)

            # Convertir la date
            if 'date' in df_perf:
                df_perf['date'] = pd.to_datetime(df_perf['date'])
                df_perf = df_perf.sort_values('date')

            # Graphique des clics et impressions
            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=df_perf['date'],
                y=df_perf['impressions'],
                name='Impressions',
                line=dict(color='#1f77b4')
            ))

            fig.add_trace(go.Scatter(
                x=df_perf['date'],
                y=df_perf['clicks'],
                name='Clics',
                yaxis='y2',
                line=dict(color='#ff7f0e')
            ))

            fig.update_layout(
                title='Impressions et Clics',
                xaxis=dict(title='Date'),
                yaxis=dict(title='Impressions', side='left'),
                yaxis2=dict(title='Clics', overlaying='y', side='right'),
                hovermode='x unified'
            )

            st.plotly_chart(fig, use_container_width=True)

            # Graphique du coût
            fig_cost = px.line(
                df_perf,
                x='date',
                y='cost',
                title='Évolution du coût',
                labels={'cost': f'Coût ({currency})', 'date': 'Date'}
            )

            st.plotly_chart(fig_cost, use_container_width=True)

            # Graphique des conversions
            if 'conversions' in df_perf and df_perf['conversions'].sum() > 0:
                fig_conv = px.bar(
                    df_perf,
                    x='date',
                    y='conversions',
                    title='Conversions par jour',
                    labels={'conversions': 'Conversions', 'date': 'Date'}
                )

                st.plotly_chart(fig_conv, use_container_width=True)

    # ========================================================================
    # ONGLET 4 : CONFIGURATION
    # ========================================================================

    with tab4:
        st.subheader("⚙️ Configuration de la campagne")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Général**")
            st.write(f"ID : {campaign.get('id')}")
            st.write(f"Type : {campaign.get('type', 'N/A')}")
            st.write(f"Statut : {campaign.get('status', 'N/A')}")

            st.markdown("---")

            st.write("**Ciblage réseau**")
            st.write(f"Réseau de recherche : {'✅' if campaign.get('targetSearch') else '❌'}")
            st.write(f"Réseau Display : {'✅' if campaign.get('targetDisplay') else '❌'}")
            st.write(f"Partenaires de recherche : {'✅' if campaign.get('targetPartners') else '❌'}")

        with col2:
            st.write("**Budget**")
            st.write(f"Budget journalier : {campaign.get('budget', 0):.2f} {currency}")
            st.write(f"Stratégie d'enchères : {campaign.get('biddingStrategy', 'N/A')}")

            st.markdown("---")

            st.write("**Dates**")
            st.write(f"Date de début : {campaign.get('startDate', 'Non définie')}")
            st.write(f"Date de fin : {campaign.get('endDate', 'Non définie')}")

        # Alertes
        st.markdown("---")
        st.subheader("⚠️ Alertes")

        alerts = []

        if campaign.get('targetDisplay'):
            alerts.append("🔴 **Réseau Display activé** : Désactivez-le pour cibler uniquement les recherches actives")

        if metrics.get('conversions', 0) == 0:
            alerts.append("🔴 **Aucune conversion** : Vérifiez le tracking ou la page de destination")

        conv_rate = metrics.get('conversionRate', 0)
        if conv_rate < 1:
            alerts.append("🟠 **Taux de conversion faible** : Optimisez la page de destination")

        cpa = metrics.get('costPerConversion', 0)
        if cpa > 100:
            alerts.append(f"🟡 **CPA élevé** : {cpa:.2f} {currency} par conversion")

        if alerts:
            for alert in alerts:
                st.warning(alert)
        else:
            st.success("✅ Aucune alerte - Campagne bien configurée")


# ============================================================================
# EXÉCUTION
# ============================================================================

if __name__ == "__main__":
    render_custom_sidebar("campaign")
    main()
