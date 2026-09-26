# RideFast BI Analyst Assessment — Full Implementation Plan

> **Revised after exploratory analysis on actual data. All figures are real.**

---

# 1. Assessment Structure (Confirmed)

This is **ONE integrated submission**. Both sections use the same 4 CSVs:

* **Part 1 (Pages 1–3):** Written strategy response — 4 questions about intercity growth failure
* **Part 2 (Pages 4–9):** Tableau dashboard (5 pages) + Python script + written problem statement PDF

### Tools & Data Pipeline

* **Tool chosen:** Tableau Public
* **Data connection:** Python preprocesses CSVs → exports `dashboard_ready.csv` → Tableau loads single file
* **Problems:** Flexible count based on what data supports — not capped at 5

---

# 2. Actual Data Profile (from EDA)

| Dataset               |    Rows | Key Facts                                                      |
| --------------------- | ------: | -------------------------------------------------------------- |
| `rides.csv`           | 120,000 | July 2023 – June 2024 (12 months, not 4 as stated — flag this) |
| `drivers.csv`         |   8,000 | 6,245 active, 1,221 churned, 534 suspended                     |
| `users.csv`           |  35,000 | 79.6% churn rate — the single most alarming number             |
| `support_tickets.csv` |  22,000 | 82.1% resolved; avg 4.6h resolution time                       |

### Overall Ride Metrics

* **Ride status:** 81.4% completed, 9.3% cancelled_driver, 6.8% cancelled_user, 2.5% no_show
* **Promo usage:** 15.6% of rides use promo; avg discount $9.55
* **Total promo spend on completed rides:** $146,405
* **Revenue:** $3.58M gross, $3.44M net (after discounts)
* **Average fare:** $36.70
* **Average distance:** 18.28 km

---

# 3. Hypotheses Validated and Revised

## What the Original Plan Assumed vs. What the Data Shows

### Hypothesis 1: Bottom-Decile Drivers Cause Disproportionate Cancellations

**REVISED.**

* Bottom 10% of drivers account for only **5.3% of driver cancellations** — not concentrated.
* However, **589 active drivers (9.4% of fleet)** with acceptance rate <60% have:

  * Average cancellation rate: **0.422**
  * Average rating: **3.31**
* High-acceptance drivers have:

  * Average cancellation rate: **0.100**
  * Average rating: **4.25**
* This is a real quality cluster, just not a Pareto-style concentration.

### Additional Anomaly

Suspended drivers have nearly identical metrics to active drivers:

| Metric            | Active | Suspended |
| ----------------- | -----: | --------: |
| Cancellation rate |  0.140 |     0.135 |
| Acceptance rate   |  0.801 |     0.808 |
| Rating            |   4.14 |      4.14 |

**Interpretation:** Suspension is not being applied to poor performers based on these available metrics.

---

## Hypothesis 2: High Promo Users Churn Faster

**REVERSED.**

* Q4 (high promo) users churn at **69.3%**
* Q1 (low promo) users churn at **82.8%**
* Promo users are the **most retained cohort**.

Q4 users also have:

* More total rides: **38.58 vs. 18.68**
* Higher wallet balances: **$64 vs. $40**

The original assumption that *“promo creates dependency and churn”* is **FALSE based on the observed data**.

The real question is:

> Are promos causing retention, or are already-engaged users self-selecting more promos?

---

## Hypothesis 3: Support Tickets Predict Churn

**FALSE.**

* Churn rate **with tickets:** 79.2%
* Churn rate **without tickets:** 79.9%
* No meaningful difference across any category.

**Decision:** Drop this as a hypothesis.

---

## Hypothesis 4: Wait Time Drives User Cancellations

**STRONGLY CONFIRMED.**

| Wait Time | Completion Rate | User Cancellation |
| --------- | --------------: | ----------------: |
| 0–5 min   |           86.0% |              6.1% |
| 10–15 min |           73.2% |              8.3% |
| 15–20 min |           54.5% |             11.4% |

The **15-minute threshold is a cliff edge in user behavior.**

---

## New Finding: 79.6% Churn Rate Is the Most Alarming Metric

