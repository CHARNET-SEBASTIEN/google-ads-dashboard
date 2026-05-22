"""
Configuration globale de Dashboard ADS.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Répertoire racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Répertoires de stockage
CREDENTIALS_DIR = BASE_DIR / os.getenv("CREDENTIALS_DIR", ".credentials")
CACHE_DIR = BASE_DIR / os.getenv("CACHE_DIR", ".cache")
EXPORTS_DIR = BASE_DIR / "exports"

# Créer les répertoires s'ils n'existent pas
CREDENTIALS_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)
EXPORTS_DIR.mkdir(exist_ok=True)

# Sécurité
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "")

# Cache
CACHE_DURATION = int(os.getenv("CACHE_DURATION", "3600"))  # 1 heure par défaut

# Debug
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Port
PORT = int(os.getenv("PORT", "8501"))

# OAuth2 Scopes pour Google Ads
GOOGLE_ADS_SCOPES = [
    "https://www.googleapis.com/auth/adwords"
]

# Fichier client_secret.json (credentials OAuth)
CLIENT_SECRET_FILE = BASE_DIR / "client_secret.json"

# API Google Ads
GOOGLE_ADS_API_VERSION = "v16"

# Périodes de temps prédéfinies
DATE_RANGES = {
    "Aujourd'hui": "TODAY",
    "Hier": "YESTERDAY",
    "7 derniers jours": "LAST_7_DAYS",
    "30 derniers jours": "LAST_30_DAYS",
    "Ce mois-ci": "THIS_MONTH",
    "Mois dernier": "LAST_MONTH",
    "90 derniers jours": "LAST_90_DAYS",
}

# Couleurs pour les statuts de campagne
STATUS_COLORS = {
    "ENABLED": "🟢",
    "PAUSED": "🟡",
    "REMOVED": "🔴",
    "UNKNOWN": "⚪",
}

# Types de campagne (traduction)
CAMPAIGN_TYPES = {
    "SEARCH": "Recherche",
    "DISPLAY": "Display",
    "SHOPPING": "Shopping",
    "VIDEO": "Vidéo",
    "PERFORMANCE_MAX": "Performance Max",
    "MULTI_CHANNEL": "Multi-canaux",
    "HOTEL": "Hôtel",
    "LOCAL": "Local",
    "SMART": "Smart",
    "UNKNOWN": "Inconnu",
}

# Stratégies d'enchères (traduction)
BIDDING_STRATEGIES = {
    "TARGET_CPA": "CPA cible",
    "TARGET_ROAS": "ROAS cible",
    "MAXIMIZE_CONVERSIONS": "Maximiser les conversions",
    "MAXIMIZE_CONVERSION_VALUE": "Maximiser la valeur de conversion",
    "TARGET_SPEND": "Dépenses cibles",
    "MANUAL_CPC": "CPC manuel",
    "ENHANCED_CPC": "CPC optimisé",
    "TARGET_IMPRESSION_SHARE": "Part d'impressions cible",
    "MANUAL_CPM": "CPM manuel",
    "MANUAL_CPV": "CPV manuel",
    "UNKNOWN": "Inconnu",
}

# Types de correspondance de mots-clés
MATCH_TYPES = {
    "EXACT": "Exacte",
    "PHRASE": "Expression",
    "BROAD": "Large",
}

# Statuts de diffusion des mots-clés
KEYWORD_STATUS = {
    "ENABLED": "Éligible",
    "PAUSED": "Suspendu",
    "REMOVED": "Supprimé",
}

# Force des annonces
AD_STRENGTH = {
    "EXCELLENT": "Excellente",
    "GOOD": "Bonne",
    "AVERAGE": "Moyenne",
    "POOR": "Mauvaise",
    "UNSPECIFIED": "Non spécifié",
    "UNKNOWN": "Inconnu",
}

# Couleurs du design Silao-treehouse
SILAO_COLORS = {
    "primary": "#1a4d8f",  # hsl(220 80% 29%) - Deep blue
    "secondary": "#ed7014",  # hsl(30 100% 47%) - Orange
    "accent": "#ffeb3b",  # hsl(56 100% 50%) - Yellow
    "brand_violet": "#3a2781",  # hsl(247 54% 33%)
    "background": "#fbfcfe",  # hsl(216 100% 99%)
    "foreground": "#1a202c",  # hsl(222 47% 11%)
    "muted": "#f0f4f8",  # hsl(210 40% 96%)
    "border": "#e2e8f0",  # hsl(214 32% 91%)
    "success": "#22c55e",  # Green
    "warning": "#f59e0b",  # Amber
    "error": "#ef4444",  # Red
}

# Sévérités de diagnostic
DIAGNOSTIC_SEVERITY = {
    "CRITIQUE": {"emoji": "🔴", "color": SILAO_COLORS["error"]},
    "IMPORTANT": {"emoji": "🟠", "color": SILAO_COLORS["secondary"]},
    "CONSEIL": {"emoji": "🟡", "color": SILAO_COLORS["warning"]},
    "INFO": {"emoji": "🔵", "color": SILAO_COLORS["primary"]},
}

# Configuration Streamlit
STREAMLIT_CONFIG = {
    "page_title": "Dashboard ADS",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}
