#!/bin/bash

# Script de démarrage du Dashboard Google Ads
# Utilisation:
#   ./start-dev.sh                    # Ports par défaut (frontend: 4200, backend: 8000)
#   ./start-dev.sh 4300              # Frontend sur 4300, backend sur 8000
#   ./start-dev.sh 4300 8001         # Frontend sur 4300, backend sur 8001

# Ports par défaut
FRONTEND_PORT=${1:-4201}
BACKEND_PORT=${2:-8000}

echo "🚀 Démarrage du Dashboard Google Ads..."
echo ""
echo "⚙️  Configuration:"
echo "   Frontend port: $FRONTEND_PORT"
echo "   Backend port:  $BACKEND_PORT"
echo ""

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "backend/app/main.py" ] || [ ! -f "frontend/package.json" ]; then
    echo "❌ Erreur: Lancer ce script depuis la racine du projet"
    exit 1
fi

# Vérifier que les ports sont disponibles
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo "⚠️  Port $1 déjà utilisé. Processus:"
        lsof -i :$1
        read -p "Voulez-vous continuer quand même ? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

check_port $FRONTEND_PORT
check_port $BACKEND_PORT

# Fonction pour gérer l'arrêt propre
cleanup() {
    echo ""
    echo "🛑 Arrêt des serveurs..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "✅ Serveurs arrêtés"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Démarrer le backend
echo "📦 Démarrage du backend FastAPI..."
cd backend
if [ ! -d "venv" ]; then
    echo "❌ Erreur: Virtual environment non trouvé"
    echo "   Exécutez: cd backend && /opt/homebrew/bin/python3.13 -m venv venv && ./venv/bin/pip install -r requirements.txt"
    exit 1
fi
source venv/bin/activate
uvicorn app.main:app --reload --port $BACKEND_PORT > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Attendre que le backend démarre
echo "⏳ Attente du démarrage du backend..."
sleep 3

# Vérifier que le backend est démarré
if ! ps -p $BACKEND_PID > /dev/null; then
    echo "❌ Erreur: Le backend n'a pas démarré correctement"
    echo "   Vérifiez les logs: tail -f backend.log"
    exit 1
fi

# Démarrer le frontend
echo "🎨 Démarrage du frontend Angular..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "❌ Erreur: node_modules non trouvé"
    echo "   Exécutez: cd frontend && npm install"
    exit 1
fi
npm start -- --port $FRONTEND_PORT > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Application démarrée !"
echo ""
echo "📍 URLs:"
echo "   Frontend:  http://localhost:$FRONTEND_PORT"
echo "   Backend:   http://localhost:$BACKEND_PORT"
echo "   API Docs:  http://localhost:$BACKEND_PORT/docs"
echo ""
echo "📝 Logs:"
echo "   Backend:   tail -f backend.log"
echo "   Frontend:  tail -f frontend.log"
echo ""
echo "💡 Tips:"
echo "   - Ouvrir frontend:  open http://localhost:$FRONTEND_PORT"
echo "   - Ouvrir API docs:  open http://localhost:$BACKEND_PORT/docs"
echo "   - Changer de port:  ./start-dev.sh 4300 8001"
echo ""
echo "🛑 Appuyez sur Ctrl+C pour arrêter"
echo ""

# Garder le script actif
wait
