# RideFast BI Analyst Assessment — Master Plan
*Stress-tested via brainstorming + grilling. All decisions locked.*

---

## The Single Question This Submission Answers

> **"RideFast is spending on acquisition. Volume is flat. Why — and where should the next dollar go?"**

The narrative is data-driven — locked after Phase 2 EDA at the **Narrative Checkpoint** (Step 13). Every deliverable answers a sub-question of this. The answer will be one of:
- **Treadmill frame:** Promos acquire users. The product breaks at 15 minutes. Users exit at the same rate.
- **Retention frame:** 79.6% of users are gone. Fix retention before spending more on acquisition.
- **Density frame:** RideFast is spread across 12 cities. Be excellent in fewer markets first.

The data decides which frame leads.

---

## Three-Phase Execution

```
Phase 1 — Understand the Battlefield   Steps 1–4
Phase 2 — Run the Analysis             Steps 5–13  (ends at Narrative Checkpoint)
Phase 3 — Build and Write              Steps 14–18
```

---

## PHASE 1 — UNDERSTAND THE BATTLEFIELD

### Step 1 — Read the Assessment as a Business Case

Build the "What They Told Us vs What We Still Need to Prove" table:

| Assessment Statement | What It Means | What We Still Need to Test |
|---|---|---|
| Supply scales with demand | Supply is not the constraint | Is demand genuinely the bottleneck in all 12 cities? |
| Prices are competitive | Price doesn't explain low demand | Is perceived value / product experience the issue? |
| Promotions are high | Company is spending heavily | Are promos incremental or subsidising existing demand? |
| RFM segmentation exists | Targeting already in use | Is it translating into incremental rides? |
| 20% market share | Challenger, not market leader | Where can RideFast create advantage without outspending? |

**Banal-Insight Filter** — apply to every finding:
1. Is it obvious? Dig deeper.
2. Is it actionable? If no, keep investigating.
3. Is it specific to RideFast? If it applies to every ride-hailing company, it is not differentiated.
4. Does the data support it? If no, label it a hypothesis.
5. Can management make a decision from it? If no, reframe as a business question.

**Output:** Opening section of `strategy_writeup.md`

---

### Step 2 — Real-World Market Lens (External Research Only)

Use Bangladesh ride-hailing context (Pathao, Uber, Shohoz, OBHAI, inDrive) as a **hypothesis generator only**. Never present external findings as RideFast data.

Research topics: market structure, network effects, supply density, intercity corridors, vehicle category demand, competitive positioning, first-mover advantages, brand consideration.

Label all content:
> *External industry context:* [finding]
> *Finding from RideFast dataset:* [finding]

**Central strategic question to carry forward:**
> "Where can RideFast create advantage that does not require simply outspending larger competitors?"

---

### Step 3 — Data Load + Quality Audit
**`analysis.py` — Module 0**

- Load all 4 CSVs with explicit dtypes
- Print: null counts, dtypes, row counts, date ranges
- Required flags (document in script output):
  - Data = 12 months (Jul 2023–Jun 2024), NOT "4 months" as stated in assessment
  - `promo_code_used=True` exists on cancelled rides — `promo_realised` = completed rides only
  - Suspended drivers have nearly identical metrics to active drivers (investigate in Step 9)
  - `rides.csv` has `city` (origin only) and `pickup_zone` — no destination city, no dropoff_zone
  - Verify `churn_flag` alignment: compute `days_since_last_ride`, confirm >60 days = True

---

### Step 4 — Strategic Hypothesis Tree

Before running any analysis, frame the investigation:

```
Why is growth insufficient?
│
├── A. AWARENESS — Users don't consider the platform?
│   Test: acquisition rate vs. city population, geographic concentration
│
├── B. CONSIDERATION — Users know it but choose alternatives?
│   Test: ratings, driver acceptance, vehicle availability by city
│
├── C. CONVERSION — Users request but don't complete?
│   Test: cancellation, no-show, driver acceptance, surge, wait time
│
├── D. RETENTION — Users ride once but don't return?
│   Test: churn_flag, first-ride → churn cohort, support tickets, ratings
│   Sub-hypothesis: First-ride failure → permanent churn (validate in Step 7)
│
├── E. ECONOMICS — Generating rides inefficiently?
│   Test: revenue per user, promo dependency, discount depth, ride frequency
│
└── F. MARKETPLACE DENSITY — Too spread out to be excellent anywhere?
    Test: rides per active driver by city, acceptance rate, completion by city
    Question: "Are we trying to be everywhere instead of being excellent somewhere?"
```

