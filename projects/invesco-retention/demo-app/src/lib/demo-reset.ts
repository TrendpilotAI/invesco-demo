export const DEMO_RESET_KEYS = [
  'push-to-sf-state',
  'signal-query',
  'signal-results',
  'selected-advisor',
  'territory-filter',
  'demo-interactions',
  'meeting-prep-advisor',
  'meeting-prep-result',
  'nl-query-history',
  'dashboard-filters',
  'signal-templates-selected',
  'demo-persona',
  'posthog-distinct-id',
];

/** Clear all demo localStorage keys */
function clearLocalStorage() {
  DEMO_RESET_KEYS.forEach(key => localStorage.removeItem(key));
  // Also clear any keys with demo- prefix added dynamically
  Object.keys(localStorage)
    .filter(k => k.startsWith('demo-') || k.startsWith('invesco-'))
    .forEach(k => localStorage.removeItem(k));
}

/** Clear all cookies for current domain */
function clearCookies() {
  document.cookie.split(';').forEach(c => {
    const eqPos = c.indexOf('=');
    const name = eqPos > -1 ? c.substring(0, eqPos).trim() : c.trim();
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/`;
  });
}

/** Full demo state reset — clears localStorage, sessionStorage, cookies, then navigates to root */
export function resetDemo(options: { navigateTo?: string; skipReload?: boolean } = {}) {
  clearLocalStorage();
  sessionStorage.clear();
  clearCookies();

  if (!options.skipReload) {
    const target = options.navigateTo ?? '/';
    window.location.href = target;
  }
}

/** Check ?reset=true URL param on mount and trigger reset if present */
export function checkResetParam() {
  if (typeof window === 'undefined') return;
  const params = new URLSearchParams(window.location.search);
  if (params.get('reset') === 'true') {
    resetDemo({ navigateTo: '/' });
  }
}

/** Returns true if running in a demo/presentation context */
export function isDemoMode(): boolean {
  if (typeof window === 'undefined') return false;
  const params = new URLSearchParams(window.location.search);
  return (
    params.has('demo') ||
    params.has('persona') ||
    localStorage.getItem('demo-persona') !== null
  );
}
