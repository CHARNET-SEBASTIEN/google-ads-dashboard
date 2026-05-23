/**
 * Google Ads Script V5 - Utilise l'API de reporting pour les annonces
 * Contourne les limitations de l'API iterator
 */

function main() {
  Logger.log('🚀 Début export V5 - via reporting API');

  var data = {
    timestamp: new Date().toISOString(),
    account: getAccountInfo(),
    campaigns: exportCampaigns(),
    adGroups: exportAdGroups(),
    keywords: exportKeywords(),
    ads: exportAdsV5Report(),  // NOUVELLE MÉTHODE via report
    searchTerms: exportSearchTermsV5(),  // Corrigé
    performance: exportPerformance(),
    performanceByDevice: exportPerformanceByDevice(),
    performanceByLocation: exportPerformanceByLocationV5()  // Corrigé
  };

  Logger.log('✅ Export terminé - ' + data.campaigns.length + ' campagnes');
  Logger.log('   - ' + data.ads.length + ' annonces');
  Logger.log('   - ' + data.keywords.length + ' mots-clés');

  saveToGoogleDrive(data);
}

function getAccountInfo() {
  return {
    customerId: AdsApp.currentAccount().getCustomerId(),
    name: AdsApp.currentAccount().getName(),
    currency: AdsApp.currentAccount().getCurrencyCode(),
    timezone: AdsApp.currentAccount().getTimeZone()
  };
}

function exportCampaigns() {
  var campaigns = [];
  var iterator = AdsApp.campaigns().withCondition('Status != REMOVED').get();

  while (iterator.hasNext()) {
    var campaign = iterator.next();
    var stats30 = campaign.getStatsFor('LAST_30_DAYS');
    var stats7 = campaign.getStatsFor('LAST_7_DAYS');
    var statsToday = campaign.getStatsFor('TODAY');

    var budget = 0;
    try {
      if (campaign.getBudget()) {
        budget = campaign.getBudget().getAmount();
      }
    } catch (e) {}

    var impressions30 = stats30.getImpressions();
    var clicks30 = stats30.getClicks();
    var cost30 = stats30.getCost();
    var conversions30 = stats30.getConversions();

    campaigns.push({
      id: campaign.getId(),
      name: campaign.getName(),
      status: campaign.isEnabled() ? 'ENABLED' : campaign.isPaused() ? 'PAUSED' : 'REMOVED',
      type: 'SEARCH',
      budget: budget,
      biddingStrategy: campaign.getBiddingStrategyType(),
      impressions: impressions30,
      clicks: clicks30,
      ctr: stats30.getCtr(),
      cost: cost30,
      conversions: conversions30,
      averageCpc: stats30.getAverageCpc(),
      metrics: {
        impressions: impressions30,
        clicks: clicks30,
        ctr: stats30.getCtr(),
        cost: cost30,
        conversions: conversions30,
        conversionRate: clicks30 > 0 ? (conversions30 / clicks30) * 100 : 0,
        averageCpc: stats30.getAverageCpc(),
        costPerConversion: conversions30 > 0 ? cost30 / conversions30 : 0
      },
      metrics7Days: {
        impressions: stats7.getImpressions(),
        clicks: stats7.getClicks(),
        cost: stats7.getCost(),
        conversions: stats7.getConversions()
      },
      metricsToday: {
        impressions: statsToday.getImpressions(),
        clicks: statsToday.getClicks(),
        cost: statsToday.getCost(),
        conversions: statsToday.getConversions()
      }
    });
  }

  return campaigns;
}

