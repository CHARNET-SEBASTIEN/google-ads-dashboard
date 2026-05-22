# 🚀 Guide Rapide - Votre Dashboard est prêt !

## ✅ Ce qui fonctionne maintenant

1. ✅ Script Google Ads simplifié (sans erreurs)
2. ✅ Import des données dans l'application
3. ✅ Authentification automatique après import
4. ✅ Accès au dashboard complet

---

## 🎯 Utilisation en 3 étapes

### Étape 1 : Lancer l'application (si pas déjà fait)

L'application devrait déjà être lancée sur :
```
http://localhost:8501
```

Si besoin de la relancer :
```bash
cd /Users/sebastiencharnet/googe_ads_perso
docker-compose up -d
```

---

### Étape 2 : Importer les données

**Option A : Via Google Drive** (recommandé)

1. Exécutez le script dans Google Ads (bouton ▶️)
2. Notez l'URL du fichier dans les logs
3. Extrayez l'ID du fichier depuis l'URL :
   ```
   https://drive.google.com/file/d/[COPIEZ_CET_ID]/view
   ```
4. Dans l'app → ⚙️ Configuration Simple → Onglet "Google Drive"
5. Collez l'ID et cliquez "Actualiser"

**Option B : Import manuel**

1. Téléchargez `latest_data.json` depuis Google Drive
2. Dans l'app → ⚙️ Configuration Simple → Onglet "Import manuel"
3. Uploadez le fichier

---

### Étape 3 : Explorer le dashboard

Une fois les données importées :
- ✅ Vous êtes automatiquement "connecté"
- ✅ Toutes les pages sont accessibles
- ✅ Les données s'affichent

**Pages disponibles :**
- 📊 Vue d'ensemble - Liste de toutes vos campagnes
- 🎯 Détail campagne - Configuration détaillée
- 🔍 Termes de recherche - Requêtes réelles
- ⚕️ Diagnostic - Recommandations automatiques

---

## 🔄 Actualiser les données

### Automatique (recommandé)

1. Planifiez le script dans Google Ads (toutes les heures)
2. Les données se mettent à jour automatiquement dans Google Drive
3. Cliquez sur "Actualiser" dans l'app quand vous voulez

### Manuel

1. Exécutez le script manuellement dans Google Ads (▶️)
2. Dans l'app, cliquez sur "🔄 Recharger les données"

---

## 📊 Données disponibles

| Type | Disponible | Période |
|------|------------|---------|
| Campagnes | ✅ Oui | Actuel + 30j |
| Mots-clés | ✅ Oui (500 max) | 30 jours |
| Termes recherche | ✅ Oui (500 max) | 30 jours |
| Performances | ✅ Oui | 30 jours |
| Métriques | ✅ Oui | Impressions, clics, coût, conversions, etc. |

---

## ❓ FAQ Rapide

### Je ne vois pas mes données

1. Vérifiez que le script s'est bien exécuté (logs OK dans Google Ads)
2. Vérifiez que le fichier existe dans Google Drive
3. Réimportez le fichier manuellement
4. Actualisez la page (F5)

### "Vous devez vous connecter d'abord"

➡️ **Corrigé !** Après import, vous êtes automatiquement connecté.
Si le message persiste :
1. Rafraîchissez la page (F5)
2. Cliquez sur "Recharger les données"

### Les données sont vieilles

➡️ Le script s'exécute toutes les heures (si planifié).
Délai max : 1 heure entre Google Ads et le dashboard.

Pour forcer une mise à jour :
1. Exécutez le script manuellement (Google Ads)
2. Attendez 30 secondes
3. Actualisez dans l'app

### Comment ajouter les annonces ?

➡️ La version simple n'exporte pas les annonces (pour éviter erreurs).
Pour l'instant, concentrez-vous sur :
- Campagnes
- Mots-clés
- Termes de recherche
- Performances

---

## 🎉 C'est tout !

Votre dashboard fonctionne maintenant sans API, sans Developer Token, sans OAuth !

**Simple, automatisé, et fonctionnel.** ✨

---

## 🆘 Besoin d'aide ?

- `README_SIMPLE.md` - Guide complet
- `INSTALLATION_SCRIPTS.md` - Guide détaillé du script
- `CORRECTIONS_SCRIPT.md` - Résolution d'erreurs

---

**Développé le 22/05/2026 - Mode Scripts activé 🚀**
