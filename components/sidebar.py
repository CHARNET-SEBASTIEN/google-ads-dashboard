"""
Sidebar personnalisée pour Dashboard ADS.
"""

import streamlit as st
from html import escape

from config.i18n import t, init_language


def render_custom_sidebar(current_page: str = "home"):
    """
    Affiche une sidebar personnalisée :
    - marque produit compacte
    - navigation en liens avec état actif
    - cache
    """
    # Initialiser la langue depuis les préférences
    init_language()

    with st.sidebar:
        st.markdown(
            """
            <div class="rafo-sidebar-brand">
                <div class="rafo-wordmark">Dashboard ADS</div>
                <div class="rafo-mascot" aria-hidden="true">G</div>
                <div class="rafo-product-label">Pilotage Google Ads</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """<div class="rafo-nav-section-label">Navigation</div>""",
            unsafe_allow_html=True
        )

        nav_pages = [
            ("▦", t("home"), "home", "app.py"),
            ("⚙", t("config"), "config", "pages/0_⚙️_Configuration_Simple.py"),
            ("◫", t("overview"), "overview", "pages/2_📊_Vue_Ensemble.py"),
            ("◎", t("campaign_detail"), "campaign", "pages/3_🎯_Detail_Campagne.py"),
            ("⌕", t("search_terms"), "search", "pages/4_🔍_Termes_Recherche.py"),
            ("✚", t("diagnostic"), "diagnostic", "pages/5_⚕️_Diagnostic.py"),
        ]

        # Utiliser des boutons Streamlit pour la navigation
        for icon, label, key, page_path in nav_pages:
            is_active = key == current_page
            if st.button(
                f"{icon}  {label}",
                key=f"nav_{key}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.switch_page(page_path)

        st.markdown(
            f"""
            <div class="rafo-sidebar-footer">
                <div>{t('version')} 2.0</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# CSS pour cacher la navigation par défaut de Streamlit et améliorer le style
HIDE_STREAMLIT_NAV_CSS = """
<style>
/* Cacher la navigation par défaut de Streamlit */
[data-testid="stSidebarNav"] {
    display: none;
}

section[data-testid="stSidebar"] [data-testid="collapsedControl"] {
    display: none;
}

section[data-testid="stSidebar"] button[data-testid="baseButton-header"],
section[data-testid="stSidebar"] div:has(> button[data-testid="baseButton-header"]) {
    display: none !important;
}
</style>
"""


def hide_default_navigation():
    """Cache la navigation par défaut de Streamlit et applique le style amélioré"""
    st.markdown(HIDE_STREAMLIT_NAV_CSS, unsafe_allow_html=True)
