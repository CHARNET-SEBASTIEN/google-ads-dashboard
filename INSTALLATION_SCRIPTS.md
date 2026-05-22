# 🚀 Installation Google Ads Scripts - Guide Simple

## Configuration en 5 minutes

### Étape 1 : Installer le script dans Google Ads (3 min)

1. **Ouvrez Google Ads** : https://ads.google.com

2. **Allez dans Scripts** :
   - Cliquez sur **Outils** (⚙️) en haut à droite
   - Section **BULK ACTIONS**
   - Cliquez sur **Scripts**

3. **Créez un nouveau script** :
   - Cliquez sur le bouton **+** (Nouveau script)
   - Supprimez le code par défaut
   - **Copiez-collez** tout le contenu du fichier `google_ads_export_script.js`

4. **Configurez votre email** :
   - Dans le script, ligne ~340, remplacez :
   ```javascript
   var email = 'sebastien.charnet@gmail.com'; // ← Votre email ici
   ```

5. **Nommez et sauvegardez** :
   - En haut, nommez le script : `Export Dashboard`
   - Cliquez sur **Enregistrer**

6. **Autorisez le script** :
   - Cliquez sur **Aperçu** (ou **Preview**)
   - Une popup apparaît → Cliquez sur **Autoriser**
   - Connectez-vous avec votre compte Google
   - Cliquez sur **Autoriser** (Google vous avertit que c'est votre propre script)

7. **Testez le script** :
   - Cliquez sur **Exécuter** (▶️)
   - Attendez 10-30 secondes
   - Vérifiez les logs en bas (devrait afficher "✅ Export terminé")

---

### Étape 2 : Planifier l'exécution automatique (1 min)

1. Dans la page du script, cliquez sur **⏰ Planifications** (ou **Schedules**)

2. Cliquez sur **+ Créer une planification**

3. Configurez :
   - **Fréquence** : Toutes les heures (ou selon vos besoins)
   - **Heure** : Toute la journée
   - Cliquez sur **Enregistrer**

Le script s'exécutera automatiquement toutes les heures !

---

### Étape 3 : Lancer l'application Dashboard (1 min)

```bash
cd /Users/sebastiencharnet/googe_ads_perso
docker-compose up -d
```

Ouvrez : http://localhost:8501

---

## 📊 Comment ça marche

```
┌─────────────────────────────────────┐
│   Google Ads (votre compte)         │
│                                     │
│   Script s'exécute automatiquement  │
│   toutes les heures                 │
└──────────────┬──────────────────────┘
               │
               │ Exporte données JSON
               ↓
┌─────────────────────────────────────┐
│   Google Drive                      │
│   Dossier: "Google Ads Dashboard"   │
│   Fichier: latest_data.json         │
└──────────────┬──────────────────────┘
               │
               │ Application lit le fichier
               ↓
┌─────────────────────────────────────┐
│   Votre Dashboard                   │
│   http://localhost:8501             │
│                                     │
│   Bouton "Refresh" → Recharge JSON  │
└─────────────────────────────────────┘
```

---

## 🔄 Utilisation quotidienne

### Option 1 : Automatique (recommandé)
- Le script s'exécute tout seul toutes les heures
- Ouvrez le dashboard : http://localhost:8501
- Cliquez sur **Refresh** pour voir les dernières données

### Option 2 : Manuel
- Allez dans Google Ads → Scripts
- Cliquez sur **Exécuter** (▶️) pour lancer manuellement
- Attendez 30 secondes
- Actualisez le dashboard

---

## 📁 Accéder aux données dans Google Drive

1. Allez sur https://drive.google.com
2. Cherchez le dossier **"Google Ads Dashboard"**
3. Le fichier **latest_data.json** contient toutes vos données
4. URL du dossier affichée dans les logs du script

---

## ❓ Résolution de problèmes

### Le script ne s'exécute pas
- Vérifiez que vous l'avez autorisé (étape 6)
- Regardez les logs (en bas de la page du script)
- Vérifiez qu'il n'y a pas d'erreur de syntaxe

### Le fichier n'apparaît pas dans Google Drive
- Le script met quelques secondes à s'exécuter
- Vérifiez les logs pour voir l'URL du dossier
- Le fichier s'appelle `latest_data.json`

### Le dashboard n'affiche pas les données
- Vérifiez que le script s'est bien exécuté (logs)
- Cliquez sur le bouton "Refresh" dans le dashboard
- Vérifiez que le fichier JSON existe dans Google Drive

---

## 🎯 Prochaines étapes

Maintenant que le script est configuré :
1. ✅ Les données s'exportent automatiquement
2. ✅ Utilisez votre dashboard pour les visualiser
3. ✅ Cliquez sur "Refresh" quand vous voulez les dernières données

**Simple et automatisé ! 🎉**
