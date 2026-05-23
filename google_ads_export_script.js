/**
 * Google Ads Script - Export complet des données de campagnes
 * À copier-coller dans Google Ads → Outils → Scripts
 *
 * Ce script exporte toutes les données nécessaires au Dashboard
 * et les envoie vers un endpoint local ou les sauvegarde
 */

function main() {
  Logger.log('🚀 Début de l\'export des données Google Ads');

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
    ads: exportAds(),
    searchTerms: exportSearchTerms(),
    performance: exportPerformance()
  };

  Logger.log('✅ Export terminé - ' + data.campaigns.length + ' campagnes');

  // Option 1 : Envoyer à un endpoint local (si serveur lancé)
  sendToLocalEndpoint(data);

  // Option 2 : Sauvegarder dans Google Drive
  saveToGoogleDrive(data);

  // Option 3 : Envoyer par email (pour debug)
  // sendByEmail(data);
}

/**
 * Exporte les données des campagnes
 */
function exportCampaigns() {
  var campaigns = [];

  var campaignIterator = AdsApp.campaigns()
    .withCondition('Status != REMOVED')
    .get();

  while (campaignIterator.hasNext()) {
    var campaign = campaignIterator.next();
    var stats = campaign.getStatsFor('LAST_30_DAYS');

    campaigns.push({
      id: campaign.getId(),
      name: campaign.getName(),
      status: campaign.isEnabled() ? 'ENABLED' : campaign.isPaused() ? 'PAUSED' : 'REMOVED',
      type: 'SEARCH', // Type de campagne (Scripts ne donne pas facilement accès au type)
      budget: campaign.getBudget() ? campaign.getBudget().getAmount() : 0,
      biddingStrategy: campaign.getBiddingStrategyType(),

      // Paramètres de ciblage
      targetSearch: true, // Par défaut pour Search
      targetDisplay: false,
      targetPartners: false,

      // Dates
      startDate: campaign.getStartDate() ? formatDate(campaign.getStartDate()) : null,
      endDate: campaign.getEndDate() ? formatDate(campaign.getEndDate()) : null,

      // Métriques 30 derniers jours
      metrics: {
        impressions: stats.getImpressions(),
        clicks: stats.getClicks(),
        ctr: stats.getCtr(),
        cost: stats.getCost(),
        conversions: stats.getConversions(),
        conversionRate: stats.getClicks() > 0 ? (stats.getConversions() / stats.getClicks()) * 100 : 0,
        averageCpc: stats.getAverageCpc(),
        costPerConversion: stats.getConversions() > 0 ? stats.getCost() / stats.getConversions() : 0
      }
    });
  }

  return campaigns;
}

/**
 * Exporte les mots-clés
 */
