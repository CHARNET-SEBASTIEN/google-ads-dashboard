# 📊 Script Google Ads COMPLET - Guide

## 🎯 Nouvelles données exportées

### Comparaison : Simple vs Complet

| Donnée | Script Simple | Script Complet | Amélioration |
|--------|---------------|----------------|--------------|
| **Mots-clés** | 500 max | ♾️ Illimités | +100% à +1000% |
| **Termes recherche** | 500 max | ♾️ Illimités | +100% à +1000% |
| **Annonces** | ❌ Vides | ✅ Complètes | Nouveau ! |
| **Groupes annonces** | ❌ Non | ✅ Oui | Nouveau ! |
| **Métriques campagne** | 30 jours | 30j + 7j + Aujourd'hui | +200% |
| **Performances appareil** | ❌ Non | ✅ Oui (Desktop/Mobile/Tablet) | Nouveau ! |
| **Géolocalisation** | ❌ Non | ✅ Oui (par pays) | Nouveau ! |
| **Part d'impressions** | ❌ Non | ✅ Oui | Nouveau ! |

---

## 📦 Données exportées en détail

### 1. Campagnes (enrichies)

**Nouvelles métriques** :
- ✅ Performances sur 7 jours (en plus de 30 jours)
- ✅ Performances aujourd'hui
- ✅ Comparaison court terme vs long terme

**Exemple** :
```json
{
  "metrics": { ... },        // 30 jours
  "metrics7Days": { ... },   // 7 derniers jours
  "metricsToday": { ... }    // Aujourd'hui uniquement
}
```

---

### 2. Groupes d'annonces (NOUVEAU !)

**Ce que vous obtenez** :
- Liste complète de tous les groupes d'annonces
- Performances par groupe (impressions, clics, coût, conversions)
- Association campagne ↔ groupe d'annonces

**Utilité** :
- Identifier les groupes d'annonces les moins performants
- Restructurer vos campagnes
- Comparer les performances entre groupes

---

### 3. Mots-clés (ILLIMITÉS)

**Changement** :
- ❌ Avant : Maximum 500 mots-clés
- ✅ Maintenant : TOUS vos mots-clés

**Informations** :
- Texte du mot-clé
- Type de correspondance (exact/expression/large)
- Groupe d'annonces associé
- Performances complètes

**Si vous avez 1000+ mots-clés** :
- Le script prendra plus de temps (1-2 minutes)
- Le fichier sera plus lourd
- Mais vous aurez TOUTES les données !

---

### 4. Annonces (COMPLÈTES - NOUVEAU !)

**Ce que vous obtenez** :
- ID de l'annonce
- Titre (headline)
- Description
- Statut (active/pause)
- Performances (impressions, clics, conversions)
- Association campagne + groupe d'annonces

**Utilité** :
- Identifier les annonces les plus performantes
- Comparer les différents messages
- Optimiser les titres et descriptions

---

### 5. Termes de recherche (ILLIMITÉS + détails)

**Changement** :
- ❌ Avant : Maximum 500 termes
- ✅ Maintenant : TOUS les termes

**Nouvelles informations** :
- Groupe d'annonces qui a déclenché
- Mot-clé qui a matché
- Type de correspondance utilisé
- CPC moyen par terme

**Exemple** :
```json
{
  "query": "logiciel comptabilité",
  "keyword": "logiciel",          // Nouveau !
  "matchType": "BROAD",            // Nouveau !
  "adGroupName": "Logiciels",     // Nouveau !
  "averageCpc": 2.50              // Nouveau !
}
```

---

### 6. Performances détaillées (enrichies)

**Nouvelles métriques** :
- ✅ Position moyenne
- ✅ Part d'impressions (impression share)
- ✅ Part de clics (click share)
- ✅ Association aux groupes d'annonces

**Utilité** :
- Voir si vous êtes bien positionné
- Identifier les opportunités de volume (impression share bas)
- Comparer votre visibilité à la concurrence

---

### 7. Performances par appareil (NOUVEAU !)

**Ce que vous obtenez** :
- Desktop : Ordinateurs
- Mobile : Smartphones
- Tablet : Tablettes

**Pour chaque appareil** :
- Impressions
- Clics
- Coût
- Conversions
- CTR
- CPC moyen

**Utilité** :
- Identifier quel appareil convertit le mieux
- Ajuster les enchères par appareil
- Optimiser pour mobile si nécessaire

**Exemple** :
```
Desktop : 15 000 impressions, 600 clics, 150€, 0 conversion
Mobile  :  8 000 impressions, 300 clics,  50€, 1 conversion
→ Mobile convertit mieux, ajuster les enchères !
```

---

### 8. Performances par géolocalisation (NOUVEAU !)

