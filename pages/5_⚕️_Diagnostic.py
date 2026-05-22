"""
Page Diagnostic - Mode Scripts (sans API)
Analyse automatique avec recommandations priorisées
"""

import streamlit as st
import pandas as pd
from datetime import datetime

from config.settings import STREAMLIT_CONFIG
from config.i18n import t, init_language
from modules.script_data_loader import script_loader
from utils.ui_helpers import load_custom_css, init_theme
from components.sidebar import render_custom_sidebar, hide_default_navigation
from components.topbar import render_topbar, TOPBAR_CSS


# ============================================================================
# CONFIGURATION
# ============================================================================

st.set_page_config(**STREAMLIT_CONFIG)
load_custom_css()
hide_default_navigation()
init_language()
init_theme()
st.markdown(TOPBAR_CSS, unsafe_allow_html=True)
render_topbar()


# ============================================================================
# RÈGLES DE DIAGNOSTIC
# ============================================================================

def analyze_campaigns(campaigns, account_info):
    """Analyse les campagnes et retourne les problèmes"""
    issues = []
    currency = account_info.get('currency', 'EUR') if account_info else 'EUR'

    for campaign in campaigns:
        campaign_name = campaign.get('name', 'Campagne sans nom')
        metrics = campaign.get('metrics', {})

        # Règle 1 : Display activé sur Search
        if campaign.get('targetDisplay') and campaign.get('type') == 'SEARCH':
            issues.append({
                'severity': 'critical',
                'category': 'Configuration',
                'campaign': campaign_name,
                'title': 'Réseau Display activé',
                'description': f"La campagne **{campaign_name}** cible le Réseau Display. Pour une campagne Search, cela dilue votre budget sur des placements moins qualifiés.",
                'recommendation': "Désactivez le Réseau Display dans les paramètres de la campagne pour concentrer votre budget sur les recherches actives.",
                'impact': 'Élevé - Budget gaspillé sur du trafic non pertinent'
            })

        # Règle 2 : Aucune conversion
        if metrics.get('conversions', 0) == 0 and metrics.get('cost', 0) > 50:
            issues.append({
                'severity': 'critical',
                'category': 'Performances',
                'campaign': campaign_name,
                'title': 'Aucune conversion',
                'description': f"La campagne **{campaign_name}** a dépensé {metrics.get('cost', 0):.2f} {currency} sans générer de conversion.",
                'recommendation': "1. Vérifiez que le suivi des conversions est bien configuré\n2. Testez la page de destination\n3. Ajoutez des mots-clés négatifs pour filtrer le trafic non qualifié",
                'impact': 'Critique - Budget sans retour sur investissement'
            })

        # Règle 3 : CPA très élevé
        cpa = metrics.get('costPerConversion', 0)
        if cpa > 100:
            issues.append({
                'severity': 'high',
                'category': 'Performances',
                'campaign': campaign_name,
                'title': f'CPA élevé ({cpa:.2f} {currency})',
                'description': f"Le coût par acquisition de **{campaign_name}** est de {cpa:.2f} {currency}, ce qui peut être élevé selon votre business model.",
                'recommendation': "1. Analysez les termes de recherche et ajoutez des négatifs\n2. Optimisez la page de destination\n3. Testez des enchères plus basses\n4. Passez les mots-clés en correspondance exacte",
                'impact': 'Élevé - Rentabilité compromise'
            })

        # Règle 4 : Taux de conversion faible
        conv_rate = metrics.get('conversionRate', 0)
        if conv_rate < 1 and metrics.get('clicks', 0) > 50:
            issues.append({
                'severity': 'medium',
                'category': 'Performances',
                'campaign': campaign_name,
                'title': f'Taux de conversion faible ({conv_rate:.2f}%)',
                'description': f"La campagne **{campaign_name}** a un taux de conversion de {conv_rate:.2f}%, ce qui est faible.",
                'recommendation': "1. Optimisez la landing page (vitesse, clarté, call-to-action)\n2. Vérifiez l'adéquation entre annonce et page\n3. Testez différentes pages de destination\n4. Ajoutez des éléments de réassurance (témoignages, garanties)",
                'impact': 'Moyen - Potentiel de conversion inexploité'
            })

        # Règle 5 : Budget trop bas pour la stratégie
        if campaign.get('biddingStrategy') == 'MAXIMIZE_CONVERSIONS' and campaign.get('budget', 0) < 20:
            issues.append({
                'severity': 'medium',
                'category': 'Configuration',
                'campaign': campaign_name,
                'title': 'Budget insuffisant pour la stratégie d\'enchères',
                'description': f"La stratégie 'Maximiser les conversions' nécessite un budget plus conséquent. Votre budget actuel est de {campaign.get('budget', 0):.2f} {currency}/jour.",
                'recommendation': "1. Augmentez le budget à au moins 30€/jour\n2. Ou passez en enchères manuelles (CPC manuel) pour mieux contrôler les coûts",
                'impact': 'Moyen - Stratégie sous-optimale'
            })

    return issues


