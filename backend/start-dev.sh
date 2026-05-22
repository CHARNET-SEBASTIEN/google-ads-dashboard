#!/bin/bash

# Script de démarrage du Dashboard Google Ads
# Utilisation: ./start-dev.sh

echo "🚀 Démarrage du Dashboard Google Ads..."
echo ""

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "backend/app/main.py" ] || [ ! -f "frontend/package.json" ]; then
    echo "❌ Erreur: Lancer ce script depuis la racine du projet"
    exit 1
fi

# Fonction pour gérer l'arrêt propre
cleanup() {
    echo ""
    echo "🛑 Arrêt des serveurs..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Démarrer le backend
echo "📦 Démarrage du backend FastAPI sur http://localhost:8000"
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Attendre que le backend démarre
sleep 3

# Démarrer le frontend
echo "🎨 Démarrage du frontend Angular sur http://localhost:4200"
cd frontend
npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Application démarrée !"
echo ""
echo "📍 URLs:"
echo "   Frontend:  http://localhost:4200"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "📝 Logs:"
echo "   Backend:   tail -f backend.log"
echo "   Frontend:  tail -f frontend.log"
echo ""
echo "🛑 Appuyez sur Ctrl+C pour arrêter"
echo ""

# Garder le script actif
wait
