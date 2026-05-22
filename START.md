# 🚀 Guide de Démarrage - start-dev.sh

## Utilisation

### Démarrage simple (ports par défaut)

```bash
./start-dev.sh
```

- Frontend : http://localhost:4200
- Backend : http://localhost:8000

### Port frontend personnalisé

```bash
./start-dev.sh 4300
```

- Frontend : http://localhost:4300
- Backend : http://localhost:8000

### Ports personnalisés (frontend + backend)

```bash
./start-dev.sh 4300 8001
```

- Frontend : http://localhost:4300
- Backend : http://localhost:8001

## 🔍 Fonctionnalités

### ✅ Vérifications automatiques

- ✓ Présence des fichiers backend/frontend
- ✓ Virtual environment Python installé
- ✓ node_modules installé
- ✓ Détection des ports déjà utilisés
- ✓ Confirmation avant d'utiliser un port occupé

### 📝 Logs

Les logs sont écrits dans :
- `backend.log` - Logs du backend FastAPI
- `frontend.log` - Logs du frontend Angular

Voir les logs en temps réel :

```bash
# Backend
tail -f backend.log

# Frontend
tail -f frontend.log

# Les deux en même temps
tail -f backend.log frontend.log
```

### 🛑 Arrêt propre

Appuyez sur **Ctrl+C** pour arrêter les deux serveurs proprement.

## 📋 Exemples d'utilisation

### Développement normal

```bash
./start-dev.sh
```

### Éviter un conflit de port

```bash
# Si le port 4200 est utilisé
./start-dev.sh 4300

# Si les deux ports sont utilisés
./start-dev.sh 4300 8001
```

### Plusieurs instances en parallèle

```bash
# Instance 1
./start-dev.sh 4200 8000

# Instance 2 (autre terminal)
./start-dev.sh 4300 8001
```

## 🐛 Troubleshooting

### Port déjà utilisé

Le script détecte automatiquement les ports occupés :

```
⚠️  Port 4200 déjà utilisé. Processus:
COMMAND   PID           USER   FD   TYPE
node    12345   username   23u  IPv4

Voulez-vous continuer quand même ? (y/N)
```

Options :
1. Répondre **N** et utiliser un autre port
2. Tuer le processus : `kill 12345`
3. Utiliser un autre port : `./start-dev.sh 4300`

### Backend ne démarre pas

```bash
# Vérifier les logs
tail -f backend.log

# Vérifier le virtual environment
cd backend
source venv/bin/activate
python --version  # Doit être 3.13
uvicorn app.main:app --reload
```

### Frontend ne démarre pas

```bash
# Vérifier les logs
tail -f frontend.log

# Vérifier node_modules
cd frontend
ls node_modules  # Doit contenir des packages
npm install      # Réinstaller si nécessaire
npm start
```

### CORS errors

Si vous changez les ports, mettez à jour `backend/.env` :

```bash
CORS_ORIGINS=http://localhost:4200,http://localhost:4300
```

## 🔧 Configuration avancée

### Changer les ports par défaut

Éditez `start-dev.sh` lignes 10-11 :

```bash
FRONTEND_PORT=${1:-4200}  # Changer 4200
BACKEND_PORT=${2:-8000}   # Changer 8000
```

### Désactiver la vérification des ports

Commentez les lignes 29-30 :

```bash
# check_port $FRONTEND_PORT
# check_port $BACKEND_PORT
```

### Ouvrir automatiquement le navigateur

Ajoutez après la ligne "Application démarrée" :

```bash
# macOS
open http://localhost:$FRONTEND_PORT

# Linux
xdg-open http://localhost:$FRONTEND_PORT
```

## 📚 Voir aussi

- `frontend/PORTS.md` - Configuration détaillée des ports frontend
- `DEPLOIEMENT.md` - Guide de déploiement production
- `README.md` - Documentation générale

## 💡 Tips

### Raccourci terminal

Ajoutez à votre `~/.zshrc` ou `~/.bashrc` :

```bash
alias gads='cd ~/googe_ads_perso && ./start-dev.sh'
alias gads-logs='cd ~/googe_ads_perso && tail -f backend.log frontend.log'
```

Usage :
```bash
gads          # Démarrer l'app
gads-logs     # Voir les logs
```

### Ouvrir directement les URLs

```bash
# macOS
./start-dev.sh && sleep 5 && open http://localhost:4200

# Ou créer un script
cat > quick-start.sh << 'SCRIPT'
#!/bin/bash
./start-dev.sh 4200 8000 &
sleep 8
open http://localhost:4200
open http://localhost:8000/docs
SCRIPT
chmod +x quick-start.sh
```

## ⚙️ Variables d'environnement

Le script utilise :

- `$1` - Port frontend (défaut: 4200)
- `$2` - Port backend (défaut: 8000)
- `$FRONTEND_PID` - PID du processus frontend
- `$BACKEND_PID` - PID du processus backend

## 🔐 Sécurité

Le script :
- ✓ Ne nécessite pas sudo
- ✓ Utilise le virtual environment isolé
- ✓ Écrit les logs dans le répertoire courant
- ✓ Nettoie proprement les processus à l'arrêt

---

**Note**: Toujours lancer depuis la racine du projet : `/Users/sebastiencharnet/googe_ads_perso/`