For each branch: note what the 4 CSVs can test and what remains a hypothesis.

**Output:** Hypothesis tree section in `strategy_writeup.md`

---

## PHASE 2 — RUN THE ANALYSIS

### Step 5 — Feature Engineering
**`analysis.py` — Modules 1–3**

**Module 1 — Rides:**
- `wait_minutes` = (pickup_time − request_time) in minutes
- `trip_duration_minutes` = (dropoff_time − pickup_time) in minutes
- `fare_per_km` = fare_amount / distance_km
- `hour_of_day`, `day_of_week`, `month`, `week`
- `wait_bracket`: 0–5, 5–10, 10–15, 15–20, 20–30, 30+
- `promo_realised` = promo_code_used AND status == 'completed'
- `distance_bucket`: short (<5 km), medium (5–20 km), long (>20 km)

**Module 2 — Drivers:**
- `driver_quality_tier`: low_accept (<60%), high_cancel (>30%), both_issues, standard
- `rides_per_online_hour` = total_rides / (online_hours_monthly × 12)
- Pareto: top 20% drivers → % of completions; bottom 20% → % of cancellations
- Print suspension anomaly: suspended vs. active avg metrics side by side

**Module 3 — Users:**
- `promo_dependency_ratio` = promo_rides / total_rides
- `promo_quartile` (Q1–Q4)
- `first_ride_date` = min(request_time) per user_id joined from rides.csv
- `user_tenure_days` = last_ride_date − first_ride_date
- `revenue_per_user` = sum of (fare_amount − promo_discount) for completed rides
- `user_segment`:
  - `high_value_active`: top 20% total_rides AND churn_flag=False
  - `high_value_churned`: top 20% total_rides AND churn_flag=True → **reactivation pool**
  - `promo_heavy_active`: Q4 AND churn_flag=False
  - `at_risk`: last_ride 31–59 days ago
  - `first_ride_churn`: only 1 lifetime ride AND churn_flag=True → **first-ride failure cohort**
  - `low_engagement`: bottom 20% total_rides

---

### Step 6 — Conversion Analysis (Wait Time Cliff)
**Module 4**

- Full distribution by bracket → completion rate, user cancel, driver cancel per bracket
- Print the cliff-edge table (hero evidence for Problem 2)
- Drill down: is the problem concentrated in specific cities / vehicle types / hours?
- Connect: do `low_accept` drivers correlate with longer wait times?
- City × wait time × completion rate interaction

Expected output table:
```
wait_bracket | ride_count | completion_rate | user_cancel | driver_cancel
0–5 min      |            | ~86%            |
5–10 min     |            | ~84%            |
10–15 min    |            | ~73%            |
15–20 min    |            | ~55%            |  ← cliff edge
20–30 min    |            |                 |
30+ min      |            |                 |
```

---

### Step 7 — Retention + First-Ride Failure Hypothesis
**Module 5**

**First-ride failure hypothesis (Problem 5 candidate):**
- For `first_ride_churn` users: what was their wait time on ride 1?
- Compare 30-day retention: first ride wait <10 min vs. first ride wait >15 min
- If materially lower retention after a bad first ride → this becomes Problem 5

**Cohort retention:**
- Group by signup month → % completing ≥2 rides in first 30 days
- Which cohort has the highest 30-day retention? What was different then?

**Dormant high-value user pool (primary reactivation target):**
- Segment: `high_value_churned`
- Count, estimated lifetime value, last-ride-date distribution

---

### Step 8 — Promo Intelligence (Substitution Effect)
**Module 6**