* **27,867 out of 35,000 users** have not ridden in 60+ days.
* Even the **top 20% of users by ride count have 74% churn**.
* This is platform-wide, not concentrated in low-engagement users.

---

## New Finding: Northgate Is a Systemic Outlier

| Metric                   |          Northgate | Platform |
| ------------------------ | -----------------: | -------: |
| Completion rate          |              76.1% |    81.4% |
| Driver cancellation rate |              13.0% |     9.3% |
| Ticket rate              | 22.8 per 100 rides |      ~18 |

Northgate has compound failures:

* Worse drivers
* Worse operations
* More complaints

---

## New Finding: Monthly Volume Is Completely Flat for 12 Months

* Rides per month: **9,474 to 10,420**
* No upward trend

This confirms the strategic context: **stagnant market share despite all interventions.**

---

# 4. Business Problems

## Problem 1: 79.6% of All Registered Users Are Inactive — The Platform Cannot Retain Anyone

### Problem Statement

RideFast has 35,000 registered users but only 7,133 (20.4%) have ridden in the past 60 days.

The churn rate is uniform across all 12 cities (78.8%–80.7%), all promo quartiles (except Q4 which is lower), and even high-frequency users.

This is **not a targeting problem — it is a platform-wide retention failure.**

### Evidence

* `churn_flag=True` for **27,867 users (79.6%)**
* Top 20% of users by ride count: **74.0% churned**
* Bottom 20%: **82.5% churned**
* City range:

  * Clearwater: **78.8%**
  * Summit Town: **80.7%**
* Monthly ride volume is flat for 12 consecutive months: **9,474–10,420**

### Root Cause Hypothesis

The platform is on a treadmill.

Acquisition brings in new users; most ride once or twice and stop.

Without knowing the first-ride experience quality (wait time, driver behavior, app friction) at user level, the exact trigger is unknown.

However, wait-time data shows that poor first experiences can be highly damaging:

> Wait >15 min → approximately 55% completion.

A user who fails to complete their first ride is likely to churn permanently.

### Data Limitation

`users.csv` has `last_ride_date` but not `first_ride_date` separately from `signup_date`.

Therefore, we cannot directly compute **“rides in first 30 days”** without the rides table join.

We **can** compute this from `rides.csv` — this is a key enrichment in the Python script.

### Recommended Action

1. Compute ride cohort retention by signup month from `rides.csv`.
2. Identify which signup cohort has the highest 30-day retention.
3. Investigate what was happening during that period:

   * Promotions
   * Features
   * Seasonality
4. Implement a **first-ride guarantee**:

   * Maximum 10-minute wait commitment
   * Applies to new users during their first 3 rides
5. If the first ride fails, treat it as a potential churn trigger.

### Success Metric

> 30-day ride retention rate — percentage of new users who complete ≥2 rides in their first 30 days — improves from baseline by **10 percentage points within 90 days** of intervention.

---

# 5. Problem 2: Wait Times Above 15 Minutes Cause Completion to Collapse

## 6.5% of Rides Are Hitting This Threshold

### Problem Statement

When a user waits more than 15 minutes for a driver, completion rate drops from approximately 83% to **54.5%** — a **29-percentage-point collapse**.

This threshold effect is the clearest actionable finding in the dataset.

**7,807 rides (6.5%)** exceeded this threshold.

### Evidence

| Wait Time | Completion Rate | User Cancellation |
| --------- | --------------: | ----------------: |
| 0–5 min   |           86.0% |              6.1% |
| 5–10 min  |           83.8% |              6.3% |
| 10–15 min |           73.2% |              8.3% |
| 15–20 min |           54.5% |             11.4% |

* Rides with wait >15 min: **7,807**
* Percentage of rides with valid wait time: **6.5%**

### Root Cause Hypothesis

The **589 active drivers with acceptance rate <60% (9.4% of fleet)** may be forcing the dispatch system to cycle through multiple drivers before finding one who accepts.

Each failed dispatch attempt adds minutes.

These same drivers also have a **0.422 cancellation rate**, meaning they may cancel after accepting and create a second wait cycle.

### Supporting Evidence

