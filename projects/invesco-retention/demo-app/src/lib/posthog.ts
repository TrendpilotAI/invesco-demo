/**
 * PostHog Analytics — INV-005
 * Tracks page views + key demo button clicks for Nathan/Megan to monitor Brian's session.
 * Replace phc_demo_invesco with the real project key before production.
 */

export const POSTHOG_KEY = 'phc_demo_invesco';
export const POSTHOG_HOST = 'https://us.i.posthog.com';

/** Key demo interactions to track */
export const DEMO_EVENTS = {
  VIEW_MEETING_BRIEF: 'clicked_view_meeting_brief',
  RUN_SIGNAL: 'clicked_run_signal',
  PUSH_TO_SALESFORCE: 'clicked_push_to_salesforce',
  RESET_DEMO: 'clicked_reset_demo',
  // App launcher
  MEETING_BRIEF_APP: 'clicked_meeting_brief_app',
  SIGNAL_STUDIO_APP: 'clicked_signal_studio_app',
  TERRITORY_DASHBOARD_APP: 'clicked_territory_dashboard_app',
  MOBILE_BRIEF_APP: 'clicked_mobile_brief_app',
} as const;

/** Safely capture a PostHog event (no-op if PostHog isn't loaded) */
export function capture(event: string, props?: Record<string, unknown>) {
  if (typeof window !== 'undefined' && (window as any).posthog?.capture) {
    (window as any).posthog.capture(event, {
      ...props,
      path: window.location.pathname,
    });
  }
}