Map what the data can and cannot measure:
```
Promo Spend          → NOT in dataset
Promo Exposure       → NOT in dataset (don't know who was offered promos)
Promo Redemption     → promo_code_used = True  (measurable)
Incremental Request  → CANNOT prove without holdout
Incremental Ride     → promo_realised  (measurable)
Repeat Behavior      → total_rides, churn_flag  (measurable, lagged)
Long-Term Value      → revenue_per_user  (measurable)
```

**Substitution effect:**
- Do Q4 users ride more in promo months vs. non-promo months, or at the same rate?
- Is promo share of completed rides growing over the 12 months?

**Churn by promo quartile** (Q1: ~82.8% → Q4: ~69.3%):
- Label conclusion confidence: **Low** — observational data cannot establish causality
- Two competing explanations: promos cause retention OR engaged users self-select more promos

---

### Step 9 — Driver Marketplace (Pareto Analysis)
**Module 7**

- Distribution of cancellation rates (histogram, not just averages)
- Top 20% drivers → % of all completed rides
- Bottom 20% drivers → % of all cancellations (concentrated or distributed?)
- Quality tier by city: which cities have most `low_accept` drivers?
- Suspension anomaly framing: *589 active drivers with <60% acceptance remain on the platform while 534 suspended drivers have identical performance metrics — suspensions are administrative, not performance-based*
- Online hours: are low-quality drivers also low-hour (supply thin at peak)?

---

### Step 10 — City-Level Analysis + Where-to-Win Framework
**Module 8**

For each of 12 cities compute:
`demand | completion_rate | driver_cancel_rate | churn_rate | promo_dependency | avg_wait_time | ticket_rate_per_100 | revenue | revenue_per_user | driver_quality_score`

Classify each city into archetypes (only where data supports):

| Archetype | Profile | Strategic Implication |
|---|---|---|
| Defend & Deepen | High demand, high retention, strong ops | Protect share, invest in experience |
| Experience Problem | High demand, low retention, poor completion | Fix ops before acquisition |
| Awareness Opportunity | Low demand, strong ops, good retention | Acquisition may work here |
| Fragmentation Risk | Low demand, weak ops | Question continued investment |
| Promo Subsidy Market | High promo dependency, low organic retention | Promos masking weak product-market fit |

**Northgate layer-by-layer drill-down:**
- Layer 1: Completion 76.1% → why?
- Layer 2: Driver cancel 13.0% → which drivers?
- Layer 3: Are `low_accept` drivers over-represented?
- Layer 4: Which vehicle types / zones drive the worst completion?
- Layer 5: Does Northgate have higher wait times (thin supply)?
- Layer 6: Is it a driver recruitment / retention problem?
→ Root cause chain → Recommended Action → Success Metric

---

### Step 11 — Customer Experience → Business Outcomes
**Module 9**

Do NOT treat as a customer service dashboard. Connect to business outcomes:
- Do ticket users churn more than non-ticket users?
- Are `fare_dispute` tickets associated with lower user ratings?
- Are `driver_behaviour` complaints concentrated in specific cities or drivers?
- Do `app_issue` tickets predict churn?
- Which ticket category, in which city, is most correlated with churn?

---

### Step 12 — Time + Geography Patterns
**Module 10**

- Hour of day × completion rate, cancellation rate
- Day of week × demand and completion
- Peak (7–9am, 17–21) vs. trough (14:00) supply/demand balance
- Zone-level demand concentration: are 3 zones generating 50%+ of requests in some cities?
- Interactions: City × vehicle type × cancellation; Promo × hour of day

---

### Step 13 — NARRATIVE CHECKPOINT + Export

**Before writing a single word of the dashboard or documents.**

Checkpoint ritual:
1. Review all outputs from Steps 6–12
2. Write one sentence: *"The single finding that most materially changes a business decision is \_\_\_."*
3. Choose the frame: Treadmill / Retention / Density
4. Rank the 5 problems in order of business impact
5. Confirm Problem 5: does first-ride failure data hold? If weak, keep 4 problems.

Then export:
```python
# Module 11 — join all enriched tables → output/exports/dashboard_ready.csv
# Print row count reconciliation
```

---

## PHASE 3 — BUILD AND WRITE

