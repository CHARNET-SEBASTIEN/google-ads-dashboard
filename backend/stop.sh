#!/bin/bash
###############################################################################
# Script d'arrêt propre du backend FastAPI
# Usage: ./stop.sh
###############################################################################

set -e

PORT=8000
PIDFILE=".uvicorn.pid"

echo "🛑 Arrêt du serveur backend sur le port $PORT..."

# Fonction pour tuer un processus proprement
kill_gracefully() {
    local pid=$1
    local name=$2

    if [ -z "$pid" ]; then
        return 1
    fi

    # Vérifier que le processus existe
    if ! ps -p "$pid" > /dev/null 2>&1; then
        echo "   ⚠️  Processus $pid déjà arrêté"
        return 1
    fi

    echo "   📍 Processus trouvé: $pid ($name)"

    # Tentative d'arrêt gracieux (SIGTERM)
    echo "   ⏳ Envoi de SIGTERM..."
    kill -TERM "$pid" 2>/dev/null || true

    # Attendre jusqu'à 5 secondes
    for i in {1..10}; do
        if ! ps -p "$pid" > /dev/null 2>&1; then
            echo "   ✅ Processus arrêté proprement"
            return 0
        fi
        sleep 0.5
    done

    # Si toujours vivant, forcer (SIGKILL)
    echo "   ⚠️  Le processus ne répond pas, envoi de SIGKILL..."
    kill -9 "$pid" 2>/dev/null || true
    sleep 1

    if ps -p "$pid" > /dev/null 2>&1; then
        echo "   ❌ Impossible d'arrêter le processus $pid"
        return 1
    else
        echo "   ✅ Processus forcé à s'arrêter"
        return 0
    fi
}

# Méthode 1: Utiliser le fichier PID si disponible
if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    PROCESS_NAME=$(ps -p "$PID" -o comm= 2>/dev/null || echo "unknown")

    if kill_gracefully "$PID" "$PROCESS_NAME"; then
        rm -f "$PIDFILE"
    else
        # Le PID du fichier n'est plus valide
        rm -f "$PIDFILE"
        echo "   🔄 Le fichier PID était obsolète"
    fi
fi

# Méthode 2: Trouver par le port
PIDS=$(lsof -ti:$PORT 2>/dev/null || true)

if [ -z "$PIDS" ]; then
    echo "   ✅ Aucun processus trouvé sur le port $PORT"
else
    for PID in $PIDS; do
        PROCESS_NAME=$(ps -p "$PID" -o comm= 2>/dev/null || echo "unknown")
        kill_gracefully "$PID" "$PROCESS_NAME"
    done
fi

# Méthode 3: Trouver par le nom du processus
UVICORN_PIDS=$(pgrep -f "uvicorn.*app.main:app" 2>/dev/null || true)

if [ -n "$UVICORN_PIDS" ]; then
    echo "   🔍 Processus uvicorn trouvés par nom:"
    for PID in $UVICORN_PIDS; do
        PROCESS_NAME=$(ps -p "$PID" -o command= 2>/dev/null || echo "unknown")

        # Vérifier que c'est bien notre backend
        if echo "$PROCESS_NAME" | grep -q "googe_ads_perso/backend"; then
            kill_gracefully "$PID" "uvicorn"
        fi
    done
fi

# Vérification finale
sleep 1
REMAINING=$(lsof -ti:$PORT 2>/dev/null || true)

if [ -z "$REMAINING" ]; then
    echo ""
    echo "✅ Backend arrêté avec succès"
    exit 0
else
    echo ""
    echo "⚠️  Des processus persistent sur le port $PORT:"
    lsof -i:$PORT
    echo ""
    echo "Pour forcer l'arrêt, exécutez:"
    echo "  lsof -ti:$PORT | xargs kill -9"
    exit 1
fi
