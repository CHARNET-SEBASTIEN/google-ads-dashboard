"""
Page de configuration - Authentification OAuth2 et gestion des credentials
"""

import streamlit as st
from pathlib import Path

from config.settings import STREAMLIT_CONFIG
from modules.auth import auth
from modules.storage import storage
from modules.google_ads_client import create_client


# ============================================================================
# CONFIGURATION
# ============================================================================

st.set_page_config(**STREAMLIT_CONFIG)


# ============================================================================
# SESSION STATE
# ============================================================================

def init_session_state():
    """Initialise les variables de session"""
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


init_session_state()


# ============================================================================
# FONCTIONS
# ============================================================================

def save_and_authenticate(developer_token: str, customer_id: str, refresh_token: str):
    """Sauvegarde les credentials et authentifie l'utilisateur"""
    try:
        # Formater le customer_id
        formatted_customer_id = auth.format_customer_id(customer_id)

        # Récupérer client_id et client_secret depuis client_secret.json
        import json
        from config.settings import CLIENT_SECRET_FILE

        with open(CLIENT_SECRET_FILE, "r") as f:
            client_secret_data = json.load(f)

        client_id = client_secret_data["installed"]["client_id"]
        client_secret = client_secret_data["installed"]["client_secret"]

        # Construire le dictionnaire de credentials
        credentials = auth.build_credentials_dict(
            developer_token=developer_token,
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=refresh_token,
            customer_id=formatted_customer_id
        )

        # Valider les credentials
        st.info("🔄 Validation des credentials...")
        if not auth.validate_credentials(developer_token, client_id, client_secret, refresh_token):
            st.error("❌ Credentials invalides. Vérifiez votre Developer Token et réessayez.")
            return False

        # Sauvegarder de manière sécurisée
        st.info("💾 Sauvegarde sécurisée...")
        storage.save_credentials(formatted_customer_id, credentials)

        # Créer le client Google Ads
        st.info("🔌 Connexion à l'API Google Ads...")
        client = create_client(credentials)

        # Récupérer les infos du compte
        customer_info = client.get_customer_info()

        # Mettre à jour le session state
        st.session_state.authenticated = True
        st.session_state.customer_id = formatted_customer_id
        st.session_state.credentials = credentials
        st.session_state.client = client
        st.session_state.customer_info = customer_info

        st.success(f"✅ Connexion réussie au compte **{customer_info.get('name', formatted_customer_id)}**")
        return True

    except Exception as e:
        st.error(f"❌ Erreur lors de l'authentification : {str(e)}")
        return False


def load_existing_credentials(customer_id: str):
    """Charge des credentials existants"""
    try:
        formatted_customer_id = auth.format_customer_id(customer_id)

        # Charger les credentials
        credentials = storage.load_credentials(formatted_customer_id)

        if not credentials:
            st.error(f"❌ Aucun credentials trouvé pour le compte {formatted_customer_id}")
            return False

        # Créer le client
        client = create_client(credentials)

        # Récupérer les infos
        customer_info = client.get_customer_info()

        # Mettre à jour le session state
        st.session_state.authenticated = True
        st.session_state.customer_id = formatted_customer_id
        st.session_state.credentials = credentials
        st.session_state.client = client
        st.session_state.customer_info = customer_info

        st.success(f"✅ Reconnecté au compte **{customer_info.get('name', formatted_customer_id)}**")
        return True

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement : {str(e)}")
        return False


def disconnect():
    """Déconnecte l'utilisateur et supprime les credentials"""
    if st.session_state.customer_id:
        storage.delete_credentials(st.session_state.customer_id)

    st.session_state.authenticated = False
    st.session_state.customer_id = None
    st.session_state.credentials = None
    st.session_state.client = None
    st.session_state.customer_info = None

    st.success("✅ Déconnexion réussie. Credentials supprimés.")


# ============================================================================
# PAGE
# ============================================================================

