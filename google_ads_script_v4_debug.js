/**
 * Google Ads Script V4 - DEBUG VERSION avec logging détaillé
 * Export des annonces avec méthodes améliorées pour RSA
 */

function main() {
  Logger.log('🚀 Début export V4 - version debug');

  var data = {
    timestamp: new Date().toISOString(),
    account: getAccountInfo(),
    campaigns: exportCampaigns(),
    adGroups: exportAdGroups(),
    keywords: exportKeywords(),
    ads: exportAdsV4Debug(),  // VERSION DEBUG
    searchTerms: exportSearchTerms(),
    performance: exportPerformance(),
    performanceByDevice: exportPerformanceByDevice(),
    performanceByLocation: exportPerformanceByLocation()
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
 * Export annonces V4 - VERSION DEBUG avec logging détaillé
 */
function exportAdsV4Debug() {
  var ads = [];
  var count = 0;

  try {
    var adsIterator = AdsApp.ads()
      .withCondition('Status IN [ENABLED, PAUSED]')
      .get();

    Logger.log('🔍 Début export annonces...');

    while (adsIterator.hasNext()) {
      var ad = adsIterator.next();
      var stats = ad.getStatsFor('LAST_30_DAYS');
      var adGroup = ad.getAdGroup();
      var campaign = adGroup.getCampaign();

      var adId = ad.getId();
      Logger.log('\n📢 Annonce ' + adId);

      // Récupérer le type
      var adType = 'UNKNOWN';
      try {
        adType = ad.getType();
        Logger.log('   Type: ' + adType);
      } catch (e) {
        Logger.log('   ⚠️ Type non disponible: ' + e);
      }

      // Structure de base
      var adData = {
        id: adId,
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
        impressions: stats.getImpressions(),
        clicks: stats.getClicks(),
        ctr: stats.getCtr(),
        cost: stats.getCost(),
        conversions: stats.getConversions()
      };

      // URL
      try {
        var urls = ad.urls();
        if (urls) {
          adData.finalUrl = urls.getFinalUrl();
          Logger.log('   URL: ' + adData.finalUrl);
        }
      } catch (e) {
        Logger.log('   ⚠️ URL erreur: ' + e);
      }

      // Méthode 1 : Test isType()
      Logger.log('   🔍 Test isType()...');
      try {
        var isRSA = ad.isType().responsiveSearchAd();
        var isETA = ad.isType().expandedTextAd();
        var isTextAd = ad.isType().textAd();
        Logger.log('   - RSA: ' + isRSA + ', ETA: ' + isETA + ', Text: ' + isTextAd);
      } catch (e) {
        Logger.log('   ⚠️ isType() error: ' + e);
      }

      // Méthode 2 : Responsive Search Ad
      if (ad.isType().responsiveSearchAd()) {
        Logger.log('   ✅ C\'est un RSA, extraction...');
        try {
          var rsa = ad.asType().responsiveSearchAd();
          Logger.log('   - RSA object: ' + (rsa ? 'OK' : 'NULL'));

          // Test 1 : headlines() direct
          try {
            var headlines = rsa.headlines();
            Logger.log('   - headlines(): ' + (headlines ? headlines.length + ' items' : 'NULL'));

            if (headlines) {
              for (var h = 0; h < Math.min(3, headlines.length); h++) {
                Logger.log('   - headline[' + h + ']: ' + JSON.stringify(headlines[h]));

                // Essayer différentes méthodes d'extraction
                var text = null;

                // Méthode A : .text
                if (headlines[h].text) {
                  text = headlines[h].text;
                  Logger.log('     → Méthode .text: ' + text);
                }

                // Méthode B : .getAssetText()
                if (!text && headlines[h].getAssetText) {
                  text = headlines[h].getAssetText();
                  Logger.log('     → Méthode .getAssetText(): ' + text);
                }

                // Méthode C : .getText()
                if (!text && headlines[h].getText) {
                  text = headlines[h].getText();
                  Logger.log('     → Méthode .getText(): ' + text);
                }

                // Méthode D : toString
                if (!text) {
                  text = headlines[h].toString();
                  Logger.log('     → Méthode .toString(): ' + text);
                }

                if (h === 0) adData.headline1 = text;
                if (h === 1) adData.headline2 = text;
                if (h === 2) adData.headline3 = text;
              }
            }
          } catch (e) {
            Logger.log('   ❌ Erreur headlines: ' + e);
          }

          // Test 2 : descriptions() direct
          try {
            var descriptions = rsa.descriptions();
            Logger.log('   - descriptions(): ' + (descriptions ? descriptions.length + ' items' : 'NULL'));

            if (descriptions) {
              for (var d = 0; d < Math.min(2, descriptions.length); d++) {
                Logger.log('   - description[' + d + ']: ' + JSON.stringify(descriptions[d]));

                var text = null;

                if (descriptions[d].text) {
                  text = descriptions[d].text;
                } else if (descriptions[d].getAssetText) {
                  text = descriptions[d].getAssetText();
                } else if (descriptions[d].getText) {
                  text = descriptions[d].getText();
                } else {
                  text = descriptions[d].toString();
                }

                Logger.log('     → Texte: ' + text);

                if (d === 0) adData.description = text;
                if (d === 1) adData.description2 = text;
              }
            }
          } catch (e) {
            Logger.log('   ❌ Erreur descriptions: ' + e);
          }

          adData.type = 'RESPONSIVE_SEARCH_AD';

        } catch (e) {
          Logger.log('   ❌ Erreur RSA extraction: ' + e);
          Logger.log('   Stack: ' + e.stack);
        }
      }

      // Méthode 3 : Expanded Text Ad
      else if (ad.isType().expandedTextAd()) {
        Logger.log('   ✅ C\'est un ETA');
        try {
          var eta = ad.asType().expandedTextAd();
          adData.headline1 = eta.getHeadlinePart1() || null;
          adData.headline2 = eta.getHeadlinePart2() || null;
          adData.headline3 = eta.getHeadlinePart3() || null;
          adData.description = eta.getDescription() || null;
          adData.description2 = eta.getDescription2() || null;
          adData.type = 'EXPANDED_TEXT_AD';
          Logger.log('   - H1: ' + adData.headline1);
          Logger.log('   - H2: ' + adData.headline2);
        } catch (e) {
          Logger.log('   ❌ Erreur ETA: ' + e);
        }
      }

      // Méthode 4 : Text Ad (ancienne)
      else if (ad.isType().textAd()) {
        Logger.log('   ✅ C\'est un Text Ad');
        try {
          var textAd = ad.asType().textAd();
          adData.headline1 = textAd.getHeadline() || null;
          adData.description = textAd.getDescription1() || null;
          adData.description2 = textAd.getDescription2() || null;
          adData.type = 'TEXT_AD';
        } catch (e) {
          Logger.log('   ❌ Erreur Text Ad: ' + e);
        }
      }

      Logger.log('   📊 Résultat:');
      Logger.log('   - H1: ' + adData.headline1);
      Logger.log('   - H2: ' + adData.headline2);
      Logger.log('   - Desc: ' + adData.description);

      ads.push(adData);
      count++;
    }

    Logger.log('\n✅ Total annonces exportées : ' + count);

  } catch (e) {
    Logger.log('❌ Erreur export annonces : ' + e);
    Logger.log('   Stack : ' + e.stack);
  }

  return ads;
}

function exportSearchTerms() {
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
