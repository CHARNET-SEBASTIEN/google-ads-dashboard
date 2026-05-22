"""
Client wrapper pour l'API Google Ads avec gestion du cache
"""

from typing import List, Dict, Any, Optional
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from config.settings import DEBUG
from modules.cache import cache_manager


class GoogleAdsClientWrapper:
    """Wrapper autour du client Google Ads avec cache intégré"""

    def __init__(self, credentials: Dict[str, Any]):
        """
        Initialise le client Google Ads

        Args:
            credentials: Dictionnaire contenant developer_token, client_id, etc.
        """
        self.credentials = credentials
        self.customer_id = credentials.get("customer_id")
        self.client = GoogleAdsClient.load_from_dict(credentials)

        if DEBUG:
            print(f"✅ Client Google Ads initialisé pour {self.customer_id}")

    def execute_query(
        self,
        query: str,
        use_cache: bool = True,
        params: dict = None
    ) -> List[Any]:
        """
        Exécute une requête GAQL avec gestion du cache

        Args:
            query: Requête GAQL
            use_cache: Utiliser le cache ou non
            params: Paramètres additionnels pour la clé de cache

        Returns:
            Liste des résultats
        """
        # Vérifier le cache
        if use_cache:
            cached_results = cache_manager.get(query, self.customer_id, params)
            if cached_results is not None:
                return cached_results

        # Exécuter la requête via l'API
        try:
            ga_service = self.client.get_service("GoogleAdsService")

            # Stream des résultats
            stream = ga_service.search_stream(
                customer_id=self.customer_id,
                query=query
            )

            # Collecter tous les résultats
            results = []
            for batch in stream:
                for row in batch.results:
                    results.append(row)

            # Cacher les résultats
            if use_cache:
                cache_manager.set(query, self.customer_id, results, params)

            if DEBUG:
                print(f"✅ Requête exécutée : {len(results)} résultats")

            return results

        except GoogleAdsException as ex:
            error_msg = self._format_google_ads_error(ex)
            if DEBUG:
                print(f"❌ Erreur Google Ads : {error_msg}")
            raise Exception(error_msg)

        except Exception as e:
            if DEBUG:
                print(f"❌ Erreur requête : {e}")
            raise

    def get_accessible_customers(self) -> List[str]:
        """
        Récupère la liste des comptes accessibles

        Returns:
            Liste des resource_names des comptes
        """
        try:
            customer_service = self.client.get_service("CustomerService")
            accessible_customers = customer_service.list_accessible_customers()

            return accessible_customers.resource_names if accessible_customers else []

        except Exception as e:
            if DEBUG:
                print(f"❌ Erreur get_accessible_customers : {e}")
            raise

    def get_customer_info(self) -> Dict[str, Any]:
        """
        Récupère les informations du compte client

        Returns:
            Dictionnaire avec les infos du compte
        """
        query = """
            SELECT
                customer.id,
                customer.descriptive_name,
                customer.currency_code,
                customer.time_zone,
                customer.manager,
                customer.test_account
            FROM customer
            WHERE customer.id = {customer_id}
        """.format(customer_id=self.customer_id)

        results = self.execute_query(query, use_cache=True)

        if results:
            customer = results[0].customer
            return {
                "id": customer.id,
                "name": customer.descriptive_name,
                "currency": customer.currency_code,
                "timezone": customer.time_zone,
                "is_manager": customer.manager,
                "is_test": customer.test_account,
            }

        return {}

    def add_negative_keyword(
        self,
        campaign_id: str,
        keyword_text: str,
        match_type: str = "EXACT"
    ) -> bool:
        """
        Ajoute un mot-clé négatif à une campagne

        Args:
            campaign_id: ID de la campagne
            keyword_text: Texte du mot-clé
            match_type: Type de correspondance (EXACT, PHRASE, BROAD)

        Returns:
            True si succès
        """
        try:
            campaign_criterion_service = self.client.get_service(
                "CampaignCriterionService"
            )

            # Créer l'opération
            campaign_criterion_operation = self.client.get_type(
                "CampaignCriterionOperation"
            )

            # Créer le critère négatif
            campaign_criterion = campaign_criterion_operation.create
            campaign_criterion.campaign = self.client.get_service(
                "CampaignService"
            ).campaign_path(self.customer_id, campaign_id)

            campaign_criterion.negative = True
            campaign_criterion.keyword.text = keyword_text
            campaign_criterion.keyword.match_type = self.client.enums.KeywordMatchTypeEnum[match_type]

            # Exécuter l'opération
            response = campaign_criterion_service.mutate_campaign_criteria(
                customer_id=self.customer_id,
                operations=[campaign_criterion_operation]
            )

            if DEBUG:
                print(f"✅ Mot-clé négatif ajouté : {keyword_text}")

            # Invalider le cache pour cette campagne
            cache_manager.clear(self.customer_id)

            return True

        except Exception as e:
            if DEBUG:
                print(f"❌ Erreur ajout mot-clé négatif : {e}")
            raise

    @staticmethod
    def _format_google_ads_error(ex: GoogleAdsException) -> str:
        """
        Formate les erreurs Google Ads de manière lisible

        Args:
            ex: Exception Google Ads

        Returns:
            Message d'erreur formaté en français
        """
        error_messages = []

        for error in ex.failure.errors:
            error_code = error.error_code

            # Mapping des codes d'erreur vers messages en français
            if hasattr(error_code, "authentication_error"):
                if error_code.authentication_error.name == "CUSTOMER_NOT_FOUND":
                    error_messages.append(
                        "❌ ID de compte introuvable. Vérifiez le format (ex : 1234567890 sans tirets)."
                    )
                elif error_code.authentication_error.name == "AUTHENTICATION_ERROR":
                    error_messages.append(
                        "❌ Erreur d'authentification. Token expiré ou révoqué. "
                        "Reconnectez-vous via la page Configuration."
                    )
                else:
                    error_messages.append(f"❌ Erreur d'authentification : {error.message}")

            elif hasattr(error_code, "authorization_error"):
                if error_code.authorization_error.name == "DEVELOPER_TOKEN_NOT_APPROVED":
                    error_messages.append(
                        "❌ Votre Developer Token n'est pas encore approuvé par Google. "
                        "Vérifiez le statut dans Google Ads → Outils → Centre API. "
                        "En mode test, vous pouvez uniquement accéder à votre propre compte."
                    )
                else:
                    error_messages.append(f"❌ Erreur d'autorisation : {error.message}")

            elif hasattr(error_code, "quota_error"):
                error_messages.append(
                    "❌ Limite de requêtes API atteinte. Réessayez dans quelques minutes "
                    "ou activez le cache pour réduire les appels."
                )

            elif hasattr(error_code, "request_error"):
                error_messages.append(f"❌ Erreur de requête : {error.message}")

            else:
                error_messages.append(f"❌ Erreur : {error.message}")

        return "\n".join(error_messages) if error_messages else str(ex)


def create_client(credentials: Dict[str, Any]) -> GoogleAdsClientWrapper:
    """
    Factory function pour créer un client Google Ads

    Args:
        credentials: Dictionnaire de credentials

    Returns:
        Instance de GoogleAdsClientWrapper
    """
    return GoogleAdsClientWrapper(credentials)
