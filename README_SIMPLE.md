# 🚀 Google Ads Dashboard - Mode Simple (Sans API)

## ✨ Nouveau : Utilisez Google Ads Scripts à la place de l'API !

**Fini les complications** avec Developer Token et OAuth. Cette version utilise **Google Ads Scripts** pour extraire les données automatiquement.

---

## 🎯 Avantages

| API Google Ads (Compliqué) | Google Ads Scripts (Simple) |
|----------------------------|------------------------------|
| ❌ Developer Token requis | ✅ Aucun token nécessaire |
| ❌ OAuth 2.0 à configurer | ✅ Autorisation en 1 clic |
| ❌ Approbation Google (jours/semaines) | ✅ Immédiat |
| ❌ Configuration complexe | ✅ Copier-coller un script |
| ✅ Temps réel | ⚡ Mise à jour automatique (1h) |

---

## 📋 Installation en 10 minutes

### Étape 1 : Lancer l'application (2 min)

```bash
cd /Users/sebastiencharnet/googe_ads_perso
docker-compose up -d
```

Ouvrez : http://localhost:8501

### Étape 2 : Installer le script Google Ads (5 min)

1. Allez sur https://ads.google.com
2. **Outils** (⚙️) → **Bulk Actions** → **Scripts**
3. Cliquez sur **+** (Nouveau script)
4. Copiez-collez le contenu de `google_ads_export_script.js`
5. **Enregistrez** (nommez-le "Export Dashboard")
6. Cliquez sur **Aperçu** → **Autoriser**
7. Cliquez sur **Exécuter** (▶️) pour tester

### Étape 3 : Planifier l'exécution automatique (2 min)

1. Dans la page du script, cliquez sur **⏰ Planifications**
2. **+ Créer une planification**
3. Fréquence : **Toutes les heures**
4. **Enregistrer**

### Étape 4 : Importer les données dans le dashboard (1 min)

**Option A : Via Google Drive (recommandé)**

1. Le script crée automatiquement un dossier "Google Ads Dashboard" dans votre Drive
2. Dans l'application → Onglet "Google Drive"
3. Copiez l'ID du fichier `latest_data.json`
4. Cliquez sur "Actualiser"

**Option B : Import manuel**

1. Téléchargez `latest_data.json` depuis Google Drive
2. Dans l'application → Onglet "Import manuel"
3. Uploadez le fichier

---

## 🎉 C'est terminé !

Votre dashboard est maintenant opérationnel :
- ✅ Données actualisées automatiquement toutes les heures
- ✅ Bouton "Refresh" pour recharger les données
- ✅ Toutes les fonctionnalités du dashboard disponibles
- ✅ Aucune configuration d'API nécessaire !

---

## 🔄 Utilisation quotidienne

1. Ouvrez http://localhost:8501
2. Les données sont automatiquement à jour (max 1h de délai)
3. Cliquez sur "Actualiser" si vous voulez forcer une mise à jour
4. Explorez vos campagnes !

---

## 📊 Que contient le dashboard ?

- **Vue d'ensemble** : Toutes vos campagnes avec KPIs
- **Détail campagne** : Configuration, mots-clés, annonces, performances
- **Termes de recherche** : Requêtes réelles des utilisateurs
- **Diagnostic** : Recommandations automatiques

---

## 🆘 Aide

### Le script ne s'exécute pas

- Vérifiez que vous l'avez bien autorisé
- Regardez les logs en bas de la page du script
- L'exécution prend 10-30 secondes

### Je ne vois pas le dossier dans Google Drive

- Exécutez le script une première fois manuellement (▶️)
- Attendez 30 secondes
- Actualisez Google Drive

### Les données ne s'affichent pas dans le dashboard

- Vérifiez que le script s'est bien exécuté (logs)
- Importez manuellement le fichier JSON depuis Google Drive
- Cliquez sur "Recharger les données"

---

## 📁 Fichiers importants

- `google_ads_export_script.js` : Script à installer dans Google Ads
- `INSTALLATION_SCRIPTS.md` : Guide détaillé complet
- `README_SIMPLE.md` : Ce fichier (guide simplifié)
- `README.md` : Documentation complète (version API)

---

## 🔄 Passer à la version API (optionnel)

Si plus tard vous voulez utiliser l'API Google Ads "classique" :
- Consultez `README.md` pour le guide complet
- Avantage : Données en temps réel
- Inconvénient : Configuration plus complexe

---

**Développé avec ❤️ pour simplifier Google Ads**

Mode Simple créé le 22/05/2026