| Driver Group           | Avg Cancellation | Avg Rating |
| ---------------------- | ---------------: | ---------: |
| Low acceptance (<60%)  |            0.422 |       3.31 |
| High acceptance (≥80%) |            0.100 |       4.25 |

Northgate also has:

* Worst completion rate: **76.1%**
* Highest driver cancellation rate: **13.0%**
* Highest proportion of churned drivers: **13.1%**

### Recommended Action

1. **Implement a wait-time alert**

   * If the driver has not moved toward pickup within 8 minutes of acceptance, automatically reassign.

2. **Performance improvement plan**

   * Place the 589 low-acceptance drivers (<60% acceptance) on a 30-day performance improvement plan.
   * Minimum acceptance target: **70%**

3. **Weekly monitoring**

   * Average wait time P50 by city
   * Average wait time P90 by city

### Success Metric

> Rides with wait >15 minutes decrease from **6.5% to <3% within 60 days**.

And:

> Platform completion rate improves from **81.4% to 84%+**.

---

# 6. Problem 3: Northgate Is a City-Level Compound Failure

## Northgate Requires Its Own Intervention Plan

### Problem Statement

Northgate is the only city with meaningfully worse operational metrics than the platform average.

Its:

* **76.1% completion rate**
* **13.0% driver cancellation rate**
* **22.8 support tickets per 100 rides**

represent compound failure across key dimensions.

With approximately 10,000 rides, it is a full-size market underperforming on multiple axes.

### Evidence

| Metric                   |        Northgate |        Platform |
| ------------------------ | ---------------: | --------------: |
| Completion rate          |            76.1% |           81.4% |
| Driver cancellation rate |            13.0% |            9.3% |
| Ticket rate              | 22.8 / 100 rides | ~18 / 100 rides |
| Churned drivers          |            13.1% |               — |
| Revenue                  |         $274,724 |               — |

Northgate has:

* 5 percentage-point gap versus next-worst Clearwater
* Highest driver cancellation rate
* Highest driver churn
* Lowest revenue of all 12 cities
* Revenue share: **7.7% vs. ~8.3–8.5% for others**

### Root Cause Hypothesis

Northgate has a higher driver attrition rate (**13.1% churned**) than the platform average.

The remaining drivers are potentially less experienced, leading to higher cancellation rates.

The worse service experience generates more support tickets.

This can create a self-reinforcing cycle:

```text
Poor service
     ↓
More complaints
     ↓
User churn
     ↓
Lower demand
     ↓
Lower driver earnings
     ↓
Driver churn
     ↓
Worse service
```

### Recommended Action

1. Launch a **Northgate-specific driver acquisition campaign**.

   * Target: 50+ new qualified drivers

2. Run a **Northgate driver quality audit**.

   * Identify drivers with:

     * Cancellation rate >30%
     * Acceptance rate <60%

3. Implement **city-level wait-time SLA monitoring** for Northgate first.

### Success Metrics

Within 90 days:

* Northgate completion rate reaches within **2 percentage points** of the platform average.
* Northgate ticket rate falls below **20 tickets per 100 rides**.

---

# 7. Problem 4: Promo Users Are the Most Retained — But Causality Is Unknown

### Problem Statement

Users in the top promo usage quartile (Q4) churn at **69.3%** versus **82.8%** for the lowest promo quartile.

This is a **13-point difference**.

This suggests promos are associated with better retention and contradicts the assumption that promos create dependency and churn.

However, causal direction is unknown.

The overall churn rate is still **79.6%**, meaning even this relatively better-performing group loses approximately 7 out of 10 users.

### Evidence

| Promo Quartile | Promo Dependency | Churn | Avg Total Rides | Avg Wallet |
| -------------- | ---------------: | ----: | --------------: | ---------: |
| Q1             |             0–2% | 82.8% |           18.68 |     $40.22 |
| Q2             |              ~6% | 83.5% |           34.26 |          — |
| Q3             |             ~14% | 82.8% |           32.26 |          — |
| Q4             |             ~30% | 69.3% |           38.58 |     $64.00 |

Additional facts:

