"""
Helpers UI pour Dashboard ADS.
"""

import streamlit as st
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo


def prevent_white_flash():
    """
    Injecte un style CSS minimal pour éviter le flash blanc
    lors de la navigation entre pages.
    À appeler EN PREMIER dans chaque page.
    """
    from utils.preferences import user_prefs

    # Choisir la couleur selon le mode
    bg_color = "#161413" if user_prefs.is_dark_mode() else "#fbfaf9"

    # Injecter le style immédiatement
    st.markdown(
        f"""
        <style>
        html, body, .stApp {{
            background-color: {bg_color} !important;
            transition: none !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def init_theme():
    """Initialise le thème dans le session state depuis les préférences"""
    if "dark_mode" not in st.session_state:
        from utils.preferences import user_prefs
        st.session_state.dark_mode = user_prefs.is_dark_mode()


def get_theme():
    """Retourne le thème actuel (dark ou light)"""
    if "dark_mode" not in st.session_state:
        init_theme()
    return "dark" if st.session_state.dark_mode else "light"


def toggle_theme():
    """Bascule entre mode sombre et mode clair et sauvegarde"""
    if "dark_mode" not in st.session_state:
        init_theme()
    st.session_state.dark_mode = not st.session_state.dark_mode
    from utils.preferences import user_prefs
    user_prefs.set_dark_mode(st.session_state.dark_mode)


def load_custom_css():
    """
    Charge le CSS personnalisé dans l'application Streamlit
    Mode clair ou sombre du dashboard
    À appeler au début de chaque page pour appliquer le thème
    """
    from utils.preferences import user_prefs

    # Fichiers CSS du thème applicatif
    light_css_file = Path(__file__).parent.parent / "assets" / "rafo-light.css"
    dark_css_file = Path(__file__).parent.parent / "assets" / "rafo-dark.css"
    app_css_file = Path(__file__).parent.parent / "assets" / "rafo-app.css"

    # Charger le CSS selon le mode
    if user_prefs.is_dark_mode():
        # Mode sombre
        if dark_css_file.exists():
            with open(dark_css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
                st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    else:
        # Mode clair
        if light_css_file.exists():
            with open(light_css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
                st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

    if app_css_file.exists():
        with open(app_css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


def convert_to_french_time(iso_timestamp: str) -> datetime:
    """
    Convertit un timestamp ISO (UTC) en heure française (Europe/Paris)

    Args:
        iso_timestamp: Timestamp au format ISO (ex: "2026-05-22T17:11:00Z")

    Returns:
        datetime object avec timezone Europe/Paris
    """
    # Parser le timestamp (remplacer Z par +00:00 pour ISO format)
    dt_utc = datetime.fromisoformat(iso_timestamp.replace('Z', '+00:00'))

    # Convertir en heure française
    dt_french = dt_utc.astimezone(ZoneInfo("Europe/Paris"))

    return dt_french


def format_french_datetime(iso_timestamp: str, format_str: str = "%d/%m/%Y à %H:%M") -> str:
    """
    Formate un timestamp ISO en heure française

    Args:
        iso_timestamp: Timestamp au format ISO
        format_str: Format de sortie (défaut: "JJ/MM/AAAA à HH:MM")

    Returns:
        String formatée en heure française
    """
    dt_french = convert_to_french_time(iso_timestamp)
    return dt_french.strftime(format_str)


def format_metric_card(label: str, value: str, delta: str = None, help_text: str = None):
    """
    Crée une carte de métrique stylisée avec le design Silao

    Args:
        label: Libellé de la métrique
        value: Valeur à afficher
        delta: Variation (optionnel)
        help_text: Texte d'aide (optionnel)
    """
    st.metric(
        label=label,
        value=value,
        delta=delta,
        help=help_text
    )
