"""
AI Diagnostics Service
Analyse intelligente des campagnes via LLM (Claude)
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import anthropic
from datetime import datetime


class AIDiagnosticsService:
    """Service d'analyse IA des campagnes Google Ads"""

    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.client = None
        if self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)

        # Cache directory
        self.cache_dir = Path(__file__).parent.parent.parent / 'data' / 'cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / 'ai_diagnostic.json'

    def is_available(self) -> bool:
        """Vérifie si l'API Claude est configurée"""
        return self.client is not None

    def get_cached_analysis(self) -> Dict[str, Any]:
        """Récupère l'analyse en cache si disponible"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading cache: {e}")
                return None
        return None

    def save_analysis_to_cache(self, result: Dict[str, Any]):
        """Sauvegarde l'analyse dans le cache"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")

    def analyze_campaigns(
        self,
        campaigns: List[Dict[str, Any]],
        keywords: List[Dict[str, Any]],
        search_terms: List[Dict[str, Any]],
        ads: List[Dict[str, Any]],
        account_info: Dict[str, Any],
        language: str = "fr"
    ) -> Dict[str, Any]:
        """
        Analyse complète des campagnes via Claude

        Args:
            campaigns: Liste des campagnes
            keywords: Liste des mots-clés
            search_terms: Liste des termes de recherche
            ads: Liste des annonces
            account_info: Informations du compte

        Returns:
            Analyse IA avec recommandations
        """
        if not self.is_available():
            return {
                "error": "API Claude non configurée",
                "message": "Veuillez configurer ANTHROPIC_API_KEY dans les variables d'environnement"
            }

        # Préparer les données pour le prompt
        data_summary = self._prepare_data_summary(
            campaigns, keywords, search_terms, ads, account_info
        )

        # Construire le prompt
        prompt = self._build_analysis_prompt(data_summary, language)

        try:
            # Appeler Claude
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            analysis = message.content[0].text

            result = {
                "success": True,
                "analysis": analysis,
                "model": "claude-sonnet-4-20250514",
                "timestamp": datetime.now().isoformat(),
                "tokens_used": {
                    "input": message.usage.input_tokens,
                    "output": message.usage.output_tokens
                }
            }

            # Sauvegarder dans le cache
            self.save_analysis_to_cache(result)

            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Erreur lors de l'analyse IA"
            }

    def _prepare_data_summary(
        self,
        campaigns: List[Dict[str, Any]],
        keywords: List[Dict[str, Any]],
        search_terms: List[Dict[str, Any]],
        ads: List[Dict[str, Any]],
        account_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prépare un résumé structuré des données"""

        # Métriques globales
        total_impressions = sum(c.get('impressions', 0) for c in campaigns)
        total_clicks = sum(c.get('clicks', 0) for c in campaigns)
        total_cost = sum(c.get('cost', 0) for c in campaigns)
        total_conversions = sum(c.get('conversions', 0) for c in campaigns)

        avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        avg_cpc = (total_cost / total_clicks) if total_clicks > 0 else 0
        cost_per_conversion = (total_cost / total_conversions) if total_conversions > 0 else 0

        # Top/Worst performers
        campaigns_sorted_by_cost = sorted(campaigns, key=lambda x: x.get('cost', 0), reverse=True)
        top_campaigns = campaigns_sorted_by_cost[:3]

        keywords_sorted_by_cost = sorted(keywords, key=lambda x: x.get('cost', 0), reverse=True)
        top_keywords = keywords_sorted_by_cost[:10]

        # Mots-clés sans conversions mais avec du coût
        expensive_no_conv = [
            kw for kw in keywords
            if kw.get('cost', 0) > 10 and kw.get('conversions', 0) == 0
        ][:5]

        # CTR par mot-clé
        low_ctr_keywords = [
            kw for kw in keywords
            if kw.get('impressions', 0) > 100 and kw.get('ctr', 0) < 1.0
        ][:5]

        # Termes de recherche les plus fréquents
        top_search_terms = sorted(
            search_terms,
            key=lambda x: x.get('impressions', 0),
            reverse=True
        )[:10]

        # Termes avec conversions
        converting_search_terms = [
            st for st in search_terms
            if st.get('conversions', 0) > 0
        ][:5]

        return {
            "account": {
                "name": account_info.get('name', 'N/A'),
                "customer_id": account_info.get('customerId', 'N/A'),
                "currency": account_info.get('currency', 'EUR'),
                "timezone": account_info.get('timezone', 'Europe/Paris')
            },
            "global_metrics": {
                "campaigns_count": len(campaigns),
                "keywords_count": len(keywords),
                "ads_count": len(ads),
                "total_impressions": total_impressions,
                "total_clicks": total_clicks,
                "total_cost": round(total_cost, 2),
                "total_conversions": round(total_conversions, 2),
                "avg_ctr": round(avg_ctr, 2),
                "avg_cpc": round(avg_cpc, 2),
                "cost_per_conversion": round(cost_per_conversion, 2) if total_conversions > 0 else None
            },
            "campaigns": [
                {
                    "name": c.get('name'),
                    "status": c.get('status'),
                    "budget": c.get('budget'),
                    "impressions": c.get('impressions', 0),
                    "clicks": c.get('clicks', 0),
                    "ctr": round(c.get('ctr', 0), 2),
                    "cost": round(c.get('cost', 0), 2),
                    "conversions": c.get('conversions', 0),
                    "cpc": round(c.get('averageCpc', 0), 2)
                }
                for c in campaigns
            ],
            "top_campaigns": [
                {
                    "name": c.get('name'),
                    "cost": round(c.get('cost', 0), 2),
                    "conversions": c.get('conversions', 0),
                    "ctr": round(c.get('ctr', 0), 2)
                }
                for c in top_campaigns
            ],
            "top_keywords": [
                {
                    "text": kw.get('text', kw.get('keywordText', '')),
                    "match_type": kw.get('matchType'),
                    "impressions": kw.get('impressions', 0),
                    "clicks": kw.get('clicks', 0),
                    "ctr": round(kw.get('ctr', 0), 2),
                    "cost": round(kw.get('cost', 0), 2),
                    "conversions": kw.get('conversions', 0)
                }
                for kw in top_keywords
            ],
            "expensive_no_conversions": [
                {
                    "text": kw.get('text', kw.get('keywordText', '')),
                    "cost": round(kw.get('cost', 0), 2),
                    "clicks": kw.get('clicks', 0),
                    "conversions": kw.get('conversions', 0)
                }
                for kw in expensive_no_conv
            ],
            "low_ctr_keywords": [
                {
                    "text": kw.get('text', kw.get('keywordText', '')),
                    "impressions": kw.get('impressions', 0),
                    "ctr": round(kw.get('ctr', 0), 2)
                }
                for kw in low_ctr_keywords
            ],
            "top_search_terms": [
                {
                    "query": st.get('query'),
                    "impressions": st.get('impressions', 0),
                    "clicks": st.get('clicks', 0),
                    "conversions": st.get('conversions', 0)
                }
                for st in top_search_terms
            ],
            "converting_search_terms": [
                {
                    "query": st.get('query'),
                    "clicks": st.get('clicks', 0),
                    "conversions": st.get('conversions', 0),
                    "cost": round(st.get('cost', 0), 2)
                }
                for st in converting_search_terms
            ]
        }

    def _build_analysis_prompt(self, data: Dict[str, Any], language: str = "fr") -> str:
        """Construit le prompt pour Claude"""

        # Map language codes to full names
        language_map = {
            "fr": "français",
            "en": "English",
            "de": "Deutsch"
        }
        lang_name = language_map.get(language, "français")

        prompt = f"""Tu es un expert consultant Google Ads avec 10 ans d'expérience. Analyse les données de ce compte Google Ads et fournis des recommandations actionnables et personnalisées.

**IMPORTANT: Réponds UNIQUEMENT en {lang_name}. Toute ton analyse doit être dans cette langue.**

# INFORMATIONS DU COMPTE

**Compte:** {data['account']['name']} ({data['account']['customer_id']})
**Devise:** {data['account']['currency']}

# MÉTRIQUES GLOBALES (30 derniers jours)

- **Campagnes actives:** {data['global_metrics']['campaigns_count']}
- **Mots-clés:** {data['global_metrics']['keywords_count']}
- **Impressions:** {data['global_metrics']['total_impressions']:,}
- **Clics:** {data['global_metrics']['total_clicks']:,}
- **CTR moyen:** {data['global_metrics']['avg_ctr']}%
- **Coût total:** {data['global_metrics']['total_cost']}€
- **CPC moyen:** {data['global_metrics']['avg_cpc']}€
- **Conversions:** {data['global_metrics']['total_conversions']}
- **Coût par conversion:** {data['global_metrics']['cost_per_conversion']}€ (si disponible)

# CAMPAGNES

"""

        # Ajouter détails des campagnes
        for campaign in data['campaigns']:
            status_emoji = "✅" if campaign['status'] == 'ENABLED' else "⏸️"
            prompt += f"""
{status_emoji} **{campaign['name']}**
- Budget: {campaign['budget']}€ | Coût: {campaign['cost']}€
- Impressions: {campaign['impressions']:,} | Clics: {campaign['clicks']}
- CTR: {campaign['ctr']}% | CPC: {campaign['cpc']}€
- Conversions: {campaign['conversions']}
"""

        prompt += f"""

# TOP MOTS-CLÉS PAR COÛT

"""
        for kw in data['top_keywords']:
            prompt += f"- **{kw['text']}** ({kw['match_type']}): {kw['cost']}€ dépensés | {kw['conversions']} conv. | CTR: {kw['ctr']}%\n"

        if data['expensive_no_conversions']:
            prompt += f"""

# ⚠️ MOTS-CLÉS COÛTEUX SANS CONVERSION

"""
            for kw in data['expensive_no_conversions']:
                prompt += f"- **{kw['text']}**: {kw['cost']}€ dépensés | {kw['clicks']} clics | 0 conversion\n"

        if data['low_ctr_keywords']:
            prompt += f"""

# 📉 MOTS-CLÉS À FAIBLE CTR

"""
            for kw in data['low_ctr_keywords']:
                prompt += f"- **{kw['text']}**: {kw['impressions']} imp. | CTR: {kw['ctr']}%\n"

        if data['top_search_terms']:
            prompt += f"""

# 🔍 TERMES DE RECHERCHE LES PLUS FRÉQUENTS

"""
            for st in data['top_search_terms'][:5]:
                prompt += f"- \"{st['query']}\": {st['impressions']} imp. | {st['clicks']} clics | {st['conversions']} conv.\n"

        if data['converting_search_terms']:
            prompt += f"""

# ✨ TERMES DE RECHERCHE AVEC CONVERSIONS

"""
            for st in data['converting_search_terms']:
                prompt += f"- \"{st['query']}\": {st['conversions']} conv. | {st['cost']}€\n"

        prompt += f"""

# TA MISSION

Analyse ces données et fournis un rapport structuré en **{lang_name}** selon ce format EXACT:

## 📊 Résumé Exécutif
Vue d'ensemble des performances en 2-3 phrases avec les points forts et faibles.

## 🎯 Analyse Par Campagne

Pour CHAQUE campagne ayant des problèmes, utilise EXACTEMENT ce format:

### [Nom de la Campagne]

**Gravité:** [Critical / High / Medium / Low]

**Problème détecté:**
- Description claire du problème principal
- Données chiffrées à l'appui

**Impact:**
- Impact business chiffré (coût, conversions perdues, etc.)
- Conséquences si non traité

**Recommandation:**
- Action concrète et précise à entreprendre
- Étapes d'exécution
- Résultat attendu après correction

---

## 💡 Actions Globales Prioritaires

Liste 3-5 optimisations transversales (budget, enchères, stratégie) qui s'appliquent à l'ensemble du compte.

## 📈 Opportunités à Exploiter

Nouveaux mots-clés à ajouter, termes de recherche prometteurs, audiences à tester.

---

**RÈGLES IMPORTANTES:**
1. Utilise EXACTEMENT les headers markdown indiqués (##, ###, **Problème détecté:**, **Impact:**, **Recommandation:**)
2. Une section par campagne avec problème
3. Indique toujours la gravité: Critical 🔴, High 🟠, Medium 🟡, ou Low 🟢
4. Sois spécifique: cite les noms exacts de campagnes/mots-clés
5. Donne des chiffres concrets (budgets, économies, conversions attendues)
6. Priorise les quick wins (actions simples à fort impact)

Rédige ton analyse maintenant en suivant ce format strictement:"""

        return prompt


# Instance globale
ai_diagnostics_service = AIDiagnosticsService()
