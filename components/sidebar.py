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
            ("app", "▦", t("home"), "home"),
            ("Configuration_Simple", "⚙", t("config"), "config"),
            ("Vue_Ensemble", "◫", t("overview"), "overview"),
            ("Detail_Campagne", "◎", t("campaign_detail"), "campaign"),
            ("Termes_Recherche", "⌕", t("search_terms"), "search"),
            ("Diagnostic", "✚", t("diagnostic"), "diagnostic"),
        ]

        nav_links = []
        for href, icon, label, key in nav_pages:
            active = " is-active" if key == current_page else ""
            nav_links.append(
                f'<a class="rafo-nav-link{active}" href="{href}" target="_self">'
                f'<span class="rafo-nav-icon">{escape(icon)}</span>'
                f'<span>{escape(label)}</span>'
                f'</a>'
            )

        st.markdown(
            f'<nav class="rafo-sidebar-nav">{"".join(nav_links)}</nav>',
            unsafe_allow_html=True
        )

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
