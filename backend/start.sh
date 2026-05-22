#!/bin/bash
###############################################################################
# Script de démarrage du backend FastAPI
# Usage: ./start.sh [options]
# Options:
#   --dev, -d       Mode développement (reload auto)
#   --prod, -p      Mode production
#   --port PORT     Port personnalisé (défaut: 8000)
#   --daemon        Démarrer en arrière-plan
###############################################################################

set -e

# Configuration par défaut
PORT=8000
MODE="dev"
DAEMON=false
PIDFILE=".uvicorn.pid"
LOGFILE="uvicorn.log"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parser les arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dev|-d)
            MODE="dev"
            shift
            ;;
        --prod|-p)
            MODE="prod"
            shift
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --daemon)
            DAEMON=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --dev, -d       Mode développement (reload auto)"
            echo "  --prod, -p      Mode production"
            echo "  --port PORT     Port personnalisé (défaut: 8000)"
            echo "  --daemon        Démarrer en arrière-plan"
            exit 0
            ;;
        *)
            echo "Option inconnue: $1"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}🚀 Démarrage du backend Google Ads Dashboard${NC}"
echo ""

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "app/main.py" ]; then
    echo -e "${RED}❌ Erreur: Veuillez exécuter ce script depuis le répertoire backend/${NC}"
    exit 1
fi

# Vérifier que le port est libre
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Le port $PORT est déjà utilisé${NC}"
    echo ""
    echo "Processus en cours:"
    lsof -Pi :$PORT -sTCP:LISTEN
    echo ""
    echo -e "Voulez-vous arrêter le processus existant ? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        ./stop.sh
        sleep 1
    else
        echo "Annulé."
        exit 1
    fi
fi

# Vérifier et activer le venv
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Environnement virtuel non trouvé${NC}"
    echo "Création de l'environnement virtuel..."
    python3 -m venv venv
    echo -e "${GREEN}✅ Environnement virtuel créé${NC}"
fi

echo "📦 Activation de l'environnement virtuel..."
source venv/bin/activate

# Vérifier les dépendances
echo "🔍 Vérification des dépendances..."
if ! python -c "import fastapi" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Installation des dépendances...${NC}"
    pip install -q -r requirements.txt
    echo -e "${GREEN}✅ Dépendances installées${NC}"
fi

# Vérifier le fichier .env
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Fichier .env non trouvé${NC}"
    if [ -f ".env.example" ]; then
        echo "Copie de .env.example vers .env..."
        cp .env.example .env
        echo -e "${GREEN}✅ Fichier .env créé${NC}"
        echo -e "${YELLOW}⚠️  N'oubliez pas de configurer vos variables d'environnement !${NC}"
    else
        echo -e "${RED}❌ Fichier .env.example non trouvé${NC}"
        exit 1
    fi
fi

# Afficher la configuration
echo ""
echo "📋 Configuration:"
echo "   - Mode: $MODE"
echo "   - Port: $PORT"
echo "   - Daemon: $DAEMON"
echo ""

# Construire la commande
CMD="uvicorn app.main:app --host 0.0.0.0 --port $PORT"

if [ "$MODE" = "dev" ]; then
    CMD="$CMD --reload"
    echo -e "${BLUE}🔄 Mode développement (auto-reload activé)${NC}"
else
    CMD="$CMD --workers 4"
    echo -e "${GREEN}🏭 Mode production (4 workers)${NC}"
fi

# Démarrer le serveur
echo ""
if [ "$DAEMON" = true ]; then
    echo -e "${BLUE}🌐 Démarrage en arrière-plan...${NC}"

    # Rediriger les logs
    nohup $CMD > "$LOGFILE" 2>&1 &
    PID=$!

    # Sauvegarder le PID
    echo $PID > "$PIDFILE"

    # Attendre que le serveur démarre
    sleep 2

    # Vérifier que le processus est toujours en cours
    if ps -p $PID > /dev/null; then
        echo -e "${GREEN}✅ Backend démarré avec succès (PID: $PID)${NC}"
        echo ""
        echo "📊 Informations:"
        echo "   - URL: http://localhost:$PORT"
        echo "   - Docs: http://localhost:$PORT/docs"
        echo "   - PID: $PID"
        echo "   - Logs: $LOGFILE"
        echo ""
        echo "Pour arrêter: ./stop.sh"
        echo "Pour voir les logs: tail -f $LOGFILE"
    else
        echo -e "${RED}❌ Le serveur a échoué au démarrage${NC}"
        echo "Consultez les logs: cat $LOGFILE"
        rm -f "$PIDFILE"
        exit 1
    fi
else
    echo -e "${BLUE}🌐 Démarrage du serveur...${NC}"
    echo ""
    echo -e "${GREEN}✅ Backend prêt !${NC}"
    echo "   - URL: http://localhost:$PORT"
    echo "   - Docs: http://localhost:$PORT/docs"
    echo ""
    echo -e "${YELLOW}Appuyez sur Ctrl+C pour arrêter${NC}"
    echo ""

    # Démarrer en mode interactif
    $CMD
fi
