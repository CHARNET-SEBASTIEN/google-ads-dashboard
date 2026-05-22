"""
Page de configuration simplifiée - Google Ads Scripts
Plus besoin de Developer Token ni OAuth !
"""

import streamlit as st
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from config.settings import STREAMLIT_CONFIG
from config.i18n import t, init_language
from modules.script_data_loader import script_loader
from utils.ui_helpers import load_custom_css, init_theme, prevent_white_flash, format_french_datetime
from components.sidebar import render_custom_sidebar, hide_default_navigation
from components.topbar import render_topbar, TOPBAR_CSS


# ============================================================================
# CONFIGURATION
# ============================================================================

st.set_page_config(**STREAMLIT_CONFIG)
prevent_white_flash()
load_custom_css()
hide_default_navigation()
init_language()
init_theme()
st.markdown(TOPBAR_CSS, unsafe_allow_html=True)
render_topbar()


# ============================================================================
# PAGE
# ============================================================================

def extract_google_drive_file_id(value: str) -> str:
    """Extrait l'ID d'un fichier Google Drive depuis une URL ou un ID brut."""
    cleaned = value.strip()
    if not cleaned:
        return ""

    parsed = urlparse(cleaned)
    query_id = parse_qs(parsed.query).get("id", [""])[0]
    if query_id:
        return query_id.strip()

    match = re.search(r"/(?:file/d|document/d|spreadsheets/d)/([^/?#]+)", cleaned)
    if match:
        return match.group(1).strip()

    return cleaned


