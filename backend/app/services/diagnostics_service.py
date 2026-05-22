"""
Diagnostics Service
Moteur de diagnostic automatique (version simplifiée)
"""

from typing import List, Dict, Any, Optional

from app.models.diagnostic import DiagnosticIssue, Severity


class DiagnosticsService:
    """Service de diagnostic des campagnes"""

    def analyze_campaign(self, campaign: Dict[str, Any]) -> List[DiagnosticIssue]:
        """
        Analyse une campagne et retourne les problèmes détectés

        Args:
            campaign: Données de la campagne

        Returns:
            Liste des problèmes
        """
        issues = []

        campaign_id = str(campaign.get('id', ''))
        campaign_name = campaign.get('name', 'Unknown')

        # Règle 1: Campagne en pause depuis longtemps
        if campaign.get('status') == 'PAUSED':
            issues.append(DiagnosticIssue(
                title="Campagne en pause",
                message=f"La campagne '{campaign_name}' est actuellement en pause.",
                severity=Severity.MEDIUM,
                category="Configuration",
                campaign_id=campaign_id,
                campaign_name=campaign_name,
                action="Activer la campagne ou la supprimer si elle n'est plus utilisée"
            ))

        # Règle 2: Budget limité
        if campaign.get('budget_limited', False):
            issues.append(DiagnosticIssue(
                title="Budget limité",
                message=f"La campagne '{campaign_name}' est limitée par le budget.",
                severity=Severity.HIGH,
                category="Budget",
                campaign_id=campaign_id,
                campaign_name=campaign_name,
                details={"budget": campaign.get('budget')},
                action="Augmenter le budget quotidien pour ne pas limiter la diffusion"
            ))

        # Règle 3: Aucune conversion
        conversions = campaign.get('conversions', 0)
        impressions = campaign.get('impressions', 0)

        if impressions > 1000 and conversions == 0:
            issues.append(DiagnosticIssue(
                title="Aucune conversion",
                message=f"La campagne '{campaign_name}' a {impressions} impressions mais aucune conversion.",
                severity=Severity.CRITICAL,
                category="Performances",
                campaign_id=campaign_id,
                campaign_name=campaign_name,
                details={"impressions": impressions, "conversions": conversions},
                action="Vérifier le suivi des conversions et optimiser les mots-clés/annonces"
            ))

        # Règle 4: CTR très faible
        ctr = campaign.get('ctr', 0.0)
        clicks = campaign.get('clicks', 0)

        if impressions > 100 and ctr < 1.0:
            issues.append(DiagnosticIssue(
                title="CTR très faible",
                message=f"La campagne '{campaign_name}' a un CTR de {ctr:.2f}%, ce qui est très faible.",
                severity=Severity.HIGH,
                category="Performances",
                campaign_id=campaign_id,
                campaign_name=campaign_name,
                details={"ctr": ctr, "impressions": impressions, "clicks": clicks},
                action="Améliorer les annonces et cibler des mots-clés plus pertinents"
            ))

        # Règle 5: Coût par conversion élevé
        cost = campaign.get('cost', 0.0)
        if conversions > 0:
            cost_per_conversion = cost / conversions

            # CPA > 100€ considéré comme élevé (à ajuster selon le secteur)
            if cost_per_conversion > 100:
                issues.append(DiagnosticIssue(
                    title="Coût par conversion élevé",
                    message=f"Le CPA de '{campaign_name}' est de {cost_per_conversion:.2f}€, ce qui est élevé.",
                    severity=Severity.MEDIUM,
                    category="Performances",
                    campaign_id=campaign_id,
                    campaign_name=campaign_name,
                    details={"cost_per_conversion": cost_per_conversion, "cost": cost, "conversions": conversions},
                    action="Optimiser les enchères et cibler des mots-clés plus qualifiés"
                ))

        # Règle 6: Faible volume d'impressions
        if impressions < 100:
            issues.append(DiagnosticIssue(
                title="Volume d'impressions très faible",
                message=f"La campagne '{campaign_name}' génère très peu d'impressions ({impressions}).",
                severity=Severity.MEDIUM,
                category="Performances",
                campaign_id=campaign_id,
                campaign_name=campaign_name,
                details={"impressions": impressions},
                action="Augmenter le budget, élargir le ciblage ou ajouter des mots-clés"
            ))

        # Règle 7: Taux de conversion faible
        if clicks > 50 and conversions > 0:
            conversion_rate = (conversions / clicks) * 100

            if conversion_rate < 2.0:  # < 2% considéré comme faible
                issues.append(DiagnosticIssue(
                    title="Taux de conversion faible",
                    message=f"Le taux de conversion de '{campaign_name}' est de {conversion_rate:.2f}%.",
                    severity=Severity.MEDIUM,
                    category="Performances",
                    campaign_id=campaign_id,
                    campaign_name=campaign_name,
                    details={"conversion_rate": conversion_rate, "clicks": clicks, "conversions": conversions},
                    action="Améliorer la page de destination et la pertinence des annonces"
                ))

        return issues

    def analyze_all_campaigns(
        self,
        campaigns: List[Dict[str, Any]],
        severity_filter: Optional[List[Severity]] = None,
        category_filter: Optional[List[str]] = None
    ) -> List[DiagnosticIssue]:
        """
        Analyse toutes les campagnes

        Args:
            campaigns: Liste des campagnes
            severity_filter: Filtrer par sévérité
            category_filter: Filtrer par catégorie

        Returns:
            Liste de tous les problèmes détectés
        """
        all_issues = []

        for campaign in campaigns:
            issues = self.analyze_campaign(campaign)
            all_issues.extend(issues)

        # Appliquer les filtres
        if severity_filter:
            all_issues = [issue for issue in all_issues if issue.severity in severity_filter]

        if category_filter:
            all_issues = [issue for issue in all_issues if issue.category in category_filter]

        # Trier par sévérité (CRITICAL > HIGH > MEDIUM > LOW)
        severity_order = {
            Severity.CRITICAL: 0,
            Severity.HIGH: 1,
            Severity.MEDIUM: 2,
            Severity.LOW: 3
        }

        all_issues.sort(key=lambda x: severity_order[x.severity])

        return all_issues


# Instance globale
diagnostics_service = DiagnosticsService()
