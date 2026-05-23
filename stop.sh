#!/bin/bash
###############################################################################
# Script d'arrêt complet - Backend + Frontend
# Usage: ./stop.sh [backend|frontend|all]
###############################################################################

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✅${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

log_error() {
    echo -e "${RED}❌${NC} $1"
}

# Fonction pour tuer un processus proprement
kill_gracefully() {
    local pid=$1
    local name=$2

    if [ -z "$pid" ]; then
        return 1
    fi

    # Vérifier que le processus existe
    if ! ps -p "$pid" > /dev/null 2>&1; then
        return 1
    fi

    log_info "Arrêt du processus $pid ($name)..."

    # Tentative d'arrêt gracieux (SIGTERM)
    kill -TERM "$pid" 2>/dev/null || true

    # Attendre jusqu'à 5 secondes
    for i in {1..10}; do
        if ! ps -p "$pid" > /dev/null 2>&1; then
            log_success "Processus arrêté proprement"
            return 0
        fi
        sleep 0.5
    done

    # Si toujours vivant, forcer (SIGKILL)
    log_warning "Le processus ne répond pas, envoi de SIGKILL..."
    kill -9 "$pid" 2>/dev/null || true
    sleep 1

    if ps -p "$pid" > /dev/null 2>&1; then
        log_error "Impossible d'arrêter le processus $pid"
        return 1
    else
        log_success "Processus forcé à s'arrêter"
        return 0
    fi
}

# Fonction pour arrêter le backend
stop_backend() {
    echo ""
    echo "=========================================="
    echo "🛑 Arrêt du Backend (port 8000)"
    echo "=========================================="

    # Méthode 1: Utiliser le script stop.sh du backend
    if [ -f "backend/stop.sh" ]; then
        log_info "Utilisation du script backend/stop.sh..."
        cd backend
        ./stop.sh
        cd ..
        return 0
    fi

    # Méthode 2: Arrêt manuel
    BACKEND_PIDS=$(lsof -ti:8000 2>/dev/null || true)

    if [ -z "$BACKEND_PIDS" ]; then
        log_success "Aucun processus backend trouvé sur le port 8000"
    else
        for PID in $BACKEND_PIDS; do
            PROCESS_NAME=$(ps -p "$PID" -o comm= 2>/dev/null || echo "unknown")
            kill_gracefully "$PID" "$PROCESS_NAME"
        done
    fi

    # Vérification
    sleep 1
    REMAINING=$(lsof -ti:8000 2>/dev/null || true)
    if [ -z "$REMAINING" ]; then
        log_success "Backend arrêté avec succès"
    else
        log_error "Des processus persistent sur le port 8000"
        return 1
    fi
}

# Fonction pour arrêter le frontend
stop_frontend() {
    echo ""
    echo "=========================================="
    echo "🛑 Arrêt du Frontend (port 4201)"
    echo "=========================================="

    # Trouver les processus Angular/Vite/ng sur le port 4201
    FRONTEND_PIDS=$(lsof -ti:4201 2>/dev/null || true)

    if [ -z "$FRONTEND_PIDS" ]; then
        log_success "Aucun processus frontend trouvé sur le port 4201"
    else
        for PID in $FRONTEND_PIDS; do
            PROCESS_NAME=$(ps -p "$PID" -o comm= 2>/dev/null || echo "unknown")
            kill_gracefully "$PID" "$PROCESS_NAME"
        done
    fi

    # Arrêter aussi les processus ng serve qui pourraient être en arrière-plan
    NG_PIDS=$(pgrep -f "ng serve" 2>/dev/null || true)
    if [ -n "$NG_PIDS" ]; then
        log_info "Arrêt des processus 'ng serve' en arrière-plan..."
        for PID in $NG_PIDS; do
            # Vérifier que c'est notre projet
            PROCESS_CMD=$(ps -p "$PID" -o command= 2>/dev/null || echo "")
            if echo "$PROCESS_CMD" | grep -q "googe_ads_perso"; then
                kill_gracefully "$PID" "ng serve"
            fi
        done
    fi

    # Vérification
    sleep 1
    REMAINING=$(lsof -ti:4201 2>/dev/null || true)
    if [ -z "$REMAINING" ]; then
        log_success "Frontend arrêté avec succès"
    else
        log_error "Des processus persistent sur le port 4201"
        return 1
    fi
}

# Fonction principale
main() {
    local target="${1:-all}"

    echo ""
    echo "╔════════════════════════════════════════╗"
    echo "║   🛑 Arrêt des Services - ADS Dashboard   ║"
    echo "╚════════════════════════════════════════╝"
    echo ""

    case "$target" in
        backend)
            stop_backend
            ;;
        frontend)
            stop_frontend
            ;;
        all)
            stop_backend
            stop_frontend
            ;;
        *)
            log_error "Argument invalide: $target"
            echo ""
            echo "Usage: $0 [backend|frontend|all]"
            echo ""
            echo "Options:"
            echo "  backend   - Arrêter uniquement le backend (port 8000)"
            echo "  frontend  - Arrêter uniquement le frontend (port 4201)"
            echo "  all       - Arrêter backend et frontend (défaut)"
            echo ""
            exit 1
            ;;
    esac

    echo ""
    echo "=========================================="
    log_success "Arrêt terminé"
    echo "=========================================="
    echo ""
}

# Exécution
main "$@"