### Step 14 — Build Tableau Dashboard (4 pages minimum, narrative-led)

**Data source:** `output/exports/dashboard_ready.csv`
**Colors:** Teal = positive/completion · Coral = cancellation/churn/negative · Grey = neutral
**Rule:** Every page title = an insight, not a topic. Every hero chart has a "So what?" annotation.
**Global filters on ALL pages:** City · Vehicle Type · Date Range (Month)

---

**Page 1 — "Where We Stand: 4 of Every 5 Users Is Gone"**
*Decision this page enables: Is this a demand problem or a retention problem?*

- KPI scorecards: Total Users (35K), Active Users (7,133 / 20.4%), Churn Rate (79.6%), Completion Rate (81.4%), Net Revenue ($3.44M), Monthly Rides (~10K)
- Monthly ride volume trend — "So what?: 12 months of strategies produced 0 measurable growth"
- Churn rate by city (all 78.8–80.7%) — "So what?: This is not a city-specific problem. It is platform-wide."
- Ride volume by city (Northgate highlighted in coral)

---

**Page 2 — "Where Growth Is Breaking: The 15-Minute Cliff"**
*Decision: Fix operations before spending more on acquisition.*

- **HERO:** Wait time bracket × completion rate (dual axis) — "So what?: Below 15 min: 83%+ completion. Above it: 55%. One threshold explains the acquisition treadmill."
- **Where-to-Win bubble chart:** X = completion rate, Y = churn rate, bubble size = ride volume, color = ticket rate per 100. Northgate isolated at bottom-left.
- Driver acceptance rate distribution (589 drivers <60% highlighted)
- Low-accept vs. high-accept driver comparison (0.422 vs 0.100 cancellation rate)

---

**Page 3 — "Inside the Marketplace: Quality Governance Is Not Working"**
*Decision: Which drivers go on a performance improvement plan?*

- Active vs. suspended driver performance comparison (nearly identical metrics)
- "So what?: Suspensions are not performance-based. 589 active underperformers remain."
- Driver quality tier by city (heatmap: % of `low_accept` drivers)
- Pareto: top 20% drivers vs. bottom 20% — completed rides and cancellations
- Driver status breakdown donut (Active 78.1% / Churned 15.3% / Suspended 6.7%)

---

**Page 4 — "Why Users Are Not Staying: The Reactivation Opportunity"**
*Decision: Which user segment receives the first reactivation investment?*

- Dormant high-value user pool: count, estimated lifetime value, time since last ride distribution
- "So what?: [X] top-20% users by lifetime rides are now inactive. Highest-ROI reactivation target."
- Churn by promo quartile — "So what?: Promo users churn less. But we cannot prove causality. Don't cut promos until a holdout test answers this."
- At-risk segment (31–59 days inactive): count, cities, ride frequency pattern
- First-ride failure cohort (if validated): % of churned users with only 1 lifetime ride

---

**Publish to Tableau Public → test in incognito → copy URL**

---

### Step 15 — Write Problem Statement Document
**File:** `E:\pathao\problem_statement.md` → export to PDF
**Paste Tableau Public URL at the very top.**

Format for each problem — 7 elements:
1. **Problem Statement** — what is wrong, where, how large (1 precise sentence)
2. **Evidence** — specific numbers + chart reference
3. **Root Cause Hypothesis** — layer-by-layer drill-down
4. **Uncertainty / Confidence** — High / Medium / Low + what would increase it
5. **Recommended Action** — Target / Location / Trigger / Intervention / Why this, not a generic discount
6. **Experiment Design** — Hypothesis / Treatment / Control / Primary KPI / Guardrail / Duration / Decision rule
7. **Success Metric** — specific, measurable, time-bound

---

**Problem 1: 79.6% of Registered Users Are Inactive — Platform-Wide Retention Failure**
- 27,867 / 35,000 users; uniform across all 12 cities (78.8–80.7%); top 20% users: 74% churned
- Monthly volume flat for 12 consecutive months
- Confidence: Medium (churn rate is clear; mechanism requires first-ride cohort analysis)
- Experiment: Reactivation holdout — `high_value_churned` segment, 80/20 split, 30-day window; primary KPI = completed rides at day 30; guardrail = don't over-discount (wallet balance must not drop)