* Total promo spend on completed rides: **$146,405**
* Average promo discount: **$9.55**

### Root Cause Hypothesis

There are two competing explanations:

#### 1. Promos Cause Retention

Discounts reduce the price barrier to re-riding, increasing frequency until habits form.

#### 2. Selection Effect

Users who already ride frequently naturally use more promos because they ride more.

In this case, promos do not cause the frequency — they follow it.

### Key Conclusion

> The current data cannot distinguish these explanations.

An experiment is required.

### Critical Management Question

If promo spend is the mechanism retaining the 30% of non-churned users, cutting promos could risk the existing active user base.

If it is primarily a selection effect, promos may be a sunk cost on users who would ride anyway.

### Recommended Action

Run a **holdout experiment**.

For new users in month X:

* Randomly assign 20% to a reduced-promo group.
* Reduced-promo group receives 1 promo/month instead of the standard 3.
* Measure 90-day retention.

This provides a way to establish causality without changing the experience of the existing user base.

### Success Metric

Within 90 days:

* Determine whether reduced promos increase or decrease 90-day ride frequency.
* Calculate **cost per retained user** for both groups.

---

# 8. Problem 5: Suspended Drivers Show Identical Performance to Active Drivers

## The Quality Governance Process May Not Be Aligned With Performance

### Problem Statement

534 drivers are suspended, but their available performance metrics are nearly identical to those of the active fleet.

Meanwhile, **589 active drivers** with acceptance rates below 60% remain on the platform.

This suggests that the quality enforcement mechanism may not be targeting the drivers identified as underperforming by these operational metrics.

### Evidence

| Driver Group          | Cancellation Rate | Acceptance Rate | Rating |
| --------------------- | ----------------: | --------------: | -----: |
| Suspended             |             0.135 |           0.808 |   4.14 |
| Active                |             0.140 |           0.801 |   4.14 |
| Low-acceptance active |             0.422 |           <0.60 |   3.31 |

The low-acceptance active cohort has:

* Approximately 4× worse cancellation rate
* Approximately 1-point lower rating

### Root Cause Hypothesis

Suspensions may be triggered by administrative or compliance reasons, such as:

* Expired documents
* Background-check failures

rather than performance data.

The performance-based quality floor either does not exist or is not being enforced.

### Recommended Action

1. Audit suspension reason codes, if available in a system not present in the CSV.
2. Implement an automated performance-based deactivation trigger:

   * Rolling 30-day acceptance rate <60%
   * AND cancellation rate >30%
3. Place those drivers into a performance improvement plan.
4. If they fail to improve within 30 days, apply temporary suspension.
5. Keep administrative/compliance suspensions separate from performance suspensions.

### Success Metric

Within 60 days:

* Reduce the 589 low-acceptance driver cohort by at least **40%**, either through improvement or deactivation.
* Increase platform average driver acceptance rate from **80.1% to 85%+**.

---

# 9. Tableau Dashboard Architecture — 5 Pages

## Design Principles

* Each page has a **thesis title** — a finding, not a topic.
* Every chart answers a specific question supporting the thesis.
* Include a **“So what?”** annotation beside key charts.
* Global filters on all pages:

  * City
  * Vehicle Type
  * Date Range / Month
* Color convention:

  * **Teal:** positive / completion
  * **Coral:** cancellation / churn / negative
  * **Grey:** neutral
* Tableau connection: single `dashboard_ready.csv` flat file.

---

# Page 1 — RideFast Has 35,000 Users, But Only 1 in 5 Is Still Active

### Purpose

Executive health check. Opens the story with the most alarming headline metric.

### Chart 1 — KPI Scorecards

Top row:

* Total Registered Users: **35,000**
* Active Users: **7,133 (20.4%)**
* Overall Churn Rate: **79.6%**
* Completion Rate: **81.4%**
* Total Revenue (net): **$3.44M**
* Monthly Rides (most recent month): **~10,000**

### Chart 2 — Monthly Ride Volume Trend

**Line/bar chart**

* X-axis: Month (Jul 2023–Jun 2024)
* Y-axis:

  * Total ride requests — bars
  * Completion rate — line

