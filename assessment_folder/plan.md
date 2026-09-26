# RideFast BI Analyst Assessment — Full Revised Plan

## Master Prompt Aligned

---

## What Changed From Original Plan

The `new.md` file contains a **Senior BI Analyst + Strategy Consultant Master Prompt** — a 24-part strategic framework.

The original plan treated this as a **"write scripts + build charts"** task. The master prompt makes it a strategic business case with:

* Root-cause chains
* Hypothesis trees
* A **"Where to Win"** framework
* Differentiated, non-generic recommendations

The plan below follows the master prompt's **Part 24 (Final Deliverable)** structure as the serial execution order.

---

# Core Philosophy

The guiding principles are:

* Every other candidate is also using AI — **be different**
* Ask: **"If I were hired as the BI Analyst, where should we invest the next dollar?"**
* Find **3–5 high-quality insights** that materially change a business decision
* Every recommendation must answer:

  * Why this?
  * Why now?
  * Why this segment/city?
  * What if management does nothing?
* Apply the **Banal-Insight Filter**:

  * Is it obvious?
  * Is it actionable?
  * Is it specific?
  * Does the data support it?
  * Can management decide from it?

---

# Serial Step-by-Step Execution Order

## STEP 1 — Assessment Interpretation

### Master Prompt Part 1

**Before touching the data:** Read the PDF as a business case.

Build a **"What They Told Us vs What We Still Need to Prove"** table:

| Assessment Statement      | What It Means                          | What We Still Need to Test                                   |
| ------------------------- | -------------------------------------- | ------------------------------------------------------------ |
| Supply scales with demand | Supply is not the constraint           | Is demand genuinely the bottleneck across all 12 cities?     |
| Prices are competitive    | Price alone doesn't explain low demand | Is perceived value/brand/product experience the issue?       |
| Promotions are high       | Company is spending heavily            | Are promos incremental or subsidizing existing demand?       |
| RFM exists                | Segmentation already in use            | Is it translating into incremental rides?                    |
| 20% market share          | Challenger, not market leader          | Where can this company create advantage without outspending? |

**Output:**
`strategy_writeup.md` → Section 1.1: **Diagnose the Problem**

---

## STEP 2 — Real-World Market Lens

### Master Prompt Part 2

Use external research **only for context and hypothesis generation**.

Research the Bangladesh ride-hailing market, including:

* Pathao
* Uber
* Shohoz
* OBHAI
* inDrive

### Research Topics

* Market structure
* Intercity corridors
* Competitive positioning
* Network effects
* Vehicle categories
* Safety considerations

### Rule

Clearly label everything as:

> **External industry context**

vs.

> **Findings from RideFast dataset**

Never present Bangladesh market data as if it describes RideFast.

**Output:**
Context section in `strategy_writeup.md`

---

## STEP 3 — Write `analysis.py`

### Master Prompt Part 22 — Data Load + Quality

**File:**

```text
E:\pathao\analysis.py
```

### Module 0 — Load & Data Quality

* Load all 4 CSVs with explicit dtypes
* Print null counts, dtypes, and date ranges
* Flag that the data covers **12 months (Jul 2023–Jun 2024)**, not "4 months" as stated in the assessment
* Flag that suspended drivers have nearly identical metrics to active drivers
* Flag that `promo_code_used=True` exists on cancelled rides

  * `promo_realised = completed rides only`
* Verify `churn_flag` aligns with `days_since_last_ride > 60`

---

## STEP 4 — Build Strategic Hypothesis Tree

### Master Prompt Part 3

Before running the full analysis, frame the investigation.

### Why Is Growth Insufficient?

```text
├── A. Awareness — Users don't consider the platform?
│   Evidence: acquisition rate, geographic concentration
│
├── B. Consideration — Users know it but choose alternatives?
│   Evidence: perceived reliability, price/value, availability
│
├── C. Conversion — Users request but don't complete?
│   Evidence: cancellation, no-show, driver acceptance, surge
│
├── D. Retention — Users ride once but don't return?
│   Evidence: churn, ratings, first-ride experience, tickets
│
├── E. Economics — Generating rides inefficiently?
│   Evidence: discounts, revenue per user, promo dependency
│
└── F. Marketplace Density — Too spread out to be excellent anywhere?
    Evidence: rides per driver, acceptance rate, completion by city
```

For each branch, identify which hypotheses can actually be tested with the 4 CSVs.

**Output:**
Hypothesis tree section in `strategy_writeup.md` → feeds Sections **1.1 and 1.3**

---

## STEP 5 — Feature Engineering in `analysis.py`

