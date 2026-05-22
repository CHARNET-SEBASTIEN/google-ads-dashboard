/**
 * Google Ads Script - Version COMPLÈTE V2 - CORRIGÉE
 * Export enrichi avec annonces responsives complètes
 */

function main() {
  Logger.log('🚀 Début de l\'export COMPLET V2 des données Google Ads');

  var data = {
    timestamp: new Date().toISOString(),
    account: getAccountInfo(),
    campaigns: exportCampaigns(),
    adGroups: exportAdGroups(),
    keywords: exportKeywordsComplete(),
    ads: exportAdsCompleteV2(), // VERSION CORRIGÉE
    searchTerms: exportSearchTermsComplete(),
    performance: exportPerformanceComplete(),
    performanceByDevice: exportPerformanceByDevice(),
    performanceByLocation: exportPerformanceByLocation()
  };

  Logger.log('✅ Export terminé - ' + data.campaigns.length + ' campagnes');
  Logger.log('   - ' + data.adGroups.length + ' groupes d\'annonces');
  Logger.log('   - ' + data.keywords.length + ' mots-clés');
  Logger.log('   - ' + data.ads.length + ' annonces');
  Logger.log('   - ' + data.searchTerms.length + ' termes de recherche');

  // Sauvegarder dans Google Drive
  saveToGoogleDrive(data);
}

/**
 * Infos du compte
 */
function getAccountInfo() {
  return {
    customerId: AdsApp.currentAccount().getCustomerId(),
    name: AdsApp.currentAccount().getName(),
    currency: AdsApp.currentAccount().getCurrencyCode(),
    timezone: AdsApp.currentAccount().getTimeZone()
  };
}

/**
 * Exporte les campagnes avec plus de détails
 */
