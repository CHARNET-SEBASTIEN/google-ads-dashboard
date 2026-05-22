"""
Système d'internationalisation (i18n)
Support : Français, Anglais, Allemand
"""

import streamlit as st

# Dictionnaire de traductions
TRANSLATIONS = {
    "fr": {
        # Navigation
        "home": "Accueil",
        "config": "Configuration",
        "overview": "Vue d'ensemble",
        "campaign_detail": "Détail campagne",
        "search_terms": "Termes de recherche",
        "diagnostic": "Diagnostic",

        # Header
        "app_title": "Dashboard ADS",
        "welcome": "Bienvenue",
        "connected": "Connecté",
        "not_connected": "Non connecté",

        # Common actions
        "refresh": "Actualiser",
        "export": "Exporter",
        "import": "Importer",
        "search": "Rechercher",
        "filter": "Filtrer",
        "download": "Télécharger",
        "close": "Fermer",
        "save": "Enregistrer",
        "cancel": "Annuler",

        # Metrics
        "impressions": "Impressions",
        "clicks": "Clics",
        "ctr": "CTR",
        "cost": "Coût",
        "conversions": "Conversions",
        "conversion_rate": "Taux de conversion",
        "avg_cpc": "CPC moyen",
        "cpa": "CPA",

        # Status
        "enabled": "Active",
        "paused": "En pause",
        "removed": "Supprimée",
        "all": "Toutes",

        # Campaign types
        "search": "Recherche",
        "display": "Display",
        "shopping": "Shopping",
        "video": "Vidéo",

        # Time periods
        "today": "Aujourd'hui",
        "yesterday": "Hier",
        "last_7_days": "7 derniers jours",
        "last_30_days": "30 derniers jours",
        "this_month": "Ce mois-ci",
        "last_month": "Mois dernier",

        # Messages
        "no_data": "Aucune donnée disponible",
        "loading": "Chargement...",
        "success": "Succès",
        "error": "Erreur",
        "warning": "Attention",
        "info": "Information",

        # Configuration
        "upload_file": "Téléverser un fichier",
        "google_drive": "Google Drive",
        "manual_import": "Import manuel",
        "last_update": "Dernière mise à jour",
        "account": "Compte",
        "customer_id": "Customer ID",

        # Settings
        "settings": "Paramètres",
        "language": "Langue",
        "theme": "Thème",
        "dark_mode": "Mode sombre",
        "light_mode": "Mode clair",

        # Campaign details
        "campaign": "Campagne",
        "campaigns": "Campagnes",
        "budget": "Budget",
        "status": "Statut",
        "type": "Type",
        "bidding_strategy": "Stratégie d'enchères",

        # Keywords
        "keyword": "Mot-clé",
        "keywords": "Mots-clés",
        "match_type": "Type de correspondance",
        "exact": "Exacte",
        "phrase": "Expression",
        "broad": "Large",

        # Tabs
        "overview_tab": "Vue d'ensemble",
        "keywords_tab": "Mots-clés",
        "performance_tab": "Performances",
        "config_tab": "Configuration",

        # Diagnostic
        "issues_found": "Problèmes détectés",
        "recommendations": "Recommandations",
        "critical": "Critique",
        "important": "Important",
        "advice": "Conseil",

        # Footer
        "powered_by": "Propulsé par",
        "version": "Version",
    },

    "en": {
        # Navigation
        "home": "Home",
        "config": "Configuration",
        "overview": "Overview",
        "campaign_detail": "Campaign detail",
        "search_terms": "Search terms",
        "diagnostic": "Diagnostic",

        # Header
        "app_title": "Dashboard ADS",
        "welcome": "Welcome",
        "connected": "Connected",
        "not_connected": "Not connected",

        # Common actions
        "refresh": "Refresh",
        "export": "Export",
        "import": "Import",
        "search": "Search",
        "filter": "Filter",
        "download": "Download",
        "close": "Close",
        "save": "Save",
        "cancel": "Cancel",

        # Metrics
        "impressions": "Impressions",
        "clicks": "Clicks",
        "ctr": "CTR",
        "cost": "Cost",
        "conversions": "Conversions",
        "conversion_rate": "Conversion rate",
        "avg_cpc": "Avg. CPC",
        "cpa": "CPA",

        # Status
        "enabled": "Enabled",
        "paused": "Paused",
        "removed": "Removed",
        "all": "All",

        # Campaign types
        "search": "Search",
        "display": "Display",
        "shopping": "Shopping",
        "video": "Video",

        # Time periods
        "today": "Today",
        "yesterday": "Yesterday",
        "last_7_days": "Last 7 days",
        "last_30_days": "Last 30 days",
        "this_month": "This month",
        "last_month": "Last month",

        # Messages
        "no_data": "No data available",
        "loading": "Loading...",
        "success": "Success",
        "error": "Error",
        "warning": "Warning",
        "info": "Information",

        # Configuration
        "upload_file": "Upload file",
        "google_drive": "Google Drive",
        "manual_import": "Manual import",
        "last_update": "Last update",
        "account": "Account",
        "customer_id": "Customer ID",

        # Settings
        "settings": "Settings",
        "language": "Language",
        "theme": "Theme",
        "dark_mode": "Dark mode",
        "light_mode": "Light mode",

        # Campaign details
        "campaign": "Campaign",
        "campaigns": "Campaigns",
        "budget": "Budget",
        "status": "Status",
        "type": "Type",
        "bidding_strategy": "Bidding strategy",

        # Keywords
        "keyword": "Keyword",
        "keywords": "Keywords",
        "match_type": "Match type",
        "exact": "Exact",
        "phrase": "Phrase",
        "broad": "Broad",

        # Tabs
        "overview_tab": "Overview",
        "keywords_tab": "Keywords",
        "performance_tab": "Performance",
        "config_tab": "Configuration",

        # Diagnostic
        "issues_found": "Issues found",
        "recommendations": "Recommendations",
        "critical": "Critical",
        "important": "Important",
        "advice": "Advice",

        # Footer
        "powered_by": "Powered by",
        "version": "Version",
    },

    "de": {
        # Navigation
        "home": "Startseite",
        "config": "Konfiguration",
        "overview": "Übersicht",
        "campaign_detail": "Kampagnendetails",
        "search_terms": "Suchbegriffe",
        "diagnostic": "Diagnose",

        # Header
        "app_title": "Dashboard ADS",
        "welcome": "Willkommen",
        "connected": "Verbunden",
        "not_connected": "Nicht verbunden",

        # Common actions
        "refresh": "Aktualisieren",
        "export": "Exportieren",
        "import": "Importieren",
        "search": "Suchen",
        "filter": "Filtern",
        "download": "Herunterladen",
        "close": "Schließen",
        "save": "Speichern",
        "cancel": "Abbrechen",

        # Metrics
        "impressions": "Impressionen",
        "clicks": "Klicks",
        "ctr": "CTR",
        "cost": "Kosten",
        "conversions": "Conversions",
        "conversion_rate": "Conversion-Rate",
        "avg_cpc": "Durchschn. CPC",
        "cpa": "CPA",

        # Status
        "enabled": "Aktiv",
        "paused": "Pausiert",
        "removed": "Entfernt",
        "all": "Alle",

        # Campaign types
        "search": "Suche",
        "display": "Display",
        "shopping": "Shopping",
        "video": "Video",

        # Time periods
        "today": "Heute",
        "yesterday": "Gestern",
        "last_7_days": "Letzte 7 Tage",
        "last_30_days": "Letzte 30 Tage",
        "this_month": "Dieser Monat",
        "last_month": "Letzter Monat",

        # Messages
        "no_data": "Keine Daten verfügbar",
        "loading": "Lädt...",
        "success": "Erfolg",
        "error": "Fehler",
        "warning": "Warnung",
        "info": "Information",

        # Configuration
        "upload_file": "Datei hochladen",
        "google_drive": "Google Drive",
        "manual_import": "Manueller Import",
        "last_update": "Letzte Aktualisierung",
        "account": "Konto",
        "customer_id": "Kunden-ID",

        # Settings
        "settings": "Einstellungen",
        "language": "Sprache",
        "theme": "Thema",
        "dark_mode": "Dunkler Modus",
        "light_mode": "Heller Modus",

        # Campaign details
        "campaign": "Kampagne",
        "campaigns": "Kampagnen",
        "budget": "Budget",
        "status": "Status",
        "type": "Typ",
        "bidding_strategy": "Gebotsstrategie",

        # Keywords
        "keyword": "Keyword",
        "keywords": "Keywords",
        "match_type": "Match-Typ",
        "exact": "Exakt",
        "phrase": "Phrase",
        "broad": "Weitgehend",

        # Tabs
        "overview_tab": "Übersicht",
        "keywords_tab": "Keywords",
        "performance_tab": "Leistung",
        "config_tab": "Konfiguration",

        # Diagnostic
        "issues_found": "Probleme gefunden",
        "recommendations": "Empfehlungen",
        "critical": "Kritisch",
        "important": "Wichtig",
        "advice": "Ratschlag",

        # Footer
        "powered_by": "Unterstützt von",
        "version": "Version",
    }
}


