/**
 * Google Ads Script - Version SIMPLIFIÉE (sans erreurs)
 * À utiliser si la version complète pose problème
 */

function main() {
  Logger.log('🚀 Début de l\'export (version simplifiée)');

  var data = {
    timestamp: new Date().toISOString(),
    account: {
      customerId: AdsApp.currentAccount().getCustomerId(),
      name: AdsApp.currentAccount().getName(),
      currency: AdsApp.currentAccount().getCurrencyCode(),
      timezone: AdsApp.currentAccount().getTimeZone()
    },
    campaigns: exportCampaigns(),
    keywords: exportKeywords(),
    ads: [], // Annonces simplifiées
    searchTerms: exportSearchTerms(),
    performance: exportPerformance()
  };

  Logger.log('✅ Export terminé - ' + data.campaigns.length + ' campagnes');

  // Sauvegarder dans Google Drive uniquement
  saveToGoogleDrive(data);
}

/**
 * Exporte les campagnes (version simplifiée)
 */
function exportCampaigns() {
  var campaigns = [];
  var campaignIterator = AdsApp.campaigns()
    .withCondition('Status != REMOVED')
    .get();

  while (campaignIterator.hasNext()) {
    var campaign = campaignIterator.next();
    var stats = campaign.getStatsFor('LAST_30_DAYS');

    var budget = 0;
    try {
      if (campaign.getBudget()) {
        budget = campaign.getBudget().getAmount();
      }
    } catch (e) {}

    var impressions = stats.getImpressions();
    var clicks = stats.getClicks();
    var cost = stats.getCost();
    var conversions = stats.getConversions();

    campaigns.push({
      id: campaign.getId(),
      name: campaign.getName(),
      status: campaign.isEnabled() ? 'ENABLED' : campaign.isPaused() ? 'PAUSED' : 'REMOVED',
      type: 'SEARCH',
      budget: budget,
      biddingStrategy: campaign.getBiddingStrategyType(),
      targetSearch: true,
      targetDisplay: false,
      targetPartners: false,
      startDate: null,
      endDate: null,
      metrics: {
        impressions: impressions,
        clicks: clicks,
        ctr: stats.getCtr(),
        cost: cost,
        conversions: conversions,
        conversionRate: clicks > 0 ? (conversions / clicks) * 100 : 0,
        averageCpc: stats.getAverageCpc(),
        costPerConversion: conversions > 0 ? cost / conversions : 0
      }
    });
  }

  return campaigns;
}

/**
 * Exporte les mots-clés (version simplifiée)
 */
function exportKeywords() {
  var keywords = [];
  var keywordIterator = AdsApp.keywords()
    .withCondition('Status != REMOVED')
    .withLimit(500)
    .get();

  while (keywordIterator.hasNext()) {
    var keyword = keywordIterator.next();
    var stats = keyword.getStatsFor('LAST_30_DAYS');
    var campaign = keyword.getCampaign();
    var adGroup = keyword.getAdGroup();

    keywords.push({
      campaignId: campaign.getId(),
      campaignName: campaign.getName(),
      adGroupId: adGroup.getId(),
      adGroupName: adGroup.getName(),
      text: keyword.getText(),
      matchType: keyword.getMatchType(),
      status: keyword.isEnabled() ? 'ENABLED' : 'PAUSED',
      maxCpc: 0,
      qualityScore: 0,
      metrics: {
        impressions: stats.getImpressions(),
        clicks: stats.getClicks(),
        ctr: stats.getCtr(),
        cost: stats.getCost(),
        conversions: stats.getConversions(),
        averageCpc: stats.getAverageCpc()
      }
    });
  }

  return keywords;
}

/**
 * Exporte les termes de recherche
 */
function exportSearchTerms() {
  var searchTerms = [];

  try {
    var report = AdsApp.report(
      'SELECT CampaignId, CampaignName, Query, Clicks, Impressions, Ctr, Conversions, Cost ' +
      'FROM SEARCH_QUERY_PERFORMANCE_REPORT ' +
      'WHERE Impressions > 0 ' +
      'DURING LAST_30_DAYS'
    );

    var rows = report.rows();
    var count = 0;
    while (rows.hasNext() && count < 500) {
      var row = rows.next();
      searchTerms.push({
        campaignId: row['CampaignId'],
        campaignName: row['CampaignName'],
        query: row['Query'],
        clicks: parseInt(row['Clicks']) || 0,
        impressions: parseInt(row['Impressions']) || 0,
        ctr: parseFloat(row['Ctr']) || 0,
        conversions: parseFloat(row['Conversions']) || 0,
        cost: parseFloat(row['Cost']) || 0
      });
      count++;
    }
  } catch (e) {
    Logger.log('⚠️ Erreur export termes de recherche: ' + e);
  }

  return searchTerms;
}

/**
 * Exporte les performances quotidiennes
 */
function exportPerformance() {
  var performance = [];

  try {
    var report = AdsApp.report(
      'SELECT Date, CampaignId, CampaignName, Impressions, Clicks, Cost, Conversions, Ctr, AverageCpc ' +
      'FROM CAMPAIGN_PERFORMANCE_REPORT ' +
      'WHERE CampaignStatus != REMOVED ' +
      'DURING LAST_30_DAYS'
    );

    var rows = report.rows();
    while (rows.hasNext()) {
      var row = rows.next();
      performance.push({
        date: row['Date'],
        campaignId: row['CampaignId'],
        campaignName: row['CampaignName'],
        impressions: parseInt(row['Impressions']) || 0,
        clicks: parseInt(row['Clicks']) || 0,
        cost: parseFloat(row['Cost']) || 0,
        conversions: parseFloat(row['Conversions']) || 0,
        ctr: parseFloat(row['Ctr']) || 0,
        averageCpc: parseFloat(row['AverageCpc']) || 0
      });
    }
  } catch (e) {
    Logger.log('⚠️ Erreur export performance: ' + e);
  }

  return performance;
}

/**
 * Sauvegarde dans Google Drive
 */
function saveToGoogleDrive(data) {
  try {
    var fileName = 'latest_data.json';
    var folder = DriveApp.getRootFolder();

    // Trouver ou créer le dossier
    var folders = DriveApp.getFoldersByName('Google Ads Dashboard');
    if (folders.hasNext()) {
      folder = folders.next();
    } else {
      folder = DriveApp.createFolder('Google Ads Dashboard');
    }

    // Créer ou mettre à jour le fichier
    var files = folder.getFilesByName(fileName);
    if (files.hasNext()) {
      var file = files.next();
      file.setContent(JSON.stringify(data, null, 2));
      Logger.log('✅ Fichier mis à jour: ' + file.getUrl());
    } else {
      var file = folder.createFile(fileName, JSON.stringify(data, null, 2));
      Logger.log('✅ Fichier créé: ' + file.getUrl());
    }

    Logger.log('📁 Dossier: ' + folder.getUrl());

  } catch (e) {
    Logger.log('❌ Erreur Google Drive: ' + e);
  }
}