def analyze_keywords(keywords):
    """Analyse les mots-clés et retourne les problèmes"""
    issues = []

    if not keywords:
        return issues

    df_keywords = pd.DataFrame(keywords)

    # Extraire les métriques
    if 'metrics' in df_keywords.columns:
        metrics_df = pd.json_normalize(df_keywords['metrics'])
        df_keywords = pd.concat([df_keywords.drop('metrics', axis=1), metrics_df], axis=1)

    # Règle 1 : Mots-clés avec termes suspects
    suspect_words = ['gratuit', 'free', 'emploi', 'job', 'formation', 'training', 'stage', 'cours', 'pdf']

    for idx, kw in df_keywords.iterrows():
        text_lower = kw.get('text', '').lower()

        if any(word in text_lower for word in suspect_words):
            issues.append({
                'severity': 'medium',
                'category': 'Mots-clés',
                'campaign': kw.get('campaignName', 'N/A'),
                'title': f'Mot-clé suspect : "{kw.get("text")}"',
                'description': f"Le mot-clé **{kw.get('text')}** contient des termes qui attirent généralement du trafic non qualifié.",
                'recommendation': f"Envisagez de le supprimer ou de le passer en mot-clé négatif si les performances ne sont pas satisfaisantes.",
                'impact': 'Moyen - Risque de trafic non pertinent'
            })

    # Règle 2 : Mots-clés en requête large sans conversion
    broad_no_conv = df_keywords[
        (df_keywords.get('matchType') == 'BROAD') &
        (df_keywords.get('clicks', 0) >= 10) &
        (df_keywords.get('conversions', 0) == 0)
    ]

    for idx, kw in broad_no_conv.head(5).iterrows():
        issues.append({
            'severity': 'high',
            'category': 'Mots-clés',
            'campaign': kw.get('campaignName', 'N/A'),
            'title': f'Requête large sans conversion : "{kw.get("text")}"',
            'description': f"Le mot-clé **{kw.get('text')}** en requête large a généré {kw.get('clicks', 0)} clics mais aucune conversion.",
            'recommendation': f"1. Passez-le en correspondance exacte ou expression\n2. Ou supprimez-le s'il ne génère que du trafic non qualifié",
            'impact': 'Élevé - Budget gaspillé'
        })

    # Règle 3 : Mots-clés avec impressions mais aucun clic
    no_clicks = df_keywords[
        (df_keywords.get('impressions', 0) > 100) &
        (df_keywords.get('clicks', 0) == 0)
    ]

    for idx, kw in no_clicks.head(3).iterrows():
        issues.append({
            'severity': 'low',
            'category': 'Mots-clés',
            'campaign': kw.get('campaignName', 'N/A'),
            'title': f'Aucun clic : "{kw.get("text")}"',
            'description': f"Le mot-clé **{kw.get('text')}** a {kw.get('impressions', 0)} impressions mais aucun clic.",
            'recommendation': f"Vérifiez que l'annonce est pertinente pour ce mot-clé, ou supprimez-le.",
            'impact': 'Faible - Opportunité manquée'
        })

    return issues


