# Directory expansion (Oct 15, 2026)
- Data in lists2.py; generator gen2.py (copy of gen.py, only these two sites, base https://<slug>.surge.sh/; privacy text now says Surge instead of GitHub Pages). gen.py/tools.py untouched.
- MoneyToolsDir: 26 listings, 7 categories (tip/split, mortgage, tax & paycheck, budgeting, currency, savings/debt/retirement, general). Live: https://moneytoolsdir.surge.sh/
- AgentPlaybooks: 27 listings, 4 categories (platforms, frameworks/SDKs, coding agents, protocols & guides). Live: https://agentusecasesdir.surge.sh/
- Every listed URL returned HTTP 200 to curl on Oct 15. Dropped because curl got 403/404 (not checked further): Zillow mortgage calc, ADP calculators, SSA calculators, BLS inflation calc, OpenAI agents guide page. NerdWallet, IRS Free File and Copilot Studio URLs swapped for working official URLs.
- I wrote the descriptions myself and didn't check them against each vendor's own wording. Pricing and whether each tool is free is unverified. Several are freemium or paid (YNAB, Monarch, Cursor, Copilot, etc.).
- No payments, domains or GitHub used.

# v3 expansion (Oct 17, 2026)
- New generator /workspace/dirs/v3/gen3.py builds all 3 sites. Data is in v3/data3.py, category intros in v3/intros.py, link checks in v3/urlcheck.json (check.py). Use gen3 from now on; gen.py and gen2.py are retired.
- Listings: ContractorAITools 66 (8 categories), MoneyToolsDir 54 (8), AgentPlaybooks 65 (7). Each category has its own page under /c/, with an intro, what to look for, cards quoting the vendor's own meta description, a comparison table and ItemList JSON-LD.
- Link check, Oct 17: 178 of 185 returned 200. Kept even though curl got bot-blocked (403/429/timeout), because they are well-known live products: Buildertrend, Downtobid, QuickBooks, Gusto, Claude, OpenAI Codex, Lovable. Dropped: Canvas.io (redirects to twindo.com) and Windsurf (redirects to Devin). Renamed SafetyCulture to Mitti (the redirect target). Updated redirected URLs (Monarch, Tiller, StackAI, Pydantic, ADK, Claude Code, Arize Phoenix, Google's Gemini Enterprise Agent Platform, BuildingConnected).
- Sponsor price changed from $299 to $99/month introductory.
- IndexNow key 4c8cfbad0b217a7af8c9ea72a261cef1 is on all 3 sites. Pings returned 202.