def init_language():
    """Initialise la langue dans le session state depuis les préférences"""
    if "language" not in st.session_state:
        from utils.preferences import user_prefs
        st.session_state.language = user_prefs.get_language()


def get_language():
    """Retourne la langue courante"""
    if "language" not in st.session_state:
        init_language()
    return st.session_state.language


def set_language(lang_code: str):
    """Définit la langue courante et sauvegarde dans les préférences"""
    if lang_code in TRANSLATIONS:
        st.session_state.language = lang_code
        from utils.preferences import user_prefs
        user_prefs.set_language(lang_code)
    else:
        st.warning(f"Langue non supportée : {lang_code}")


def t(key: str) -> str:
    """
    Traduit une clé dans la langue courante

    Args:
        key: Clé de traduction

    Returns:
        Texte traduit ou clé si non trouvé
    """
    lang = get_language()

    if lang in TRANSLATIONS and key in TRANSLATIONS[lang]:
        return TRANSLATIONS[lang][key]

    # Fallback sur l'anglais
    if key in TRANSLATIONS["en"]:
        return TRANSLATIONS["en"][key]

    # Si pas trouvé, retourner la clé
    return key


def get_available_languages():
    """Retourne la liste des langues disponibles"""
    return {
        "fr": "🇫🇷 Français",
        "en": "🇬🇧 English",
        "de": "🇩🇪 Deutsch"
    }
