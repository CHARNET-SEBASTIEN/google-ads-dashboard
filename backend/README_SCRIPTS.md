# 🚀 Scripts de gestion du serveur backend

## 📋 Scripts disponibles

### 🎯 `server.sh` - Script principal (RECOMMANDÉ)

Script tout-en-un pour gérer le serveur.

```bash
./server.sh start      # Démarrer
./server.sh stop       # Arrêter
./server.sh restart    # Redémarrer
./server.sh status     # Voir le statut
./server.sh logs       # Suivre les logs
./server.sh test       # Tester les endpoints
```

### ⚙️ Options avancées

```bash
# Mode développement (défaut) avec auto-reload
./server.sh start --dev

# Mode production avec 4 workers
./server.sh start --prod

# Démarrer en arrière-plan (daemon)
./server.sh start --daemon

# Port personnalisé
./server.sh start --port 8080

# Combinaisons
./server.sh start --daemon --prod --port 8080
```

---

## 🎬 Utilisation courante

### Développement quotidien

```bash
# Démarrer en mode dev (auto-reload)
./server.sh start

# Le serveur tourne maintenant sur http://localhost:8000
# Ctrl+C pour arrêter

# OU en arrière-plan
./server.sh start --daemon
./server.sh logs              # Voir les logs en temps réel
./server.sh stop              # Arrêter quand terminé
```

### Production

```bash
# Démarrer en mode production
./server.sh start --prod --daemon

# Vérifier que tout fonctionne
./server.sh status
./server.sh test

# Redémarrer si nécessaire
./server.sh restart --prod --daemon
```

### Debugging

```bash
# Voir le statut détaillé
./server.sh status

# Suivre les logs en temps réel
./server.sh logs

# Tester les endpoints
./server.sh test

# Arrêter proprement
./server.sh stop
```

---

## 📦 Scripts individuels

Si vous préférez utiliser les scripts séparément :

### `start.sh` - Démarrage

```bash
./start.sh              # Mode dev interactif
./start.sh --daemon     # Mode dev en arrière-plan
./start.sh --prod       # Mode production interactif
./start.sh --port 9000  # Port personnalisé
```

### `stop.sh` - Arrêt propre

```bash
./stop.sh
```

Arrête le serveur de manière propre :
1. Essaie d'abord SIGTERM (arrêt gracieux)
2. Attend jusqu'à 5 secondes
3. Force avec SIGKILL si nécessaire
4. Vérifie que le port est libéré

---

## 🔍 Détails techniques

### Fichiers créés

- `.uvicorn.pid` - PID du processus serveur (mode daemon)
- `uvicorn.log` - Logs du serveur (mode daemon)

### Ports utilisés

- **8000** (défaut) - API backend
- **4200** - Frontend Angular (séparé)

### Vérifications effectuées

Les scripts vérifient automatiquement :
- ✅ Environnement virtuel (venv)
- ✅ Dépendances installées
- ✅ Fichier .env présent
- ✅ Port disponible
- ✅ Processus existants

---

## 🆘 Dépannage

### Le port est déjà utilisé

```bash
# Le script propose automatiquement d'arrêter le processus
./server.sh start

# Ou forcer manuellement
./stop.sh
./server.sh start
```

### Le serveur ne démarre pas

```bash
# Vérifier les logs
cat uvicorn.log

# Vérifier l'environnement
source venv/bin/activate
pip install -r requirements.txt

# Vérifier le fichier .env
cat .env
```

### Processus zombie

```bash
# Le script stop gère ça automatiquement
./stop.sh

# Si ça persiste, forcer :
lsof -ti:8000 | xargs kill -9
```

### Tester manuellement

```bash
# Activer le venv
source venv/bin/activate

# Démarrer manuellement
uvicorn app.main:app --reload --port 8000
```

---

## 📊 Endpoints disponibles

Une fois le serveur démarré :

- **Documentation interactive** : http://localhost:8000/docs
- **API principale** : http://localhost:8000/api
- **Status données** : http://localhost:8000/api/data/status
- **Diagnostics** : http://localhost:8000/api/diagnostics
- **Analyse IA** : http://localhost:8000/api/diagnostics/ai-analysis

---

## 🎯 Exemples de workflows

### Développement frontend + backend

```bash
# Terminal 1 : Backend
cd backend
./server.sh start --daemon
./server.sh logs

# Terminal 2 : Frontend
cd frontend
ng serve
```

### Redéploiement rapide

```bash
# Après un pull ou des changements
git pull
cd backend
./server.sh restart --daemon
./server.sh test
```

### Monitoring en production

```bash
# Vérifier régulièrement
watch -n 5 './server.sh status'

# Ou voir les logs
./server.sh logs
```

---

## ✅ Checklist de déploiement

Avant de mettre en production :

1. [ ] Variables d'environnement configurées dans `.env`
2. [ ] Dépendances installées (`pip install -r requirements.txt`)
3. [ ] Tests backend passent (`./server.sh test`)
4. [ ] Mode production testé localement (`./server.sh start --prod`)
5. [ ] Logs vérifiés (`./server.sh logs`)
6. [ ] Endpoints API testés manuellement

---

## 📝 Notes

- Les scripts détectent automatiquement le répertoire de travail
- Tous les logs sont timestampés
- Les arrêts sont toujours gracieux (SIGTERM avant SIGKILL)
- Le mode daemon est idéal pour le développement long
- Le mode production utilise 4 workers pour de meilleures performances

**Bon développement ! 🚀**