Shows the flat trend with no growth over 12 months.

**So what?**

> “12 months of strategies produced 0 measurable growth in ride volume.”

### Chart 3 — Churn Rate by City

**Horizontal bar chart**

* X-axis: Churn %
* Y-axis: City
* Sorted descending

All cities fall between **78.8%–80.7%**.

**So what?**

> “This is not a city-specific problem — it is platform-wide.”

### Chart 4 — Ride Volume by City

**Bar chart**

* X-axis: City
* Y-axis: Completed rides
* Northgate highlighted as the volume laggard
* Completion rate shown as a line

---

# Page 2 — When Users Wait More Than 15 Minutes, Over Half of Them Leave

### Purpose

Show the single most actionable operational finding.

### Chart 1 — Wait Time vs. Completion Rate

**Hero Chart — Bar + Line Dual Axis**

* X-axis: Wait time brackets:

  * 0–5
  * 5–10
  * 10–15
  * 15–20
  * 20–30
  * 30+
* Left Y-axis: Ride volume
* Right Y-axis: Completion rate

Completion rate drops sharply at the 15–20 minute bracket.

**So what?**

> “The 15-minute mark is a cliff edge. Below it: 83%+ completion. Above it: 54.5%.”

### Chart 2 — Driver Acceptance Rate Distribution

**Histogram**

* X-axis: Acceptance rate bins
* Y-axis: Driver count
* Highlight left tail (<60%)
* Annotate **589 drivers**

**So what?**

> “9.4% of active drivers (589) accept fewer than 60% of dispatched rides — potentially forcing the system to try multiple drivers before one accepts, adding wait minutes.”

### Chart 3 — Low-Accept vs. High-Accept Driver Comparison

Side-by-side bars:

| Metric                | <60% Acceptance | ≥80% Acceptance |
| --------------------- | --------------: | --------------: |
| Avg cancellation rate |           0.422 |           0.100 |
| Avg rating            |            3.31 |            4.25 |

Visual emphasis on the approximately **4× cancellation gap**.

### Chart 4 — Northgate Deep Dive

KPI cards + comparison bars:

* Northgate completion rate: **76.1% vs. 81.4%**
* Northgate driver cancellation: **13.0% vs. 9.3%**
* Northgate ticket rate: **22.8 vs. 18.0**

**So what?**

> “Northgate is the only city where every operational metric is worse. It is not just an outlier — it is a city in compound failure.”

---

# Page 3 — Promo Users Are Your Most Loyal, But We Don't Know Why

### Purpose

Challenge the assumption that promos are wasteful and surface the strategic dilemma.

### Chart 1 — Churn Rate by Promo Quartile

**Hero Chart — Bar Chart**

* X-axis: Q1 Low → Q4 High promo dependency
* Y-axis: Churn rate %
* Q1: **82.8%**
* Q2: **83.5%**
* Q3: **82.8%**
* Q4: **69.3%**

**So what?**

> “Users who use the most promos churn 13 points less than users who don't. This contradicts the assumption that promos create dependency and churn.”

### Chart 2 — Promo Quartile Profile Table

Rows:

* Q1
* Q2
* Q3
* Q4

Columns:

* User count
* Avg total rides
* Avg promo rides
* Churn %
* Avg wallet balance

Shows that Q4 users are also the highest-frequency riders.

Raises the key question:

> “Are promos causing retention, or are already-active users self-selecting more promos?”

### Chart 3 — Monthly Promo vs. Organic Ride Volume

**Stacked area chart**

* X-axis: Month
* Y-axis: Completed rides
* Stack:

  * Promo realised = True
  * Promo realised = False

Shows whether promo share is growing or holding steady.

If promo rides are growing while organic rides remain flat, this could indicate increasing dependency.

### Chart 4 — Promo Spend Scorecard

* Total promo spend: **$146,405**
* Average promo discount: **$9.55**
* Promo rides as % of completed: **15.6%**
* Cost per promo ride: **~$7.80**

---

# Page 4 — The Quality Control System Is Not Removing Underperforming Drivers

### Purpose

Surface the suspension anomaly and low-acceptance driver problem.

