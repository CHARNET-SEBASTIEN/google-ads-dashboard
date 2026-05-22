const { chromium } = require('playwright');

(async () => {
  console.log('🎨 Test mode sombre...\n');

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });
  const page = await context.newPage();

  // Aller sur l'app
  await page.goto('http://localhost:8501');
  await page.waitForTimeout(5000);

  console.log('📸 Capture avant activation mode sombre');
  await page.screenshot({ path: 'screenshots/test-light.png', fullPage: true });

  // Chercher le bouton avec différents sélecteurs
  try {
    // Essayer de trouver le bouton dans la topbar
    const themeButtons = await page.locator('button').all();
    console.log(`\n🔍 Trouvé ${themeButtons.length} boutons`);

    for (let i = 0; i < themeButtons.length; i++) {
      const text = await themeButtons[i].textContent();
      console.log(`  Bouton ${i}: "${text}"`);

      if (text && (text.includes('🌙') || text.includes('☀️'))) {
        console.log(`  ✅ Bouton thème trouvé, clic...`);
        await themeButtons[i].click();
        await page.waitForTimeout(2000);
        break;
      }
    }

    console.log('📸 Capture après activation mode sombre');
    await page.screenshot({ path: 'screenshots/test-dark.png', fullPage: true });

  } catch (error) {
    console.log('⚠️  Erreur:', error.message);
  }

  await page.waitForTimeout(2000);
  await browser.close();
  console.log('\n✅ Test terminé');
})();
