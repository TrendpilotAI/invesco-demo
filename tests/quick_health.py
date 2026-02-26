import requests

services = {
    'DjangoBackend': 'https://django-backend-production-3b94.up.railway.app/api/v1/easy-button/dashboard/',
    'SignalStudioNew': 'https://signal-studio-production-a258.up.railway.app/healthz',
    'EntityExtraction': 'https://entity-extraction-production.up.railway.app/health',
}

for name, url in services.items():
    try:
        r = requests.get(url, timeout=8)
        code = r.status_code
        ok = code // 100 == 2
    except Exception as e:
        code = None
        ok = False
        e_msg = str(e)
    print(f"{name}: status={code} ok={ok}")
    if not ok:
        if 'e_msg' in locals(): print(f"  error: {e_msg}")