### Chart 1 — Active vs. Suspended Driver Performance

Bar comparison:

| Metric            | Active | Suspended |
| ----------------- | -----: | --------: |
| Cancellation rate |  0.140 |     0.135 |
| Acceptance rate   |  0.801 |     0.808 |
| Avg rating        |   4.14 |      4.14 |

Bars should appear nearly identical.

**So what?**

> “Suspended drivers look exactly like active drivers. The 534 suspensions do not appear to be performance-based.”

### Chart 2 — Driver Cancellation Rate Distribution

**Histogram**

* X-axis: Cancellation rate bins
* Y-axis: Driver count
* Active drivers only
* Highlight right tail: cancellation rate >30%

Shows that the problem is spread rather than concentrated.

### Chart 3 — Driver Quality by City

**Heatmap or grouped bar**

* X-axis: City
* Y-axis: % of active drivers with acceptance <60%

Shows Westville and Clearwater as having the highest proportion of low-quality drivers.

### Chart 4 — Driver Status Breakdown

Donut + table:

* Active: **6,245 (78.1%)**
* Churned: **1,221 (15.3%)**
* Suspended: **534 (6.7%)**

Table should include average metrics for each status group.

---

# Page 5 — City and Vehicle Operations at a Glance

### Purpose

Operational reference page for stakeholder exploration.

### Chart 1 — City Performance Matrix

**Bubble chart / scatter plot**

* X-axis: Completion rate
* Y-axis: Churn rate
* Bubble size: Total ride volume
* Color: Ticket rate per 100 rides

Northgate should appear clearly isolated toward the lower-left.

### Chart 2 — Vehicle Type Performance Table

Rows:

* Economy
* Comfort
* XL

Columns:

* Rides
* Completion rate
* Average fare
* Average rating
* Promo %

The analysis shows near-uniform performance across vehicle types, with XL slightly worse.

### Chart 3 — Support Ticket Breakdown

**Stacked bar chart**

* X-axis: Category
* Y-axis: Ticket count
* Color: Severity

Observations:

* `app_issue` and `driver_behaviour` lead in volume.
* `safety` has the highest proportion of critical tickets.

### Chart 4 — Hourly Ride Volume and Completion Rate

**Bar + line chart**

* X-axis: Hour of day
* Y-axis:

  * Ride volume — bars
  * Completion rate — line

Shows:

* Morning peak: 7–9 AM
* Evening peak: 17–21
* Afternoon trough: 14:00
* Worst completion rate: **80.3%**

---

# 10. Python Script Structure — `analysis.py`

The script is part of the submission checklist. It must be clean, readable, and commented.

## Module 0 — Load & Data Quality Report

* Load all 4 CSVs with explicit dtypes.
* Print:

  * Null counts
  * Data types
  * Date ranges
* Flag:

  * Rides span 12 months, not “4 months” as stated.
  * Document this assumption.
* Flag:

  * `promo_code_used=True` exists on cancelled rides.
  * Treat `promo_discount` as realised only on completed rides.
* Flag:

  * Suspended drivers are not statistically different from active drivers.
  * Document this as a data quality question.
* Verify `churn_flag`:

  * Compute days since last ride for all users.
  * Confirm alignment with `churn_flag=True`.

---

## Module 1 — Rides Feature Engineering

* Parse datetimes.
* Compute:

```python
wait_minutes = (
    pickup_time - request_time
).dt.total_seconds() / 60
```

* Compute:

```python
trip_duration_minutes = (
    dropoff_time - pickup_time
).dt.total_seconds() / 60
```

* Compute `fare_per_km`.
* Engineer:

  * `hour_of_day`
  * `day_of_week`
  * `month`
* Compute `wait_bracket`:

  * 0–5
  * 5–10
  * 10–15
  * 15–20
  * 20–30
  * 30+
* Compute `distance_bucket`.
* Compute:

```python
promo_realised = promo_code_used AND status == 'completed'
```

---

## Module 2 — Driver Enrichment

Classify `driver_quality_tier`:

```text
low_accept    → acceptance_rate < 0.60
low_cancel    → cancellation_rate > 0.30
both_issues   → both conditions
standard      → everything else
```

