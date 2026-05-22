const { chromium } = require('playwright');

(async () => {
  console.log('═══════════════════════════════════════════════════════════');
  console.log('  EXPLORATION COMPLÈTE RAFO - Tous les menus et modes');
  console.log('═══════════════════════════════════════════════════════════\n');

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });
  const page = await context.newPage();

  try {
    // Connexion
    console.log('🔐 Connexion à RAFO...');
    await page.goto('https://rafo-chapters.com');
    await page.waitForTimeout(2000);

    await page.fill('input[type="email"]', 's.charnet@majelis.net');
    await page.fill('input[type="password"]', 'rafo2026');
    await page.click('button:has-text("Sign In")');
    await page.waitForTimeout(3000);
    console.log('✅ Connecté\n');

    // Recherche du toggle dark mode
    console.log('🌙 Recherche du toggle dark/light mode...');
    const darkModeToggles = await page.locator('button[class*="theme"], button[class*="dark"], button[class*="mode"], [class*="theme-toggle"]').all();
    console.log(`   Toggles trouvés: ${darkModeToggles.length}`);

    // Chercher des icônes soleil/lune
    const moonIcon = await page.locator('svg, span, i').filter({ hasText: /🌙|moon/i }).count();
    const sunIcon = await page.locator('svg, span, i').filter({ hasText: /☀️|sun/i }).count();
    console.log(`   Icônes lune: ${moonIcon}, Icônes soleil: ${sunIcon}`);

    // Chercher dans le header/topbar
    const header = await page.locator('header, [role="banner"]').first();
    if (header) {
      await header.screenshot({ path: 'screenshots/rafo-header.png' });
      console.log('   📸 Header capturé');

      const headerButtons = await header.locator('button').all();
      console.log(`   Boutons dans header: ${headerButtons.length}`);

      for (let i = 0; i < headerButtons.length; i++) {
        const btn = headerButtons[i];
        const ariaLabel = await btn.getAttribute('aria-label');
        const title = await btn.getAttribute('title');
        const className = await btn.getAttribute('class');
        console.log(`   Bouton ${i+1}: aria-label="${ariaLabel}", title="${title}", class="${className}"`);
      }
    }

    // Navigation - lister tous les liens du menu
    console.log('\n🧭 EXPLORATION DU MENU PRINCIPAL:\n');
    const navLinks = await page.locator('aside a, nav a, [class*="sidebar"] a').all();
    console.log(`   Liens de navigation: ${navLinks.length}`);

    const menuItems = [];
    for (let i = 0; i < navLinks.length; i++) {
      const link = navLinks[i];
      const text = await link.textContent();
      const href = await link.getAttribute('href');
      if (text && text.trim()) {
        menuItems.push({ text: text.trim(), href });
        console.log(`   ${i+1}. ${text.trim()} → ${href}`);
      }
    }

    // Visiter chaque page du menu
    console.log('\n📄 VISITE DE CHAQUE PAGE:\n');

    const pages = [
      { name: 'Dashboard', url: 'https://rafo-chapters.com/dashboard' },
      { name: 'User Management', url: 'https://rafo-chapters.com/user-management' },
      { name: 'Benchmarking', url: 'https://rafo-chapters.com/benchmarking' },
      { name: 'Initiatives', url: 'https://rafo-chapters.com/initiatives' },
    ];

    for (const pageInfo of pages) {
      console.log(`\n   📑 ${pageInfo.name}...`);
      try {
        await page.goto(pageInfo.url);
        await page.waitForTimeout(2000);

        // Analyser les couleurs de cette page
        const bodyBg = await page.evaluate(() => {
          return window.getComputedStyle(document.body).backgroundColor;
        });
        console.log(`      Background: ${bodyBg}`);

        // Chercher des cards/composants
        const cards = await page.locator('[class*="card"], [class*="Card"], [class*="panel"]').count();
        const buttons = await page.locator('button').count();
        const tables = await page.locator('table').count();
        const inputs = await page.locator('input').count();

        console.log(`      Composants: ${cards} cards, ${buttons} buttons, ${tables} tables, ${inputs} inputs`);

        // Screenshot
        await page.screenshot({
          path: `screenshots/rafo-page-${pageInfo.name.toLowerCase().replace(/ /g, '-')}.png`,
          fullPage: false
        });
        console.log(`      ✅ Screenshot enregistré`);

      } catch (error) {
        console.log(`      ⚠️  Erreur: ${error.message}`);
      }
    }

    // Analyser les patterns de design
    console.log('\n🎨 ANALYSE DES PATTERNS DE DESIGN:\n');

    await page.goto('https://rafo-chapters.com/user-management');
    await page.waitForTimeout(2000);

    // Spacing/Padding
    const sidebar = await page.locator('aside').first();
    if (sidebar) {
      const sidebarStyles = await sidebar.evaluate(el => ({
        width: window.getComputedStyle(el).width,
        padding: window.getComputedStyle(el).padding,
        gap: window.getComputedStyle(el).gap
      }));
      console.log('   Sidebar styles:', JSON.stringify(sidebarStyles, null, 2));
    }

    // Typography
    const allHeadings = await page.locator('h1, h2, h3').all();
    console.log(`\n   Typographie (${allHeadings.length} headers):`);

    for (let i = 0; i < Math.min(3, allHeadings.length); i++) {
      const heading = allHeadings[i];
      const tag = await heading.evaluate(el => el.tagName);
      const styles = await heading.evaluate(el => ({
        fontSize: window.getComputedStyle(el).fontSize,
        fontWeight: window.getComputedStyle(el).fontWeight,
        lineHeight: window.getComputedStyle(el).lineHeight,
        letterSpacing: window.getComputedStyle(el).letterSpacing
      }));
      console.log(`   ${tag}:`, JSON.stringify(styles));
    }

    // Border radius
    const buttonsWithRadius = await page.locator('button').first();
    if (buttonsWithRadius) {
      const borderRadius = await buttonsWithRadius.evaluate(el =>
        window.getComputedStyle(el).borderRadius
      );
      console.log(`\n   Border radius (buttons): ${borderRadius}`);
    }

    // Chercher des transitions/animations
    const hasTransitions = await page.evaluate(() => {
      const allElements = document.querySelectorAll('*');
      let transitionCount = 0;
      allElements.forEach(el => {
        const transition = window.getComputedStyle(el).transition;
        if (transition && transition !== 'all 0s ease 0s') {
          transitionCount++;
        }
      });
      return transitionCount;
    });
    console.log(`   Éléments avec transitions: ${hasTransitions}`);

    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('  ✅ EXPLORATION TERMINÉE');
    console.log('═══════════════════════════════════════════════════════════\n');

  } catch (error) {
    console.error('\n❌ Erreur:', error.message);
  }

  await page.waitForTimeout(2000);
  await browser.close();
})();
