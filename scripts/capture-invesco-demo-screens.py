#!/usr/bin/env python3
"""
Capture real screenshots from the live Signal Studio Easy Button app.
Uses embed mode + localStorage token injection to bypass auth.
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

APP_URL = "https://signal-studio-production-a258.up.railway.app"
OUTPUT_DIR = Path("/data/workspace/invesco-demo/public/captures")

async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # Desktop viewport — Salesforce Lightning size
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=2,
        )
        page = await context.new_page()
        
        # Set a fake JWT token in localStorage before navigating
        # This lets the app load with mock data instead of redirecting to login
        await page.goto(APP_URL + "/login", wait_until="domcontentloaded", timeout=15000)
        await page.evaluate("""() => {
            localStorage.setItem('token', 'demo-token-for-screenshots');
            localStorage.setItem('user', JSON.stringify({
                email: 'demo@forwardlane.com',
                name: 'Jordan Mitchell',
                role: 'Wholesaler'
            }));
        }""")
        
        # Now navigate to easy-button with embed=true
        print("📸 Loading Signal Studio Easy Button (embed mode)...")
        await page.goto(APP_URL + "/easy-button?embed=true", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(4000)  # Let animations + mock data settle
        
        # Check if we're on the right page
        title = await page.title()
        print(f"   Page title: {title}")
        
        # Check if we got redirected to login
        url = page.url
        print(f"   Current URL: {url}")
        
        if "login" in url:
            print("   ⚠️ Redirected to login — trying direct easy-button without embed...")
            await page.goto(APP_URL + "/easy-button", wait_until="networkidle", timeout=30000)
            await page.wait_for_timeout(4000)
            url = page.url
            print(f"   URL now: {url}")
        
        # Take screenshot regardless
        print("📸 1/8 — Dashboard overview")
        await page.screenshot(path=str(OUTPUT_DIR / "01-dashboard-full.png"), full_page=False)
        
        # Get page content for debugging
        visible_text = await page.evaluate("() => document.body.innerText.substring(0, 500)")
        print(f"   Visible text: {visible_text[:200]}...")
        
        # Try to find interactive elements
        print("📸 2/8 — Looking for UI elements...")
        all_buttons = await page.query_selector_all('button')
        for b in all_buttons[:10]:
            txt = await b.inner_text()
            if txt.strip():
                print(f"   Button: '{txt.strip()}'")
        
        # Find any tables
        tables = await page.query_selector_all('table, .ant-table')
        print(f"   Tables found: {len(tables)}")
        
        # Find any cards
        cards = await page.query_selector_all('.ant-card, [class*="card"]')
        print(f"   Cards found: {len(cards)}")
        
        # Find any stats/numbers
        stats = await page.query_selector_all('.ant-statistic, [class*="statistic"], [class*="stat"]')
        print(f"   Stats found: {len(stats)}")
        
        # Try segmented controls / tabs
        segments = await page.query_selector_all('.ant-segmented-item, .ant-tabs-tab')
        print(f"   Segments/tabs: {len(segments)}")
        
        # Screenshot the current state at different scroll positions
        print("📸 3/8 — Scrolled view")
        await page.evaluate("window.scrollTo(0, 400)")
        await page.wait_for_timeout(500)
        await page.screenshot(path=str(OUTPUT_DIR / "02-scrolled.png"), full_page=False)
        
        print("📸 4/8 — Full page")
        await page.screenshot(path=str(OUTPUT_DIR / "03-full-page.png"), full_page=True)
        
        # Try interacting with first clickable row
        rows = await page.query_selector_all('tr.ant-table-row, [data-row-key], .ant-list-item')
        if rows:
            print(f"📸 5/8 — Clicking first row of {len(rows)} rows")
            await rows[0].click()
            await page.wait_for_timeout(2000)
            await page.screenshot(path=str(OUTPUT_DIR / "04-row-clicked.png"), full_page=False)
        else:
            print("📸 5/8 — No rows found, capturing current state")
            await page.screenshot(path=str(OUTPUT_DIR / "04-current-state.png"), full_page=False)
        
        # Try to find and click meeting prep
        prep_buttons = await page.query_selector_all('button')
        for btn in prep_buttons:
            text = (await btn.inner_text()).strip().lower()
            if any(kw in text for kw in ['prep', 'meeting', 'brief', 'generate']):
                print(f"📸 6/8 — Clicking '{text}'")
                await btn.click()
                await page.wait_for_timeout(3000)
                await page.screenshot(path=str(OUTPUT_DIR / "05-meeting-prep.png"), full_page=False)
                # Close modal
                close = await page.query_selector('.ant-modal-close, .ant-drawer-close, [aria-label="Close"]')
                if close:
                    await close.click()
                    await page.wait_for_timeout(500)
                break
        
        # Try the search/NL query
        search_inputs = await page.query_selector_all('input, textarea, .ant-input')
        for inp in search_inputs:
            placeholder = await inp.get_attribute('placeholder') or ''
            if any(kw in placeholder.lower() for kw in ['search', 'ask', 'query', 'question', 'natural']):
                print(f"📸 7/8 — Found search: '{placeholder}'")
                await inp.click()
                await inp.fill("Show me rising stars with TTM increase over $1M")
                await page.wait_for_timeout(1000)
                await page.screenshot(path=str(OUTPUT_DIR / "06-nl-query.png"), full_page=False)
                # Try pressing Enter
                await inp.press("Enter")
                await page.wait_for_timeout(3000)
                await page.screenshot(path=str(OUTPUT_DIR / "07-nl-results.png"), full_page=False)
                break
        
        # Mobile capture
        print("📱 8/8 — Mobile view")
        mobile = await browser.new_context(
            viewport={"width": 428, "height": 926},
            device_scale_factor=3,
            is_mobile=True,
        )
        mp = await mobile.new_page()
        await mp.goto(APP_URL + "/login", wait_until="domcontentloaded", timeout=15000)
        await mp.evaluate("""() => {
            localStorage.setItem('token', 'demo-token-for-screenshots');
        }""")
        await mp.goto(APP_URL + "/easy-button?embed=true", wait_until="networkidle", timeout=30000)
        await mp.wait_for_timeout(4000)
        await mp.screenshot(path=str(OUTPUT_DIR / "08-mobile.png"), full_page=False)
        await mp.screenshot(path=str(OUTPUT_DIR / "09-mobile-full.png"), full_page=True)
        
        await browser.close()
    
    print(f"\n✅ Captures saved to {OUTPUT_DIR}")
    for f in sorted(OUTPUT_DIR.glob("*.png")):
        size_mb = f.stat().st_size / 1024 / 1024
        print(f"   {f.name} ({size_mb:.1f} MB)")

if __name__ == "__main__":
    asyncio.run(main())
