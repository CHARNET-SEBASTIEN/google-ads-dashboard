"""
Requêtes GAQL prédéfinies pour l'API Google Ads
"""

# ============================================================================
# CAMPAGNES
# ============================================================================

QUERY_CAMPAIGNS_OVERVIEW = """
SELECT
  campaign.id,
  campaign.name,
  campaign.status,
  campaign.advertising_channel_type,
  campaign.bidding_strategy_type,
  campaign_budget.amount_micros,
  campaign_budget.delivery_method,
  campaign.network_settings.target_search_network,
  campaign.network_settings.target_content_network,
  campaign.network_settings.target_partner_search_network,
  campaign.optimization_score,
  campaign.start_date,
  campaign.end_date
FROM campaign
WHERE campaign.status != 'REMOVED'
ORDER BY campaign.name
"""

QUERY_CAMPAIGN_DETAIL = """
SELECT
  campaign.id,
  campaign.name,
  campaign.status,
  campaign.advertising_channel_type,
  campaign.bidding_strategy_type,
  campaign_budget.amount_micros,
  campaign_budget.delivery_method,
  campaign.network_settings.target_search_network,
  campaign.network_settings.target_content_network,
  campaign.network_settings.target_partner_search_network,
  campaign.geo_target_type_setting.positive_geo_target_type,
  campaign.target_restriction_status,
  campaign.ad_serving_optimization_status,
  campaign.url_custom_parameters,
  campaign.tracking_url_template,
  campaign.final_url_suffix,
  campaign.optimization_score,
  campaign.start_date,
  campaign.end_date
FROM campaign
WHERE campaign.id = {campaign_id}
"""

QUERY_CAMPAIGN_PERFORMANCE = """
SELECT
  segments.date,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion
FROM campaign
WHERE campaign.id = {campaign_id}
  AND segments.date DURING {date_range}
ORDER BY segments.date ASC
"""

# ============================================================================
# MOTS-CLÉS
# ============================================================================

QUERY_KEYWORDS = """
SELECT
  campaign.id,
  campaign.name,
  ad_group.id,
  ad_group.name,
  ad_group_criterion.criterion_id,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  ad_group_criterion.status,
  ad_group_criterion.system_serving_status,
  ad_group_criterion.cpc_bid_micros,
  ad_group_criterion.quality_info.quality_score,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversion_rate
FROM keyword_view
WHERE campaign.id = {campaign_id}
  AND ad_group_criterion.status != 'REMOVED'
  AND segments.date DURING {date_range}
ORDER BY metrics.impressions DESC
"""

QUERY_ALL_KEYWORDS = """
SELECT
  campaign.id,
  campaign.name,
  ad_group.id,
  ad_group.name,
  ad_group_criterion.criterion_id,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  ad_group_criterion.status,
  ad_group_criterion.system_serving_status,
  ad_group_criterion.cpc_bid_micros,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions
FROM keyword_view
WHERE campaign.status = 'ENABLED'
  AND ad_group_criterion.status != 'REMOVED'
  AND segments.date DURING {date_range}
ORDER BY campaign.name, ad_group.name
"""

# ============================================================================
# ANNONCES
# ============================================================================

QUERY_ADS = """
SELECT
  campaign.id,
  ad_group.id,
  ad_group.name,
  ad_group_ad.ad.id,
  ad_group_ad.ad.final_urls,
  ad_group_ad.ad.responsive_search_ad.headlines,
  ad_group_ad.ad.responsive_search_ad.descriptions,
  ad_group_ad.ad.responsive_search_ad.path1,
  ad_group_ad.ad.responsive_search_ad.path2,
  ad_group_ad.ad_strength,
  ad_group_ad.status,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.conversions,
  metrics.conversion_rate
FROM ad_group_ad
WHERE campaign.id = {campaign_id}
  AND ad_group_ad.status != 'REMOVED'
  AND ad_group_ad.ad.type = 'RESPONSIVE_SEARCH_AD'
  AND segments.date DURING {date_range}
ORDER BY ad_group.name, metrics.impressions DESC
"""

# ============================================================================
# TERMES DE RECHERCHE
# ============================================================================

QUERY_SEARCH_TERMS = """
SELECT
  campaign.id,
  campaign.name,
  ad_group.id,
  ad_group.name,
  segments.search_term_view.search_term,
  segments.search_term_view.status,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversion_rate
FROM search_term_view
WHERE campaign.id = {campaign_id}
  AND segments.date DURING {date_range}
ORDER BY metrics.clicks DESC
LIMIT 1000
"""

QUERY_ALL_SEARCH_TERMS = """
SELECT
  campaign.id,
  campaign.name,
  segments.search_term_view.search_term,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.conversions
FROM search_term_view
WHERE campaign.status = 'ENABLED'
  AND segments.date DURING {date_range}
ORDER BY metrics.clicks DESC
LIMIT 5000
"""