function exportCampaigns() {
  var campaigns = [];
  var campaignIterator = AdsApp.campaigns()
    .withCondition('Status != REMOVED')
    .get();

  while (campaignIterator.hasNext()) {
    var campaign = campaignIterator.next();
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

      // Métriques principales (pour compatibilité)
      impressions: impressions30,
      clicks: clicks30,
      ctr: stats30.getCtr(),
      cost: cost30,
      conversions: conversions30,
      averageCpc: stats30.getAverageCpc(),

      // Métriques détaillées
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

/**
 * Exporte les groupes d'annonces
 */
function exportAdGroups() {
  var adGroups = [];
  var adGroupIterator = AdsApp.adGroups()
    .withCondition('Status != REMOVED')
    .get();

  while (adGroupIterator.hasNext()) {
    var adGroup = adGroupIterator.next();
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

/**
 * Exporte TOUS les mots-clés (filtrés - sans texte vide)
 */
function exportKeywordsComplete() {
  var keywords = [];
  var keywordIterator = AdsApp.keywords()
    .withCondition('Status != REMOVED')
    .get();

  var count = 0;
  while (keywordIterator.hasNext()) {
    var keyword = keywordIterator.next();
    var keywordText = keyword.getText();

    // FILTRE : Ignorer les mots-clés sans texte
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

      // Métriques principales (pour compatibilité)
      impressions: stats.getImpressions(),
      clicks: stats.getClicks(),
      ctr: stats.getCtr(),
      cost: stats.getCost(),

      // Métriques détaillées
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
      Logger.log('   Mots-clés exportés : ' + count);
    }
  }

  return keywords;
}

/**
 * Exporte les annonces COMPLÈTES V2 - CORRIGÉ
 * Utilise l'itérateur d'annonces pour avoir TOUTES les informations
 */
function exportAdsCompleteV2() {
  var ads = [];
  var count = 0;

  try {
    // Méthode 1 : Annonces responsives (RSA)
    var rsaIterator = AdsApp.ads()
      .withCondition('Type = RESPONSIVE_SEARCH_AD')
      .withCondition('Status != REMOVED')
      .get();

    while (rsaIterator.hasNext()) {
      var ad = rsaIterator.next();
      var stats = ad.getStatsFor('LAST_30_DAYS');
      var campaign = ad.getCampaign();
      var adGroup = ad.getAdGroup();

      // Récupérer les assets de l'annonce RSA
      var rsa = ad.asType().responsive().get();
      var headlines = [];
      var descriptions = [];

      // Extraire les titres
      try {
        var headlineAssets = rsa.headlines();
        for (var i = 0; i < headlineAssets.length && i < 15; i++) {
          headlines.push(headlineAssets[i].text);
        }
      } catch (e) {}

      // Extraire les descriptions
      try {
        var descAssets = rsa.descriptions();
        for (var i = 0; i < descAssets.length && i < 4; i++) {
          descriptions.push(descAssets[i].text);
        }
      } catch (e) {}

      ads.push({
        id: ad.getId(),
        campaignId: campaign.getId(),
        campaignName: campaign.getName(),
        adGroupId: adGroup.getId(),
        adGroupName: adGroup.getName(),
        type: 'RESPONSIVE_SEARCH_AD',
        status: ad.isEnabled() ? 'ENABLED' : ad.isPaused() ? 'PAUSED' : 'REMOVED',

        // Titres multiples (headline1, headline2, headline3)
        headline1: headlines[0] || null,
        headline2: headlines[1] || null,
        headline3: headlines[2] || null,
        allHeadlines: headlines,

        // Descriptions multiples
        description: descriptions[0] || null,
        description2: descriptions[1] || null,
        allDescriptions: descriptions,

        // Métriques
        impressions: stats.getImpressions(),
        clicks: stats.getClicks(),
        ctr: stats.getCtr(),
        cost: stats.getCost(),
        conversions: stats.getConversions()
      });

      count++;
    }

    // Méthode 2 : Annonces textuelles étendues (ETA)
    var etaIterator = AdsApp.ads()
      .withCondition('Type = EXPANDED_TEXT_AD')
      .withCondition('Status != REMOVED')
      .get();

    while (etaIterator.hasNext()) {
      var ad = etaIterator.next();
      var stats = ad.getStatsFor('LAST_30_DAYS');
      var campaign = ad.getCampaign();
      var adGroup = ad.getAdGroup();

      var eta = ad.asType().expandedTextAd().get();

      ads.push({
        id: ad.getId(),
        campaignId: campaign.getId(),
        campaignName: campaign.getName(),
        adGroupId: adGroup.getId(),
        adGroupName: adGroup.getName(),
        type: 'EXPANDED_TEXT_AD',
        status: ad.isEnabled() ? 'ENABLED' : ad.isPaused() ? 'PAUSED' : 'REMOVED',

        headline1: eta.getHeadlinePart1() || null,
        headline2: eta.getHeadlinePart2() || null,
        headline3: eta.getHeadlinePart3() || null,
        description: eta.getDescription() || null,
        description2: eta.getDescription2() || null,

        impressions: stats.getImpressions(),
        clicks: stats.getClicks(),
        ctr: stats.getCtr(),
        cost: stats.getCost(),
        conversions: stats.getConversions()
      });

      count++;
    }

    Logger.log('   Annonces exportées : ' + count);

  } catch (e) {
    Logger.log('⚠️ Erreur export annonces : ' + e);
    Logger.log('   Stack: ' + e.stack);
  }

  return ads;
}

/**
 * Exporte TOUS les termes de recherche
 */
function exportSearchTermsComplete() {
  var searchTerms = [];

  try {
    var report = AdsApp.report(
      'SELECT CampaignId, CampaignName, AdGroupId, AdGroupName, ' +
      'Query, KeywordTextMatchingQuery, MatchType, ' +
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
        matchType: row['MatchType'] || '',
        clicks: parseInt(row['Clicks']) || 0,
        impressions: parseInt(row['Impressions']) || 0,
        ctr: parseFloat(row['Ctr']) || 0,
        conversions: parseFloat(row['Conversions']) || 0,
        cost: parseFloat(row['Cost']) || 0,
        averageCpc: parseFloat(row['AverageCpc']) || 0
      });

      count++;
      if (count % 100 == 0) {
        Logger.log('   Termes de recherche exportés : ' + count);
      }
    }
  } catch (e) {
    Logger.log('⚠️ Erreur export termes de recherche: ' + e);
  }

  return searchTerms;
}

/**
 * Exporte les performances détaillées
 */
function exportPerformanceComplete() {
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

/**
 * Exporte les performances par appareil
 */
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
 * Exporte les performances par géolocalisation
 */
function exportPerformanceByLocation() {
  var locationPerf = [];

  try {
    var report = AdsApp.report(
      'SELECT CampaignId, CampaignName, CountryCriteriaId, ' +
      'Impressions, Clicks, Cost, Conversions ' +
      'FROM GEO_PERFORMANCE_REPORT ' +
      'WHERE CampaignStatus != REMOVED ' +
      'AND Impressions > 0 ' +
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

    // Afficher la taille du fichier
    var sizeKB = file.getSize() / 1024;
    Logger.log('📦 Taille du fichier: ' + sizeKB.toFixed(2) + ' KB');

  } catch (e) {
    Logger.log('❌ Erreur Google Drive: ' + e);
  }
}
