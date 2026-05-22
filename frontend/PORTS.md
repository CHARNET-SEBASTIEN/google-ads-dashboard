# 🔌 Configuration des Ports Frontend

## Ports disponibles

### Port par défaut : 4200

Le frontend démarre par défaut sur http://localhost:4200

## 🚀 Méthodes de changement de port

### 1. Ligne de commande (Temporaire)

```bash
cd frontend

# Port 4300
npm start -- --port 4300

# Port 5000
ng serve --port 5000

# Port 8080
ng serve --port 8080
```

### 2. Scripts npm prédéfinis (package.json)

```bash
# Port 4200 (défaut)
npm start

# Port 4300
npm run start:4300

# Port 5000
npm run start:5000
```

### 3. Configuration angular.json (Permanent)

Le port par défaut est configuré dans `angular.json` :

```json
"serve": {
  "options": {
    "port": 4200
  }
}
```

Pour changer le port par défaut :
1. Ouvrir `angular.json`
2. Modifier la valeur `port` dans `"serve" → "options"`
3. Relancer `npm start`

## 🌐 Avec le backend

Si vous changez le port frontend, pensez à :

### 1. Mettre à jour le CORS backend

Éditez `backend/.env` :

```bash
CORS_ORIGINS=http://localhost:4300,http://localhost:5000
```

### 2. Mettre à jour l'environnement frontend

Si le backend change de port, éditez `frontend/src/environments/environment.ts` :

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'  // Changer ici si besoin
};
```

## 📝 Exemples d'utilisation

### Développement standard
```bash
npm start
# → http://localhost:4200
```

### Éviter un conflit de port
```bash
npm start -- --port 4300
# → http://localhost:4300
```

### Plusieurs instances en parallèle
```bash
# Terminal 1
npm run start:4300

# Terminal 2
npm run start:5000
```

## 🔧 Options supplémentaires

### Ouvrir automatiquement le navigateur
```bash
ng serve --open --port 4300
# ou
npm start -- --open --port 4300
```

### Désactiver live reload
```bash
ng serve --port 4300 --live-reload=false
```

### Changer l'host (pour accès réseau)
```bash
ng serve --host 0.0.0.0 --port 4300
# Accessible depuis le réseau local
```

## ⚠️ Ports à éviter

- **3000** : Souvent utilisé par React/Next.js
- **8000** : Utilisé par le backend FastAPI
- **8080** : Commun pour serveurs web
- **5000** : Souvent utilisé par Flask

## 🐛 Troubleshooting

### Port déjà utilisé
```bash
# macOS/Linux - Trouver le processus
lsof -i :4200

# Tuer le processus
kill -9 <PID>

# Ou utiliser un autre port
npm start -- --port 4300
```

### CORS errors après changement de port
Vérifiez que le nouveau port est dans `CORS_ORIGINS` du backend.