def analyze_search_terms(search_terms):
    """Analyse les termes de recherche et retourne les problèmes"""
    issues = []

    if not search_terms:
        return issues

    df_terms = pd.DataFrame(search_terms)

    # Règle 1 : Termes suspects avec clics
    suspect_words = ['gratuit', 'free', 'emploi', 'job', 'formation', 'training', 'stage', 'cours', 'pdf', 'télécharger', 'download']

    suspect_terms = df_terms[
        df_terms['query'].str.lower().str.contains('|'.join(suspect_words), na=False) &
        (df_terms['clicks'] > 0)
    ]

    for idx, term in suspect_terms.head(10).iterrows():
        issues.append({
            'severity': 'high',
            'category': 'Termes de recherche',
            'campaign': term.get('campaignName', 'N/A'),
            'title': f'Terme hors-cible : "{term.get("query")}"',
            'description': f"Le terme **{term.get('query')}** a généré {term.get('clicks', 0)} clics pour {term.get('cost', 0):.2f}€.",
            'recommendation': f"Ajoutez les mots suspects en mots-clés négatifs au niveau de la campagne.",
            'impact': 'Élevé - Budget gaspillé sur trafic non qualifié'
        })

    # Règle 2 : Termes avec beaucoup de clics mais pas de conversion
    no_conv_terms = df_terms[
        (df_terms['clicks'] >= 5) &
        (df_terms['conversions'] == 0)
    ].sort_values('clicks', ascending=False)

    for idx, term in no_conv_terms.head(5).iterrows():
        if not any(word in term.get('query', '').lower() for word in suspect_words):  # Éviter les doublons
            issues.append({
                'severity': 'medium',
                'category': 'Termes de recherche',
                'campaign': term.get('campaignName', 'N/A'),
                'title': f'Pas de conversion : "{term.get("query")}"',
                'description': f"Le terme **{term.get('query')}** a {term.get('clicks', 0)} clics mais aucune conversion.",
                'recommendation': f"Analysez si ce terme est pertinent pour votre business. Si non, ajoutez-le en négatif.",
                'impact': 'Moyen - ROI négatif'
            })

    return issues


# ============================================================================
# PAGE PRINCIPALE
# ============================================================================

