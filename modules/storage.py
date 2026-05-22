"""
Gestion sécurisée du stockage des credentials (chiffrement AES-256)
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet

from config.settings import CREDENTIALS_DIR, ENCRYPTION_KEY, DEBUG


class SecureStorage:
    """Stockage sécurisé avec chiffrement AES-256"""

    def __init__(self):
        """Initialise le système de chiffrement"""
        self.credentials_dir = Path(CREDENTIALS_DIR)
        self.credentials_dir.mkdir(exist_ok=True)

        # Générer ou charger la clé de chiffrement
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher = Fernet(self.encryption_key)

    def _get_or_create_encryption_key(self) -> bytes:
        """Génère ou récupère la clé de chiffrement"""
        key_file = self.credentials_dir / ".key"

        # Si une clé existe dans .env, l'utiliser
        if ENCRYPTION_KEY:
            return ENCRYPTION_KEY.encode()

        # Sinon, charger depuis le fichier ou en créer une
        if key_file.exists():
            with open(key_file, "rb") as f:
                return f.read()
        else:
            # Générer une nouvelle clé
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)

            # Sécuriser le fichier (permissions)
            os.chmod(key_file, 0o600)

            if DEBUG:
                print(f"✅ Nouvelle clé de chiffrement générée : {key_file}")

            return key

    def save_credentials(self, user_id: str, credentials: Dict[str, Any]) -> bool:
        """
        Sauvegarde les credentials de manière sécurisée

        Args:
            user_id: Identifiant unique de l'utilisateur (Customer ID)
            credentials: Dictionnaire contenant les credentials

        Returns:
            True si succès, False sinon
        """
        try:
            # Convertir en JSON
            credentials_json = json.dumps(credentials)

            # Chiffrer
            encrypted_data = self.cipher.encrypt(credentials_json.encode())

            # Sauvegarder dans un fichier nommé d'après le user_id
            credentials_file = self.credentials_dir / f"{user_id}.enc"
            with open(credentials_file, "wb") as f:
                f.write(encrypted_data)

            # Sécuriser le fichier
            os.chmod(credentials_file, 0o600)

            if DEBUG:
                print(f"✅ Credentials sauvegardés pour {user_id}")

            return True

        except Exception as e:
            if DEBUG:
                print(f"❌ Erreur lors de la sauvegarde : {e}")
            return False

    def load_credentials(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Charge et déchiffre les credentials

        Args:
            user_id: Identifiant unique de l'utilisateur

        Returns:
            Dictionnaire des credentials ou None si non trouvé
        """
        try:
            credentials_file = self.credentials_dir / f"{user_id}.enc"

            if not credentials_file.exists():
                if DEBUG:
                    print(f"⚠️ Aucun credentials trouvé pour {user_id}")
                return None

            # Lire le fichier chiffré
            with open(credentials_file, "rb") as f:
                encrypted_data = f.read()

            # Déchiffrer
            decrypted_data = self.cipher.decrypt(encrypted_data)

            # Parser le JSON
            credentials = json.loads(decrypted_data.decode())

            if DEBUG:
                print(f"✅ Credentials chargés pour {user_id}")

            return credentials

        except Exception as e:
            if DEBUG:
                print(f"❌ Erreur lors du chargement : {e}")
            return None

    def delete_credentials(self, user_id: str) -> bool:
        """
        Supprime les credentials d'un utilisateur

        Args:
            user_id: Identifiant unique de l'utilisateur

        Returns:
            True si succès, False sinon
        """
        try:
            credentials_file = self.credentials_dir / f"{user_id}.enc"

            if credentials_file.exists():
                credentials_file.unlink()
                if DEBUG:
                    print(f"✅ Credentials supprimés pour {user_id}")
                return True

            return False

        except Exception as e:
            if DEBUG:
                print(f"❌ Erreur lors de la suppression : {e}")
            return False

    def list_users(self) -> list[str]:
        """
        Liste tous les utilisateurs ayant des credentials stockés

        Returns:
            Liste des user_ids
        """
        try:
            users = []
            for file in self.credentials_dir.glob("*.enc"):
                user_id = file.stem  # Nom du fichier sans extension
                users.append(user_id)
            return users
        except Exception as e:
            if DEBUG:
                print(f"❌ Erreur lors du listing : {e}")
            return []

    def credentials_exist(self, user_id: str) -> bool:
        """Vérifie si des credentials existent pour un utilisateur"""
        credentials_file = self.credentials_dir / f"{user_id}.enc"
        return credentials_file.exists()


# Instance globale
storage = SecureStorage()