### Master Prompt Part 22

### Module 1 — Rides

Create:

* `wait_minutes`
* `trip_duration_minutes`
* `fare_per_km`
* `hour_of_day`
* `day_of_week`
* `month`
* `week`
* `wait_bracket`

  * 0–5
  * 5–10
  * 10–15
  * 15–20
  * 20–30
  * 30+
* `promo_realised = promo_code_used AND status == 'completed'`
* `distance_bucket`

### Module 2 — Drivers

Create:

* `driver_quality_tier`

  * `low_accept` < 60%
  * `low_cancel` > 30%
  * `both_issues`
  * `standard`
* `rides_per_online_hour`
* Pareto analysis:

  * Top 10% of drivers → what % of cancellations?
* Print suspension anomaly in output

### Module 3 — Users

Create:

* `promo_dependency_ratio`
* `promo_quartile` (Q1–Q4)
* `user_segment`

  * `high_value_active`
  * `high_value_churned`
  * `promo_heavy`
  * `at_risk`
  * `low_engagement`
* `first_ride_date` via join with `rides.csv`

  * `min(request_time)` per `user_id`
* `user_tenure_days`
* `revenue_per_user`

Also create **behavior-oriented segments beyond RFM**, as described in Master Prompt Part 8.

---

## STEP 6 — Deep Exploratory Analysis

### Master Prompt Parts 5, 9, 10, 11

Run the following analyses in `analysis.py`.

### Module 4 — Wait Time

**Conversion hypothesis**

* Full distribution by wait bracket:

  * Completion rate
  * User cancellation
  * Driver cancellation
* Print the **cliff-edge table** around the 15-minute threshold
* Identify whether the wait-time problem is concentrated in:

  * Specific cities
  * Zones
  * Vehicle types
  * Hours

### Module 5 — City-Level Aggregation

### Where-to-Win Framework

For each of the 12 cities, calculate:

* Demand
* Completion
* Cancellation
* Churn
* Promo dependency
* Driver performance
* Support burden
* Revenue
* User value

Classify cities into archetypes such as:

* High Demand / High Retention
* High Demand / Low Retention
* Low Demand / Strong Operations
* etc.

Only create archetypes where the data supports them.

### Northgate Isolation

Perform a layer-by-layer drill-down of Northgate.

---

### Module 6 — Promotion Intelligence

Map the full promo funnel:

```text
Promo Spend
     ↓
Redemption
     ↓
Completed Ride
     ↓
Repeat Behavior
     ↓
Long-Term Value
```

Identify:

* Which stages can be measured
* Which stages cannot be measured with the available data
* Churn by promo quartile (Q1–Q4)
* Monthly promo vs organic rides
* Whether promo share is growing
* Substitution effect:

  * Are promo users riding more than they would without promos?
  * Or are promos simply subsidizing existing behavior?
* Dormant users who received promos vs those who did not

---

### Module 7 — Customer Experience → Business Outcomes

Analyze:

* Do support-ticket users churn more than non-ticket users?
* Are fare disputes associated with lower ratings?
* Are driver-behavior complaints concentrated in specific cities/drivers?
* Do app issues correlate with churn?
* Can experience issues be connected to business outcomes rather than simply counting tickets?

---

### Module 8 — Driver Marketplace

### Pareto Analysis

Analyze:

* Distribution of cancellation rates
* Top 20% of drivers → what % of completed rides?
* Bottom 20% of drivers → what % of cancellations?
* City × vehicle type × cancellation interactions
* Zone × demand concentration

---

### Module 9 — Time & Geography Patterns

Analyze:

* Hour × completion rate
* Hour × cancellation rate
* Day-of-week patterns
* Peak vs trough performance
* Zone-level demand concentration

---

### Module 10 — Dashboard Export

Join all enriched data and export:

```text
output/exports/dashboard_ready.csv
```

Print row-count reconciliation to verify that no data was unexpectedly lost during joins.

---

# STEP 7 — Build the "Where to Win" Framework

### Master Prompt Part 4

Using the Module 5 outputs, classify all 12 cities.

Do **not** ask:

> "Which city has the most rides?"

Instead ask:

> **"Which market has the strongest combination of demand opportunity, operational feasibility, retention potential, and strategic whitespace?"**

Identify market archetypes **only where the data supports them**.

These findings will feed the strategic recommendations.

---

# STEP 8 — Identify the Top 3–5 Business Problems

### Master Prompt Part 14

For every candidate problem, answer:

1. How large is it?
2. How many users are affected?
3. Is it recurring?
4. Is it strategically important?
5. Can management act on it?
6. Can we measure improvement?
7. How confident are we?

