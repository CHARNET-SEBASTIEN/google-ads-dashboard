"""
Data Loader Service
Gestion de l'import et du chargement des données Google Ads
"""

import json
import requests
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.config.settings import settings


class DataLoaderService:
    """Service pour charger et gérer les données Google Ads"""

    def __init__(self):
        self.data_dir = settings.DATA_DIR
        self.data_file = self.data_dir / "google_ads_data.json"

    def load_data(self) -> Optional[Dict[str, Any]]:
        """
        Charge les données depuis le fichier JSON

        Returns:
            Dict contenant toutes les données ou None
        """
        try:
            if not self.data_file.exists():
                return None

            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return data

        except Exception as e:
            print(f"Failed to load data: {e}")
            return None

    def get_campaigns(self) -> List[Dict[str, Any]]:
        """Récupère la liste des campagnes"""
        data = self.load_data()
        return data.get('campaigns', []) if data else []

    def get_keywords(self, campaign_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Récupère les mots-clés (filtrés par campagne si fourni)"""
        data = self.load_data()
        if not data:
            return []

        keywords = data.get('keywords', [])

        if campaign_id:
            keywords = [kw for kw in keywords if str(kw.get('campaignId')) == campaign_id]

        return keywords

    def get_ads(self, campaign_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Récupère les annonces (filtrées par campagne si fourni)"""
        data = self.load_data()
        if not data:
            return []

        ads = data.get('ads', [])

        if campaign_id:
            ads = [ad for ad in ads if str(ad.get('campaignId')) == campaign_id]

        return ads

    def get_search_terms(self, campaign_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Récupère les termes de recherche (filtrés par campagne si fourni)"""
        data = self.load_data()
        if not data:
            return []

        search_terms = data.get('searchTerms', [])

        if campaign_id:
            search_terms = [st for st in search_terms if str(st.get('campaignId')) == campaign_id]

        return search_terms

    def get_performance(self, campaign_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Récupère les données de performance (filtrées par campagne si fourni)"""
        data = self.load_data()
        if not data:
            return []

        performance = data.get('performance', [])

        if campaign_id:
            performance = [p for p in performance if str(p.get('campaignId')) == campaign_id]

        return performance

    def get_account_info(self) -> Optional[Dict[str, Any]]:
        """Récupère les informations du compte"""
        data = self.load_data()
        return data.get('account', {}) if data else None

    def get_last_update(self) -> Optional[str]:
        """Récupère la date de dernière mise à jour"""
        data = self.load_data()
        return data.get('timestamp') if data else None

    def data_exists(self) -> bool:
        """Vérifie si des données existent"""
        return self.data_file.exists()

    def save_data(self, data: Dict[str, Any]) -> bool:
        """
        Sauvegarde les données dans le fichier JSON

        Args:
            data: Données à sauvegarder

        Returns:
            True si succès
        """
        try:
            # Valider les champs requis
            required_fields = ['campaigns', 'keywords', 'ads']
            if not all(field in data for field in required_fields):
                raise ValueError("Missing required fields in data")

            # Ajouter timestamp si absent
            if 'timestamp' not in data:
                data['timestamp'] = datetime.utcnow().isoformat()

            # Sauvegarder
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"Failed to save data: {e}")
            return False

    def import_from_file(self, file_path: str) -> bool:
        """
        Importe des données depuis un fichier JSON

        Args:
            file_path: Chemin vers le fichier

        Returns:
            True si succès
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return self.save_data(data)

        except Exception as e:
            print(f"Failed to import from file: {e}")
            return False

    def download_from_google_drive(self, file_id: str, save_url: bool = True) -> bool:
        """
        Télécharge les données depuis Google Drive

        Args:
            file_id: ID du fichier Google Drive
            save_url: Si True, sauvegarde l'URL pour les prochains rafraîchissements

        Returns:
            True si succès
        """
        try:
            # Essayer plusieurs formats d'URL Google Drive
            urls = [
                f"https://drive.google.com/uc?export=download&id={file_id}",
                f"https://drive.google.com/uc?id={file_id}&export=download",
                f"https://docs.google.com/uc?export=download&id={file_id}"
            ]

            data = None
            last_error = None

            for url in urls:
                try:
                    print(f"Trying URL: {url}")
                    response = requests.get(url, timeout=30, allow_redirects=True)

                    # Vérifier si c'est du JSON
                    content_type = response.headers.get('Content-Type', '')

                    if response.status_code == 200:
                        # Essayer de parser en JSON
                        try:
                            data = response.json()
                            print(f"✅ Successfully downloaded from: {url}")
                            break
                        except json.JSONDecodeError:
                            # Peut-être une page HTML d'erreur
                            if 'html' in content_type.lower():
                                continue
                            raise

                except requests.exceptions.RequestException as e:
                    last_error = e
                    continue

            if data is None:
                raise Exception(f"Failed to download from any URL. Last error: {last_error}")

            # Valider les données
            if 'campaigns' not in data:
                raise Exception("Invalid data format: missing 'campaigns' field")

            # Sauvegarder les données
            if self.save_data(data):
                # Sauvegarder l'URL pour les prochains rafraîchissements
                if save_url:
                    self._save_drive_config(file_id)
                return True

            return False

        except Exception as e:
            print(f"Failed to download from Google Drive: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _save_drive_config(self, file_id: str):
        """Sauvegarde la configuration Google Drive"""
        try:
            config_file = self.data_dir / 'drive_config.json'
            config = {
                'file_id': file_id,
                'last_sync': datetime.utcnow().isoformat()
            }
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Failed to save drive config: {e}")

    def get_drive_config(self) -> Optional[Dict[str, str]]:
        """Récupère la configuration Google Drive sauvegardée"""
        try:
            config_file = self.data_dir / 'drive_config.json'
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Failed to load drive config: {e}")
        return None

    def refresh_from_drive(self) -> bool:
        """Rafraîchit les données depuis le dernier fichier Drive configuré"""
        config = self.get_drive_config()
        if not config or 'file_id' not in config:
            return False

        return self.download_from_google_drive(config['file_id'], save_url=False)

    def refresh_from_url(self, url: str) -> bool:
        """
        Actualise les données depuis une URL

        Args:
            url: URL du fichier JSON

        Returns:
            True si succès
        """
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            data = response.json()

            return self.save_data(data)

        except Exception as e:
            print(f"Failed to refresh from URL: {e}")
            return False

    def get_stats(self) -> Dict[str, int]:
        """
        Retourne les statistiques des données chargées

        Returns:
            Dict avec les counts
        """
        data = self.load_data()
        if not data:
            return {
                "campaigns": 0,
                "keywords": 0,
                "ads": 0,
                "search_terms": 0
            }

        return {
            "campaigns": len(data.get('campaigns', [])),
            "keywords": len(data.get('keywords', [])),
            "ads": len(data.get('ads', [])),
            "search_terms": len(data.get('searchTerms', []))
        }


# Instance globale
data_loader_service = DataLoaderService()
