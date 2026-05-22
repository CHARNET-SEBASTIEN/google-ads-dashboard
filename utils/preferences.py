"""
Gestion des préférences utilisateur
Sauvegarde : langue, mode sombre, etc.
"""

import json
from pathlib import Path
from typing import Dict, Any


class UserPreferences:
    """Gestion des préférences utilisateur avec persistance"""

    def __init__(self):
        self.prefs_file = Path(__file__).parent.parent / ".user_preferences.json"
        self.preferences = self.load()

    def load(self) -> Dict[str, Any]:
        """Charge les préférences depuis le fichier"""
        if self.prefs_file.exists():
            try:
                with open(self.prefs_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass

        # Préférences par défaut
        return {
            "language": "fr",
            "dark_mode": False,
            "last_campaign_id": None,
        }

    def save(self):
        """Sauvegarde les préférences dans le fichier"""
        try:
            with open(self.prefs_file, 'w', encoding='utf-8') as f:
                json.dump(self.preferences, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur sauvegarde préférences : {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Récupère une préférence"""
        return self.preferences.get(key, default)

    def set(self, key: str, value: Any):
        """Définit une préférence et sauvegarde"""
        self.preferences[key] = value
        self.save()

    def get_language(self) -> str:
        """Récupère la langue préférée"""
        return self.get("language", "fr")

    def set_language(self, lang: str):
        """Définit la langue préférée"""
        self.set("language", lang)

    def is_dark_mode(self) -> bool:
        """Vérifie si le mode sombre est activé"""
        return self.get("dark_mode", False)

    def set_dark_mode(self, enabled: bool):
        """Active/désactive le mode sombre"""
        self.set("dark_mode", enabled)

    def toggle_dark_mode(self) -> bool:
        """Bascule le mode sombre et retourne le nouvel état"""
        new_state = not self.is_dark_mode()
        self.set_dark_mode(new_state)
        return new_state


# Instance globale
user_prefs = UserPreferences()
