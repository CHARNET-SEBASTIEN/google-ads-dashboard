#!/bin/bash
###############################################################################
# Script de gestion du serveur backend
# Usage: ./server.sh {start|stop|restart|status|logs}
###############################################################################

set -e

PORT=8000
PIDFILE=".uvicorn.pid"
LOGFILE="uvicorn.log"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Fonction pour afficher le statut
status() {
    echo -e "${BLUE}📊 Statut du serveur backend${NC}"
    echo ""

    # Vérifier par le port
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        PID=$(lsof -ti:$PORT)
        PROCESS=$(ps -p $PID -o command= 2>/dev/null || echo "unknown")

        echo -e "${GREEN}✅ Serveur EN COURS${NC}"
        echo "   - PID: $PID"
        echo "   - Port: $PORT"
        echo "   - URL: http://localhost:$PORT"
        echo "   - Docs: http://localhost:$PORT/docs"
        echo ""
        echo "Processus:"
        echo "   $PROCESS"

        # Tester la connexion
        echo ""
        echo "Test de connexion..."
        if curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT/docs | grep -q "200"; then
            echo -e "${GREEN}✅ API répond correctement${NC}"
        else
            echo -e "${YELLOW}⚠️  API ne répond pas (peut-être en train de démarrer)${NC}"
        fi

        return 0
    else
        echo -e "${RED}❌ Serveur ARRÊTÉ${NC}"

        # Vérifier si un PID file existe
        if [ -f "$PIDFILE" ]; then
            echo -e "${YELLOW}⚠️  Fichier PID obsolète trouvé${NC}"
        fi

        return 1
    fi
}

# Fonction pour afficher les logs
logs() {
    if [ ! -f "$LOGFILE" ]; then
        echo -e "${YELLOW}⚠️  Aucun fichier de logs trouvé${NC}"
        echo "Le serveur n'a peut-être pas été démarré en mode daemon."
        return 1
    fi

    echo -e "${BLUE}📄 Logs du serveur (Ctrl+C pour quitter)${NC}"
    echo ""
    tail -f "$LOGFILE"
}

# Fonction principale
case "${1:-}" in
    start)
        echo -e "${BLUE}🚀 Démarrage du serveur...${NC}"
        ./start.sh "${@:2}"
        ;;

    stop)
        echo -e "${BLUE}🛑 Arrêt du serveur...${NC}"
        ./stop.sh
        ;;

    restart)
        echo -e "${BLUE}🔄 Redémarrage du serveur...${NC}"
        ./stop.sh
        sleep 2
        ./start.sh "${@:2}"
        ;;

    status)
        status
        ;;

    logs)
        logs
        ;;

    test)
        echo -e "${BLUE}🧪 Test du serveur...${NC}"
        echo ""

        if ! status > /dev/null 2>&1; then
            echo -e "${RED}❌ Le serveur n'est pas en cours d'exécution${NC}"
            exit 1
        fi

        echo "Test des endpoints principaux:"
        echo ""

        # Test 1: Health check
        echo -n "1. Health check... "
        if curl -s http://localhost:$PORT/docs > /dev/null; then
            echo -e "${GREEN}✓${NC}"
        else
            echo -e "${RED}✗${NC}"
        fi

        # Test 2: Data status
        echo -n "2. Data status... "
        if curl -s http://localhost:$PORT/api/data/status > /dev/null; then
            echo -e "${GREEN}✓${NC}"
        else
            echo -e "${RED}✗${NC}"
        fi

        # Test 3: Diagnostics
        echo -n "3. Diagnostics... "
        if curl -s http://localhost:$PORT/api/diagnostics/rules > /dev/null; then
            echo -e "${GREEN}✓${NC}"
        else
            echo -e "${RED}✗${NC}"
        fi

        # Test 4: AI Analysis (optionnel)
        echo -n "4. AI Analysis... "
        RESPONSE=$(curl -s -w "%{http_code}" -o /dev/null -X POST http://localhost:$PORT/api/diagnostics/ai-analysis)
        if [ "$RESPONSE" = "200" ] || [ "$RESPONSE" = "500" ]; then
            echo -e "${GREEN}✓${NC} (endpoint disponible)"
        else
            echo -e "${YELLOW}⚠${NC} (non configuré ou erreur)"
        fi

        echo ""
        echo -e "${GREEN}✅ Tests terminés${NC}"
        ;;

    *)
        echo "Usage: $0 {start|stop|restart|status|logs|test}"
        echo ""
        echo "Commandes:"
        echo "  start     Démarrer le serveur"
        echo "  stop      Arrêter le serveur"
        echo "  restart   Redémarrer le serveur"
        echo "  status    Afficher le statut"
        echo "  logs      Suivre les logs en temps réel"
        echo "  test      Tester les endpoints"
        echo ""
        echo "Options de start:"
        echo "  --dev, -d       Mode développement (défaut)"
        echo "  --prod, -p      Mode production"
        echo "  --daemon        Démarrer en arrière-plan"
        echo "  --port PORT     Port personnalisé"
        echo ""
        echo "Exemples:"
        echo "  $0 start --daemon    # Démarrer en arrière-plan"
        echo "  $0 start --prod      # Démarrer en mode production"
        echo "  $0 restart --dev     # Redémarrer en mode dev"
        exit 1
        ;;
esac
