"""
Moteur de diagnostic automatique pour détecter les problèmes de configuration
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    """Niveaux de sévérité des diagnostics"""
    CRITIQUE = "CRITIQUE"
    IMPORTANT = "IMPORTANT"
    CONSEIL = "CONSEIL"
    INFO = "INFO"


@dataclass
class DiagnosticResult:
    """Résultat d'un diagnostic"""
    title: str
    message: str
    severity: Severity
    category: str  # Configuration, Performances, Mots-clés, Annonces, etc.
    details: Dict[str, Any] = None
    action: str = None  # Action recommandée


class CampaignDiagnostics:
    """Analyse diagnostique d'une campagne"""

    def __init__(self, campaign_data: Dict[str, Any]):
        """
        Initialise le moteur de diagnostic

        Args:
            campaign_data: Données complètes de la campagne (config + métriques)
        """
        self.campaign_data = campaign_data
        self.results: List[DiagnosticResult] = []

    def run_all_diagnostics(self) -> List[DiagnosticResult]:
        """
        Exécute tous les diagnostics et retourne les résultats

        Returns:
            Liste des problèmes détectés, triés par sévérité
        """
        self.results = []

        # Diagnostics de configuration
        self._check_display_enabled_on_search()
        self._check_partner_network_enabled()
        self._check_budget_limited()
        self._check_campaign_dates()

        # Diagnostics de performances
        self._check_no_conversions()
        self._check_low_conversion_rate()
        self._check_high_cost_per_conversion()
        self._check_low_ctr()
        self._check_low_impressions()

        # Diagnostics de mots-clés
        self._check_rarely_served_keywords()
        self._check_broad_match_without_conversions()
        self._check_negative_keywords_needed()
        self._check_low_quality_score()

        # Diagnostics d'annonces
        self._check_ad_strength()
        self._check_single_ad()
        self._check_missing_headlines()

        # Diagnostics généraux
        self._check_optimization_score()

        # Trier par sévérité (Critique > Important > Conseil > Info)
        severity_order = {
            Severity.CRITIQUE: 0,
            Severity.IMPORTANT: 1,
            Severity.CONSEIL: 2,
            Severity.INFO: 3,
        }

        self.results.sort(key=lambda x: severity_order[x.severity])

        return self.results

    # ========================================================================
    # DIAGNOSTICS DE CONFIGURATION
    # ========================================================================

    def _check_display_enabled_on_search(self):
        """Vérifie si le réseau Display est activé sur une campagne Search"""
        campaign_type = self.campaign_data.get("advertising_channel_type")
        display_enabled = self.campaign_data.get("target_content_network", False)

        if campaign_type == "SEARCH" and display_enabled:
            self.results.append(DiagnosticResult(
                title="Réseau Display activé sur campagne Search",
                message=(
                    "Le Réseau Display est activé alors que cette campagne est de type Recherche. "
                    "Cela peut générer du trafic non qualifié et augmenter les coûts. "
                    "Les campagnes Search devraient cibler uniquement le Réseau de Recherche."
                ),
                severity=Severity.CRITIQUE,
                category="Configuration",
                details={"display_enabled": display_enabled},
                action="Désactivez le Réseau Display dans les paramètres de campagne"
            ))

    def _check_partner_network_enabled(self):
        """Vérifie si les partenaires de recherche sont activés"""
        partners_enabled = self.campaign_data.get("target_partner_search_network", False)

        if partners_enabled:
            # Note: Ce n'est pas forcément un problème, mais un avertissement
            self.results.append(DiagnosticResult(
                title="Partenaires de recherche activés",
                message=(
                    "Les partenaires de recherche Google sont activés. "
                    "Ces sites peuvent générer du trafic de moindre qualité. "
                    "Vérifiez les performances séparément dans les rapports."
                ),
                severity=Severity.CONSEIL,
                category="Configuration",
                details={"partners_enabled": partners_enabled},
                action="Analysez les performances sur les partenaires de recherche"
            ))

    def _check_budget_limited(self):
        """Vérifie si la campagne est limitée par le budget"""
        # Cette info viendrait normalement des recommandations Google
        # ou d'un champ spécifique dans les données
        pass

    def _check_campaign_dates(self):
        """Vérifie les dates de début/fin de campagne"""
        start_date = self.campaign_data.get("start_date")
        end_date = self.campaign_data.get("end_date")

        if end_date:
            # La campagne a une date de fin définie
            self.results.append(DiagnosticResult(
                title="Date de fin définie",
                message=(
                    f"Cette campagne est programmée pour se terminer le {end_date}. "
                    "Assurez-vous que c'est intentionnel."
                ),
                severity=Severity.INFO,
                category="Configuration",
                details={"end_date": end_date},
                action="Vérifiez la date de fin ou supprimez-la si la campagne doit continuer"
            ))

    # ========================================================================
    # DIAGNOSTICS DE PERFORMANCES
    # ========================================================================

    def _check_no_conversions(self):
        """Vérifie si la campagne a généré des conversions"""
        conversions = self.campaign_data.get("metrics", {}).get("conversions", 0)

        if conversions == 0:
            self.results.append(DiagnosticResult(
                title="Aucune conversion détectée",
                message=(
                    "Cette campagne n'a généré aucune conversion sur la période analysée. "
                    "Vérifiez le suivi des conversions, la pertinence des mots-clés, "
                    "ou l'expérience sur la page de destination."
                ),
                severity=Severity.CRITIQUE,
                category="Performances",
                details={"conversions": 0},
                action="Vérifiez le suivi des conversions dans Google Ads → Outils → Conversions"
            ))

    def _check_low_conversion_rate(self):
        """Vérifie si le taux de conversion est anormalement bas"""
        conversion_rate = self.campaign_data.get("metrics", {}).get("conversion_rate", 0)

        if conversion_rate > 0 and conversion_rate < 0.01:  # < 1%
            self.results.append(DiagnosticResult(
                title="Taux de conversion faible",
                message=(
                    f"Le taux de conversion est de {conversion_rate*100:.2f}%, ce qui est inférieur à 1%. "
                    "Cela peut indiquer un problème avec la page de destination, "
                    "un mauvais ciblage, ou des mots-clés non pertinents."
                ),
                severity=Severity.IMPORTANT,
                category="Performances",
                details={"conversion_rate": conversion_rate},
                action="Optimisez la page de destination et affinez le ciblage"
            ))

    def _check_high_cost_per_conversion(self):
        """Vérifie si le coût par conversion est élevé"""
        cost_per_conversion = self.campaign_data.get("metrics", {}).get("cost_per_conversion", 0)
        conversions = self.campaign_data.get("metrics", {}).get("conversions", 0)

        # Seuil dépend du secteur, ici on utilise 100€ comme exemple
        if conversions > 0 and cost_per_conversion > 100_000_000:  # > 100€ (en micros)
            self.results.append(DiagnosticResult(
                title="Coût par conversion élevé",
                message=(
                    f"Le coût par conversion est élevé ({cost_per_conversion/1_000_000:.2f}€). "
                    "Vérifiez la rentabilité de cette campagne."
                ),
                severity=Severity.IMPORTANT,
                category="Performances",
                details={"cost_per_conversion_euros": cost_per_conversion / 1_000_000},
                action="Revoyez les enchères et la stratégie de ciblage"
            ))

    def _check_low_ctr(self):
        """Vérifie si le CTR est anormalement bas"""
        ctr = self.campaign_data.get("metrics", {}).get("ctr", 0)
        impressions = self.campaign_data.get("metrics", {}).get("impressions", 0)

        if impressions > 1000 and ctr < 0.01:  # < 1%
            self.results.append(DiagnosticResult(
                title="Taux de clics faible",
                message=(
                    f"Le CTR est de {ctr*100:.2f}%, ce qui est faible. "
                    "Les annonces ne sont pas assez attrayantes ou pertinentes."
                ),
                severity=Severity.IMPORTANT,
                category="Performances",
                details={"ctr": ctr, "impressions": impressions},
                action="Améliorez les titres et descriptions des annonces"
            ))

    def _check_low_impressions(self):
        """Vérifie si le volume d'impressions est très faible"""
        impressions = self.campaign_data.get("metrics", {}).get("impressions", 0)

        if impressions < 100:  # < 100 impressions sur 30 jours
            self.results.append(DiagnosticResult(
                title="Volume d'impressions très faible",
                message=(
                    f"Seulement {impressions} impressions sur la période. "
                    "Les mots-clés sont peut-être trop spécifiques, les enchères trop basses, "
                    "ou le budget insuffisant."
                ),
                severity=Severity.CONSEIL,
                category="Performances",
                details={"impressions": impressions},
                action="Élargissez les mots-clés ou augmentez les enchères"
            ))

    # ========================================================================
    # DIAGNOSTICS DE MOTS-CLÉS
    # ========================================================================

    def _check_rarely_served_keywords(self):
        """Vérifie s'il y a des mots-clés rarement diffusés"""
        keywords = self.campaign_data.get("keywords", [])
        rarely_served = [
            kw for kw in keywords
            if kw.get("system_serving_status") == "RARELY_SERVED"
        ]

        if rarely_served:
            self.results.append(DiagnosticResult(
                title=f"{len(rarely_served)} mot(s)-clé(s) rarement diffusé(s)",
                message=(
                    f"{len(rarely_served)} mot(s)-clé(s) ont le statut 'Rarement diffusé'. "
                    "Cela signifie que le volume de recherche est trop faible. "
                    "Envisagez des variantes plus larges ou supprimez-les."
                ),
                severity=Severity.CONSEIL,
                category="Mots-clés",
                details={"rarely_served_count": len(rarely_served)},
                action="Examinez les mots-clés rarement diffusés et optimisez-les"
            ))

    def _check_broad_match_without_conversions(self):
        """Vérifie les mots-clés en requête large sans conversion"""
        keywords = self.campaign_data.get("keywords", [])
        broad_no_conv = [
            kw for kw in keywords
            if kw.get("match_type") == "BROAD" and kw.get("conversions", 0) == 0
        ]

        if broad_no_conv:
            self.results.append(DiagnosticResult(
                title=f"{len(broad_no_conv)} mot(s)-clé(s) en large sans conversion",
                message=(
                    f"{len(broad_no_conv)} mot(s)-clé(s) en requête large n'ont généré aucune conversion. "
                    "La requête large peut attirer du trafic non qualifié. "
                    "Passez en expression ou exacte, ou ajoutez des mots-clés négatifs."
                ),
                severity=Severity.IMPORTANT,
                category="Mots-clés",
                details={"broad_no_conv_count": len(broad_no_conv)},
                action="Restreignez le type de correspondance ou ajoutez des négatifs"
            ))

    def _check_negative_keywords_needed(self):
        """Détecte les termes de recherche qui devraient être exclus"""
        search_terms = self.campaign_data.get("search_terms", [])

        # Mots déclencheurs courants à exclure
        negative_triggers = ["gratuit", "emploi", "formation", "stage", "cours", "pdf", "tuto", "tutoriel"]

        terms_to_exclude = [
            term for term in search_terms
            if any(trigger in term.get("search_term", "").lower() for trigger in negative_triggers)
        ]

        if terms_to_exclude:
            self.results.append(DiagnosticResult(
                title=f"{len(terms_to_exclude)} terme(s) de recherche à exclure détecté(s)",
                message=(
                    f"{len(terms_to_exclude)} terme(s) de recherche contiennent des mots hors-cible "
                    f"(gratuit, emploi, formation, etc.). "
                    "Ajoutez-les comme mots-clés négatifs pour économiser du budget."
                ),
                severity=Severity.IMPORTANT,
                category="Mots-clés",
                details={"terms_to_exclude_count": len(terms_to_exclude)},
                action="Ajoutez ces termes en mots-clés négatifs"
            ))

    def _check_low_quality_score(self):
        """Vérifie s'il y a des mots-clés avec un score de qualité faible"""
        keywords = self.campaign_data.get("keywords", [])
        low_quality = [
            kw for kw in keywords
            if kw.get("quality_score", 10) <= 5
        ]

        if low_quality:
            self.results.append(DiagnosticResult(
                title=f"{len(low_quality)} mot(s)-clé(s) avec score de qualité ≤ 5",
                message=(
                    f"{len(low_quality)} mot(s)-clé(s) ont un score de qualité de 5 ou moins. "
                    "Cela augmente vos coûts et réduit la visibilité. "
                    "Améliorez la pertinence des annonces et pages de destination."
                ),
                severity=Severity.IMPORTANT,
                category="Mots-clés",
                details={"low_quality_count": len(low_quality)},
                action="Optimisez la pertinence annonces/mots-clés/landing page"
            ))

    # ========================================================================
    # DIAGNOSTICS D'ANNONCES
    # ========================================================================

    def _check_ad_strength(self):
        """Vérifie la force des annonces (ad strength)"""
        ads = self.campaign_data.get("ads", [])

        poor_ads = [ad for ad in ads if ad.get("ad_strength") in ["POOR", "AVERAGE"]]

        if poor_ads:
            self.results.append(DiagnosticResult(
                title=f"{len(poor_ads)} annonce(s) avec force insuffisante",
                message=(
                    f"{len(poor_ads)} annonce(s) ont une force 'Mauvaise' ou 'Moyenne'. "
                    "Ajoutez plus de titres, descriptions et variantes pour atteindre 'Bonne' ou 'Excellente'."
                ),
                severity=Severity.IMPORTANT,
                category="Annonces",
                details={"poor_ads_count": len(poor_ads)},
                action="Ajoutez des titres et descriptions pour améliorer la force des annonces"
            ))

    def _check_single_ad(self):
        """Vérifie s'il n'y a qu'une seule annonce par groupe"""
        ad_groups = self.campaign_data.get("ad_groups", {})

        single_ad_groups = [
            ag for ag_id, ag in ad_groups.items()
            if len(ag.get("ads", [])) < 2
        ]

        if single_ad_groups:
            self.results.append(DiagnosticResult(
                title=f"{len(single_ad_groups)} groupe(s) avec une seule annonce",
                message=(
                    f"{len(single_ad_groups)} groupe(s) d'annonces n'ont qu'une seule annonce active. "
                    "Il est recommandé d'avoir au moins 2-3 variantes pour permettre les tests A/B."
                ),
                severity=Severity.CONSEIL,
                category="Annonces",
                details={"single_ad_groups_count": len(single_ad_groups)},
                action="Créez 2-3 variantes d'annonces par groupe"
            ))

    def _check_missing_headlines(self):
        """Vérifie si des annonces n'ont pas assez de titres"""
        ads = self.campaign_data.get("ads", [])

        few_headlines = [
            ad for ad in ads
            if len(ad.get("headlines", [])) < 10
        ]

        if few_headlines:
            self.results.append(DiagnosticResult(
                title=f"{len(few_headlines)} annonce(s) avec moins de 10 titres",
                message=(
                    f"{len(few_headlines)} annonce(s) n'ont pas 10 titres. "
                    "Plus vous fournissez de variantes, mieux Google peut optimiser la diffusion."
                ),
                severity=Severity.CONSEIL,
                category="Annonces",
                details={"few_headlines_count": len(few_headlines)},
                action="Ajoutez des titres pour atteindre 10-15 variantes"
            ))

    # ========================================================================
    # DIAGNOSTICS GÉNÉRAUX
    # ========================================================================

    def _check_optimization_score(self):
        """Vérifie le score d'optimisation de la campagne"""
        optimization_score = self.campaign_data.get("optimization_score", 1.0)

        if optimization_score < 0.7:  # < 70%
            self.results.append(DiagnosticResult(
                title=f"Score d'optimisation faible ({optimization_score*100:.0f}%)",
                message=(
                    f"Le score d'optimisation est de {optimization_score*100:.0f}%. "
                    "Google détecte des opportunités d'amélioration. "
                    "Consultez les recommandations dans l'interface Google Ads."
                ),
                severity=Severity.CONSEIL,
                category="Optimisation",
                details={"optimization_score": optimization_score},
                action="Appliquez les recommandations Google Ads"
            ))


def run_diagnostics(campaign_data: Dict[str, Any]) -> List[DiagnosticResult]:
    """
    Lance l'analyse diagnostique complète d'une campagne

    Args:
        campaign_data: Données de la campagne (config + métriques + mots-clés + annonces)

    Returns:
        Liste des diagnostics triés par sévérité
    """
    diagnostics = CampaignDiagnostics(campaign_data)
    return diagnostics.run_all_diagnostics()