Compute:

```text
rides_per_online_hour =
    total_rides / (online_hours_monthly * 12)
```

Flag the suspension anomaly in the printed output.

---

## Module 3 — User Enrichment

Compute:

```text
promo_dependency_ratio = promo_rides / total_rides
```

Assign `promo_quartile`:

* Q1
* Q2
* Q3
* Q4

Assign `user_segment`:

* `high_value_active`

  * Top 20% total rides AND `churn_flag=False`
* `high_value_churned`

  * Top 20% total rides AND `churn_flag=True`
* `promo_heavy_active`

  * Q4 promo AND `churn_flag=False`
* `promo_heavy_churned`

  * Q4 promo AND `churn_flag=True`
* `low_engagement`

  * Bottom 20% total rides

Additional calculations:

* Compute `first_ride_date` by joining `rides.csv` on `user_id` and taking minimum `request_time`.
* Compute `user_tenure_days`.
* Compute `revenue_per_user` from completed rides.

---

# 11. Module 4 — Wait Time Analysis

* Compute the full wait-time distribution.
* Group by `wait_bracket`:

  * Completion rate
  * User cancellation rate
  * Driver cancellation rate
* Print the **cliff-edge table**.

This is the hero evidence for Problem 2.

---

# 12. Module 5 — City-Level Aggregation

For each city, calculate:

* Total rides
* Completion rate
* Driver cancellation rate
* User cancellation rate
* Churn rate
* Ticket rate per 100
* Average wait time
* Revenue

Then perform a **Northgate isolation analysis**.

---

# 13. Module 6 — Promo Effectiveness Analysis

Calculate:

* Churn rate by promo quartile
* Monthly promo vs. organic completed rides
* Revenue impact:

  * Gross fare
  * Net revenue after discounts
  * By city

---

# 14. Module 7 — Dashboard Export

* Join all enriched data into a single flat file.
* Export:

```text
output/exports/dashboard_ready.csv
```

* Print row-count reconciliation.

---

# 15. Part 1 — Strategy Write-Up (Pages 1–3 Answers)

## Central Argument

The data exposes a platform with a **retention crisis**, not primarily a demand-generation problem.

**79.6% of registered users are inactive.**

Before investing more in promotional acquisition, RideFast must understand why it cannot retain the users it already has.

---

# Answer 1 — Why Isn't the Current Approach Working Despite Promo Spend?

Monthly ride volume has been completely flat for 12 months:

> **9,474–10,420 rides/month**

Promotions are running:

> **15.6% of rides use promos**

But total volume does not grow.

This is consistent with a treadmill:

* Promos attract new users or re-engage dormant users.
* Completion failures, particularly wait times >15 minutes, reduce completion to **54.5%**.
* Poor experiences push users out at approximately the same rate new users are acquired.
* The result is effectively zero growth.

Additionally, the most retained user cohort — Q4 promo users — is already highly promo-engaged.

The program may be maintaining a core of promo-engaged users while the rest churn.

---

# Answer 2 — Are Current Targeting Methods Effective?

**Partially.**

The RFM-based segmentation succeeds in identifying the most promo-engaged users.

The Q4 cohort has lower churn.

However, targeting does not address the operational friction that causes churn:

* Wait times
* Driver quality
* Completion failures

Therefore:

> **Targeting cannot solve an operations problem.**

The funnel appears to break **after the ride is requested**, rather than before.

---

# Answer 3 — Key Metrics to Monitor

## Tier 1 — Operational / Weekly

* Wait time P50 and P90 by city
* Completion rate broken down by failure type:

  * User cancellation
  * Driver cancellation
  * No-show
* % of rides with wait >15 minutes

  * Target: **<3%**
* Low-acceptance driver count

  * Target: reduce from **589**

## Tier 2 — Retention / Monthly

* 30-day ride retention by signup cohort

  * % of new users completing ≥2 rides in 30 days
* Churn rate by promo quartile
* Revenue per active user

## Tier 3 — Strategic / Quarterly

* Net new active users

  * New activations minus churn
* Market share proxy

  * Monthly ride volume trend