function exportKeywords() {
  var keywords = [];

  var keywordIterator = AdsApp.keywords()
    .withCondition('Status != REMOVED')
    .withLimit(1000)
    .get();

  while (keywordIterator.hasNext()) {
    var keyword = keywordIterator.next();
    var stats = keyword.getStatsFor('LAST_30_DAYS');
    var campaign = keyword.getCampaign();
    var adGroup = keyword.getAdGroup();

    // Récupérer le CPC max (peut ne pas être disponible)
    var maxCpc = 0;
    try {
      var bidding = keyword.bidding();
      if (bidding && bidding.getCpc) {
        maxCpc = bidding.getCpc();
      }
    } catch (e) {
      // CPC non disponible
    }

    keywords.push({
      campaignId: campaign.getId(),
      campaignName: campaign.getName(),
      adGroupId: adGroup.getId(),
      adGroupName: adGroup.getName(),
      text: keyword.getText(),
      matchType: keyword.getMatchType(),
      status: keyword.isEnabled() ? 'ENABLED' : 'PAUSED',
      maxCpc: maxCpc,
      qualityScore: 0, // Quality Score non accessible via Scripts API

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
 * Exporte les annonces
 */
function exportAds() {
  var ads = [];

  var adIterator = AdsApp.ads()
    .withCondition('Status != REMOVED')
    .withLimit(500)
    .get();

  while (adIterator.hasNext()) {
    var ad = adIterator.next();
    var stats = ad.getStatsFor('LAST_30_DAYS');
    var campaign = ad.getCampaign();
    var adGroup = ad.getAdGroup();

    var adData = {
      campaignId: campaign.getId(),
      campaignName: campaign.getName(),
      adGroupId: adGroup.getId(),
      adGroupName: adGroup.getName(),
      type: ad.getType(),
      status: ad.isEnabled() ? 'ENABLED' : 'PAUSED',

      metrics: {
        impressions: stats.getImpressions(),
        clicks: stats.getClicks(),
        ctr: stats.getCtr(),
        conversions: stats.getConversions()
      }
    };

    // Extraire les headlines et descriptions selon le type
    if (ad.isType().responsiveSearchAd()) {
      var rsa = ad.asType().responsiveSearchAd();
      adData.headlines = [];
      adData.descriptions = [];

      // Headlines
      for (var i = 0; i < 15; i++) {
        var headline = rsa.getHeadline(i);
        if (headline) {
          adData.headlines.push({
            text: headline.text || '',
            position: i
          });
        }
      }

      // Descriptions
      for (var i = 0; i < 4; i++) {
        var description = rsa.getDescription(i);
        if (description) {
          adData.descriptions.push({
            text: description.text || '',
            position: i
          });
        }
      }

      adData.finalUrls = rsa.urls().getFinalUrl() ? [rsa.urls().getFinalUrl()] : [];
    }

    ads.push(adData);
  }

  return ads;
}

/**
 * Exporte les termes de recherche
 */
function exportSearchTerms() {
  var searchTerms = [];

  var report = AdsApp.report(
    'SELECT CampaignId, CampaignName, Query, Clicks, Impressions, Ctr, Conversions, Cost ' +
    'FROM SEARCH_QUERY_PERFORMANCE_REPORT ' +
    'WHERE Impressions > 0 ' +
    'DURING LAST_30_DAYS'
  );

  var rows = report.rows();
  while (rows.hasNext()) {
    var row = rows.next();
    searchTerms.push({
      campaignId: row['CampaignId'],
      campaignName: row['CampaignName'],
      query: row['Query'],
      clicks: parseInt(row['Clicks']),
      impressions: parseInt(row['Impressions']),
      ctr: parseFloat(row['Ctr']),
      conversions: parseFloat(row['Conversions']),
      cost: parseFloat(row['Cost'])
    });
  }

  return searchTerms;
}

/**
 * Exporte les performances quotidiennes (30 derniers jours)
 */
function exportPerformance() {
  var performance = [];

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
      impressions: parseInt(row['Impressions']),
      clicks: parseInt(row['Clicks']),
      cost: parseFloat(row['Cost']),
      conversions: parseFloat(row['Conversions']),
      ctr: parseFloat(row['Ctr']),
      averageCpc: parseFloat(row['AverageCpc'])
    });
  }

  return performance;
}

/**
 * Envoie les données à un endpoint local
 */
function sendToLocalEndpoint(data) {
  var endpoint = 'http://localhost:8501/api/import'; // Endpoint de l'application

  try {
    var response = UrlFetchApp.fetch(endpoint, {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(data),
      muteHttpExceptions: true
    });

    Logger.log('✅ Données envoyées à l\'endpoint local');
    Logger.log('Réponse: ' + response.getContentText());
  } catch (e) {
    Logger.log('⚠️ Impossible d\'envoyer à l\'endpoint local: ' + e);
    Logger.log('L\'application n\'est peut-être pas lancée ou l\'endpoint n\'est pas accessible');
  }
}

/**
 * Sauvegarde dans Google Drive
 */
function saveToGoogleDrive(data) {
  try {
    var fileName = 'google_ads_data_' + Utilities.formatDate(new Date(), 'GMT', 'yyyy-MM-dd_HH-mm') + '.json';
    var folder = DriveApp.getRootFolder(); // Ou créer un dossier spécifique

    // Essayer de trouver un dossier "Google Ads Dashboard"
    var folders = DriveApp.getFoldersByName('Google Ads Dashboard');
    if (folders.hasNext()) {
      folder = folders.next();
    } else {
      // Créer le dossier s'il n'existe pas
      folder = DriveApp.createFolder('Google Ads Dashboard');
    }

    // Créer ou mettre à jour le fichier
    var files = folder.getFilesByName('latest_data.json');
    if (files.hasNext()) {
      // Mettre à jour le fichier existant
      var file = files.next();
      file.setContent(JSON.stringify(data, null, 2));
      Logger.log('✅ Fichier mis à jour dans Google Drive: ' + file.getUrl());
    } else {
      // Créer un nouveau fichier
      var file = folder.createFile('latest_data.json', JSON.stringify(data, null, 2));
      Logger.log('✅ Fichier créé dans Google Drive: ' + file.getUrl());
    }

    Logger.log('📁 Dossier Google Drive: ' + folder.getUrl());
  } catch (e) {
    Logger.log('❌ Erreur sauvegarde Google Drive: ' + e);
  }
}

/**
 * Envoie par email (pour debug)
 */
function sendByEmail(data) {
  var email = 'sebastien.charnet@gmail.com'; // Votre email
  var subject = 'Export Google Ads - ' + new Date().toLocaleString();
  var body = 'Données exportées avec succès.\n\n' +
             'Campagnes: ' + data.campaigns.length + '\n' +
             'Mots-clés: ' + data.keywords.length + '\n' +
             'Annonces: ' + data.ads.length + '\n' +
             'Termes de recherche: ' + data.searchTerms.length;

  MailApp.sendEmail(email, subject, body);
  Logger.log('📧 Email envoyé à ' + email);
}

/**
 * Formatte une date
 */
function formatDate(dateObj) {
  if (!dateObj) return null;
  return Utilities.formatDate(new Date(dateObj.year, dateObj.month - 1, dateObj.day), 'GMT', 'yyyy-MM-dd');
}
