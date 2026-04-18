#!/usr/bin/env bash
# Remove AgentOps.app from /Applications. Optionally wipe ~/.agentops/.
set -euo pipefail

rm -rf /Applications/AgentOps.app
echo "Removed /Applications/AgentOps.app"

if [[ "${1:-}" == "--purge" ]]; then
  rm -rf "$HOME/.agentops"
  echo "Removed ~/.agentops"
else
  echo "User config preserved at ~/.agentops (use --purge to remove)"
fi