function exportAdGroups() {
  var adGroups = [];
  var iterator = AdsApp.adGroups().withCondition('Status != REMOVED').get();

  while (iterator.hasNext()) {
    var adGroup = iterator.next();
    var stats = adGroup.getStatsFor('LAST_30_DAYS');
    var campaign = adGroup.getCampaign();

    adGroups.push({
      id: adGroup.getId(),
      name: adGroup.getName(),
      campaignId: campaign.getId(),
      campaignName: campaign.getName(),
      status: adGroup.isEnabled() ? 'ENABLED' : 'PAUSED',
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

  return adGroups;
}

function exportKeywords() {
  var keywords = [];
  var iterator = AdsApp.keywords().withCondition('Status != REMOVED').get();
  var count = 0;

  while (iterator.hasNext()) {
    var keyword = iterator.next();
    var keywordText = keyword.getText();

    if (!keywordText || keywordText.trim() === '') {
      continue;
    }

    var stats = keyword.getStatsFor('LAST_30_DAYS');
    var campaign = keyword.getCampaign();
    var adGroup = keyword.getAdGroup();

    keywords.push({
      id: keyword.getId(),
      campaignId: campaign.getId(),
      campaignName: campaign.getName(),
      adGroupId: adGroup.getId(),
      adGroupName: adGroup.getName(),
      text: keywordText,
      matchType: keyword.getMatchType(),
      status: keyword.isEnabled() ? 'ENABLED' : 'PAUSED',
      impressions: stats.getImpressions(),
      clicks: stats.getClicks(),
      ctr: stats.getCtr(),
      cost: stats.getCost(),
      metrics: {
        impressions: stats.getImpressions(),
        clicks: stats.getClicks(),
        ctr: stats.getCtr(),
        cost: stats.getCost(),
        conversions: stats.getConversions(),
        averageCpc: stats.getAverageCpc()
      }
    });

    count++;
    if (count % 100 == 0) {
      Logger.log('   Mots-clés : ' + count);
    }
  }

  return keywords;
}

/**
 * Export annonces V5 - Via AD_PERFORMANCE_REPORT
 * Permet d'accéder aux champs que l'iterator ne fournit pas
 */
function exportAdsV5Report() {
  var ads = [];
  var count = 0;

  try {
    Logger.log('🔍 Export annonces via report API...');

    // Utiliser le rapport AD_PERFORMANCE_REPORT qui contient le contenu des annonces
    var report = AdsApp.report(
      'SELECT ' +
      'AdGroupId, AdGroupName, ' +
      'CampaignId, CampaignName, ' +
      'Id, ' +
      'Status, ' +
      'AdType, ' +
      'HeadlinePart1, HeadlinePart2, HeadlinePart3, ' +
      'Description, Description2, ' +
      'DisplayUrl, ' +
      'Impressions, Clicks, Ctr, Cost, Conversions ' +
      'FROM AD_PERFORMANCE_REPORT ' +
      'WHERE Status IN [ENABLED, PAUSED] ' +
      'DURING LAST_30_DAYS'
    );

    var rows = report.rows();

    while (rows.hasNext()) {
      var row = rows.next();

      var adData = {
        id: row['Id'],
        campaignId: row['CampaignId'],
        campaignName: row['CampaignName'],
        adGroupId: row['AdGroupId'],
        adGroupName: row['AdGroupName'],
        type: row['AdType'] || 'UNKNOWN',
        status: row['Status'] || 'UNKNOWN',

        // Contenu
        headline1: row['HeadlinePart1'] || null,
        headline2: row['HeadlinePart2'] || null,
        headline3: row['HeadlinePart3'] || null,
        description: row['Description'] || null,
        description2: row['Description2'] || null,
        finalUrl: row['DisplayUrl'] || null,

        // Métriques
        impressions: parseInt(row['Impressions']) || 0,
        clicks: parseInt(row['Clicks']) || 0,
        ctr: parseFloat(row['Ctr']) || 0,
        cost: parseFloat(row['Cost']) || 0,
        conversions: parseFloat(row['Conversions']) || 0
      };

      ads.push(adData);
      count++;

      if (count % 10 == 0) {
        Logger.log('   Annonces : ' + count);
      }
    }

    Logger.log('✅ Total annonces : ' + count);

  } catch (e) {
    Logger.log('❌ Erreur export annonces : ' + e);
    Logger.log('   Message : ' + e.message);

    // Si le report ne fonctionne pas, fallback sur l'iterator sans contenu
    Logger.log('⚠️ Fallback sur iterator (sans contenu)...');
    return exportAdsFallback();
  }

  return ads;
}

/**
 * Fallback : export basique sans contenu si report échoue
 */
function exportAdsFallback() {
  var ads = [];

  try {
    var adsIterator = AdsApp.ads()
      .withCondition('Status IN [ENABLED, PAUSED]')
      .get();

    while (adsIterator.hasNext()) {
      var ad = adsIterator.next();
      var stats = ad.getStatsFor('LAST_30_DAYS');
      var adGroup = ad.getAdGroup();
      var campaign = adGroup.getCampaign();

      var adType = 'UNKNOWN';
      try {
        adType = ad.getType();
      } catch (e) {}

      var finalUrl = null;
      try {
        var urls = ad.urls();
        if (urls) {
          finalUrl = urls.getFinalUrl();
        }
      } catch (e) {}

      ads.push({
        id: ad.getId(),
        campaignId: campaign.getId(),
        campaignName: campaign.getName(),
        adGroupId: adGroup.getId(),
        adGroupName: adGroup.getName(),
        type: adType,
        status: ad.isEnabled() ? 'ENABLED' : ad.isPaused() ? 'PAUSED' : 'REMOVED',
        headline1: null,
        headline2: null,
        headline3: null,
        description: null,
        description2: null,
        finalUrl: finalUrl,
        impressions: stats.getImpressions(),
        clicks: stats.getClicks(),
        ctr: stats.getCtr(),
        cost: stats.getCost(),
        conversions: stats.getConversions()
      });
    }
  } catch (e) {
    Logger.log('❌ Erreur fallback : ' + e);
  }

  return ads;
}

/**
 * Export termes de recherche V5 - Corrigé pour nouvelle API
 */
function exportSearchTermsV5() {
  var searchTerms = [];

  try {
    // Champs corrects pour la nouvelle API
    var report = AdsApp.report(
      'SELECT CampaignId, CampaignName, AdGroupId, AdGroupName, ' +
      'Query, KeywordTextMatchingQuery, ' +
      'Clicks, Impressions, Ctr, Conversions, Cost, AverageCpc ' +
      'FROM SEARCH_QUERY_PERFORMANCE_REPORT ' +
      'WHERE Impressions > 0 ' +
      'DURING LAST_30_DAYS'
    );

    var rows = report.rows();
    var count = 0;

    while (rows.hasNext()) {
      var row = rows.next();

      searchTerms.push({
        campaignId: row['CampaignId'],
        campaignName: row['CampaignName'],
        adGroupId: row['AdGroupId'],
        adGroupName: row['AdGroupName'],
        query: row['Query'],
        keyword: row['KeywordTextMatchingQuery'] || '',
        matchType: '',  // Non disponible dans cette version
        clicks: parseInt(row['Clicks']) || 0,
        impressions: parseInt(row['Impressions']) || 0,
        ctr: parseFloat(row['Ctr']) || 0,
        conversions: parseFloat(row['Conversions']) || 0,
        cost: parseFloat(row['Cost']) || 0,
        averageCpc: parseFloat(row['AverageCpc']) || 0
      });

      count++;
      if (count % 100 == 0) {
        Logger.log('   Termes de recherche : ' + count);
      }
    }
  } catch (e) {
    Logger.log('⚠️ Erreur export termes de recherche: ' + e);
  }

  return searchTerms;
}

function exportPerformance() {
  var performance = [];

  try {
    var report = AdsApp.report(
      'SELECT Date, CampaignId, CampaignName, ' +
      'Impressions, Clicks, Cost, Conversions, Ctr, AverageCpc ' +
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

function exportPerformanceByDevice() {
  var devicePerf = [];

  try {
    var report = AdsApp.report(
      'SELECT CampaignId, CampaignName, Device, ' +
      'Impressions, Clicks, Cost, Conversions, Ctr, AverageCpc ' +
      'FROM CAMPAIGN_PERFORMANCE_REPORT ' +
      'WHERE CampaignStatus != REMOVED ' +
      'DURING LAST_30_DAYS'
    );

    var rows = report.rows();
    while (rows.hasNext()) {
      var row = rows.next();
      devicePerf.push({
        campaignId: row['CampaignId'],
        campaignName: row['CampaignName'],
        device: row['Device'],
        impressions: parseInt(row['Impressions']) || 0,
        clicks: parseInt(row['Clicks']) || 0,
        cost: parseFloat(row['Cost']) || 0,
        conversions: parseFloat(row['Conversions']) || 0,
        ctr: parseFloat(row['Ctr']) || 0,
        averageCpc: parseFloat(row['AverageCpc']) || 0
      });
    }
  } catch (e) {
    Logger.log('⚠️ Erreur export par appareil: ' + e);
  }

  return devicePerf;
}

/**
 * Export performance par localisation V5
 * Utilise USER_LOCATION_PERFORMANCE_REPORT au lieu de GEO_PERFORMANCE_REPORT
 */
function exportPerformanceByLocationV5() {
  var locationPerf = [];

  try {
    // Nouvelle API : USER_LOCATION_PERFORMANCE_REPORT
    var report = AdsApp.report(
      'SELECT CampaignId, CampaignName, CountryCriteriaId, ' +
      'Impressions, Clicks, Cost, Conversions ' +
      'FROM USER_LOCATION_PERFORMANCE_REPORT ' +
      'WHERE Impressions > 0 ' +
      'DURING LAST_30_DAYS'
    );

    var rows = report.rows();
    var count = 0;

    while (rows.hasNext() && count < 100) {
      var row = rows.next();
      locationPerf.push({
        campaignId: row['CampaignId'],
        campaignName: row['CampaignName'],
        countryCode: row['CountryCriteriaId'],
        impressions: parseInt(row['Impressions']) || 0,
        clicks: parseInt(row['Clicks']) || 0,
        cost: parseFloat(row['Cost']) || 0,
        conversions: parseFloat(row['Conversions']) || 0
      });
      count++;
    }
  } catch (e) {
    Logger.log('⚠️ Erreur export par localisation: ' + e);
  }

  return locationPerf;
}

function saveToGoogleDrive(data) {
  try {
    var fileName = 'latest_data.json';
    var folder = DriveApp.getRootFolder();

    var folders = DriveApp.getFoldersByName('Google Ads Dashboard');
    if (folders.hasNext()) {
      folder = folders.next();
    } else {
      folder = DriveApp.createFolder('Google Ads Dashboard');
    }

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
    var sizeKB = file.getSize() / 1024;
    Logger.log('📦 Taille: ' + sizeKB.toFixed(2) + ' KB');

  } catch (e) {
    Logger.log('❌ Erreur Google Drive: ' + e);
  }
}
