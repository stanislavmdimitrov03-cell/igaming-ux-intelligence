# iGaming Player Behaviour — UX Intelligence Dashboard

> A behavioural analytics project that surfaces actionable UX insights from player session data — framed not as observations, but as product hypotheses with measurable business impact.
>
> **Built in one day.** Data generation, dashboard, wireframes, and automated insight pipeline — conceived and delivered end to end in under 24 hours.

**[→ View Live Dashboard](https://public.tableau.com/app/profile/stanislav.dimitrov/viz/iGamingPlayerBehaviourUXIntelligenceDashboard/Dashboard1?publish=yes)**

---

## What This Project Is

Built in a single day to demonstrate how a UX strategist thinks with data — not just what the numbers show, but what to do about them. Every finding is framed as a UX problem with a root cause, a wireframe fix, and a projected KPI impact.

| Layer | Tool | Purpose |
|-------|------|---------|
| Analyse | Python + Tableau | Surface behavioural patterns across 5,000 players |
| Hypothesise | Figma | Translate findings into wireframe solutions |
| Automate | Make.com + Claude AI | Deliver weekly UX insight recommendations automatically |

---

## The Data

Synthetic dataset modelled on real iGaming behavioural benchmarks — KYC completion rates, mobile/desktop conversion gaps, near-miss mechanics, and responsible gaming patterns. Fully reproducible via `/data/generate_data.py`.

**5,000 players · 38,696 sessions · Full year 2024**

---

## Six Insights, Six UX Hypotheses

### 01 — Player Acquisition Funnel
**Finding:** 35.8% of players abandon at KYC — the biggest drop in the funnel.
**Root Cause:** Mobile KYC is clunky — no progress indicator, no real-time validation, no camera shortcut.
**Impact:** 1,792 players never converted — **€93,184 in unrealised FTD revenue.**
**Hypothesis:** A 3-step mobile-optimised KYC flow with real-time feedback recovers 10+ percentage points.

---

### 02 — Near-Miss Mechanics & The Reward Loop
**Finding:** Sessions with 3+ near-misses show **31% higher next-day return rate** (59% vs 45%).
**Root Cause:** Near-miss events create unresolved tension that pulls players back. Slots generate near-misses at 28% of bets vs 15% in live casino.
**Impact:** This is the core retention mechanic — any UX change reducing near-miss frequency risks directly hitting 30-day retention.
**Hypothesis:** Surfacing near-miss mechanics more deliberately in live casino lifts cross-vertical retention by 8-12%.

---

### 03 — Mobile vs Desktop Conversion Gap
**Finding:** Mobile converts at **38% FTD vs 61% desktop** — a 23-point gap on the highest-traffic device.
**Root Cause:** Too many steps, payment options buried below the fold, no trust signals at the moment of highest commitment anxiety.
**Impact:** Closing half this gap generates approximately **370 additional FTDs — ~€19,000 incremental revenue.**
**Hypothesis:** Single-view deposit screen with quick-select amounts and native wallet as primary CTA closes 10+ percentage points.

---

### 04 — Responsible Gaming Risk by Hour
**Finding:** RG flag rate peaks at **18% between 1-2am**. Evening sessions show under 1% despite generating the highest revenue.
**Root Cause:** RG interventions are either absent or applied uniformly — not targeted at the windows where risk actually concentrates.
**Hypothesis:** Time-aware friction (00:00-09:00 only) reduces early-morning flags by 30-40% with zero impact on evening revenue.

---

### 05 — Reward Loop Decay
**Finding:** The near-miss effect **peaks in week 1 (59%) then decays to baseline by week 5** (~45%).
**Root Cause:** The psychological novelty of near-miss events diminishes over time without a win reinforcing the loop.
**Hypothesis:** Re-engagement trigger at day 21-28 post-FTD improves 30-day retention by 6-9 percentage points.

---

### 06 — Channel Quality: FTD Rate vs LTV
**Finding:** Affiliate drives the highest FTD rate (49%) but **lowest LTV (2.18)**. Organic players generate 20% more lifetime value.
**Root Cause:** Affiliate players arrive with purchase intent but low platform familiarity — they convert fast then churn.
**Hypothesis:** Channel-specific onboarding flows improve affiliate 30-day retention by 12-15 percentage points.

---

## UX Wireframes

Three Figma screens translating the device gap finding into a concrete deposit flow redesign.

| Screen | Change | Targets |
|--------|--------|---------|
| Amount | Quick-select buttons (€10/€25/€50/€100) | Reduces decision friction |
| Payment | Trust signals above fold, native wallet primary | Addresses #1 mobile abandonment reason |
| Confirm | RG message at confirmation step | Targets 1-2am risk without blocking conversion |

**Success metrics:** Mobile FTD rate (primary) · Time-to-deposit (secondary) · 2-week A/B test

---

## Automated UX Insight Pipeline

A Make.com scenario runs every Monday at 08:00 and delivers a prioritised UX recommendation automatically.

```
Google Sheets (live KPIs)
        ↓
Make.com reads latest week's data
        ↓
Claude AI identifies the most urgent UX problem
        ↓
Formatted insight email delivered to product team
```

**Sample output — Week 05:**
> *"Mobile FTD dropped to 34.6% — 4.6pts below baseline. Likely cause: deposit screen friction on mobile. Recommended fix: A/B test one-tap Apple Pay as primary CTA."*

This is the operational layer that keeps the dashboard alive in a real product team. The dashboard shows historical analysis. Make provides the weekly forward-looking signal.

---

## Tools & Stack

| Tool | Purpose |
|------|---------|
| Python (Pandas, NumPy) | Data generation, transformation, aggregation |
| Tableau Public | Interactive dashboard, 6 analytical views + homepage |
| Figma | Low-fidelity UX wireframes |
| Make.com | Automated weekly insight pipeline |
| Claude AI (Anthropic) | Natural language UX recommendation engine |
| Google Sheets | Live KPI tracking layer |

---

## Key Numbers

| Metric | Value |
|--------|-------|
| Players simulated | 5,000 |
| Sessions generated | 38,696 |
| KYC completion rate | 64.2% |
| First deposit rate | 45.7% |
| 30-day retention | 50.3% |
| Mobile FTD rate | 38.0% |
| Desktop FTD rate | 61.0% |
| Revenue opportunity identified | €206,958 |

---

## What I'd Do Next

- Connect Make to a real data source replacing the static Google Sheet
- Add player-level churn prediction using session decay signals at days 18-21
- Build a heatmap overlay showing where mobile users drop within the deposit flow
- Run the A/B test on the mobile deposit wireframe with a real engineering team

---

## Author

**Stanislav Dimitrov**
