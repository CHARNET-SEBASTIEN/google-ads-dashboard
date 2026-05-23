const { chromium } = require('playwright');

(async () => {
  console.log('═══════════════════════════════════════════════════════════');
  console.log('  ANALYSE DÉTAILLÉE DU DESIGN RAFO');
  console.log('═══════════════════════════════════════════════════════════\n');

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });
  const page = await context.newPage();

  try {
    // Connexion à RAFO
    console.log('🔐 Connexion à RAFO...');
    await page.goto('https://rafo-chapters.com');
    await page.waitForTimeout(2000);

    await page.fill('input[type="email"]', 's.charnet@majelis.net');
    await page.fill('input[type="password"]', 'rafo2026');
    await page.click('button:has-text("Sign In")');
    await page.waitForTimeout(3000);

    console.log('✅ Connecté\n');

    // Aller sur la page user-management
    await page.goto('https://rafo-chapters.com/user-management');
    await page.waitForTimeout(3000);

    console.log('📸 Capture de la page user-management');
    await page.screenshot({ path: 'screenshots/rafo-analysis-full.png', fullPage: true });

    // Analyser les couleurs et styles
    console.log('\n🎨 ANALYSE DES COULEURS:\n');

    // Body/Main
    const body = await page.locator('body').first();
    const bodyBg = await body.evaluate(el => window.getComputedStyle(el).backgroundColor);
    const bodyColor = await body.evaluate(el => window.getComputedStyle(el).color);
    console.log(`   Body background: ${bodyBg}`);
    console.log(`   Body color: ${bodyColor}`);

    // Sidebar
    const sidebar = await page.locator('aside, nav, [class*="sidebar"]').first();
    if (sidebar) {
      const sidebarBg = await sidebar.evaluate(el => window.getComputedStyle(el).backgroundColor);
      const sidebarBorder = await sidebar.evaluate(el => window.getComputedStyle(el).borderColor);
      const sidebarWidth = await sidebar.evaluate(el => window.getComputedStyle(el).width);
      console.log(`\n   Sidebar background: ${sidebarBg}`);
      console.log(`   Sidebar border: ${sidebarBorder}`);
      console.log(`   Sidebar width: ${sidebarWidth}`);
    }

    // Header/Title
    const h1 = await page.locator('h1').first();
    if (h1) {
      const h1Color = await h1.evaluate(el => window.getComputedStyle(el).color);
      const h1Size = await h1.evaluate(el => window.getComputedStyle(el).fontSize);
      const h1Weight = await h1.evaluate(el => window.getComputedStyle(el).fontWeight);
      const h1Family = await h1.evaluate(el => window.getComputedStyle(el).fontFamily);
      console.log(`\n   H1 color: ${h1Color}`);
      console.log(`   H1 font-size: ${h1Size}`);
      console.log(`   H1 font-weight: ${h1Weight}`);
      console.log(`   H1 font-family: ${h1Family}`);
    }

    // Buttons
    console.log('\n🔘 ANALYSE DES BOUTONS:\n');
    const buttons = await page.locator('button').all();
    console.log(`   Nombre de boutons: ${buttons.length}`);

    if (buttons.length > 0) {
      const btn = buttons[0];
      const btnBg = await btn.evaluate(el => window.getComputedStyle(el).backgroundColor);
      const btnColor = await btn.evaluate(el => window.getComputedStyle(el).color);
      const btnBorder = await btn.evaluate(el => window.getComputedStyle(el).border);
      const btnRadius = await btn.evaluate(el => window.getComputedStyle(el).borderRadius);
      const btnPadding = await btn.evaluate(el => window.getComputedStyle(el).padding);
      console.log(`   Button bg: ${btnBg}`);
      console.log(`   Button color: ${btnColor}`);
      console.log(`   Button border: ${btnBorder}`);
      console.log(`   Button radius: ${btnRadius}`);
      console.log(`   Button padding: ${btnPadding}`);
    }

    // Cards/Tables
    console.log('\n📋 ANALYSE DES CARDS/TABLES:\n');
    const tables = await page.locator('table').all();
    console.log(`   Tables trouvées: ${tables.length}`);

    if (tables.length > 0) {
      const table = tables[0];
      const tableBg = await table.evaluate(el => window.getComputedStyle(el).backgroundColor);
      const tableBorder = await table.evaluate(el => window.getComputedStyle(el).borderColor);
      console.log(`   Table bg: ${tableBg}`);
      console.log(`   Table border: ${tableBorder}`);

      // Header du tableau
      const thead = await table.locator('thead').first();
      if (thead) {
        const theadBg = await thead.evaluate(el => window.getComputedStyle(el).backgroundColor);
        console.log(`   Table header bg: ${theadBg}`);
      }
    }

    // Cards
    const cards = await page.locator('[class*="card"], [class*="Card"]').all();
    console.log(`\n   Cards trouvées: ${cards.length}`);
    if (cards.length > 0) {
      const card = cards[0];
      const cardBg = await card.evaluate(el => window.getComputedStyle(el).backgroundColor);
      const cardBorder = await card.evaluate(el => window.getComputedStyle(el).border);
      const cardRadius = await card.evaluate(el => window.getComputedStyle(el).borderRadius);
      const cardShadow = await card.evaluate(el => window.getComputedStyle(el).boxShadow);
      console.log(`   Card bg: ${cardBg}`);
      console.log(`   Card border: ${cardBorder}`);
      console.log(`   Card radius: ${cardRadius}`);
      console.log(`   Card shadow: ${cardShadow}`);
    }

    // Navigation items
    console.log('\n🧭 ANALYSE DE LA NAVIGATION:\n');
    const navItems = await page.locator('nav a, aside a, [class*="nav"] a').all();
    console.log(`   Liens de navigation: ${navItems.length}`);

    if (navItems.length > 0) {
      const navItem = navItems[0];
      const navBg = await navItem.evaluate(el => window.getComputedStyle(el).backgroundColor);
      const navColor = await navItem.evaluate(el => window.getComputedStyle(el).color);
      const navPadding = await navItem.evaluate(el => window.getComputedStyle(el).padding);
      const navRadius = await navItem.evaluate(el => window.getComputedStyle(el).borderRadius);
      console.log(`   Nav item bg: ${navBg}`);
      console.log(`   Nav item color: ${navColor}`);
      console.log(`   Nav item padding: ${navPadding}`);
      console.log(`   Nav item radius: ${navRadius}`);
    }

    // Input fields
    console.log('\n⌨️  ANALYSE DES INPUTS:\n');
    const inputs = await page.locator('input[type="text"], input[type="search"]').all();
    console.log(`   Inputs trouvés: ${inputs.length}`);

    if (inputs.length > 0) {
      const input = inputs[0];
      const inputBg = await input.evaluate(el => window.getComputedStyle(el).backgroundColor);
      const inputBorder = await input.evaluate(el => window.getComputedStyle(el).border);
      const inputRadius = await input.evaluate(el => window.getComputedStyle(el).borderRadius);
      const inputPadding = await input.evaluate(el => window.getComputedStyle(el).padding);
      console.log(`   Input bg: ${inputBg}`);
      console.log(`   Input border: ${inputBorder}`);
      console.log(`   Input radius: ${inputRadius}`);
      console.log(`   Input padding: ${inputPadding}`);
    }

    // Extraire les couleurs principales
    console.log('\n🎨 EXTRACTION DES COULEURS PRINCIPALES:\n');
    const allColors = await page.evaluate(() => {
      const colors = new Set();
      const elements = document.querySelectorAll('*');

      elements.forEach(el => {
        const styles = window.getComputedStyle(el);
        if (styles.backgroundColor !== 'rgba(0, 0, 0, 0)' && styles.backgroundColor !== 'transparent') {
          colors.add(styles.backgroundColor);
        }
        if (styles.color !== 'rgba(0, 0, 0, 0)' && styles.color !== 'transparent') {
          colors.add(styles.color);
        }
      });

      return Array.from(colors);
    });

    console.log('   Couleurs utilisées:');
    allColors.slice(0, 20).forEach(color => console.log(`   - ${color}`));

    // Capture d'une zone spécifique
    console.log('\n📸 Captures détaillées...');

    // Sidebar seule
    if (sidebar) {
      await sidebar.screenshot({ path: 'screenshots/rafo-sidebar.png' });
      console.log('   ✅ Sidebar capturée');
    }

    // Table/content area
    const mainContent = await page.locator('main, [role="main"], .content').first();
    if (mainContent) {
      await mainContent.screenshot({ path: 'screenshots/rafo-content.png' });
      console.log('   ✅ Contenu principal capturé');
    }

    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('  ✅ ANALYSE TERMINÉE');
    console.log('═══════════════════════════════════════════════════════════\n');

  } catch (error) {
    console.error('\n❌ Erreur:', error.message);
  }

  await page.waitForTimeout(2000);
  await browser.close();
})();
