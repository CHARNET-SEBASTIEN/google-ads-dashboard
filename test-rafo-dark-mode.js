const { chromium } = require('playwright');

(async () => {
  console.log('═══════════════════════════════════════════════════════════');
  console.log('  TEST MODE SOMBRE RAFO');
  console.log('═══════════════════════════════════════════════════════════\n');

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });
  const page = await context.newPage();

  try {
    // Connexion
    console.log('🔐 Connexion...');
    await page.goto('https://rafo-chapters.com');
    await page.waitForTimeout(2000);

    await page.fill('input[type="email"]', 's.charnet@majelis.net');
    await page.fill('input[type="password"]', 'rafo2026');
    await page.click('button:has-text("Sign In")');
    await page.waitForTimeout(3000);
    console.log('✅ Connecté\n');

    // Aller sur user-management
    await page.goto('https://rafo-chapters.com/user-management');
    await page.waitForTimeout(2000);

    // Mode clair - capture avant
    console.log('📸 MODE CLAIR:');
    await page.screenshot({ path: 'screenshots/rafo-light-mode-full.png', fullPage: true });

    const bodyBgLight = await page.evaluate(() => window.getComputedStyle(document.body).backgroundColor);
    const sidebarBgLight = await page.evaluate(() => {
      const sidebar = document.querySelector('aside');
      return sidebar ? window.getComputedStyle(sidebar).backgroundColor : 'N/A';
    });
    console.log(`   Body bg: ${bodyBgLight}`);
    console.log(`   Sidebar bg: ${sidebarBgLight}`);

    // Cliquer sur le toggle dark mode
    console.log('\n🌙 Activation du mode sombre...');
    const themeButton = await page.locator('button[aria-label="Changer de thème"], button[title*="mode sombre"]').first();

    if (themeButton) {
      await themeButton.click();
      await page.waitForTimeout(2000);
      console.log('✅ Mode sombre activé\n');

      // Mode sombre - capture après
      console.log('📸 MODE SOMBRE:');
      await page.screenshot({ path: 'screenshots/rafo-dark-mode-full.png', fullPage: true });

      const bodyBgDark = await page.evaluate(() => window.getComputedStyle(document.body).backgroundColor);
      const sidebarBgDark = await page.evaluate(() => {
        const sidebar = document.querySelector('aside');
        return sidebar ? window.getComputedStyle(sidebar).backgroundColor : 'N/A';
      });
      const textColorDark = await page.evaluate(() => window.getComputedStyle(document.body).color);
      const borderColorDark = await page.evaluate(() => {
        const sidebar = document.querySelector('aside');
        return sidebar ? window.getComputedStyle(sidebar).borderColor : 'N/A';
      });

      console.log(`   Body bg: ${bodyBgDark}`);
      console.log(`   Sidebar bg: ${sidebarBgDark}`);
      console.log(`   Text color: ${textColorDark}`);
      console.log(`   Border color: ${borderColorDark}`);

      // Extraire toutes les couleurs du mode sombre
      console.log('\n🎨 PALETTE MODE SOMBRE:\n');

      const darkColors = await page.evaluate(() => {
        const colors = {
          backgrounds: new Set(),
          texts: new Set(),
          borders: new Set()
        };

        const elements = document.querySelectorAll('*');

        elements.forEach(el => {
          const styles = window.getComputedStyle(el);

          if (styles.backgroundColor !== 'rgba(0, 0, 0, 0)' && styles.backgroundColor !== 'transparent') {
            colors.backgrounds.add(styles.backgroundColor);
          }

          if (styles.color !== 'rgba(0, 0, 0, 0)' && styles.color !== 'transparent') {
            colors.texts.add(styles.color);
          }

          if (styles.borderColor !== 'rgba(0, 0, 0, 0)' && styles.borderColor !== 'transparent') {
            colors.borders.add(styles.borderColor);
          }
        });

        return {
          backgrounds: Array.from(colors.backgrounds).slice(0, 10),
          texts: Array.from(colors.texts).slice(0, 10),
          borders: Array.from(colors.borders).slice(0, 10)
        };
      });

      console.log('   Backgrounds:');
      darkColors.backgrounds.forEach(c => console.log(`     - ${c}`));

      console.log('\n   Texts:');
      darkColors.texts.forEach(c => console.log(`     - ${c}`));

      console.log('\n   Borders:');
      darkColors.borders.forEach(c => console.log(`     - ${c}`));

      // Analyser les composants en mode sombre
      console.log('\n📊 COMPOSANTS EN MODE SOMBRE:\n');

      // Buttons
      const btn = await page.locator('button').first();
      if (btn) {
        const btnStyles = await btn.evaluate(el => ({
          bg: window.getComputedStyle(el).backgroundColor,
          color: window.getComputedStyle(el).color,
          border: window.getComputedStyle(el).border
        }));
        console.log('   Button:', JSON.stringify(btnStyles, null, 2));
      }

      // Table header
      const th = await page.locator('th').first();
      if (th) {
        const thStyles = await th.evaluate(el => ({
          bg: window.getComputedStyle(el).backgroundColor,
          color: window.getComputedStyle(el).color
        }));
        console.log('\n   Table header:', JSON.stringify(thStyles, null, 2));
      }

      // Navigation link
      const navLink = await page.locator('aside a').first();
      if (navLink) {
        const navStyles = await navLink.evaluate(el => ({
          bg: window.getComputedStyle(el).backgroundColor,
          color: window.getComputedStyle(el).color
        }));
        console.log('\n   Nav link:', JSON.stringify(navStyles, null, 2));
      }

      // Captures détaillées
      const sidebar = await page.locator('aside').first();
      if (sidebar) {
        await sidebar.screenshot({ path: 'screenshots/rafo-dark-sidebar.png' });
        console.log('\n   ✅ Sidebar dark capturée');
      }

      // Visiter d'autres pages en mode sombre
      console.log('\n📄 Pages en mode sombre:\n');

      const pages = ['dashboard', 'benchmarking', 'initiatives'];

      for (const pageName of pages) {
        await page.goto(`https://rafo-chapters.com/${pageName}`);
        await page.waitForTimeout(2000);
        await page.screenshot({
          path: `screenshots/rafo-dark-${pageName}.png`,
          fullPage: false
        });
        console.log(`   ✅ ${pageName} capturé`);
      }

    } else {
      console.log('⚠️  Bouton dark mode non trouvé');
    }

    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('  ✅ TEST TERMINÉ');
    console.log('═══════════════════════════════════════════════════════════\n');

  } catch (error) {
    console.error('\n❌ Erreur:', error.message);
  }

  await page.waitForTimeout(2000);
  await browser.close();
})();
