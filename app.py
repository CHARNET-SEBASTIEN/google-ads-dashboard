"""
Dashboard ADS
Application principale Streamlit
"""

import streamlit as st

from config.settings import STREAMLIT_CONFIG
from config.i18n import t, init_language
from modules.storage import storage
from utils.ui_helpers import load_custom_css, init_theme, prevent_white_flash
from components.sidebar import render_custom_sidebar, hide_default_navigation
from components.topbar import render_topbar, TOPBAR_CSS


# ============================================================================
# CONFIGURATION DE LA PAGE
# ============================================================================

st.set_page_config(**STREAMLIT_CONFIG)

# Éviter le flash blanc lors de la navigation
prevent_white_flash()

# Charger le CSS personnalisé
load_custom_css()

# Cacher la navigation par défaut
hide_default_navigation()

# Initialiser la langue et le thème
init_language()
init_theme()

# Afficher la topbar avec contrôles langue et thème
st.markdown(TOPBAR_CSS, unsafe_allow_html=True)
render_topbar()


# ============================================================================
# SESSION STATE
# ============================================================================

def init_session_state():
    """Initialise les variables de session"""
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "customer_id" not in st.session_state:
        st.session_state.customer_id = None

    if "credentials" not in st.session_state:
        st.session_state.credentials = None

    if "client" not in st.session_state:
        st.session_state.client = None

    if "customer_info" not in st.session_state:
        st.session_state.customer_info = None

    # Vérifier si des données scripts existent (mode sans API)
    try:
        from modules.script_data_loader import script_loader
        if script_loader.data_exists() and not st.session_state.authenticated:
            st.session_state.authenticated = True
            account_info = script_loader.get_account_info()
            if account_info:
                st.session_state.customer_id = account_info.get('customerId')
                st.session_state.customer_info = account_info
    except:
        pass


init_session_state()


# ============================================================================
# VÉRIFICATION CLIENT_SECRET.JSON
# ============================================================================

def check_client_secret():
    """Vérifie si le fichier client_secret.json existe"""
    from config.settings import CLIENT_SECRET_FILE
    return CLIENT_SECRET_FILE.exists()


# ============================================================================
# PAGE D'ACCUEIL
# ============================================================================

