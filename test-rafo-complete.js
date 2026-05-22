const { chromium } = require('playwright');

(async () => {
  console.log('═══════════════════════════════════════════════════════════');
  console.log('  TEST COMPLET RAFO - Menu & Mode Sombre');
  console.log('═══════════════════════════════════════════════════════════\n');

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });
  const page = await context.newPage();

  try {
    // Aller sur l'app
    console.log('🌐 Ouverture de l\'application...');
    await page.goto('http://localhost:8501');
    await page.waitForTimeout(5000);

    // Vérifier mode actuel
    const body = await page.locator('body').first();
    const bgColor = await body.evaluate(el => window.getComputedStyle(el).backgroundColor);
    console.log(`   Couleur de fond: ${bgColor}`);

    // Si pas en mode sombre, activer
    const themeButtons = await page.locator('button').all();
    let isDarkMode = bgColor.includes('10, 10, 10') || bgColor.includes('0, 0, 0');

    if (!isDarkMode) {
      console.log('🌙 Activation du mode sombre...');
      for (let btn of themeButtons) {
        const text = await btn.textContent();
        if (text && text.includes('🌙')) {
          await btn.click();
          await page.waitForTimeout(2000);
          break;
        }
      }
    } else {
      console.log('✅ Mode sombre déjà activé');
    }

    // Test 1: Page d'accueil
    console.log('\n📊 TEST 1: Page d\'accueil (Dashboard)');
    await page.waitForTimeout(2000);
    await page.screenshot({
      path: 'screenshots/rafo-test-1-home.png',
      fullPage: true
    });
    console.log('   ✅ Capture enregistrée');

    // Vérifier la sidebar
    console.log('\n🔍 Vérification de la sidebar...');
    const sidebar = await page.locator('section[data-testid="stSidebar"]').first();
    if (sidebar) {
      const sidebarBg = await sidebar.evaluate(el => window.getComputedStyle(el).backgroundColor);
      console.log(`   Fond sidebar: ${sidebarBg}`);

      // Vérifier le logo
      const svgCount = await page.locator('section[data-testid="stSidebar"] svg').count();
      console.log(`   Logos SVG trouvés: ${svgCount}`);

      // Vérifier le titre
      const title = await page.locator('section[data-testid="stSidebar"] h2').first();
      if (title) {
        const titleText = await title.textContent();
        const titleColor = await title.evaluate(el => window.getComputedStyle(el).color);
        console.log(`   Titre: "${titleText}" - Couleur: ${titleColor}`);
      }
    }

    // Vérifier les cards des colonnes
    console.log('\n🎴 Vérification des cards (Fonctionnalités, Sécurité, Cache)...');
    const columns = await page.locator('div[data-testid="column"]').all();
    console.log(`   Colonnes trouvées: ${columns.length}`);

    if (columns.length >= 3) {
      for (let i = 0; i < 3; i++) {
        const verticalBlock = columns[i].locator('div[data-testid="stVerticalBlock"]').first();
        if (verticalBlock) {
          const cardBg = await verticalBlock.evaluate(el => window.getComputedStyle(el).backgroundColor);
          const cardBorder = await verticalBlock.evaluate(el => window.getComputedStyle(el).borderColor);
          console.log(`   Card ${i+1}: bg=${cardBg}, border=${cardBorder}`);
        }
      }
    }

    // Test 2: Navigation vers Configuration
    console.log('\n📊 TEST 2: Page Configuration');
    const configBtn = await page.locator('button:has-text("Configuration")').first();
    if (configBtn) {
      await configBtn.click();
      await page.waitForTimeout(3000);
      await page.screenshot({
        path: 'screenshots/rafo-test-2-config.png',
        fullPage: true
      });
      console.log('   ✅ Capture enregistrée');
    } else {
      console.log('   ⚠️  Bouton Configuration non trouvé');
    }

    // Test 3: Navigation vers Vue d'ensemble
    console.log('\n📊 TEST 3: Page Vue d\'ensemble');
    const overviewBtn = await page.locator('button:has-text("Vue d\'ensemble")').first();
    if (overviewBtn) {
      await overviewBtn.click();
      await page.waitForTimeout(3000);
      await page.screenshot({
        path: 'screenshots/rafo-test-3-overview.png',
        fullPage: true
      });
      console.log('   ✅ Capture enregistrée');

      // Vérifier si il y a des tableaux
      const dataframes = await page.locator('.stDataFrame').count();
      console.log(`   Tableaux trouvés: ${dataframes}`);
    } else {
      console.log('   ⚠️  Bouton Vue d\'ensemble non trouvé');
    }

    // Test 4: Navigation vers Détail campagne
    console.log('\n📊 TEST 4: Page Détail campagne');
    const campaignBtn = await page.locator('button:has-text("Détail campagne")').first();
    if (campaignBtn) {
      await campaignBtn.click();
      await page.waitForTimeout(3000);
      await page.screenshot({
        path: 'screenshots/rafo-test-4-campaign.png',
        fullPage: true
      });
      console.log('   ✅ Capture enregistrée');

      // Vérifier les tabs si présents
      const tabs = await page.locator('[data-baseweb="tab"]').count();
      if (tabs > 0) {
        console.log(`   Tabs trouvés: ${tabs}`);
      }
    } else {
      console.log('   ⚠️  Bouton Détail campagne non trouvé');
    }

    // Test 5: Navigation vers Termes de recherche
    console.log('\n📊 TEST 5: Page Termes de recherche');
    const searchBtn = await page.locator('button:has-text("Termes de recherche")').first();
    if (searchBtn) {
      await searchBtn.click();
      await page.waitForTimeout(3000);
      await page.screenshot({
        path: 'screenshots/rafo-test-5-search.png',
        fullPage: true
      });
      console.log('   ✅ Capture enregistrée');
    } else {
      console.log('   ⚠️  Bouton Termes de recherche non trouvé');
    }

    // Test 6: Navigation vers Diagnostic
    console.log('\n📊 TEST 6: Page Diagnostic');
    const diagBtn = await page.locator('button:has-text("Diagnostic")').first();
    if (diagBtn) {
      await diagBtn.click();
      await page.waitForTimeout(3000);
      await page.screenshot({
        path: 'screenshots/rafo-test-6-diagnostic.png',
        fullPage: true
      });
      console.log('   ✅ Capture enregistrée');
    } else {
      console.log('   ⚠️  Bouton Diagnostic non trouvé');
    }

    // Retour à l'accueil
    console.log('\n📊 Retour à l\'accueil');
    const homeBtn = await page.locator('button:has-text("Accueil")').first();
    if (homeBtn) {
      await homeBtn.click();
      await page.waitForTimeout(2000);
    }

    // Test des boutons de navigation - vérifier le hover
    console.log('\n🎯 Test des effets hover sur les boutons de navigation...');
    const navButtons = await page.locator('section[data-testid="stSidebar"] button').all();
    console.log(`   Boutons de navigation: ${navButtons.length}`);

    if (navButtons.length > 3) {
      const testBtn = navButtons[4]; // Prendre un bouton au milieu
      const beforeHover = await testBtn.evaluate(el => ({
        bg: window.getComputedStyle(el).backgroundColor,
        borderLeft: window.getComputedStyle(el).borderLeftColor,
        transform: window.getComputedStyle(el).transform
      }));
      console.log(`   Avant hover: ${JSON.stringify(beforeHover)}`);

      await testBtn.hover();
      await page.waitForTimeout(500);

      const afterHover = await testBtn.evaluate(el => ({
        bg: window.getComputedStyle(el).backgroundColor,
        borderLeft: window.getComputedStyle(el).borderLeftColor,
        transform: window.getComputedStyle(el).transform
      }));
      console.log(`   Après hover: ${JSON.stringify(afterHover)}`);

      if (afterHover.borderLeft !== beforeHover.borderLeft) {
        console.log('   ✅ Effet hover détecté (bordure gauche change)');
      }
    }

    // Test du topbar
    console.log('\n🎚️  Vérification du topbar...');
    const langSelector = await page.locator('.stSelectbox').first();
    if (langSelector) {
      const langBg = await langSelector.evaluate(el => window.getComputedStyle(el).backgroundColor);
      console.log(`   Sélecteur langue - bg: ${langBg}`);
    }

    const themeBtn = await page.locator('button').filter({ hasText: /[🌙☀️]/ }).first();
    if (themeBtn) {
      const themeBtnBg = await themeBtn.evaluate(el => window.getComputedStyle(el).backgroundColor);
      const themeBtnBorder = await themeBtn.evaluate(el => window.getComputedStyle(el).borderColor);
      console.log(`   Bouton thème - bg: ${themeBtnBg}, border: ${themeBtnBorder}`);
    }

    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('  ✅ TEST COMPLET TERMINÉ');
    console.log('═══════════════════════════════════════════════════════════');
    console.log('\n📁 6 captures d\'écran enregistrées dans screenshots/');
    console.log('   - rafo-test-1-home.png');
    console.log('   - rafo-test-2-config.png');
    console.log('   - rafo-test-3-overview.png');
    console.log('   - rafo-test-4-campaign.png');
    console.log('   - rafo-test-5-search.png');
    console.log('   - rafo-test-6-diagnostic.png\n');

  } catch (error) {
    console.error('\n❌ Erreur:', error.message);
  }

  await page.waitForTimeout(2000);
  await browser.close();
})();
