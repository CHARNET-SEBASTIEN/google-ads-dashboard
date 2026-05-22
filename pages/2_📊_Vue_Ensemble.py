"""
Page Vue d'ensemble - Mode Scripts (sans API)
"""

import streamlit as st
import pandas as pd
from datetime import datetime

from config.settings import STREAMLIT_CONFIG, STATUS_COLORS
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
        st.info("Importez vos données depuis la page ⚙️ Configuration Simple")
        if st.button("⚙️ Aller à la configuration"):
            st.switch_page("pages/0_⚙️_Configuration_Simple.py")
        st.stop()


def load_campaigns() -> pd.DataFrame:
    """Charge les campagnes depuis les données du script"""
    campaigns = script_loader.get_campaigns()

    if not campaigns:
        return pd.DataFrame()

    # Convertir en DataFrame
    df = pd.DataFrame(campaigns)

    # Ajouter les métriques si elles existent
    if 'metrics' in df.columns:
        # Extraire les métriques dans des colonnes séparées
        metrics_df = pd.json_normalize(df['metrics'])
        df = pd.concat([df.drop('metrics', axis=1), metrics_df], axis=1)

    return df


# ============================================================================
# PAGE PRINCIPALE
# ============================================================================

def main():
    """Page principale"""

    # Vérifier les données
    check_data()

    # Header
    st.title("Vue d'ensemble des campagnes")

    # Infos compte
    account_info = script_loader.get_account_info()
    if account_info:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Compte", account_info.get('name', 'N/A'))
        with col2:
            st.metric("Customer ID", account_info.get('customerId', 'N/A'))
        with col3:
            st.metric("Devise", account_info.get('currency', 'N/A'))

    # Dernière mise à jour
    last_update = script_loader.get_last_update()
    if last_update:
        update_time = datetime.fromisoformat(last_update.replace('Z', '+00:00'))
        st.info(f"📅 Dernière mise à jour : {update_time.strftime('%d/%m/%Y à %H:%M')}")

    # Charger les campagnes
    df_campaigns = load_campaigns()

    if df_campaigns.empty:
        st.warning("⚠️ Aucune campagne trouvée")
        return

    # Statistiques globales
    st.subheader("Statistiques globales (30 derniers jours)")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_impressions = df_campaigns.get('impressions', pd.Series([0])).sum()
        st.metric("👁️ Impressions", f"{total_impressions:,.0f}")

    with col2:
        total_clicks = df_campaigns.get('clicks', pd.Series([0])).sum()
        st.metric("🖱️ Clics", f"{total_clicks:,.0f}")

    with col3:
        total_cost = df_campaigns.get('cost', pd.Series([0])).sum()
        currency = account_info.get('currency', 'EUR') if account_info else 'EUR'
        st.metric("💰 Coût", f"{total_cost:,.2f} {currency}")

    with col4:
        total_conversions = df_campaigns.get('conversions', pd.Series([0])).sum()
        st.metric("🎯 Conversions", f"{total_conversions:,.0f}")

    # Tableau des campagnes
    st.subheader(f"Campagnes ({len(df_campaigns)})")

    # Filtres
    col1, col2 = st.columns(2)

    with col1:
        status_filter = st.multiselect(
            "Statut",
            options=df_campaigns['status'].unique() if 'status' in df_campaigns else [],
            default=df_campaigns['status'].unique() if 'status' in df_campaigns else []
        )

    with col2:
        search = st.text_input("🔍 Rechercher une campagne", "")

    # Appliquer les filtres
    df_filtered = df_campaigns.copy()

    if status_filter and 'status' in df_filtered:
        df_filtered = df_filtered[df_filtered['status'].isin(status_filter)]

    if search:
        df_filtered = df_filtered[df_filtered['name'].str.contains(search, case=False, na=False)]

    # Afficher le tableau
    for idx, campaign in df_filtered.iterrows():
        with st.expander(f"**{campaign['name']}** ({campaign.get('status', 'N/A')})"):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.write("**Informations**")
                st.write(f"ID : {campaign.get('id', 'N/A')}")
                st.write(f"Type : {campaign.get('type', 'N/A')}")
                st.write(f"Statut : {campaign.get('status', 'N/A')}")

                # Badge coloré selon le statut
                if campaign.get('status') == 'ENABLED':
                    st.success("✅ Active")
                elif campaign.get('status') == 'PAUSED':
                    st.warning("⏸️ En pause")
                else:
                    st.error("❌ Suspendue")

            with col2:
                st.write("**Budget & Enchères**")
                budget = campaign.get('budget', 0)
                st.write(f"Budget journalier : {budget:.2f} {currency}")
                st.write(f"Stratégie : {campaign.get('biddingStrategy', 'N/A')}")

            with col3:
                st.write("**Performances (30j)**")
                st.write(f"👁️ Impressions : {campaign.get('impressions', 0):,.0f}")
                st.write(f"🖱️ Clics : {campaign.get('clicks', 0):,.0f}")
                st.write(f"💰 Coût : {campaign.get('cost', 0):,.2f} {currency}")
                st.write(f"🎯 Conversions : {campaign.get('conversions', 0):,.0f}")

            # Bouton pour voir le détail
            if st.button(f"📊 Voir le détail", key=f"detail_{campaign.get('id')}"):
                st.session_state.selected_campaign_id = campaign.get('id')
                st.switch_page("pages/3_🎯_Detail_Campagne.py")

    # Actions
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Actualiser les données", use_container_width=True):
            st.info("Actualisez depuis Google Drive dans Configuration Simple")

    with col2:
        if st.button("⚙️ Configuration", use_container_width=True):
            st.switch_page("pages/0_⚙️_Configuration_Simple.py")

    with col3:
        if st.button("📥 Exporter (CSV)", use_container_width=True):
            csv = df_campaigns.to_csv(index=False)
            st.download_button(
                "Télécharger",
                csv,
                "campagnes.csv",
                "text/csv"
            )


# ============================================================================
# EXÉCUTION
# ============================================================================

if __name__ == "__main__":
    render_custom_sidebar("overview")
    main()