# ============================================================================
# CIBLAGE GÉOGRAPHIQUE
# ============================================================================

QUERY_GEO_TARGETS = """
SELECT
  campaign.id,
  campaign_criterion.criterion_id,
  campaign_criterion.location.geo_target_constant,
  campaign_criterion.negative
FROM campaign_criterion
WHERE campaign.id = {campaign_id}
  AND campaign_criterion.type = 'LOCATION'
"""

# ============================================================================
# BUDGETS
# ============================================================================

QUERY_BUDGETS = """
SELECT
  campaign_budget.id,
  campaign_budget.name,
  campaign_budget.amount_micros,
  campaign_budget.period,
  campaign_budget.delivery_method,
  campaign_budget.explicitly_shared,
  campaign_budget.total_amount_micros
FROM campaign_budget
"""

# ============================================================================
# EXTENSIONS D'ANNONCE
# ============================================================================

QUERY_AD_EXTENSIONS = """
SELECT
  campaign.id,
  campaign_extension_setting.extension_type,
  extension_feed_item.sitelink_feed_item.link_text,
  extension_feed_item.sitelink_feed_item.line1,
  extension_feed_item.sitelink_feed_item.line2,
  extension_feed_item.callout_feed_item.callout_text,
  extension_feed_item.structured_snippet_feed_item.header,
  extension_feed_item.structured_snippet_feed_item.values,
  extension_feed_item.status
FROM campaign_extension_setting
WHERE campaign.id = {campaign_id}
"""

# ============================================================================
# CONVERSIONS
# ============================================================================

QUERY_CONVERSIONS = """
SELECT
  campaign.id,
  segments.conversion_action_name,
  segments.conversion_action,
  metrics.conversions,
  metrics.conversions_value,
  metrics.cost_per_conversion,
  metrics.conversion_rate
FROM campaign
WHERE campaign.id = {campaign_id}
  AND segments.date DURING {date_range}
ORDER BY metrics.conversions DESC
"""

# ============================================================================
# RECOMMANDATIONS
# ============================================================================

QUERY_RECOMMENDATIONS = """
SELECT
  recommendation.resource_name,
  recommendation.type,
  recommendation.impact.base_metrics.clicks,
  recommendation.impact.base_metrics.conversions,
  recommendation.impact.base_metrics.cost_micros,
  recommendation.dismissed
FROM recommendation
WHERE recommendation.dismissed = FALSE
LIMIT 100
"""

# ============================================================================
# GROUPES D'ANNONCES
# ============================================================================

QUERY_AD_GROUPS = """
SELECT
  campaign.id,
  ad_group.id,
  ad_group.name,
  ad_group.status,
  ad_group.type,
  ad_group.cpc_bid_micros,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.cost_micros,
  metrics.conversions
FROM ad_group
WHERE campaign.id = {campaign_id}
  AND ad_group.status != 'REMOVED'
  AND segments.date DURING {date_range}
ORDER BY ad_group.name
"""

# ============================================================================
# AUDIENCES
# ============================================================================

QUERY_AUDIENCES = """
SELECT
  campaign.id,
  campaign_criterion.user_list.user_list,
  campaign_criterion.status,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.conversions
FROM campaign_audience_view
WHERE campaign.id = {campaign_id}
  AND segments.date DURING {date_range}
"""


# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def format_query(query: str, **kwargs) -> str:
    """
    Formate une requête GAQL avec des paramètres

    Args:
        query: Requête GAQL avec placeholders
        **kwargs: Paramètres à injecter (campaign_id, date_range, etc.)

    Returns:
        Requête formatée

    Example:
        >>> format_query(QUERY_CAMPAIGN_DETAIL, campaign_id="123456")
    """
    return query.format(**kwargs)


def get_date_range_predicate(date_range: str) -> str:
    """
    Convertit un nom de plage en prédicat GAQL

    Args:
        date_range: Nom de la plage (ex: "LAST_30_DAYS")

    Returns:
        Prédicat GAQL (ex: "LAST_30_DAYS" ou "20240101, 20240131")
    """
    # Liste des plages prédéfinies Google Ads
    predefined_ranges = [
        "TODAY",
        "YESTERDAY",
        "LAST_7_DAYS",
        "LAST_BUSINESS_WEEK",
        "THIS_WEEK_SUN_TODAY",
        "THIS_WEEK_MON_TODAY",
        "LAST_WEEK_SUN_SAT",
        "LAST_14_DAYS",
        "LAST_30_DAYS",
        "THIS_MONTH",
        "LAST_MONTH",
        "LAST_90_DAYS",
        "ALL_TIME",
    ]

    if date_range in predefined_ranges:
        return date_range

    # Si c'est une plage personnalisée (format: "YYYYMMDD, YYYYMMDD")
    return date_range
