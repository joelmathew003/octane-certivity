#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=================================================="
echo "  🚀 Starting Certivity Octane Demo Application"
echo "=================================================="

# Trap Ctrl+C to cleanly kill both processes
cleanup() {
    echo ""
    echo "Stopping Octane services..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    exit 0
}
trap cleanup SIGINT SIGTERM EXIT

# 1. Start Python API Backend (PDF & Requirements Server)
echo "[1/2] Starting Python Backend API on http://localhost:8000..."
.venv/bin/python src/api/server.py &
BACKEND_PID=$!

sleep 1

# 2. Start Frontend UI
echo "[2/2] Starting Frontend UI on http://localhost:8080..."
cd "$DIR/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "=================================================="
echo "  🎉 Octane Demo is live!"
echo "  👉 Open: http://localhost:8080"
echo "  👉 API / PDFs: http://localhost:8000"
echo "  Press Ctrl+C to stop both servers."
echo "=================================================="

wait $FRONTEND_PID