---

**Problem 2: Wait Times Above 15 Minutes Collapse Completion — 6.5% of Rides Cross This Threshold**
- 7,807 rides (6.5%) exceed 15 min; completion drops from 83% to 54.5%
- Root cause: 589 active drivers (<60% acceptance, avg cancellation 0.422) force dispatch to cycle through multiple drivers — each failed attempt adds wait minutes
- Suspension anomaly = forensic evidence: suspended drivers (534) have identical metrics to active drivers (cancel 0.135 vs 0.140, rating 4.14 vs 4.14) — quality governance is not performance-based. This is supporting evidence, not a standalone problem.
- Confidence: High
- Experiment: Performance improvement plan for 589 low-accept drivers; measure wait P90 weekly; Northgate vs. best city as natural comparison

---

**Problem 3: Northgate Is a City-Level Compound Failure**
- Completion 76.1% vs 81.4%; driver cancel 13.0% vs 9.3%; tickets 22.8 vs ~18 per 100 rides; revenue 7.7% share vs 8.3–8.5%
- Root cause: driver attrition (13.1% churned) → less experienced fleet → more cancellations → worse service → complaints → user churn → less demand → drivers earn less → more driver churn (self-reinforcing)
- Confidence: Medium
- Experiment: Targeted driver recruitment (50+ new qualified drivers in Northgate); measure completion rate monthly vs. platform avg

---

**Problem 4: Promo Program May Be Subsidising Existing Demand — Causality Unknown**
- Q4 churn 69.3% vs Q1 82.8%; Q4 users have most rides (38.58 vs 18.68); total promo spend $146,405
- Data cannot distinguish: do promos cause retention, or do already-engaged users self-select more promos?
- What happens if management does nothing: $146,405/year continues with unknown incrementality
- Confidence: Low (correlation clear; causality requires experiment)
- Experiment: Holdout — new users only, 80% standard promo cadence vs. 20% reduced (1/month vs 3); 90-day window; primary KPI = completed rides at day 90; guardrail = churn rate must not increase in holdout group

---

**Problem 5: First-Ride Failure May Be the Primary Churn Trigger** *(validate in EDA — include only if data supports)*
- Hypothesis: users who experience wait >15 min on their first ride exit permanently
- If validated: most commercially important finding — explains the churn *mechanism*, not just the rate; makes intervention specific (fix ride 1, not all rides)
- Confidence: Hypothesis (to be confirmed at Narrative Checkpoint)
- Experiment: First-ride guarantee pilot — new users in 2 cities get max 10-minute wait commitment for first 3 rides; measure 30-day retention vs. control cities

---

### Step 16 — Write Part 1 Strategy Write-up
**File:** `E:\pathao\strategy_writeup.md`

---

**Section 1.1 — Diagnose the Problem**
*Open with the promo question — this is what the assessment explicitly asks first.*

Lead argument:
> "The data shows promotional spend is not the primary failure point. Volume is flat not because promos are targeting the wrong users — it is because the product breaks before retention can form. The 15-minute wait threshold and the platform-wide 79.6% churn rate are the mechanisms. Before increasing acquisition spend, RideFast must fix the reason users do not return."

Structure:
- "What They Told Us vs What We Still Need to Prove" table
- Hypothesis tree results: which branches the data settled, which remain hypotheses
- Funnel diagnosis: where does demand break? (Conversion is the cliff; Retention is the bleeding)
- Observable funnel issues with specific numbers

---

**Section 1.2 — Define Key Metrics**

Tier 1 — Operational (weekly):
- Wait time P50 and P90 by city
- Completion rate by failure type (user cancel / driver cancel / no-show)
- % rides with wait >15 min (target: <3%)
- Low-acceptance driver count (target: reduce from 589)
- First-ride completion rate for new users

Tier 2 — Retention (monthly):
- 30-day ride retention by signup cohort (% completing ≥2 rides in first 30 days)
- Churn rate by promo quartile
- Revenue per active user
- At-risk user count (31–59 days inactive)

