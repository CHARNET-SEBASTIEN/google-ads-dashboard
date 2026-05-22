"""
Barre de navigation supérieure avec contrôle du thème.
"""

import streamlit as st
from utils.preferences import user_prefs


def render_topbar():
    """
    Affiche une barre de navigation compacte avec le toggle clair/sombre.
    """
    is_dark = user_prefs.is_dark_mode()

    st.markdown('<div class="rafo-topbar-anchor"></div>', unsafe_allow_html=True)

    # Streamlit ne permet pas de placer des widgets dans un bloc HTML fixe.
    # La mise en page est donc pilotée par CSS autour de cette première ligne.
    col_spacer, col_theme = st.columns([20, 1])

    with col_theme:
        # Toggle mode sombre avec icône
        if st.button(
            "☾" if not is_dark else "☀",
            key="topbar_theme_toggle",
            help="Mode sombre" if not is_dark else "Mode clair",
            use_container_width=True
        ):
            user_prefs.toggle_dark_mode()
            st.rerun()


# CSS pour la topbar applicative
TOPBAR_CSS = """
<style>
header[data-testid="stHeader"] {
    display: none;
}

[data-testid="element-container"]:has(.rafo-topbar-anchor) + div[data-testid="stHorizontalBlock"] {
    position: fixed;
    top: 0;
    left: 224px;
    right: 0;
    height: 56px;
    z-index: 999;
    background: var(--rafo-header);
    border-bottom: 1px solid var(--rafo-border);
    padding: 12px 24px;
    display: grid;
    grid-template-columns: minmax(0, 1fr) 32px;
    align-items: center;
    gap: 16px;
}

[data-testid="element-container"]:has(.rafo-topbar-anchor) + div[data-testid="stHorizontalBlock"] > div {
    display: flex;
    align-items: center;
    min-width: 0 !important;
    width: auto !important;
    flex: none !important;
}

[data-testid="element-container"]:has(.rafo-topbar-anchor) + div[data-testid="stHorizontalBlock"] [data-testid="stVerticalBlock"] {
    background: transparent !important;
    border: 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    padding: 0 !important;
    height: auto !important;
    min-height: 0 !important;
}

[data-testid="element-container"]:has(.rafo-topbar-anchor) + div[data-testid="stHorizontalBlock"] .stButton button {
    min-width: 32px !important;
    width: 32px !important;
    height: 32px !important;
    min-height: 32px !important;
    padding: 0 !important;
    border-radius: 6px !important;
    background: transparent !important;
    border: 1px solid var(--rafo-border) !important;
    color: var(--rafo-text-secondary) !important;
    font-size: 1rem !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
}

[data-testid="element-container"]:has(.rafo-topbar-anchor) + div[data-testid="stHorizontalBlock"] .stButton button:hover {
    background: var(--rafo-hover) !important;
    color: var(--rafo-text) !important;
    border-color: var(--rafo-border) !important;
}

[data-testid="element-container"]:has(.rafo-topbar-anchor) + div[data-testid="stHorizontalBlock"] label[data-testid="stWidgetLabel"] {
    display: none;
}

@media (max-width: 900px) {
    [data-testid="element-container"]:has(.rafo-topbar-anchor) + div[data-testid="stHorizontalBlock"] {
        left: 0;
        padding-left: 64px;
    }

}
</style>
"""
