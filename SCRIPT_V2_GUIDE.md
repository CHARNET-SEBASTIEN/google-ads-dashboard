# 📊 Script Google Ads V2 - CORRIGÉ

## 🔧 Corrections apportées

### 1. ✅ Annonces - Export complet et correct

**Avant (V1)** ❌ :
- Utilisait `AD_PERFORMANCE_REPORT` (obsolète)
- Un seul titre et une description
- Type d'annonce : "UNKNOWN"
- Données incomplètes

**Maintenant (V2)** ✅ :
- Utilise les **itérateurs d'annonces** natifs
- Support **Responsive Search Ads** (RSA) avec :
  - ✅ Tous les titres (headline1, headline2, headline3, ..., jusqu'à 15)
  - ✅ Toutes les descriptions (description, description2, ..., jusqu'à 4)
  - ✅ Type correct : `RESPONSIVE_SEARCH_AD`
- Support **Expanded Text Ads** (ETA) :
  - ✅ 3 titres (headlinePart1, headlinePart2, headlinePart3)
  - ✅ 2 descriptions
  - ✅ Type correct : `EXPANDED_TEXT_AD`

### 2. ✅ Mots-clés - Filtrés et nettoyés

**Avant (V1)** ❌ :
- Exportait les mots-clés vides (`text: ""`)
- Créait des entrées "N/A" dans l'interface

**Maintenant (V2)** ✅ :
- **Filtre automatique** : ignore les mots-clés sans texte
- Vérifie `keywordText.trim() === ''` avant d'ajouter
- Ajout du champ `id` pour l'identification unique

### 3. ✅ Structure de données améliorée

**Nouvelles garanties** :
- Chaque annonce a un `type` valide
- Les champs null sont explicitement `null` (pas de chaînes vides)
- Métriques structurées pour compatibilité backend

---

## 📦 Exemple de données exportées

### Annonce Responsive Search Ad (RSA)
```json
{
  "id": "123456789",
  "campaignId": "987654321",
  "type": "RESPONSIVE_SEARCH_AD",
  "status": "ENABLED",
  "headline1": "Achetez des Chaussures",
  "headline2": "Livraison Gratuite",
  "headline3": "Retours Faciles",
  "allHeadlines": ["Achetez des Chaussures", "Livraison Gratuite", "Retours Faciles", ...],
  "description": "Découvrez notre collection",
  "description2": "Qualité premium garantie",
  "allDescriptions": ["Découvrez notre collection", "Qualité premium garantie"],
  "impressions": 15000,
  "clicks": 450,
  "conversions": 12
}
```

### Mot-clé (filtré)
```json
{
  "id": "246813579",
  "text": "chaussures running",
  "matchType": "PHRASE",
  "status": "ENABLED",
  "campaignName": "Campagne Sport",
  "impressions": 5000,
  "clicks": 150
}
```

---

## 🚀 Installation du script V2

### Étape 1 : Ouvrir Google Ads Scripts

1. Connectez-vous à **Google Ads**
2. Allez dans **Outils et paramètres** (icône clé à molette)
3. Sous **Automatisation**, cliquez sur **Scripts**

### Étape 2 : Créer ou modifier le script

**Option A - Nouveau script** :
1. Cliquez sur **➕ Nouveau script**
2. Donnez-lui un nom : "Export Dashboard V2"
3. Copiez tout le contenu de `google_ads_script_complet_v2.js`
4. Collez dans l'éditeur
5. Cliquez sur **Enregistrer**

**Option B - Remplacer l'ancien** :
1. Sélectionnez votre script existant
2. **Supprimez** tout le contenu
3. Copiez le nouveau contenu de `google_ads_script_complet_v2.js`
4. Collez et **Enregistrez**

### Étape 3 : Autoriser le script

1. Cliquez sur **Aperçu** (ou **Exécuter**)
2. Si demandé, cliquez sur **Autoriser**
3. Sélectionnez votre compte Google
4. Cliquez sur **Autoriser** pour donner les permissions

### Étape 4 : Première exécution

1. Cliquez sur **Exécuter** ▶️
2. Attendez **1-3 minutes** (selon la taille de votre compte)
3. Vérifiez les logs dans le panneau du bas

**Logs attendus** :
```
🚀 Début de l'export COMPLET V2 des données Google Ads
   Mots-clés exportés : 100
   Mots-clés exportés : 200
   ...
   Annonces exportées : 45
   Termes de recherche exportés : 100
   ...
✅ Export terminé - 5 campagnes
   - 12 groupes d'annonces
   - 234 mots-clés
   - 45 annonces
   - 567 termes de recherche
✅ Fichier mis à jour: https://drive.google.com/file/d/...
📁 Dossier: https://drive.google.com/drive/folders/...
📦 Taille du fichier: 456.78 KB
```

### Étape 5 : Planifier l'exécution quotidienne

1. Cliquez sur **⏰ Planification** (en haut à droite)
2. Choisissez **Quotidiennement**
3. Sélectionnez l'heure (ex: 6h du matin)
4. Cliquez sur **Enregistrer**

Maintenant, vos données seront exportées automatiquement chaque jour !

---

## 📥 Importer dans l'application

### Option 1 : Import depuis Google Drive

1. Ouvrez votre application → **⚙️ Configuration**
2. Onglet **☁️ Google Drive**
3. Collez l'URL du fichier (depuis les logs du script)
4. Cliquez sur **Importer depuis Drive**

### Option 2 : Télécharger et uploader

1. Ouvrez le lien **Fichier mis à jour** dans les logs
2. Téléchargez `latest_data.json`
3. Dans l'app → **⚙️ Configuration** → **📤 Import JSON**
4. Sélectionnez le fichier téléchargé
5. Cliquez sur **Importer**

---

## ✅ Vérifier que ça marche

Après l'import, vérifiez les pages :

### Page Configuration
✅ Devrait afficher :
- Nombre de campagnes
- Nombre de mots-clés (sans entrées vides)
- Nombre d'annonces
- Date de mise à jour formatée

### Page Détail Campagne
✅ **Onglet Mots-clés** :
- Plus de "Mot-clé sans texte"
- Textes réels des mots-clés
- Statuts traduits (Activée, En pause)

✅ **Onglet Annonces** :
- Types corrects : "Annonce adaptative" ou "Annonce textuelle"
- Titres visibles (headline1, headline2, headline3)
- Descriptions visibles
- Statuts traduits

---

## 🔍 Diagnostic des problèmes

### ❌ "Aucune annonce exportée"

**Causes possibles** :
- Toutes vos annonces sont de type ancien (Text Ads)
- Erreur d'autorisation du script

**Solution** :
1. Vérifiez les logs : cherchez "⚠️ Erreur export annonces"
2. Si erreur, copiez le message et cherchez de l'aide
3. Vérifiez que vous avez bien des annonces actives dans Google Ads

### ❌ "Mots-clés toujours vides"

**Causes possibles** :
- Données Google Ads réellement vides
- Mots-clés supprimés mais encore visibles

**Solution** :
1. Allez dans Google Ads → Mots-clés
2. Vérifiez que vos mots-clés ont bien du texte
3. Réexécutez le script après avoir vérifié

### ❌ "Le script prend trop de temps"

**C'est normal** si vous avez :
- Plus de 500 mots-clés
- Plus de 50 annonces
- Plus de 1000 termes de recherche

**Temps normaux** :
- Petit compte : 30-60 sec
- Moyen compte : 1-3 min
- Grand compte : 3-10 min

---

## 📊 Comparaison V1 vs V2

| Fonctionnalité | Script V1 | Script V2 |
|----------------|-----------|-----------|
| **Annonces - Type** | ❌ UNKNOWN | ✅ RSA / ETA |
| **Annonces - Titres** | ❌ 1 seul | ✅ 3+ titres |
| **Annonces - Descriptions** | ❌ 1 seule | ✅ 2+ descriptions |
| **Mots-clés vides** | ❌ Exportés | ✅ Filtrés |
| **Mots-clés - ID** | ❌ Non | ✅ Oui |
| **Format données** | ⚠️ Incohérent | ✅ Cohérent |
| **Compatibilité app** | ⚠️ Partielle | ✅ Totale |

---

## 💡 Conseils

### Pour accélérer l'export

Si vous n'avez pas besoin de toutes les données, commentez certaines sections :

```javascript
var data = {
  timestamp: new Date().toISOString(),
  account: getAccountInfo(),
  campaigns: exportCampaigns(),
  // adGroups: exportAdGroups(),                    // ← Commenter si pas besoin
  keywords: exportKeywordsComplete(),
  ads: exportAdsCompleteV2(),
  searchTerms: exportSearchTermsComplete(),
  // performance: exportPerformanceComplete(),      // ← Commenter si pas besoin
  // performanceByDevice: exportPerformanceByDevice(), // ← Commenter si pas besoin
  // performanceByLocation: exportPerformanceByLocation() // ← Commenter si pas besoin
};
```

### Pour débugger

Ajoutez des logs temporaires :

```javascript
// Dans exportAdsCompleteV2(), après la ligne 336
Logger.log('DEBUG - RSA trouvées : ' + count);
Logger.log('DEBUG - Première annonce : ' + JSON.stringify(ads[0]));
```

---

## 🎯 Prochaines étapes

1. ✅ Installez le script V2
2. ✅ Exécutez-le et vérifiez les logs
3. ✅ Importez les données dans l'app
4. ✅ Vérifiez que les annonces et mots-clés s'affichent correctement
5. ✅ Planifiez l'exécution quotidienne

**Profitez de données complètes et correctes ! 🎉**