Tier 3 — Strategic (quarterly):
- Net new active users (activations minus churned)
- Monthly ride volume trend
- Market share proxy: volume growth vs. estimated market growth

What to deprioritise: Overall completion rate alone; gross promo redemption count; raw user registrations (79.6% churn makes them a vanity metric).

---

**Section 1.3 — Analytical Methodologies**

- Cohort retention analysis: signup month → rides in 30 days
- Pareto analysis: driver quality concentration
- Funnel decomposition: request → acceptance → pickup → completion by city/hour/vehicle
- City archetype classification (Where-to-Win)
- Root-cause chain: Observed Problem → Metric → Where → Who → Drivers → Evidence → Uncertainty → Test → Action
- "What Could Make Me Wrong?" review for each major conclusion:
  - Seasonality? 12-month data helps but does not eliminate
  - City mix? Churn is uniform across cities — no
  - Selection bias in promo finding? Yes — this is why holdout is essential
  - Missing data distortion? No destination city, no first-ride timestamp in users.csv (derived via join)

---

**Section 1.4 — Strategic Recommendations**

**1.4.1 — STOP:**
- Measuring acquisition success by registrations
- Using overall completion rate as the health metric
- Applying promotions uniformly without measuring incrementality
- Expanding into new cities before being excellent in current ones

**1.4.2 — START:**
- First-ride guarantee: max 10-minute wait commitment for new users' first 3 rides (pilot 2 cities)
- Performance-based driver deactivation: rolling 30-day acceptance <60% + cancellation >30% = performance improvement plan; failure → temporary suspension
- Northgate rescue plan: targeted driver recruitment + quality audit of bottom-decile drivers
- Promo holdout experiment before next budget cycle

**1.4.3 — CONTINUE:**
- Q4 promo program: most retained cohort — do not cut until holdout proves causality
- RFM segmentation: partially effective but must be paired with operational fixes

**1.4.4 — Feature Evaluation Framework**

Every newly launched product feature must have a pre-declared measurement protocol before launch.

| Element | Requirement |
|---|---|
| Randomisation unit | User-level only — not city-level (city-level contaminates due to supply effects) |
| Primary KPI | One metric only, pre-declared. Booking features: completion rate. Retention features: 30-day ride frequency. Promo features: incremental completed rides — not redemption rate. |
| Secondary KPIs | Maximum 2. Must be directionally consistent with primary. |
| Guardrail KPIs | Must NOT worsen: wait time P90, user churn rate, driver cancel rate. Breach = halt experiment. |
| Minimum detectable effect | Pre-calculate sample size for 80% power to detect the minimum business-meaningful lift (typically 3pp). Determines test duration — minimum 30 days. |
| Decomposition rule | All results must be cut by: (a) city, (b) promo quartile, (c) vehicle type. A feature that works for Q4 users but not Q1 is a different finding than one that works uniformly. |

Decision rule: adopt only where primary KPI improves AND no guardrail breaches AND effect holds in at least 2 of 3 decomposition cuts.

**1.4.5 — Long-Term Strategic Direction (Where to Win)**

> "What can RideFast become unusually good at?"

Using the city archetype analysis, identify the 3–4 markets with the strongest combination of demand, operational feasibility, and retention potential. Concentrate driver recruitment, quality investment, and product improvements there first. Demonstrate excellence in fewer markets, then expand. The alternative — trying to be present everywhere — is why volume has been flat for 12 months despite significant promotional spending.

**Management Decision Matrix:**

| Finding | Business Implication | Recommended Decision | Measurement |
|---|---|---|---|
| 79.6% churn, uniform across 12 cities | Retention is broken platform-wide | Fix product experience before acquisition | 30-day retention by signup cohort monthly |
| Wait >15 min → 54.5% completion | 589 low-accept drivers are the mechanism | Performance improvement plan for 589 drivers | Wait P90 + % rides >15 min weekly |
| Northgate compound failure | Self-reinforcing cycle: bad drivers → bad service → less demand | City-specific driver acquisition + quality audit | Northgate completion vs. platform avg monthly |
| Promo users churn less (causality unknown) | Cannot cut promos without risking most retained cohort | Holdout experiment before next budget cycle | Incremental rides in holdout vs. control at day 90 |
| First-ride failure cohort (if validated) | One bad first ride → permanent churn | First-ride guarantee pilot in 2 cities | New user 30-day retention: pilot vs. control |

