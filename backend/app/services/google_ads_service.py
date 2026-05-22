"""
Google Ads Service
Gestion de l'authentification et du client Google Ads API
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from google.ads.googleads.client import GoogleAdsClient
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

from app.config.settings import settings


class GoogleAdsService:
    """Service pour gérer l'authentification Google Ads"""

    def __init__(self):
        self.scopes = ["https://www.googleapis.com/auth/adwords"]
        self.client_secret_file = settings.BASE_DIR / "client_secret.json"
        self.credentials_dir = settings.CREDENTIALS_DIR

    def check_client_secret_exists(self) -> bool:
        """Vérifie si client_secret.json existe"""
        return self.client_secret_file.exists()

    def create_oauth_flow(self, redirect_uri: str = "http://localhost:8080/callback") -> Flow:
        """
        Crée un flow OAuth2 pour l'authentification

        Args:
            redirect_uri: URI de redirection après auth

        Returns:
            Flow OAuth2
        """
        if not self.check_client_secret_exists():
            raise FileNotFoundError(
                f"client_secret.json not found at {self.client_secret_file}"
            )

        flow = Flow.from_client_secrets_file(
            str(self.client_secret_file),
            scopes=self.scopes,
            redirect_uri=redirect_uri
        )

        return flow

    def get_authorization_url(self, redirect_uri: str) -> tuple[str, str]:
        """
        Génère l'URL d'autorisation OAuth

        Returns:
            (authorization_url, state)
        """
        flow = self.create_oauth_flow(redirect_uri)
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )

        return authorization_url, state

    def exchange_code_for_token(self, code: str, redirect_uri: str) -> str:
        """
        Échange le code d'autorisation contre un refresh_token

        Args:
            code: Authorization code from OAuth callback
            redirect_uri: Must match the one used in authorization

        Returns:
            refresh_token
        """
        flow = self.create_oauth_flow(redirect_uri)
        flow.fetch_token(code=code)

        credentials = flow.credentials
        return credentials.refresh_token

    def validate_credentials(
        self,
        developer_token: str,
        client_id: str,
        client_secret: str,
        refresh_token: str
    ) -> bool:
        """
        Valide des credentials en testant l'accès API

        Returns:
            True si valide, False sinon
        """
        try:
            credentials_dict = {
                "developer_token": developer_token,
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
                "use_proto_plus": True,
            }

            client = GoogleAdsClient.load_from_dict(credentials_dict)
            customer_service = client.get_service("CustomerService")
            accessible_customers = customer_service.list_accessible_customers()

            return bool(accessible_customers and accessible_customers.resource_names)

        except Exception as e:
            print(f"Credential validation failed: {e}")
            return False

    def get_accessible_customers(
        self,
        developer_token: str,
        client_id: str,
        client_secret: str,
        refresh_token: str
    ) -> List[str]:
        """
        Récupère la liste des comptes accessibles

        Returns:
            Liste des customer IDs
        """
        try:
            credentials_dict = {
                "developer_token": developer_token,
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
                "use_proto_plus": True,
            }

            client = GoogleAdsClient.load_from_dict(credentials_dict)
            customer_service = client.get_service("CustomerService")
            accessible_customers = customer_service.list_accessible_customers()

            # Extraire les IDs (format: customers/1234567890)
            customer_ids = [
                resource_name.split('/')[-1]
                for resource_name in accessible_customers.resource_names
            ]

            return customer_ids

        except Exception as e:
            print(f"Failed to get accessible customers: {e}")
            return []

    def get_customer_info(
        self,
        developer_token: str,
        client_id: str,
        client_secret: str,
        refresh_token: str,
        customer_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Récupère les informations d'un compte client

        Returns:
            Dict avec infos du compte ou None
        """
        try:
            credentials_dict = {
                "developer_token": developer_token,
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
                "customer_id": customer_id,
                "use_proto_plus": True,
            }

            client = GoogleAdsClient.load_from_dict(credentials_dict)
            ga_service = client.get_service("GoogleAdsService")

            query = """
                SELECT
                    customer.id,
                    customer.descriptive_name,
                    customer.currency_code,
                    customer.time_zone,
                    customer.manager
                FROM customer
                WHERE customer.id = {customer_id}
            """.format(customer_id=customer_id)

            response = ga_service.search(customer_id=customer_id, query=query)

            for row in response:
                customer = row.customer
                return {
                    "id": str(customer.id),
                    "name": customer.descriptive_name,
                    "currency": customer.currency_code,
                    "timezone": customer.time_zone,
                    "is_manager": customer.manager
                }

            return None

        except Exception as e:
            print(f"Failed to get customer info: {e}")
            return None

    def save_credentials(self, user_id: str, credentials: Dict[str, Any]) -> bool:
        """
        Sauvegarde les credentials de manière sécurisée

        Args:
            user_id: Identifiant unique de l'utilisateur
            credentials: Dict des credentials

        Returns:
            True si succès
        """
        try:
            credentials_file = self.credentials_dir / f"{user_id}.json"

            with open(credentials_file, 'w') as f:
                json.dump(credentials, f, indent=2)

            # Permissions restrictives
            credentials_file.chmod(0o600)

            return True

        except Exception as e:
            print(f"Failed to save credentials: {e}")
            return False

    def load_credentials(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Charge les credentials d'un utilisateur

        Args:
            user_id: Identifiant de l'utilisateur

        Returns:
            Dict des credentials ou None
        """
        try:
            credentials_file = self.credentials_dir / f"{user_id}.json"

            if not credentials_file.exists():
                return None

            with open(credentials_file, 'r') as f:
                credentials = json.load(f)

            return credentials

        except Exception as e:
            print(f"Failed to load credentials: {e}")
            return None

    def delete_credentials(self, user_id: str) -> bool:
        """
        Supprime les credentials d'un utilisateur

        Args:
            user_id: Identifiant de l'utilisateur

        Returns:
            True si succès
        """
        try:
            credentials_file = self.credentials_dir / f"{user_id}.json"

            if credentials_file.exists():
                credentials_file.unlink()

            return True

        except Exception as e:
            print(f"Failed to delete credentials: {e}")
            return False

    @staticmethod
    def format_customer_id(customer_id: str) -> str:
        """Formate un Customer ID (retire les tirets)"""
        return customer_id.replace("-", "").strip()

    @staticmethod
    def validate_customer_id_format(customer_id: str) -> bool:
        """Valide le format d'un Customer ID (10 chiffres)"""
        formatted_id = GoogleAdsService.format_customer_id(customer_id)
        return formatted_id.isdigit() and len(formatted_id) == 10


# Instance globale
google_ads_service = GoogleAdsService()