### Metrics to Deprioritize

#### Overall completion rate alone

It hides the wait-time cliff.

#### Gross promo redemption count

It does not measure incremental rides.

#### Raw user registration count

With **79.6% churn**, registrations are a vanity metric.

---

# Answer 4 — How to Evaluate Newly Launched Product Features

Use an **instrumented holdout experiment**.

### Experiment Design

* User-level randomisation rather than city-level.
* **20% holdout group.**
* Pre-declare:

  * 1 primary metric
  * 2 guardrail metrics
* Minimum measurement window: **30 days**

### Segmentation

Decompose results by:

* Promo quartile
* City

A feature improving Q4 users but not Q1 users represents a different finding from one that works uniformly.

### For Booking Experience Features

**Primary metric:**

> Completion rate for rides requested through the new feature.

**Guardrails:**

* Wait time P90
* User cancellation rate

---

# 16. Submission Checklist

Based on Page 8 of the assessment:

* [ ] Tableau Public dashboard URL published and accessible in incognito
* [ ] Python script (`analysis.py`) clean and submitted
* [ ] Dashboard has meaningful KPIs on every page
* [ ] Proper breakdowns with filters:

  * [ ] City
  * [ ] Vehicle Type
  * [ ] Date Range
* [ ] Written problem statement covers 5 problems
* [ ] Each problem includes:

  * [ ] Problem statement
  * [ ] Evidence / specific metric or chart
  * [ ] Root cause hypothesis
  * [ ] Recommended action
  * [ ] Success metric
* [ ] Dashboard link included in problem statement document
* [ ] Submission filename:

```text
{name}_BI Analyst
```

---

# 17. File Structure

```text
E:/pathao/
│
├── csvs/                              # Input, read-only
│
├── output/
│   ├── exports/
│   │   └── dashboard_ready.csv       # Tableau data source
│   │
│   └── analysis/
│       ├── wait_time_analysis.csv
│       ├── driver_quality_clusters.csv
│       ├── user_promo_cohorts.csv
│       ├── city_metrics.csv
│       └── monthly_trends.csv
│
├── analysis.py                        # Submitted with dashboard
├── problem_statement.md               # Content for PDF submission
└── strategy_writeup.md                # Part 1 answers
```

---

# 18. Key Numbers to Reference Throughout Submission

| Metric                              |                               Value |
| ----------------------------------- | ----------------------------------: |
| Overall churn rate                  |                           **79.6%** |
| Active users                        |                 **7,133 of 35,000** |
| Completion rate                     |                           **81.4%** |
| Completion rate at wait >15 min     |                           **54.5%** |
| Rides with wait >15 min             |                    **7,807 (6.5%)** |
| Low-acceptance drivers              |      **589 (9.4% of active fleet)** |
| Low-accept avg cancellation rate    | **0.422 vs. 0.100 for high-accept** |
| Northgate completion                |             **76.1% vs. 81.4% avg** |
| Northgate driver cancellation rate  |              **13.0% vs. 9.3% avg** |
| Northgate ticket rate               |  **22.8 vs. ~18 avg per 100 rides** |
| Q4 promo users churn rate           |              **69.3% vs. Q1 82.8%** |
| Monthly rides                       |                    **9,474–10,420** |
| Promo spend on completed rides      |                        **$146,405** |
| Suspended vs. active driver metrics |      **Nearly identical — anomaly** |
| Support ticket → churn linkage      |         **FALSE (79.2% vs. 79.9%)** |

---

# Final Submission Structure

The complete submission should therefore contain:

```text
1. Strategy Write-Up
   └── Pages 1–3 questions

2. Python Analysis
   └── analysis.py

3. Tableau Public Dashboard
   ├── Page 1 — Executive Health
   ├── Page 2 — Wait Time / Operations
   ├── Page 3 — Promo & Retention
   ├── Page 4 — Driver Quality
   └── Page 5 — City & Vehicle Operations

4. Problem Statement PDF
   └── 5 evidence-based business problems
       ├── Problem
       ├── Evidence
       ├── Root Cause Hypothesis
       ├── Recommended Action
       └── Success Metric
```
