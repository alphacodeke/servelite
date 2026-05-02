set -euo pipefail

PORT=8000
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

BOLD="\033[1m"
GREEN="\033[0;32m"
CYAN="\033[0;36m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
RESET="\033[0m"

if ! command -v python3 &>/dev/null; then
  echo -e "${RED}✗ python3 not found. Please install Python 3.6+.${RESET}"
  exit 1
fi

detect_ip() {
  local ip=""

  if command -v hostname &>/dev/null; then
    ip=$(hostname -I 2>/dev/null | awk '{print $1}')
  fi

  if [[ -z "$ip" ]] && command -v ipconfig &>/dev/null; then
    # Windows Git-Bash / WSL fallback
    ip=$(ipconfig 2>/dev/null | awk '/IPv4/{print $NF}' | head -1 | tr -d '\r')
  fi

  if [[ -z "$ip" ]] && command -v ifconfig &>/dev/null; then
    ip=$(ifconfig 2>/dev/null \
      | grep -Eo 'inet (addr:)?([0-9]{1,3}\.){3}[0-9]{1,3}' \
      | grep -v '127\.0\.0\.1' \
      | awk '{print $2}' \
      | sed 's/addr://' \
      | head -1)
  fi

  if [[ -z "$ip" ]]; then
    ip=$(python3 -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
print(s.getsockname()[0])
s.close()
" 2>/dev/null || true)
  fi

  echo "${ip:-127.0.0.1}"
}

LOCAL_IP=$(detect_ip)


mkdir -p "$SCRIPT_DIR/uploads"

echo ""
echo -e "${BOLD}${CYAN}  ╔══════════════════════════════════════╗${RESET}"
echo -e "${BOLD}${CYAN}  ║         ServeLite  ⚡                ║${RESET}"
echo -e "${BOLD}${CYAN}  ║   Instant local file sharing         ║${RESET}"
echo -e "${BOLD}${CYAN}  ╚══════════════════════════════════════╝${RESET}"
echo ""
echo -e "  ${GREEN}✓${RESET} Server running at ${BOLD}http://${LOCAL_IP}:${PORT}${RESET}"
echo -e "  ${YELLOW}→${RESET} Share that URL with other devices on this WiFi"
echo -e "  ${YELLOW}→${RESET} Uploads saved to: ${SCRIPT_DIR}/uploads/"
echo -e "  ${YELLOW}→${RESET} Press ${BOLD}Ctrl+C${RESET} to stop"
echo ""

open_browser() {
  local url="http://localhost:${PORT}"
  # Give server 1 second to bind
  sleep 1
  if command -v xdg-open &>/dev/null; then
    xdg-open "$url" &>/dev/null &
  elif command -v open &>/dev/null; then
    open "$url" &>/dev/null &
  elif command -v start &>/dev/null; then
    start "" "$url" &>/dev/null &
  else
    echo -e "  ${YELLOW}⚠${RESET}  Could not auto-open browser. Visit: ${BOLD}${url}${RESET}"
  fi
}

open_browser &

cd "$SCRIPT_DIR"
exec python3 server.py
