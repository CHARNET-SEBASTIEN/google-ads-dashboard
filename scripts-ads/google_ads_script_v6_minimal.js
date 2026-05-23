/**
 * Google Ads Script V6 - Champs minimaux compatibles
 * Utilise uniquement les champs universellement disponibles
 */

function main() {
  Logger.log('🚀 Début export V6 - champs minimaux');

  var data = {
    timestamp: new Date().toISOString(),
    account: getAccountInfo(),
    campaigns: exportCampaigns(),
    adGroups: exportAdGroups(),
    keywords: exportKeywords(),
    ads: exportAdsV6Minimal(),
    searchTerms: exportSearchTermsV6(),
    performance: exportPerformance(),
    performanceByDevice: exportPerformanceByDevice(),
    performanceByLocation: exportPerformanceByLocationV6()
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
 * Export annonces V6 - Approche progressive
 * Teste d'abord les champs disponibles
 */
function exportAdsV6Minimal() {
  var ads = [];

  try {
    Logger.log('🔍 Test 1: Champs basiques seulement...');

    // Essai 1 : Champs vraiment minimaux
    try {
      var report = AdsApp.report(
        'SELECT ' +
        'AdGroupId, AdGroupName, ' +
        'CampaignId, CampaignName, ' +
        'Id, Status, AdType, ' +
        'Headline, ' +
        'Description, ' +
        'DisplayUrl, ' +
        'Impressions, Clicks ' +
        'FROM AD_PERFORMANCE_REPORT ' +
        'WHERE Status IN [ENABLED, PAUSED] ' +
        'DURING LAST_30_DAYS'
      );

      var rows = report.rows();
      var count = 0;

      while (rows.hasNext()) {
        var row = rows.next();

        ads.push({
          id: row['Id'],
          campaignId: row['CampaignId'],
          campaignName: row['CampaignName'],
          adGroupId: row['AdGroupId'],
          adGroupName: row['AdGroupName'],
          type: row['AdType'] || 'UNKNOWN',
          status: row['Status'] || 'UNKNOWN',
          headline1: row['Headline'] || null,
          headline2: null,
          headline3: null,
          description: row['Description'] || null,
          description2: null,
          finalUrl: row['DisplayUrl'] || null,
          impressions: parseInt(row['Impressions']) || 0,
          clicks: parseInt(row['Clicks']) || 0,
          ctr: 0,
          cost: 0,
          conversions: 0
        });

        count++;
      }

      Logger.log('✅ Méthode 1 OK - ' + count + ' annonces');
      return ads;

    } catch (e) {
      Logger.log('❌ Méthode 1 échouée: ' + e.message);
    }

    // Essai 2 : HeadlinePart1, HeadlinePart2 (sans Part3)
    Logger.log('🔍 Test 2: HeadlinePart1 et HeadlinePart2...');
    try {
      var report2 = AdsApp.report(
        'SELECT ' +
        'AdGroupId, CampaignId, Id, Status, ' +
        'HeadlinePart1, HeadlinePart2, ' +
        'Description, Description2, ' +
        'Impressions, Clicks ' +
        'FROM AD_PERFORMANCE_REPORT ' +
        'WHERE Status IN [ENABLED, PAUSED] ' +
        'DURING LAST_30_DAYS'
      );

      var rows2 = report2.rows();
      var count2 = 0;

      while (rows2.hasNext()) {
        var row2 = rows2.next();

        ads.push({
          id: row2['Id'],
          campaignId: row2['CampaignId'],
          campaignName: '',
          adGroupId: row2['AdGroupId'],
          adGroupName: '',
          type: 'TEXT_AD',
          status: row2['Status'] || 'UNKNOWN',
          headline1: row2['HeadlinePart1'] || null,
          headline2: row2['HeadlinePart2'] || null,
          headline3: null,
          description: row2['Description'] || null,
          description2: row2['Description2'] || null,
          finalUrl: null,
          impressions: parseInt(row2['Impressions']) || 0,
          clicks: parseInt(row2['Clicks']) || 0,
          ctr: 0,
          cost: 0,
          conversions: 0
        });

        count2++;
      }

      Logger.log('✅ Méthode 2 OK - ' + count2 + ' annonces');
      return ads;

    } catch (e2) {
      Logger.log('❌ Méthode 2 échouée: ' + e2.message);
    }

    // Essai 3 : Fallback iterator
    Logger.log('⚠️ Fallback iterator (sans contenu)...');
    return exportAdsFallback();

  } catch (e) {
    Logger.log('❌ Erreur globale: ' + e);
    return exportAdsFallback();
  }
}

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

    Logger.log('✅ Fallback : ' + ads.length + ' annonces (sans contenu)');

  } catch (e) {
    Logger.log('❌ Erreur fallback : ' + e);
  }

  return ads;
}

function exportSearchTermsV6() {
  var searchTerms = [];

  try {
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
        matchType: '',
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

function exportPerformanceByLocationV6() {
  var locationPerf = [];

  try {
    // Revenir à GEO_PERFORMANCE_REPORT (avec warning mais fonctionne)
    var report = AdsApp.report(
      'SELECT CampaignId, CampaignName, CountryCriteriaId, ' +
      'Impressions, Clicks, Cost, Conversions ' +
      'FROM GEO_PERFORMANCE_REPORT ' +
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