---

### Step 17 — Final Submission Assembly
**Filename:** `{YourName}_BI Analyst`

- [ ] `analysis.py` — runs clean, commented, documents all data flags
- [ ] `output/exports/dashboard_ready.csv` exists, row count reconciled
- [ ] Tableau Public URL published, accessible in incognito
- [ ] `problem_statement.pdf` — Tableau URL at top, 3–5 problems, all 7 elements per problem
- [ ] `strategy_writeup.md` — 4 sections (1.1–1.4) including Management Decision Matrix
- [ ] All files renamed `{YourName}_BI Analyst`
- [ ] Dashboard URL embedded inside the problem statement document

---

### Step 18 — Interview Preparation

**5 questions the panel will probe:**

**"How confident are you in this data?"**
> "The wait-time cliff is high confidence — the threshold effect is unambiguous and consistent across cities. The promo-retention finding is low confidence — correlation is clear but causality requires a holdout. The first-ride failure hypothesis is medium confidence depending on the cohort analysis. I labelled confidence levels explicitly throughout."

**"If you had 2 people and 1 week, what do you prioritise?"**
> "The wait-time problem first — fixing the 589 low-acceptance drivers is an operational change that can begin immediately, costs nothing upfront, and directly improves completion and first-ride experience. Simultaneously, design the promo holdout — that decision needs to be made before the next budget cycle and the experiment design takes a day."

**"What would happen if management does nothing?"**
> "The treadmill continues. Promos bring in users. The product breaks at 15 minutes for 6.5% of rides. Those users exit permanently. Volume stays flat at ~10K/month. The $146,405 promo spend continues with unknown incrementality. Northgate's cycle deepens. Market share stays at 20% while competitors consolidate."

**"Where should the company NOT invest?"**
> "More acquisition spend before fixing retention economics. More city expansion before being excellent in 3–4 markets. More promo spend without first establishing whether it is incremental or substitutive."

**"What would have increased your confidence?"**
> "A `dropoff_zone` column for true origin-destination pairs. A `promo_offered` flag to separate exposure from redemption — critical for incrementality analysis. User-level app event data to identify where in the booking flow abandonment occurs. A `cancellation_reason` field. More than 12 months of data to separate seasonality from trend."

---

## File Structure

```
E:\pathao\
  csvs\                              ← input, read-only
  output\
    exports\
      dashboard_ready.csv            ← Tableau data source
    analysis\
      wait_time_analysis.csv
      driver_quality_clusters.csv
      user_promo_cohorts.csv
      city_metrics.csv
      monthly_trends.csv
  analysis.py                        ← submitted with dashboard
  problem_statement.md               ← convert to PDF for submission
  strategy_writeup.md                ← Part 1 write-up
  assessment_folder\
    plan2.md                         ← this file
```

## Key Numbers

| Metric | Value | Confidence |
|--------|-------|-----------|
| Overall churn rate | 79.6% | High |
| Active users | 7,133 / 35,000 (20.4%) | High |
| Completion rate | 81.4% | High |
| Completion at wait >15 min | 54.5% | High |
| Rides with wait >15 min | 7,807 (6.5%) | High |
| Low-acceptance active drivers | 589 (9.4% of fleet) | High |
| Low-accept cancellation rate | 0.422 vs 0.100 (high-accept) | High |
| Northgate completion | 76.1% vs 81.4% avg | High |
| Q4 promo churn | 69.3% vs Q1 82.8% | High (correlation) / Low (causality) |
| Promo spend on completed rides | $146,405 | High |
| Monthly rides flat 12 months | 9,474–10,420 | High |
| Suspended = active driver metrics | Anomaly confirmed | High — interpretation uncertain |
| First-ride failure → churn | Hypothesis | Validate in EDA at Step 7 |
