#!/bin/bash
# Service health checker — called by cron
# Outputs status for each service, returns non-zero if any are down

SERVICES=(
  "Signal Studio (new)|https://signal-studio-production-a258.up.railway.app"
  "Django Backend|https://django-backend-production-3b94.up.railway.app/healthz"
  "Signal Builder API|https://signal-builder-api-production.up.railway.app/docs"
  "Agent Ops Center|https://agent-ops-center-production.up.railway.app"
  "Signal Studio (old)|https://signal-studio-production.up.railway.app"
  "Entity Extraction|https://entity-extraction-production.up.railway.app"
)

FAILED=0
STATUS=""

for entry in "${SERVICES[@]}"; do
  IFS='|' read -r name url <<< "$entry"
  code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 --max-time 15 "$url" 2>/dev/null)
  if [[ "$code" == "200" ]]; then
    STATUS="$STATUS\n✅ $name ($code)"
  else
    STATUS="$STATUS\n❌ $name ($code)"
    FAILED=$((FAILED + 1))
  fi
done

echo -e "$STATUS"
echo ""
echo "Failed: $FAILED / ${#SERVICES[@]}"
exit $FAILED
