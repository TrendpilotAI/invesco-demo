#!/bin/bash
# Self-Healing Service Monitor
# Checks all services, outputs JSON status for the healing agent to act on

SERVICES=(
  "signal-studio-new|https://signal-studio-production-a258.up.railway.app|Signal Studio (new)|4538677c-0867-483f-9a00-d046b3167671"
  "signal-studio-old|https://signal-studio-production.up.railway.app|Signal Studio (old)|9644ecb1-98d0-4eca-9b0b-cbfeb68e7e68"
  "django-backend|https://django-backend-production-3b94.up.railway.app/healthz|Django Backend|196ed607-9967-4f69-9ca8-5ab89afe0b3d"
  "signal-builder-api|https://signal-builder-api-production.up.railway.app/docs|Signal Builder API|657117cd-868a-4a93-be43-bfd6826099ec"
  "agent-ops-center|https://agent-ops-center-production.up.railway.app|Agent Ops Center|3a012d0a-d8a4-427c-b7fc-4294c9272d8d"
  "entity-extraction|https://entity-extraction-production.up.railway.app|Entity Extraction|f7d1861d-bd56-46ec-b841-4e28e0569d68"
)

# Known failures to ignore
KNOWN_FAILURES="entity-extraction|signal-studio-old"

FAILURES=""
ALL_STATUS=""

for entry in "${SERVICES[@]}"; do
  IFS='|' read -r id url name service_id <<< "$entry"
  code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 --max-time 15 "$url" 2>/dev/null)
  latency=$(curl -s -o /dev/null -w "%{time_total}" --connect-timeout 10 --max-time 15 "$url" 2>/dev/null)
  
  status="healthy"
  if [[ "$code" != "200" ]]; then
    if [[ "$KNOWN_FAILURES" == *"$id"* ]]; then
      status="known_failure"
    else
      status="FAILED"
      FAILURES="$FAILURES|$id|$name|$code|$service_id|$url"
    fi
  fi
  
  ALL_STATUS="$ALL_STATUS\n$id|$code|$latency|$status|$service_id"
done

echo "=== SERVICE STATUS ==="
echo -e "$ALL_STATUS"
echo ""
echo "=== FAILURES ==="
if [ -z "$FAILURES" ]; then
  echo "NONE"
else
  echo -e "$FAILURES"
fi