def main():
    """Page de configuration"""

    st.title("🔧 Configuration")
    st.markdown("Configurez vos credentials Google Ads pour accéder à l'API")

    st.markdown("---")

    # Si déjà authentifié
    if st.session_state.authenticated:
        st.success(f"✅ **Connecté au compte :** {st.session_state.customer_id}")

        if st.session_state.customer_info:
            info = st.session_state.customer_info

            col1, col2 = st.columns(2)

            with col1:
                st.info(f"**Nom du compte :** {info.get('name', 'N/A')}")
                st.info(f"**Devise :** {info.get('currency', 'N/A')}")

            with col2:
                st.info(f"**Type :** {'Test' if info.get('is_test') else 'Production'}")
                st.info(f"**Manager :** {'Oui' if info.get('is_manager') else 'Non'}")

        st.markdown("---")

        if st.button("🚪 Déconnecter et supprimer mes données", type="secondary"):
            disconnect()
            st.rerun()

        st.markdown("---")

        st.success("✅ Vous pouvez maintenant utiliser les autres pages de l'application.")

        if st.button("📊 Aller à la vue d'ensemble", type="primary"):
            st.switch_page("pages/2_📊_Vue_Ensemble.py")

    else:
        # Vérifier s'il y a des comptes existants
        existing_users = storage.list_users()

        if existing_users:
            st.info(f"🔄 {len(existing_users)} compte(s) déjà configuré(s)")

            selected_user = st.selectbox(
                "Se reconnecter à un compte existant :",
                options=["-- Nouveau compte --"] + existing_users
            )

            if selected_user != "-- Nouveau compte --":
                if st.button("🔌 Se reconnecter", type="primary"):
                    load_existing_credentials(selected_user)
                    st.rerun()

                st.markdown("---")

        st.markdown("### ➕ Nouvelle configuration")

        with st.form("auth_form"):
            st.markdown("#### 1️⃣ Developer Token")
            st.caption(
                "Obtenez-le dans Google Ads → **Outils** → **Centre API**"
            )
            developer_token = st.text_input(
                "Developer Token",
                type="password",
                help="Commence généralement par un underscore (_) en mode test"
            )

            st.markdown("#### 2️⃣ Customer ID")
            st.caption(
                "Numéro de compte à 10 chiffres (visible en haut à droite dans Google Ads)"
            )
            customer_id = st.text_input(
                "Customer ID",
                placeholder="123-456-7890 ou 1234567890",
                help="Format : 10 chiffres, avec ou sans tirets"
            )

            st.markdown("#### 3️⃣ Authentification OAuth2")
            st.caption(
                "Cliquez sur le bouton ci-dessous pour autoriser l'accès à votre compte Google Ads"
            )

            get_token_button = st.form_submit_button(
                "🔐 Autoriser avec Google",
                type="primary",
                use_container_width=True
            )

        # Traitement du formulaire
        if get_token_button:
            if not developer_token:
                st.error("❌ Veuillez saisir votre Developer Token")
            elif not customer_id:
                st.error("❌ Veuillez saisir votre Customer ID")
            elif not auth.validate_customer_id_format(customer_id):
                st.error("❌ Format de Customer ID invalide (doit être 10 chiffres)")
            else:
                try:
                    # Vérifier que client_secret.json existe
                    if not auth.check_client_secret_exists():
                        st.error(
                            "❌ Fichier `client_secret.json` introuvable. "
                            "Téléchargez-le depuis Google Cloud Console et placez-le à la racine."
                        )
                        st.stop()

                    # Lancer le flow OAuth2
                    st.info(
                        "🌐 Une fenêtre de navigateur va s'ouvrir...\n\n"
                        "Connectez-vous avec votre compte Google et autorisez l'accès."
                    )

                    with st.spinner("En attente de l'autorisation..."):
                        refresh_token = auth.get_refresh_token_interactive()

                    if refresh_token:
                        st.success("✅ Autorisation obtenue !")

                        # Sauvegarder et authentifier
                        if save_and_authenticate(developer_token, customer_id, refresh_token):
                            st.balloons()
                            st.rerun()
                    else:
                        st.error("❌ Échec de l'autorisation OAuth2")

                except Exception as e:
                    st.error(f"❌ Erreur : {str(e)}")

        # Documentation
        st.markdown("---")

        with st.expander("📖 Comment obtenir les credentials ?"):
            st.markdown(
                """
                ### Developer Token

                1. Connectez-vous à [Google Ads](https://ads.google.com/)
                2. Cliquez sur **Outils** (icône clé à molette)
                3. Allez dans **Configuration** → **Centre API**
                4. Notez votre **Developer Token**

                **Note :** Si votre token n'est pas encore approuvé (statut "En attente"),
                vous pouvez l'utiliser en mode test sur votre propre compte uniquement.

                ---

                ### Customer ID

                1. Dans Google Ads, regardez en haut à droite
                2. Notez le numéro de compte (format : `123-456-7890`)
                3. Vous pouvez l'entrer avec ou sans tirets

                ---

                ### OAuth2

                Le bouton "Autoriser avec Google" lance un processus sécurisé :
                1. Une fenêtre de navigateur s'ouvre
                2. Vous vous connectez avec votre compte Google
                3. Vous autorisez l'accès à l'API Google Ads
                4. Le **refresh token** est généré automatiquement
                5. Vos credentials sont chiffrés et stockés localement

                **Aucune donnée n'est envoyée vers un serveur externe.**
                """
            )


# ============================================================================
# EXÉCUTION
# ============================================================================

if __name__ == "__main__":
    main()