def main():
    """Page principale"""

    # Vérifier les données
    if not script_loader.data_exists():
        st.error("❌ Aucune donnée disponible")
        if st.button("⚙️ Aller à la configuration"):
            st.switch_page("pages/0_⚙️_Configuration_Simple.py")
        st.stop()

    st.title("Diagnostic")
    st.markdown("Recommandations priorisées sur la configuration, les mots-clés et les termes de recherche.")

    # Infos compte
    account_info = script_loader.get_account_info()
    last_update = script_loader.get_last_update()

    if last_update:
        update_time = datetime.fromisoformat(last_update.replace('Z', '+00:00'))
        st.info(f"📅 Analyse basée sur les données du {update_time.strftime('%d/%m/%Y à %H:%M')}")

    # Lancer l'analyse
    with st.spinner("🔍 Analyse en cours..."):
        campaigns = script_loader.get_campaigns()
        keywords = script_loader.get_keywords()
        search_terms = script_loader.get_search_terms()

        # Collecter tous les problèmes
        all_issues = []
        all_issues.extend(analyze_campaigns(campaigns, account_info))
        all_issues.extend(analyze_keywords(keywords))
        all_issues.extend(analyze_search_terms(search_terms))

    # Statistiques
    col1, col2, col3, col4 = st.columns(4)

    critical_count = len([i for i in all_issues if i['severity'] == 'critical'])
    high_count = len([i for i in all_issues if i['severity'] == 'high'])
    medium_count = len([i for i in all_issues if i['severity'] == 'medium'])
    low_count = len([i for i in all_issues if i['severity'] == 'low'])

    with col1:
        st.metric("🔴 Critique", critical_count)
    with col2:
        st.metric("🟠 Élevé", high_count)
    with col3:
        st.metric("🟡 Moyen", medium_count)
    with col4:
        st.metric("🟢 Faible", low_count)

    st.markdown("---")

    # Résumé
    if not all_issues:
        st.success("🎉 **Félicitations !** Aucun problème majeur détecté.")
        st.info("Continuez à surveiller vos performances régulièrement.")
        return

    st.subheader(f"📋 {len(all_issues)} problème(s) détecté(s)")

    # Filtres
    col1, col2 = st.columns(2)

    with col1:
        severity_filter = st.multiselect(
            "Sévérité",
            options=['critical', 'high', 'medium', 'low'],
            default=['critical', 'high', 'medium', 'low'],
            format_func=lambda x: {
                'critical': '🔴 Critique',
                'high': '🟠 Élevé',
                'medium': '🟡 Moyen',
                'low': '🟢 Faible'
            }[x]
        )

    with col2:
        categories = list(set([i['category'] for i in all_issues]))
        category_filter = st.multiselect(
            "Catégorie",
            options=categories,
            default=categories
        )

    # Filtrer
    filtered_issues = [
        i for i in all_issues
        if i['severity'] in severity_filter and i['category'] in category_filter
    ]

    # Trier par sévérité
    severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    filtered_issues.sort(key=lambda x: severity_order[x['severity']])

    st.markdown("---")

    # Afficher les problèmes
    for idx, issue in enumerate(filtered_issues, 1):
        severity_icon = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢'
        }[issue['severity']]

        severity_label = {
            'critical': 'CRITIQUE',
            'high': 'ÉLEVÉ',
            'medium': 'MOYEN',
            'low': 'FAIBLE'
        }[issue['severity']]

        with st.expander(
            f"{severity_icon} **#{idx} - {issue['title']}** ({severity_label})",
            expanded=(issue['severity'] in ['critical', 'high'] and idx <= 3)
        ):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"**📂 Catégorie** : {issue['category']}")
                if issue.get('campaign'):
                    st.markdown(f"**🎯 Campagne** : {issue['campaign']}")

                st.markdown("---")

                st.markdown("**📝 Description**")
                st.markdown(issue['description'])

                st.markdown("---")

                st.markdown("**💡 Recommandation**")
                st.markdown(issue['recommendation'])

            with col2:
                st.markdown("**🎯 Impact**")
                st.info(issue['impact'])

                st.markdown("**✅ Statut**")
                st.checkbox("Problème résolu", key=f"resolved_{idx}")

    # Résumé des actions
    st.markdown("---")
    st.subheader("🎯 Plan d'action recommandé")

    action_plan = []

    if critical_count > 0:
        action_plan.append("🔴 **Priorité 1 (Urgent)** : Résoudre les problèmes critiques (aucune conversion, Display activé)")

    if high_count > 0:
        action_plan.append("🟠 **Priorité 2 (Important)** : Optimiser les mots-clés et termes hors-cible")

    if medium_count > 0:
        action_plan.append("🟡 **Priorité 3 (Amélioration)** : Améliorer le taux de conversion et la configuration")

    for i, action in enumerate(action_plan, 1):
        st.markdown(f"{i}. {action}")

    # Export
    st.markdown("---")
    if st.button("📥 Exporter le rapport (CSV)", use_container_width=True):
        df_export = pd.DataFrame(filtered_issues)
        csv = df_export.to_csv(index=False)
        st.download_button(
            "Télécharger CSV",
            csv,
            "diagnostic_google_ads.csv",
            "text/csv"
        )


# ============================================================================
# EXÉCUTION
# ============================================================================

if __name__ == "__main__":
    render_custom_sidebar("diagnostic")
    main()