**Ce que vous obtenez** :
- Top 100 pays/régions
- Performances par pays

**Pour chaque localisation** :
- Impressions
- Clics
- Coût
- Conversions

**Utilité** :
- Identifier les régions performantes
- Exclure les zones non rentables
- Ajuster les enchères par région

---

## 🚀 Installation du script complet

### Étape 1 : Remplacer le script

1. Google Ads → Scripts → "Export Dashboard"
2. **Supprimez** tout le contenu actuel
3. **Copiez** le contenu de `google_ads_script_complet.js`
4. **Collez** et **Enregistrez**

### Étape 2 : Première exécution

1. Cliquez sur **Exécuter** (▶️)
2. **Attendez 1-3 minutes** (plus de données = plus long)
3. Vérifiez les logs

**Logs attendus** :
```
🚀 Début de l'export COMPLET des données Google Ads
   Mots-clés exportés : 100
   ... (si vous en avez beaucoup)
   Termes de recherche exportés : 100
   ...
✅ Export terminé - X campagnes
   - X groupes d'annonces
   - X mots-clés
   - X annonces
   - X termes de recherche
✅ Fichier mis à jour: [URL]
📁 Dossier: [URL]
📦 Taille du fichier: XXX KB
```

### Étape 3 : Importer dans l'application

1. Dans l'app → ⚙️ Configuration Simple
2. Onglet "Google Drive" → Actualisez
3. Ou téléchargez le fichier et uploadez-le

---

## ⏱️ Temps d'exécution

| Taille compte | Script Simple | Script Complet |
|---------------|---------------|----------------|
| Petit (< 50 mots-clés) | 10-20 sec | 30-40 sec |
| Moyen (50-500 mots-clés) | 20-30 sec | 1-2 min |
| Grand (500-2000 mots-clés) | N/A (limité) | 2-5 min |
| Très grand (2000+ mots-clés) | N/A (limité) | 5-10 min |

**Note** : Google Ads Scripts a une limite de 30 minutes par exécution. Suffisant pour la plupart des comptes.

---

## 📊 Taille des fichiers

| Taille compte | Script Simple | Script Complet |
|---------------|---------------|----------------|
| Petit | 50-100 KB | 100-200 KB |
| Moyen | 100-200 KB | 200-500 KB |
| Grand | 200-300 KB | 500 KB - 1 MB |
| Très grand | N/A | 1-5 MB |

**Note** : Google Drive peut héberger jusqu'à 15 GB gratuitement. Aucun problème !

---

## 💡 Conseils d'utilisation

### Quand utiliser le script complet ?

✅ **OUI si** :
- Vous avez beaucoup de mots-clés (> 100)
- Vous voulez analyser TOUS les termes de recherche
- Vous voulez voir les performances par appareil
- Vous voulez optimiser par région
- Vous voulez analyser vos annonces

❌ **Non nécessaire si** :
- Vous avez peu de données (< 50 mots-clés)
- Vous voulez juste un aperçu rapide
- Le script simple vous suffit

### Optimiser les performances

**Si le script est trop lent** :
1. Gardez uniquement les sections qui vous intéressent
2. Commentez les exports inutiles
3. Réduisez l'historique (30 jours → 14 jours)

**Exemple - Ne garder que l'essentiel** :
```javascript
var data = {
  timestamp: new Date().toISOString(),
  account: getAccountInfo(),
  campaigns: exportCampaigns(),
  keywords: exportKeywordsComplete(),     // Garder
  searchTerms: exportSearchTermsComplete(), // Garder
  // adGroups: exportAdGroups(),          // Commenter si pas besoin
  // ads: exportAdsComplete(),            // Commenter si pas besoin
  // performanceByDevice: exportPerformanceByDevice(), // Commenter si pas besoin
  // performanceByLocation: exportPerformanceByLocation() // Commenter si pas besoin
};
```

---

## 🎯 Prochaines étapes

1. **Installez** le script complet
2. **Exécutez-le** une première fois
3. **Importez** les nouvelles données dans l'app
4. **Explorez** les nouvelles informations disponibles

Les pages de l'application afficheront automatiquement les nouvelles données !

---

## ❓ FAQ

### Le script prend trop de temps
➡️ Normal si vous avez beaucoup de données. Attendez jusqu'à 5 minutes.

### Le fichier est très gros
➡️ Normal avec toutes les données. Google Drive peut le gérer sans problème.

### J'ai une erreur "timeout"
➡️ Votre compte est très grand. Commentez certaines sections (voir "Optimiser les performances").

### Je ne vois pas les nouvelles données dans l'app
➡️ Réimportez le fichier depuis Configuration Simple.

---

**Profitez de TOUTES vos données Google Ads ! 📊**