### Root-Cause Chain

Use:

```text
Observed Problem
      ↓
Metric Evidence
      ↓
Where It Happens
      ↓
Who Is Affected
      ↓
Potential Drivers
      ↓
Supporting Evidence
      ↓
Remaining Uncertainty
      ↓
Recommended Test
      ↓
Business Action
```

Separate **symptoms** from **root causes** for every problem.

Label confidence as:

* High
* Medium
* Low

### Likely Candidates

*To be validated against the data*

1. Platform-wide retention failure — 79.6% churn
2. Wait-time cliff at 15 minutes damaging conversion
3. Northgate compound failure
4. Promo program may be subsidizing existing demand rather than creating it
5. Quality governance not targeting underperformers

---

# STEP 9 — Develop Non-Generic Recommendations

### Master Prompt Part 15

Every recommendation must specify:

| Element                      | Question                           |
| ---------------------------- | ---------------------------------- |
| **Target**                   | Who? Specific segment, not "users" |
| **Location**                 | Where? Specific city/zone          |
| **Trigger**                  | When? Specific condition           |
| **Intervention**             | What? Specific action              |
| **Expected Behavior Change** | Why will this work?                |
| **Measurement**              | How will we know?                  |

### Experiment Design

### Master Prompt Part 16

For each recommendation define:

* Hypothesis
* Target population
* Treatment
* Control
* Primary KPI
* Secondary KPI
* Guardrail KPI
* Test duration
* Statistical method
* Decision rule

---

# STEP 10 — "What Could Make Me Wrong?" Review

### Master Prompt Part 22

For every major conclusion, ask:

* Could this be a data artifact?
* Could seasonality explain it?
* Could selection bias explain it?
* Could promotions be correlated with users already likely to ride?
* What additional data would increase confidence?

This section is especially important for interview preparation.

---

# STEP 11 — Build Tableau Dashboard

### Master Prompt Parts 18–19

### Philosophy

The dashboard should be a **narrative, not a collection of charts**.

Each page should tell a story.

## Dashboard Structure

Minimum: **4 pages**

### Page 1 — "Where We Stand"

**Executive health**

Headline:

> **79.6% churn — 4 of every 5 users is gone.**

Include:

* KPI scorecards
* Monthly ride-volume trend
* 12-month flat trend
* Churn uniformity across cities

### Page 2 — "Where Growth Is Breaking"

**Conversion + user behavior**

Include:

* Wait-time cliff — hero chart
* 15-minute threshold
* Driver acceptance distribution
* Where-to-Win city archetypes

### Page 3 — "What Is Happening Inside the Marketplace"

**Driver operations**

Include:

* Active vs suspended driver paradox
* Driver quality tier by city
* Pareto analysis:

  * Is a small driver group causing disproportionate problems?

### Page 4 — "Why Users Are Not Staying"

**Experience + retention root causes**

Include:

* Promo quartile churn
* Q4 churn = 69.3%
* Customer experience → churn connection
* Dormant high-value user pool

### Global Filters

Apply to **all pages**:

* City
* Vehicle Type
* Date Range / Month

### Dashboard Design Rules

* Use insight-led titles
* Avoid generic titles such as `"Rides by City"`
* Add a **"So What?"** annotation to every hero chart

### Publishing

Publish to **Tableau Public**, then:

1. Test in incognito
2. Confirm accessibility
3. Copy the public URL

---

# STEP 12 — Write Problem Statement Document

**File:**

```text
E:\pathao\problem_statement.md
```

Export to PDF.

## Structure Per Problem

Each problem should contain:

* **Problem Statement**
* **Evidence**

  * Specific metrics
  * Chart reference
* **Root Cause Hypothesis**
* **Uncertainty / Confidence Level**
* **Recommendation**

  * Target
  * Location
  * Trigger
  * Intervention
* **Experiment Design**

  * Hypothesis
  * Treatment
  * Control
  * KPIs
* **Success Metric**

At the top of the document:

> **Embed Tableau Public URL**

---

# STEP 13 — Write Part 1 Strategy Write-Up

**File:**

```text
E:\pathao\strategy_writeup.md
```

## Section 1.1 — Diagnose the Problem

Include:

* "What They Told Us vs What We Still Need to Prove" table
* Hypothesis tree results from the data
* Funnel analysis:

  * Where does demand break?

## Section 1.2 — Define Key Metrics

### Tier 1 — Weekly

* Wait P50/P90
* Completion by failure type
* % rides >15 minutes
* Low-acceptance driver count

### Tier 2 — Monthly

