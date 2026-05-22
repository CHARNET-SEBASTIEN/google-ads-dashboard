"""
Gestion de l'authentification OAuth2 avec Google Ads
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from config.settings import GOOGLE_ADS_SCOPES, CLIENT_SECRET_FILE, DEBUG


class GoogleAdsAuth:
    """Gestion de l'authentification OAuth2 pour Google Ads"""

    def __init__(self):
        """Initialise le gestionnaire d'authentification"""
        self.scopes = GOOGLE_ADS_SCOPES
        self.client_secret_file = CLIENT_SECRET_FILE

    def check_client_secret_exists(self) -> bool:
        """Vérifie si le fichier client_secret.json existe"""
        return self.client_secret_file.exists()

    def get_refresh_token_interactive(self) -> Optional[str]:
        """
        Lance le flow OAuth2 interactif pour obtenir un refresh_token

        Returns:
            refresh_token si succès, None sinon
        """
        try:
            if not self.check_client_secret_exists():
                raise FileNotFoundError(
                    f"Fichier {self.client_secret_file} introuvable. "
                    "Téléchargez-le depuis Google Cloud Console."
                )

            # Créer le flow OAuth2
            flow = InstalledAppFlow.from_client_secrets_file(
                str(self.client_secret_file),
                scopes=self.scopes
            )

            # Lancer le serveur local pour l'authentification
            # Port 8080 par défaut (configurable)
            credentials = flow.run_local_server(
                port=8080,
                authorization_prompt_message="Autorisation en cours... Une fenêtre de navigateur va s'ouvrir.",
                success_message="✅ Autorisation réussie ! Vous pouvez fermer cette fenêtre.",
                open_browser=True
            )

            if DEBUG:
                print(f"✅ OAuth2 réussi")

            return credentials.refresh_token

        except Exception as e:
            if DEBUG:
                print(f"❌ Erreur OAuth2 : {e}")
            raise

    def validate_credentials(
        self,
        developer_token: str,
        client_id: str,
        client_secret: str,
        refresh_token: str,
    ) -> bool:
        """
        Valide un ensemble de credentials en testant l'accès à l'API

        Args:
            developer_token: Token développeur Google Ads
            client_id: OAuth2 Client ID
            client_secret: OAuth2 Client Secret
            refresh_token: OAuth2 Refresh Token

        Returns:
            True si les credentials sont valides, False sinon
        """
        try:
            # Import ici pour éviter les dépendances circulaires
            from google.ads.googleads.client import GoogleAdsClient

            # Créer un client temporaire pour tester
            credentials_dict = {
                "developer_token": developer_token,
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
                "use_proto_plus": True,
            }

            client = GoogleAdsClient.load_from_dict(credentials_dict)

            # Test simple : lister les comptes accessibles
            customer_service = client.get_service("CustomerService")
            accessible_customers = customer_service.list_accessible_customers()

            if accessible_customers and accessible_customers.resource_names:
                if DEBUG:
                    print(f"✅ Credentials valides — {len(accessible_customers.resource_names)} compte(s) accessible(s)")
                return True

            return False

        except Exception as e:
            if DEBUG:
                print(f"❌ Validation échouée : {e}")
            return False

    def build_credentials_dict(
        self,
        developer_token: str,
        client_id: str,
        client_secret: str,
        refresh_token: str,
        customer_id: str,
        login_customer_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Construit le dictionnaire de credentials au format attendu par l'API

        Args:
            developer_token: Token développeur
            client_id: OAuth2 Client ID
            client_secret: OAuth2 Client Secret
            refresh_token: OAuth2 Refresh Token
            customer_id: ID du compte Google Ads (sans tirets)
            login_customer_id: ID du compte MCC parent (optionnel)

        Returns:
            Dictionnaire de credentials
        """
        credentials = {
            "developer_token": developer_token,
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "customer_id": customer_id,
            "use_proto_plus": True,
        }

        if login_customer_id:
            credentials["login_customer_id"] = login_customer_id

        return credentials

    @staticmethod
    def format_customer_id(customer_id: str) -> str:
        """
        Formate un Customer ID en retirant les tirets

        Args:
            customer_id: ID avec ou sans tirets (ex: 123-456-7890 ou 1234567890)

        Returns:
            ID sans tirets (ex: 1234567890)
        """
        return customer_id.replace("-", "").strip()

    @staticmethod
    def validate_customer_id_format(customer_id: str) -> bool:
        """
        Valide le format d'un Customer ID (10 chiffres)

        Args:
            customer_id: ID à valider

        Returns:
            True si valide, False sinon
        """
        formatted_id = GoogleAdsAuth.format_customer_id(customer_id)
        return formatted_id.isdigit() and len(formatted_id) == 10


# Instance globale
auth = GoogleAdsAuth()
