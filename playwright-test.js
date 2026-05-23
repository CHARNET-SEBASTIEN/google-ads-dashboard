/**
 * Test Playwright - Google Ads Dashboard + RAFO
 */

const { chromium } = require('playwright');

async function testLocalApp() {
  console.log('\n📊 TEST 1: Application locale Google Ads Dashboard\n');

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });
  const page = await context.newPage();

  try {
    // Aller sur l'app locale
    console.log('🌐 Ouverture de http://localhost:8501...');
    await page.goto('http://localhost:8501', { waitUntil: 'networkidle', timeout: 30000 });

    // Attendre que Streamlit charge
    console.log('⏳ Attente du chargement de Streamlit...');
    await page.waitForTimeout(5000);

    // Prendre une capture d'écran
    console.log('📸 Capture 1: Page d\'accueil (mode clair)');
    await page.screenshot({ path: 'screenshots/app-home-light.png', fullPage: true });

    // Chercher le bouton mode sombre (🌙)
    console.log('🔍 Recherche du bouton mode sombre...');

    // Essayer de cliquer sur le bouton avec l'emoji lune
    try {
      await page.click('text=🌙', { timeout: 5000 });
      console.log('✅ Bouton mode sombre cliqué');

      // Attendre le rechargement
      await page.waitForTimeout(3000);

      // Capture en mode sombre
      console.log('📸 Capture 2: Page d\'accueil (mode sombre)');
      await page.screenshot({ path: 'screenshots/app-home-dark.png', fullPage: true });
    } catch (e) {
      console.log('⚠️  Bouton mode sombre non trouvé:', e.message);
    }

    // Vérifier la sidebar
    console.log('\n🔍 Vérification de la sidebar...');
    const sidebar = await page.$('[data-testid="stSidebar"]');
    if (sidebar) {
      console.log('✅ Sidebar trouvée');
    } else {
      console.log('❌ Sidebar non trouvée');
    }

    // Vérifier le logo
    const logo = await page.$('svg');
    if (logo) {
      console.log('✅ Logo SVG trouvé');
    } else {
      console.log('❌ Logo non trouvé');
    }

    console.log('\n✅ Test local terminé');
    console.log('📁 Captures sauvegardées dans screenshots/\n');

  } catch (error) {
    console.error('❌ Erreur:', error.message);
  } finally {
    await browser.close();
  }
}

async function testRAFO() {
  console.log('\n🎨 TEST 2: RAFO - Analyse du design\n');

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });
  const page = await context.newPage();

  try {
    // Aller sur RAFO
    console.log('🌐 Ouverture de https://rafo-chapters.com...');
    await page.goto('https://rafo-chapters.com', { waitUntil: 'networkidle', timeout: 30000 });

    // Attendre chargement
    await page.waitForTimeout(2000);

    // Capture de la page de login
    console.log('📸 Capture 1: Page de login RAFO');
    await page.screenshot({ path: 'screenshots/rafo-login.png', fullPage: true });

    // Connexion
    console.log('🔐 Tentative de connexion...');

    try {
      // Remplir email
      await page.fill('input[type="email"]', 's.charnet@majelis.net');
      console.log('✅ Email rempli');

      // Remplir mot de passe
      await page.fill('input[type="password"]', 'rafo2026');
      console.log('✅ Mot de passe rempli');

      // Cliquer sur Sign In
      await page.click('button:has-text("Sign In")');
      console.log('✅ Bouton Sign In cliqué');

      // Attendre la navigation
      await page.waitForNavigation({ waitUntil: 'networkidle', timeout: 10000 });
      console.log('✅ Connecté !');

      // Attendre chargement du dashboard
      await page.waitForTimeout(3000);

      // Capture du dashboard principal
      console.log('📸 Capture 2: Dashboard principal');
      await page.screenshot({ path: 'screenshots/rafo-dashboard.png', fullPage: true });

      // Aller sur user-management
      console.log('🔍 Navigation vers user-management...');
      await page.goto('https://rafo-chapters.com/user-management', { waitUntil: 'networkidle' });
      await page.waitForTimeout(2000);

      // Capture de user-management
      console.log('📸 Capture 3: User Management');
      await page.screenshot({ path: 'screenshots/rafo-user-management.png', fullPage: true });

      // Analyser les couleurs
      console.log('\n🎨 Analyse des couleurs...');
      const bgColor = await page.evaluate(() => {
        return window.getComputedStyle(document.body).backgroundColor;
      });
      console.log('Couleur de fond body:', bgColor);

      // Analyser la sidebar
      const sidebarColor = await page.evaluate(() => {
        const sidebar = document.querySelector('[role="navigation"]') ||
                       document.querySelector('aside') ||
                       document.querySelector('nav');
        if (sidebar) {
          return window.getComputedStyle(sidebar).backgroundColor;
        }
        return 'non trouvée';
      });
      console.log('Couleur sidebar:', sidebarColor);

      console.log('\n✅ Test RAFO terminé');
      console.log('📁 Captures sauvegardées dans screenshots/\n');

    } catch (loginError) {
      console.log('⚠️  Erreur de connexion:', loginError.message);
      console.log('📸 Capture de l\'état actuel');
      await page.screenshot({ path: 'screenshots/rafo-error.png', fullPage: true });
    }

  } catch (error) {
    console.error('❌ Erreur:', error.message);
  } finally {
    await browser.close();
  }
}

async function main() {
  console.log('═'.repeat(60));
  console.log('  PLAYWRIGHT - Tests Google Ads Dashboard + RAFO');
  console.log('═'.repeat(60));

  // Créer le dossier screenshots
  const fs = require('fs');
  if (!fs.existsSync('screenshots')) {
    fs.mkdirSync('screenshots');
    console.log('\n📁 Dossier screenshots/ créé\n');
  }

  // Test 1: App locale
  await testLocalApp();

  // Pause entre les tests
  console.log('\n⏸️  Pause de 3 secondes...\n');
  await new Promise(resolve => setTimeout(resolve, 3000));

  // Test 2: RAFO
  await testRAFO();

  console.log('\n═'.repeat(60));
  console.log('  ✅ TOUS LES TESTS TERMINÉS');
  console.log('═'.repeat(60));
  console.log('\n📁 Consultez le dossier screenshots/ pour les captures\n');
}

// Lancer les tests
main().catch(console.error);