def main():
    """Page de configuration simplifiée"""

    st.title("Configuration des données")

    # Vérifier si des données existent
    data_exists = script_loader.data_exists()
    last_update = script_loader.get_last_update()
    account_info = script_loader.get_account_info()

    # Statut actuel
    if data_exists and account_info:
        st.success("✅ Données disponibles")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Compte", account_info.get('name', 'N/A'))

        with col2:
            st.metric("Customer ID", account_info.get('customerId', 'N/A'))

        with col3:
            if last_update:
                update_time_str = format_french_datetime(last_update, "%d/%m/%Y %H:%M")
                st.metric("Dernière mise à jour", update_time_str)
            else:
                st.metric("Dernière mise à jour", "Inconnue")

        st.markdown("---")

        # Statistiques des données
        campaigns = script_loader.get_campaigns()
        keywords = script_loader.get_keywords()
        ads = script_loader.get_ads()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("📊 Campagnes", len(campaigns))

        with col2:
            st.metric("🔑 Mots-clés", len(keywords))

        with col3:
            st.metric("📢 Annonces", len(ads))

    else:
        st.warning("⚠️ Aucune donnée disponible")
        st.info(
            "Pour utiliser l'application, vous devez d'abord exporter vos données "
            "depuis Google Ads avec le script fourni."
        )

    st.markdown("---")

    # Onglets de configuration
    tab1, tab2, tab3 = st.tabs(["Import manuel", "Google Drive", "Guide"])

    # ========================================================================
    # TAB 1 : IMPORT MANUEL
    # ========================================================================

    with tab1:
        st.subheader("Import manuel du fichier JSON")

        st.markdown(
            """
            Si vous avez téléchargé le fichier JSON depuis Google Drive, vous pouvez l'importer ici.

            **Étapes :**
            1. Allez sur [Google Drive](https://drive.google.com)
            2. Ouvrez le dossier **"Dashboard ADS"**
            3. Téléchargez le fichier **latest_data.json**
            4. Importez-le ci-dessous
            """
        )

        uploaded_file = st.file_uploader(
            "Choisissez le fichier JSON",
            type=['json'],
            help="Fichier exporté par le script Google Ads"
        )

        if uploaded_file is not None:
            try:
                # Lire et valider le fichier
                data = json.load(uploaded_file)

                # Vérifier les champs requis
                required_fields = ['campaigns', 'keywords', 'ads', 'account']
                if all(field in data for field in required_fields):
                    # Sauvegarder le fichier
                    temp_path = Path("/tmp/uploaded_data.json")
                    with open(temp_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f)

                    if script_loader.import_from_file(str(temp_path)):
                        # Marquer comme authentifié
                        st.session_state.authenticated = True

                        # Charger les infos du compte
                        account_info = script_loader.get_account_info()
                        if account_info:
                            st.session_state.customer_id = account_info.get('customerId')
                            st.session_state.customer_info = account_info

                        st.success("✅ Données importées avec succès !")
                        st.rerun()
                    else:
                        st.error("❌ Erreur lors de l'import")
                else:
                    st.error("❌ Fichier JSON invalide - champs manquants")

            except json.JSONDecodeError:
                st.error("❌ Fichier JSON invalide")
            except Exception as e:
                st.error(f"❌ Erreur : {e}")

    # ========================================================================
    # TAB 2 : GOOGLE DRIVE
    # ========================================================================

    with tab2:
        st.subheader("Actualisation depuis Google Drive")

        st.markdown(
            """
            Pour actualiser automatiquement les données depuis Google Drive, vous devez :
            1. Rendre le fichier **public** (ou obtenir un lien de partage)
            2. Coller l'URL de partage complète ou l'ID du fichier
            """
        )

        st.info(
            "**Comment obtenir le lien ?**\n\n"
            "1. Ouvrez le fichier dans Google Drive\n"
            "2. Cliquez sur **Partager** → **Obtenir le lien**\n"
            "3. Collez l'URL complète ci-dessous : "
            "`https://drive.google.com/file/d/[ID_DU_FICHIER]/view`"
        )

        drive_input = st.text_input(
            "URL ou ID du fichier Google Drive",
            placeholder="https://drive.google.com/file/d/1a2B3c4D5e6F7g8H9i0J/view",
            help="Collez l'URL de partage Google Drive ou l'ID du fichier."
        )
        file_id = extract_google_drive_file_id(drive_input)

        if drive_input and file_id != drive_input.strip():
            st.caption(f"ID détecté : `{file_id}`")

        col1, col2 = st.columns([1, 3])

        with col1:
            if st.button("Actualiser les données", type="primary", disabled=not file_id):
                with st.spinner("Téléchargement en cours..."):
                    if script_loader.download_from_google_drive(file_id):
                        # Marquer comme authentifié
                        st.session_state.authenticated = True

                        # Charger les infos du compte
                        account_info = script_loader.get_account_info()
                        if account_info:
                            st.session_state.customer_id = account_info.get('customerId')
                            st.session_state.customer_info = account_info

                        st.success("✅ Données actualisées !")
                        st.rerun()
                    else:
                        st.error(
                            "❌ Impossible de télécharger le fichier. "
                            "Vérifiez que l'ID est correct et que le fichier est public."
                        )

        with col2:
            if file_id:
                st.markdown(f"[🔗 Ouvrir dans Google Drive](https://drive.google.com/file/d/{file_id}/view)")

        st.markdown("---")

        # Sauvegarder l'ID dans la session pour actualisation rapide
        if file_id and st.checkbox("💾 Mémoriser ce fichier"):
            st.session_state.google_drive_file_id = file_id
            st.success("✅ ID sauvegardé")

    # ========================================================================
    # TAB 3 : GUIDE
    # ========================================================================

    with tab3:
        st.subheader("Guide d'installation")

        st.markdown(
            """
            ## Comment configurer le flux Google Ads

            ### Étape 1 : Installer le script (3 minutes)

            1. Allez sur [Google Ads](https://ads.google.com)
            2. **Outils** (⚙️) → **Bulk Actions** → **Scripts**
            3. Créez un nouveau script (+)
            4. Copiez-collez le contenu de `google_ads_export_script.js`
            5. Remplacez votre email dans le script
            6. **Enregistrez** et **Autorisez** le script

            ### Étape 2 : Planifier l'exécution (1 minute)

            1. Dans la page du script, cliquez sur **⏰ Planifications**
            2. Créez une planification : **Toutes les heures**
            3. Sauvegardez

            ### Étape 3 : Première exécution (1 minute)

            1. Cliquez sur **Exécuter** (▶️)
            2. Attendez 30 secondes
            3. Vérifiez les logs (doit afficher "✅ Export terminé")

            ### Étape 4 : Accéder aux données

            **Option A : Google Drive**
            1. Allez sur [Google Drive](https://drive.google.com)
            2. Ouvrez le dossier **"Dashboard ADS"**
            3. Le fichier **latest_data.json** contient vos données
            4. Utilisez l'onglet "Google Drive" ci-dessus pour actualiser

            **Option B : Import manuel**
            1. Téléchargez **latest_data.json** depuis Google Drive
            2. Utilisez l'onglet "Import manuel" ci-dessus

            ---

            ## ✅ C'est tout !

            Une fois configuré :
            - Le script s'exécute automatiquement toutes les heures
            - Vos données sont toujours à jour
            - Utilisez le bouton "Actualiser" pour récupérer les dernières données
            - Explorez Dashboard ADS !

            ---

            ## 📁 Fichiers

            - `google_ads_export_script.js` : Script à copier dans Google Ads
            - `INSTALLATION_SCRIPTS.md` : Guide détaillé complet

            ---

            ## 🆘 Besoin d'aide ?

            Consultez le fichier `INSTALLATION_SCRIPTS.md` pour le guide complet
            avec captures d'écran et résolution de problèmes.
            """
        )

# ============================================================================
# EXÉCUTION
# ============================================================================

if __name__ == "__main__":
    render_custom_sidebar("config")
    main()