* 30-day retention by signup cohort
* Churn by promo quartile
* Revenue per active user

### Tier 3 — Quarterly

* Net new active users
* Volume trend
* Market-share proxy

## Section 1.3 — Analytical Methodologies

Use:

* Cohort retention analysis
* Pareto analysis for driver quality
* Promo incrementality holdout experiment
* City archetype classification / Where-to-Win
* Root-cause chain methodology

## Section 1.4 — Strategic Recommendations

### STOP

* Measuring acquisition before fixing retention
* Treating overall completion rate as the health metric
* Applying promotions uniformly

### START

* First-ride guarantee:

  * Maximum 10-minute wait for new users' first 3 rides
* Performance-based driver deactivation
* Northgate city-specific plan
* Promo holdout experiment to test causality

### CONTINUE

* Q4 promo users

  * Most retained
  * Do not cut until holdout testing establishes causality

### LONG-TERM

Answer:

> **"What can RideFast become unusually good at?"**

Use the **Where-to-Win framework** to answer this.

---

## Management Decision Matrix

### Master Prompt Part 21

| Finding | Business Implication | Recommended Decision | Measurement |
| ------- | -------------------- | -------------------- | ----------- |
|         |                      |                      |             |

---

# STEP 14 — Final Submission Assembly

**Filename:**

```text
{YourName}_BI Analyst
```

## Checklist

* [ ] `analysis.py` — clean, readable, commented, runs without errors
* [ ] `output/exports/dashboard_ready.csv` exists
* [ ] Tableau Public URL published
* [ ] Tableau dashboard accessible in incognito
* [ ] Problem statement PDF

  * Tableau URL at top
  * 3–5 problems
  * All required elements
  * Experiment designs
* [ ] Strategy write-up

  * Sections 1.1–1.4
  * Management decision matrix
* [ ] All files renamed:

```text
{YourName}_BI Analyst
```

---

# STEP 15 — Interview Preparation

### Master Prompt Part 25

Prepare answers to these questions before the interview.

### "How confident are you in this data?"

Key points:

* Data covers 12 months, not 4
* Suspension anomaly suggests governance may not be performance-based
* Promo causality is unknown
* First-ride date is not directly available and must be derived through the rides join

### "If you had 2 people and 1 week, what's the priority?"

Prioritize:

1. Fix the wait-time cliff

   * Operations → completion → retention
2. Design the promo holdout experiment
3. Run the Northgate city-specific work in parallel

### "How would you track if recommendations worked?"

Track:

* 30-day ride retention by signup cohort — weekly
* Wait P90 by city — weekly
* Northgate completion — monthly

### "What would happen if management did nothing?"

Potential scenario to test:

> Promos acquire users → poor first experiences push them out → volume stays flat at ~10K/month → market share remains around 20% while competitors consolidate.

### "Where should the company NOT invest?"

Avoid:

* More acquisition spend before fixing retention economics
* More city expansion before achieving strong performance in fewer markets
* More promo spend before testing incrementality

---

# File Structure

```text
E:\pathao\
│
├── csvs\                              # Input, read-only
│
├── output\
│   ├── exports\
│   │   └── dashboard_ready.csv       # Tableau data source
│   │
│   └── analysis\
│       ├── wait_time_analysis.csv
│       ├── driver_quality_clusters.csv
│       ├── user_promo_cohorts.csv
│       ├── city_metrics.csv
│       └── monthly_trends.csv
│
├── analysis.py                        # Submitted with dashboard
├── problem_statement.md               # Convert to PDF
└── strategy_writeup.md                # Part 1 write-up
```

---

# Critical Numbers

| Metric                         |                                    Value |
| ------------------------------ | ---------------------------------------: |
| Overall churn rate             |                                **79.6%** |
| Active users                   |               **7,133 / 35,000 (20.4%)** |
| Completion rate                |                                **81.4%** |
| Completion at wait >15 min     |                                **54.5%** |
| Rides with wait >15 min        |                         **7,807 (6.5%)** |
| Low-acceptance active drivers  |                  **589 (9.4% of fleet)** |
| Low-accept cancellation rate   |         **0.422 vs 0.100 (high-accept)** |
| Northgate completion           |               **76.1% vs 81.4% average** |
| Q4 promo churn                 |                    **69.3% vs Q1 82.8%** |
| Promo spend — completed rides  |                             **$146,405** |
| Monthly rides — flat 12 months |                         **9,474–10,420** |
| Suspended vs active metrics    |           **Nearly identical — anomaly** |
| Support ticket → churn         | **79.2% vs 79.9% — FALSE; drill deeper** |

---
