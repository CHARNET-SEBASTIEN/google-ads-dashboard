"""
Module pour charger les données exportées par Google Ads Script
Alternative à l'API Google Ads - pas besoin de Developer Token
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import requests

from config.settings import DEBUG


class ScriptDataLoader:
    """Charge les données exportées par Google Ads Script"""

    def __init__(self):
        """Initialise le loader"""
        self.data_dir = Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.data_file = self.data_dir / "google_ads_data.json"

    def load_data(self) -> Optional[Dict[str, Any]]:
        """
        Charge les données depuis le fichier JSON

        Returns:
            Dictionnaire contenant toutes les données ou None si erreur
        """
        try:
            if not self.data_file.exists():
                if DEBUG:
                    print(f"⚠️ Fichier de données introuvable : {self.data_file}")
                return None

            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if DEBUG:
                print(f"✅ Données chargées : {len(data.get('campaigns', []))} campagnes")

            return data

        except Exception as e:
            if DEBUG:
                print(f"❌ Erreur lors du chargement des données : {e}")
            return None

    def get_campaigns(self) -> list:
        """Récupère la liste des campagnes"""
        data = self.load_data()
        if data:
            return data.get('campaigns', [])
        return []

    def get_keywords(self, campaign_id: Optional[int] = None) -> list:
        """Récupère les mots-clés (filtrés par campagne si campaign_id fourni)"""
        data = self.load_data()
        if not data:
            return []

        keywords = data.get('keywords', [])

        if campaign_id:
            keywords = [kw for kw in keywords if kw.get('campaignId') == campaign_id]

        return keywords

    def get_ads(self, campaign_id: Optional[int] = None) -> list:
        """Récupère les annonces (filtrées par campagne si campaign_id fourni)"""
        data = self.load_data()
        if not data:
            return []

        ads = data.get('ads', [])

        if campaign_id:
            ads = [ad for ad in ads if ad.get('campaignId') == campaign_id]

        return ads

    def get_search_terms(self, campaign_id: Optional[int] = None) -> list:
        """Récupère les termes de recherche (filtrés par campagne si campaign_id fourni)"""
        data = self.load_data()
        if not data:
            return []

        search_terms = data.get('searchTerms', [])

        if campaign_id:
            search_terms = [st for st in search_terms if st.get('campaignId') == campaign_id]

        return search_terms

    def get_performance(self, campaign_id: Optional[int] = None) -> list:
        """Récupère les données de performance (filtrées par campagne si campaign_id fourni)"""
        data = self.load_data()
        if not data:
            return []

        performance = data.get('performance', [])

        if campaign_id:
            performance = [p for p in performance if p.get('campaignId') == campaign_id]

        return performance

    def get_account_info(self) -> Optional[Dict[str, Any]]:
        """Récupère les informations du compte"""
        data = self.load_data()
        if data:
            return data.get('account', {})
        return None

    def get_last_update(self) -> Optional[str]:
        """Récupère la date de dernière mise à jour"""
        data = self.load_data()
        if data:
            return data.get('timestamp', None)
        return None

    def data_exists(self) -> bool:
        """Vérifie si des données existent"""
        return self.data_file.exists()

    def import_from_file(self, file_path: str) -> bool:
        """
        Importe des données depuis un fichier JSON externe

        Args:
            file_path: Chemin vers le fichier JSON

        Returns:
            True si succès, False sinon
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Valider que les données contiennent les champs requis
            required_fields = ['campaigns', 'keywords', 'ads']
            if not all(field in data for field in required_fields):
                if DEBUG:
                    print(f"❌ Fichier invalide - champs manquants")
                return False

            # Copier le fichier dans le répertoire data
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            if DEBUG:
                print(f"✅ Données importées depuis {file_path}")

            return True

        except Exception as e:
            if DEBUG:
                print(f"❌ Erreur lors de l'import : {e}")
            return False

    def download_from_google_drive(self, file_id: str) -> bool:
        """
        Télécharge les données depuis Google Drive

        Args:
            file_id: ID du fichier dans Google Drive

        Returns:
            True si succès, False sinon
        """
        try:
            # URL de téléchargement Google Drive
            url = f"https://drive.google.com/uc?export=download&id={file_id}"

            response = requests.get(url, timeout=30)
            response.raise_for_status()

            data = response.json()

            # Sauvegarder localement
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            if DEBUG:
                print(f"✅ Données téléchargées depuis Google Drive")

            return True

        except Exception as e:
            if DEBUG:
                print(f"❌ Erreur téléchargement Google Drive : {e}")
            return False

    def refresh_from_url(self, url: str) -> bool:
        """
        Récupère les dernières données depuis une URL

        Args:
            url: URL du fichier JSON

        Returns:
            True si succès, False sinon
        """
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            data = response.json()

            # Sauvegarder localement
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            if DEBUG:
                print(f"✅ Données actualisées depuis {url}")

            return True

        except Exception as e:
            if DEBUG:
                print(f"❌ Erreur actualisation : {e}")
            return False


# Instance globale
script_loader = ScriptDataLoader()
