"""
Système de cache pour réduire les appels à l'API Google Ads
"""

import json
import hashlib
from pathlib import Path
from typing import Any, Optional
from datetime import datetime, timedelta
from diskcache import Cache

from config.settings import CACHE_DIR, CACHE_DURATION, DEBUG


class CacheManager:
    """Gestionnaire de cache disque avec expiration"""

    def __init__(self, cache_duration: int = CACHE_DURATION):
        """
        Initialise le gestionnaire de cache

        Args:
            cache_duration: Durée de vie du cache en secondes (défaut: 3600 = 1h)
        """
        self.cache_dir = Path(CACHE_DIR)
        self.cache_dir.mkdir(exist_ok=True)

        # Utiliser diskcache pour le stockage
        self.cache = Cache(str(self.cache_dir))
        self.cache_duration = cache_duration

    def _generate_key(self, query: str, customer_id: str, params: dict = None) -> str:
        """
        Génère une clé de cache unique basée sur la requête et les paramètres

        Args:
            query: Requête GAQL
            customer_id: ID du compte
            params: Paramètres additionnels

        Returns:
            Clé de cache (hash MD5)
        """
        # Créer une chaîne unique combinant tous les paramètres
        key_data = f"{customer_id}:{query}"

        if params:
            # Trier les paramètres pour avoir une clé consistante
            sorted_params = json.dumps(params, sort_keys=True)
            key_data += f":{sorted_params}"

        # Générer un hash MD5
        return hashlib.md5(key_data.encode()).hexdigest()

    def get(
        self,
        query: str,
        customer_id: str,
        params: dict = None
    ) -> Optional[Any]:
        """
        Récupère une valeur du cache si elle existe et n'est pas expirée

        Args:
            query: Requête GAQL
            customer_id: ID du compte
            params: Paramètres additionnels

        Returns:
            Données en cache ou None si inexistant/expiré
        """
        try:
            key = self._generate_key(query, customer_id, params)

            # Vérifier si la clé existe
            if key in self.cache:
                cached_data = self.cache.get(key)

                if cached_data:
                    # Vérifier l'expiration
                    timestamp = cached_data.get("timestamp")
                    if timestamp:
                        cached_time = datetime.fromisoformat(timestamp)
                        expiration_time = cached_time + timedelta(seconds=self.cache_duration)

                        if datetime.now() < expiration_time:
                            if DEBUG:
                                age_seconds = (datetime.now() - cached_time).seconds
                                print(f"✅ Cache HIT (âge: {age_seconds}s) - {key[:8]}...")
                            return cached_data.get("data")
                        else:
                            if DEBUG:
                                print(f"⏰ Cache EXPIRÉ - {key[:8]}...")
                            # Supprimer l'entrée expirée
                            del self.cache[key]

            if DEBUG:
                print(f"❌ Cache MISS - {key[:8]}...")

            return None

        except Exception as e:
            if DEBUG:
                print(f"⚠️ Erreur lecture cache : {e}")
            return None

    def set(
        self,
        query: str,
        customer_id: str,
        data: Any,
        params: dict = None
    ) -> bool:
        """
        Stocke une valeur dans le cache

        Args:
            query: Requête GAQL
            customer_id: ID du compte
            data: Données à cacher
            params: Paramètres additionnels

        Returns:
            True si succès, False sinon
        """
        try:
            key = self._generate_key(query, customer_id, params)

            cached_data = {
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "customer_id": customer_id,
                "params": params,
                "data": data,
            }

            self.cache.set(key, cached_data)

            if DEBUG:
                print(f"💾 Données cachées - {key[:8]}...")

            return True

        except Exception as e:
            if DEBUG:
                print(f"⚠️ Erreur écriture cache : {e}")
            return False

    def clear(self, customer_id: Optional[str] = None) -> bool:
        """
        Vide le cache (entièrement ou pour un compte spécifique)

        Args:
            customer_id: Si fourni, supprime uniquement le cache de ce compte

        Returns:
            True si succès
        """
        try:
            if customer_id:
                # Supprimer uniquement les entrées de ce compte
                keys_to_delete = []
                for key in self.cache:
                    cached_data = self.cache.get(key)
                    if cached_data and cached_data.get("customer_id") == customer_id:
                        keys_to_delete.append(key)

                for key in keys_to_delete:
                    del self.cache[key]

                if DEBUG:
                    print(f"🗑️ Cache vidé pour {customer_id} ({len(keys_to_delete)} entrées)")

            else:
                # Vider tout le cache
                self.cache.clear()
                if DEBUG:
                    print("🗑️ Cache entièrement vidé")

            return True

        except Exception as e:
            if DEBUG:
                print(f"⚠️ Erreur vidage cache : {e}")
            return False

    def get_stats(self) -> dict:
        """
        Récupère des statistiques sur le cache

        Returns:
            Dictionnaire avec les stats (taille, nombre d'entrées, etc.)
        """
        try:
            stats = {
                "size_bytes": self.cache.volume(),
                "entries_count": len(self.cache),
                "cache_duration": self.cache_duration,
                "cache_dir": str(self.cache_dir),
            }
            return stats

        except Exception as e:
            if DEBUG:
                print(f"⚠️ Erreur stats cache : {e}")
            return {}


# Instance globale
cache_manager = CacheManager()