def main():
    """Page d'accueil"""

    account_label = st.session_state.customer_id or "Aucun compte connecté"
    status_label = "Connecté" if st.session_state.authenticated else "À configurer"

    st.markdown(
        f"""
        <section class="ads-home-hero">
            <div class="ads-page-kicker">Dashboard ADS</div>
            <h1>Pilotage Google Ads</h1>
            <p>
                Analysez la structure de vos campagnes, repérez les problèmes de configuration
                et suivez les signaux utiles depuis une interface locale, claire et rapide.
            </p>
            <div class="ads-status-strip">
                <span class="ads-status-pill">{status_label}</span>
                <span class="ads-status-pill">{account_label}</span>
                <span class="ads-status-pill">Données locales</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True
    )

    # Vérifier si client_secret.json existe
    if not check_client_secret():
        st.error("❌ **Fichier `client_secret.json` introuvable**")
        st.warning(
            "Pour utiliser cette application, vous devez télécharger votre fichier "
            "`client_secret.json` depuis Google Cloud Console et le placer à la racine du projet."
        )

        st.info(
            "**Comment obtenir client_secret.json ?**\n\n"
            "1. Allez sur [Google Cloud Console](https://console.cloud.google.com/)\n"
            "2. Créez un projet ou sélectionnez-en un\n"
            "3. Activez l'API Google Ads\n"
            "4. Allez dans **APIs & Services** → **Credentials**\n"
            "5. Créez des **OAuth 2.0 Client IDs** (type: Desktop app)\n"
            "6. Téléchargez le fichier JSON\n"
            "7. Renommez-le `client_secret.json` et placez-le à la racine du projet"
        )
        st.stop()

    # Si non authentifié
    if not st.session_state.authenticated:
        st.info("Importez vos données Google Ads dans Configuration pour activer les vues d'analyse.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### Analyse")
            st.markdown(
                "- Vue d'ensemble des campagnes\n"
                "- Configuration détaillée\n"
                "- Analyse des mots-clés\n"
                "- Performances détaillées\n"
                "- Termes de recherche réels\n"
                "- Diagnostic automatique"
            )

        with col2:
            st.markdown("### Données")
            st.markdown(
                "- Import JSON manuel\n"
                "- Actualisation Google Drive\n"
                "- Cache local contrôlé\n"
                "- Export CSV\n"
                "- Aucun serveur tiers"
            )

        with col3:
            st.markdown("### Contrôle")
            st.markdown(
                "- Lecture sans OAuth complexe\n"
                "- Statuts de campagne\n"
                "- Budgets et enchères\n"
                "- Requêtes utilisateurs\n"
                "- Recommandations"
            )

        st.markdown('<div class="ads-section-title">Documentation</div>', unsafe_allow_html=True)

        with st.expander("📖 Comment ça marche ?"):
            st.markdown(
                """
                **1. Import des données**

                Depuis la page **Configuration**, importez le fichier JSON généré par
                le script Google Ads ou renseignez l'ID du fichier Google Drive partagé.

                **2. Analyse**
                - **Vue d'ensemble** : Liste de toutes vos campagnes
                - **Détail campagne** : Configuration complète d'une campagne
                - **Termes de recherche** : Requêtes réelles des utilisateurs
                - **Diagnostic** : Analyse automatique avec recommandations

                **3. Export**

                Les vues principales disposent d'un export CSV pour conserver les résultats.

                **4. Cache**

                Les données restent locales et peuvent être rechargées depuis la configuration.
                """
            )

        with st.expander("❓ Résolution de problèmes"):
            st.markdown(
                """
                **"DEVELOPER_TOKEN_NOT_APPROVED"**

                Votre token est en mode test — vous pouvez uniquement accéder à votre propre compte.
                Pour un usage production, soumettez une demande d'approbation dans le Centre API.

                **"AUTHENTICATION_ERROR"**

                Token expiré. Retournez dans Configuration et recliquez sur "Autoriser avec Google".

                **"CUSTOMER_NOT_FOUND"**

                Vérifiez le format du Customer ID (10 chiffres sans tirets, ex : 1234567890).

                **"QUOTA_ERROR"**

                Limite API atteinte. Attendez quelques minutes ou activez le cache.

                **Erreur de connexion**

                Vérifiez que :
                1. L'API Google Ads est activée dans Google Cloud Console
                2. Le fichier `client_secret.json` est présent à la racine
                3. Votre compte Google a accès au compte Google Ads spécifié
                """
            )

        with st.expander("🔐 Où sont stockées mes données ?"):
            st.markdown(
                """
                **Stockage local uniquement**

                Les données d'import et le cache restent sur cette machine.
                Aucune donnée n'est envoyée vers un serveur applicatif externe.

                **Cache**

                Le cache est stocké dans `.cache/` et contient les réponses API :
                - Durée de vie : 1 heure (configurable)
                - Permet de réduire les appels API
                - Peut être vidé à tout moment

                **Déconnexion**

                Le bouton "Déconnecter" dans Configuration supprime tous vos credentials chiffrés.
                """
            )

        # Stats si déjà des utilisateurs
        users = storage.list_users()
        if users:
            st.success(f"✅ {len(users)} compte(s) configuré(s) sur cette installation")

    else:
        # Si authentifié, afficher un récapitulatif
        st.success(f"Compte actif : {st.session_state.customer_id}")

        if st.session_state.customer_info:
            info = st.session_state.customer_info

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Nom du compte", info.get("name", "N/A"))

            with col2:
                st.metric("Devise", info.get("currency", "N/A"))

            with col3:
                st.metric("Type", "Test" if info.get("is_test") else "Production")

            with col4:
                st.metric("Manager", "Oui" if info.get("is_manager") else "Non")

        # Liens rapides
        st.markdown('<div class="ads-section-title">Accès rapide</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Vue d'ensemble", use_container_width=True):
                st.switch_page("pages/2_📊_Vue_Ensemble.py")

        with col2:
            if st.button("Termes de recherche", use_container_width=True):
                st.switch_page("pages/4_🔍_Termes_Recherche.py")

        with col3:
            if st.button("Diagnostic", use_container_width=True):
                st.switch_page("pages/5_⚕️_Diagnostic.py")


# ============================================================================
# EXÉCUTION
# ============================================================================

if __name__ == "__main__":
    render_custom_sidebar("home")
    main()
