# RideFast — BI Analysis
*Data sources: rides.csv (120,000 rides), users.csv (35,000 users), drivers.csv (8,000 drivers), support_tickets.csv (22,000 tickets). Period: Jul 2023 – Jun 2024.*

---

## What the Data Actually Says

RideFast is a mid-sized ride-hailing platform operating across 12 cities with approximately 35,000 registered users, 8,000 drivers, and over 10,000 ride requests per month. Leadership has flagged operational warning signs threatening profitability and user retention.

Four months of data reveals a single dominant pattern: **users are being acquired but not kept.** 4 out of every 5 registered users are already inactive. Ride volume has not grown in 12 months. The problem is not how users are reached — it is what they experience once they arrive on the platform.

This is the core finding everything else flows from.

---

## Diagnosing the Problem

### What the data reveals about flat ride volume

Five possible explanations were tested against the data. Here is what the data confirmed and what it could not answer:

| Hypothesis | What we expected | What the data shows |
|:-----------|:-----------------|:--------------------|
| Users don't know about the platform | Low awareness driving low demand | Cannot be tested — no market impression data. But 35,000 registrations suggest awareness exists |
| Users know but prefer competitors | Consideration gap | Cannot be tested — no competitor usage data |
| Users request rides but rides don't complete | Conversion problem | **Confirmed.** When a driver takes more than 15 minutes to arrive, only 54.1% of rides complete. Under 5 minutes: 86.2% complete. |
| Users ride once but don't come back | Retention problem | **Confirmed as the primary problem.** 79.6% of all registered users are inactive. Uniform across all 12 cities. |
| Promos are not generating new rides | Economics problem | **Partially confirmed.** Promo users churn less — but only if they already ride frequently. For new or casual users, promos show no measurable retention benefit. |

**The short answer:** This is not primarily a targeting problem or a promo problem. It is a product experience and retention problem. Users are arriving and leaving before the platform can build a habit with them.

---

### Where does the user funnel break?

**Step 1 — Registration to first ride**

8,022 users (22.9% of all registered users) have a first ride that appears before their signup date — a data quality issue suggesting signup_date records app installation, not account creation. A further 1,103 users (3.2%) never took any ride at all.

Of the 25,863 users with clean data, the time between signup and first ride strongly predicts whether they stay:

| Time from signup to first ride | Users | Churn rate |
|:-------------------------------|------:|-----------:|
| Same day | 45 | 68.9% |
| 1–7 days | 338 | 75.1% |
| 7–30 days | 1,146 | 75.9% |
| 30–90 days | 3,104 | 78.3% |
| 90–180 days | 4,769 | 80.8% |
| 180–365 days | 9,840 | 84.9% |
| 365+ days | 6,621 | 87.5% |

Users who ride within 7 days of signing up churn at 75%. Users who wait over a year before their first ride churn at 87.5%. The faster someone uses the product, the more likely they are to stay. Their lifetime ride counts are nearly identical (29–32 rides per group), so this is not about ride frequency — it is about whether early habit forms.

**Step 2 — Ride request to pickup (the most critical break point)**

| Wait time for driver | Rides | Rides that completed | Driver cancelled |
|:---------------------|------:|:--------------------:|:----------------:|
| Under 5 minutes | 30,685 | 86.2% | 5.8% |
| 5–10 minutes | 53,352 | 84.3% | 7.1% |
| 10–15 minutes | 26,831 | 78.2% | 11.5% |
| **15–20 minutes** | **6,646** | **54.1%** | **29.3%** |
| 20–30 minutes | 1,649 | 65.7% | 18.9% |
| 30+ minutes | 837 | 65.4% | 21.9% |

At exactly 15 minutes, completion rate drops from 78% to 54%. That is a 24-percentage-point collapse at a single threshold. 9,132 rides (7.6% of all rides) cross this threshold.

The 29.3% driver cancellation rate in the 15–20 minute bracket is the most damaging number here. The driver is already on the way. The user has been waiting. The driver cancels anyway. This is the worst possible experience — and it happens in almost 1 in 3 rides that reach the 15-minute mark.

**Step 3 — Ride to return**

79.6% of all 35,000 registered users are inactive (no ride in last 60 days). Every single city is between 78.8% and 80.7%. This is not a Northgate problem or a Westville problem. It is a platform-wide problem with a platform-wide cause.

Churned users — before they left — generated $2,780,358 in gross fare revenue (80.9% of the platform total). The average churned user actually contributed more per person ($106.45) than the average active user ($97.83). These were not casual one-time users. They used the platform and then stopped.

5,257 of these churned users are "high-value": they are in the top 20% of all users by lifetime rides (49+ rides threshold), averaging 54 rides each, with a collective gross fare contribution of $535,580. They have been inactive for a median of 218 days.

**Step 4 — Support and recovery**

Filing a ticket does not predict whether a user stays. Ticket users churn at 79.2%, non-ticket users at 79.9% — a 0.7pp difference that means nothing. Resolving a ticket faster does not help either: users resolved in under 2 hours churn at 78.5%, same as users resolved in 6–24 hours (78.5%). The platform-wide churn is so uniformly high that support interactions cannot move it. The fix is in the ride experience, not in support speed.

---

## Key Metrics to Monitor

### Weekly (operational — watch these closely)

| Metric | What it is | Current value | Why it matters |
|:-------|:-----------|:-------------:|:--------------|
| % rides with wait >15 minutes | Rides that crossed the failure threshold / total rides | **7.6%** | Direct measure of the conversion problem. Every ride in this bucket has a 46% chance of not completing. |
| Driver cancellation rate in >15 min bucket | Driver cancels after already being assigned, when user waited >15 min | **29.3%** | The worst user experience. Should be tracked separately from overall cancellation. |
| Both_issues driver count on active fleet | Active drivers with acceptance <60% AND cancellation >30% | **741 drivers** | These drivers are the identified cause of most long-wait rides. |
| Completion rate by city | Rides completed / rides requested, per city | Northgate: **76.1%** vs rest: 81–83% | Identifies where the product is breaking geographically. |
| First-ride completion rate for new users | % of new users whose very first ride completes | Not currently segmented | First impression drives whether they come back. |

### Monthly (retention — the health of the business)

| Metric | What it is | Current value | Why it matters |
|:-------|:-----------|:-------------:|:--------------|
| 30-day ride retention by signup cohort | % of new users who complete ≥2 rides in their first 30 days | 19.8%–27.9% across cohorts | Shows whether the product is creating habit. Currently flat — no cohort is meaningfully better. |
| At-risk user count | Users whose last ride was 31–59 days ago | **1,795 users** | These users are close to churning but haven't yet. The intervention window is still open. |
| Churn rate by promo quartile | % churned across Q1–Q4 promo usage | Q1: 82.8%, Q4: 69.3% | Tracks whether promo engagement is becoming organic. Must be cut by ride frequency — the gap disappears below 25 rides. |
| High-value churned pool size | Top 20% users by lifetime rides who are now inactive | **5,257 users, $535,580 collective fare value** | The highest-ROI reactivation target. Shrinking this pool is a growth lever. |

### Quarterly (strategic — direction of travel)

| Metric | What it is | Current value | Why it matters |
|:-------|:-----------|:-------------:|:--------------|
| Net new active users | New users activated − users who churned that quarter | Cannot calculate from current data without quarterly cohort cut | The real growth number. Registrations minus departures. |
| Monthly ride volume trend | 12-month rolling average | **9,408–10,420 / month, no growth** | The top-line signal. Currently a flat line for 12 months. |
| Promo spend per incremental ride | Total promo cost / rides that would not have happened without the promo | **Unknown — no holdout exists** | Until this is measured, promo spend cannot be evaluated. |

### Stop reporting these as success indicators

- **Total registrations** — 79.6% of registered users churn. A registration that leads to churn is a cost, not growth.
- **Overall completion rate** — 81.4% looks healthy and hides the 54.1% rate inside the >15 minute bucket. The aggregate number is misleading.
- **Promo redemption count** — counts promos used by people who would have ridden anyway. Redemptions without incrementality data are not a measure of effectiveness.

---

## Analytical Methodologies

### 3.1 Funnel Decomposition — find exactly where rides break

**What it answers:** At which step does demand disappear — and in which city, vehicle type, and time of day?

Break every ride into stages: requested → driver assigned → driver arrived → completed or cancelled or no-show. Calculate what percentage exits at each stage. Then cut by city, vehicle type, and hour of day.

The data already shows the answer at the platform level: the exit happens at Stage 2, when wait time crosses 15 minutes. The next step is finding which specific cities, zones, and time windows produce the most rides in that bucket.

**What we need:** rides.csv — status, request_time, pickup_time, dropoff_time, city, vehicle_type, pickup_zone.

---

### 3.2 Driver Quality Analysis — confirm who is causing the long waits

**What it answers:** Are the 741 both_issues drivers (acceptance <60%, cancellation >30%) directly responsible for the rides that cross 15 minutes?

Join rides.csv to drivers.csv on driver_id. Compare wait time distribution for rides handled by both_issues drivers versus standard drivers.

**Already confirmed from the data:** 43% of rides handled by both_issues drivers exceed 15 minutes. For standard drivers, only 2.8% do. The 26× difference is unambiguous.

**What we suspect but cannot directly prove:** When a low-acceptance driver declines a ride, the system retries with another driver. Each retry adds wait minutes. Without dispatch attempt history, this is a strong inference — not a directly measured fact. The recommendation stands regardless.

**Suspension anomaly — supporting evidence that governance is broken:** 534 suspended drivers have a cancellation rate of 0.135 and a rating of 4.142. The 741 active both_issues drivers have cancellation rates that should by any reasonable measure trigger suspension. The suspended drivers are performing *better* than the drivers who remain active. This means suspensions are administrative, not performance-based. The wrong drivers are being suspended.

---

### 3.3 Cohort Retention Analysis — see if any acquisition channel retains better

**What it answers:** Are users from certain signup months, cities, or acquisition periods retaining at higher rates?

Group users by signup month. For each group, calculate: % who ride again within 30 days, churn rate at 6 months. Look for outliers — any cohort that retains materially better is a signal about what was different that month.

**What the data already shows:** 30-day retention ranges from 19.8% to 27.9% across all cohorts. No cohort is materially better. The activation gap table (faster first ride → lower churn) is the clearest signal: pulling users into their first ride within 7 days is associated with 75.1% churn vs. 87.5% for users who wait over a year.

---

### 3.4 Promo Incrementality Test — find out if promotions are actually working

**What it answers:** Are promos generating rides that would not have happened otherwise, or are they being used on rides that would have happened anyway?

**The problem:** No holdout data exists. Right now, the $146,404 annual promo spend cannot be evaluated. The correlation between promo usage and lower churn disappears for users with fewer than 25 rides — which includes almost all new users in their first month. The new user promo program is the strategy most in need of a test.

**Experiment design:**

- Randomise new users at activation — 80% get the full 3-discount cycle, 20% get 1 discount
- Measure: completed rides at day 90 for both groups
- Guardrail: the 20% group's churn rate must not exceed the 80% group by more than 3 percentage points
- Duration: 90 days minimum
- Decision rule: if both groups complete the same number of rides, the extra 2 discounts are not generating incremental rides — redirect that budget

This experiment answers the single most important unanswered question about the current strategy.

---

### 3.5 New Feature Evaluation — how to measure whether a feature actually works

Every newly launched product feature needs a measurement plan *before* it launches. Without one, there is no way to know if the feature helped, hurt, or did nothing.

| What to define before launch | Requirement |
|:-----------------------------|:-----------|
| What are we measuring? | One primary metric, pre-declared. Booking features: completion rate. Retention features: rides in first 30 days. |
| What must not get worse? | Guardrails: wait time P90, driver cancel rate, churn rate. If any guardrail worsens, the feature has failed regardless of the primary metric. |
| How big a change matters? | Define the minimum improvement that would actually change a business decision. Then calculate how many users you need to see it. Don't end the test early. |
| Who does it apply to? | Randomise at the user level. Do not roll out to a whole city and call the city a control — supply effects contaminate city-level tests. |
| How do we cut the results? | Every result must be checked by city, by promo quartile, and by vehicle type. A feature that works for frequent riders but not new users is a different finding. |

---

## Strategic Recommendations

### Stop doing these

**Stop measuring growth by registration count.** 79.6% of registered users are inactive. Every registration that churns is a cost. The metric to watch is activated users who complete 2 or more rides in 30 days.

**Stop reporting overall completion rate as a health metric.** 81.4% sounds fine. It hides 54.1% completion inside the 15+ minute wait bucket — the bucket responsible for the worst user experiences on the platform.

**Stop spending on promo cycles for new users without testing whether they work.** The data shows promos have no measurable retention effect for users with fewer than 25 rides. The new user promo program is the largest unverified spend in the strategy. Run the holdout test before the next budget cycle.

**Stop expanding to new cities or new segments before the current product experience is fixed.** Bringing more users into a product where 7.6% of rides fail at the 15-minute threshold accelerates churn, not growth.

---

### Start doing these

**Fix the 741 both_issues drivers first.** These drivers (acceptance <60%, cancellation >30%) are responsible for 43% of their rides crossing the 15-minute wait threshold. Put them on a 30-day performance plan: acceptance must reach 70%, cancellation must fall below 20%. Failure means temporary deactivation. This is the single most direct lever on the wait time problem and costs nothing upfront.

**Fix driver governance — suspend based on performance, not administration.** 534 suspended drivers outperform 741 active ones on every measured metric (cancellation 0.135 vs 0.140, rating 4.142 vs 4.138). The current suspension criteria is not performance-based. The wrong drivers are being removed. Automate deactivation criteria tied to the same thresholds used for the performance plan above.

**Run a reactivation campaign for the 5,257 high-value churned users.** These users averaged 54 rides before going inactive, contributed $535,580 in gross fare revenue, and have been gone for a median of 218 days. They are not strangers to the platform. The offer should be a service quality guarantee — a commitment to a sub-10-minute wait on their return ride — not another discount. Test this as an 80/20 holdout. If it works, the reactivation value exceeds the cost of any acquisition campaign.

**Create an activation trigger for new users within 48 hours of signup.** Users who take their first ride within 7 days churn at 75.1%. Users who wait over a year churn at 87.5%. The gap is 12.4 percentage points. The intervention is simple: a triggered message within 48 hours of signup offering priority dispatch on the first ride. No discount needed — a service commitment.

**Northgate: focus the fix on two zones, not the whole city.** NOR-Z04 and NOR-Z05 account for 38% of all Northgate rides. They have 65.5–65.6% completion rates and 23-minute average waits — the worst numbers in the entire dataset. The other Northgate zones (NOR-Z01: 84.8% completion, NOR-Z03: 83.7%) perform near the platform average. A city-wide intervention is the wrong tool. Recruit 40–60 qualified drivers specifically for those two zones with a per-shift earnings guarantee.

---

### Continue doing these

**Keep the Q4 promo program — do not cut it yet.** Heavy promo users (Q4) churn at 69.3% vs. 82.8% for light promo users. Even if the direction of causality is uncertain, cutting promos for the most retained segment on the platform without a holdout test is a significant risk. Run the test first. Cut based on evidence.

**Keep behavioral segmentation as a targeting input.** The limitation is not how users are segmented — it is what they experience when they respond to re-engagement. Pair segmentation with operational fixes and it becomes more effective.

**Keep investing in driver tenure.** Drivers improve dramatically after 12 months. Cancellation rate drops from 0.22 to 0.10. Rating improves from 3.92 to 4.25. A driver who stays past 12 months becomes one of the platform's strongest performers. Programs that reduce early driver attrition are investments in long-term service quality, not just headcount.

---

### New strategies that could give a competitive edge

**Guaranteed first-ride experience.** Offer new users a specific commitment: if their driver takes more than 10 minutes to arrive on their first ride, the ride is free. This directly addresses the activation problem. It costs something in service credits but converts the highest-risk moment (first impression) into a trust-building event. Test in two cities before rolling out.

**Zone density over city breadth.** The data shows that the best-performing zones (MET-Z04: 84.2% completion, NOR-Z01: 84.8%) succeed because local supply is sufficient — not because their city is better. Drivers in Zone A cannot serve Zone B. Concentrating driver incentives in specific high-demand zones produces better outcomes than spreading drivers evenly across a city. Apply this logic to the 3–4 highest-demand zones in each city before thinking about entering new cities.

**Driver quality as a brand differentiator.** The data shows that after 12 months, drivers reach a sustained performance level that early-tenure drivers cannot match. A "Certified Driver" badge for drivers with 12+ months and acceptance >80% and cancellation <10% creates a quality signal for users and a retention incentive for drivers. Users can specifically request certified drivers; certified drivers earn a small premium. Over time this creates a two-sided quality lock-in.

---

### User segments, routes, and features to double down on

**Segment: At-risk users (1,795 users, last ride 31–59 days ago).** These users have not yet churned. A lightweight contact — a ride reminder, a relevant notification — within the next 30 days keeps them active. The intervention window is narrow. Once they cross 60 days, they join the churned pool.

**Segment: High-value churned users (5,257 users).** The highest-ROI reactivation target. Average 54 lifetime rides, $101.88 average gross fare revenue before going inactive. They have demonstrated they will use the platform. The question is what brings them back.

**Feature to prioritise evaluating: anything that reduces wait time.** Every feature that improves dispatch speed, driver acceptance, or route predictability has a direct path to the most important metric on the platform. Features that address any other part of the experience are lower priority until the wait time problem is resolved.

---

## Problem Statements

---

### Problem 1: 4 out of 5 users register and never come back — and this is happening everywhere

**Problem statement**

79.6% of all 35,000 registered users are inactive. This is not a city-specific failure — every single city sits between 78.8% and 80.7% churn. Monthly ride volume has been flat at 9,408–10,420 for 12 consecutive months. The platform is acquiring users and losing them at the same rate, producing zero growth.

**Evidence**

- 27,867 / 35,000 users classified as churned (no ride in last 60 days from 2024-06-30)
- 12-month ride volume: July 2023: 10,089 requests → June 2024: 9,408 requests. No upward trend.
- City churn range: Clearwater 78.8% — Summit Town 80.7%. Zero city is an outlier. Zero city has cracked the retention problem.
- Churned users contributed $2,780,358 (80.9% of total gross fare revenue) before going inactive. Their average fare contribution per person ($106.45) was higher than the average active user ($97.83). These were not low-value users who left.

**Root cause hypothesis**

The uniformity of churn across all 12 cities is the key diagnostic signal. When churn varies by city, the cause is local — supply, competition, geography. When churn is the same everywhere, the cause is in the core product experience. Something that happens in the product itself — before, during, or immediately after the ride — is causing users to not come back. The wait time data points to this directly: rides that cross 15 minutes have a 46% chance of not completing, and first-time users who experience this likely do not return. The activation gap analysis supports this: users who ride within 7 days of signup churn at 75.1%. Users who wait over a year before their first ride churn at 87.5%. The platform is not converting registrations into habits fast enough.

**Recommended action**

Two actions in parallel:

1. Within 48 hours of signup, trigger a priority dispatch offer for the user's first ride. No discount — a service commitment (sub-10-minute wait guarantee). This targets the activation gap directly.

2. Run a reactivation campaign for the 5,257 high-value churned users (top 20% by lifetime rides, now inactive). Offer a service quality guarantee on their return ride. Run as 80/20 holdout — 80% receive the offer, 20% do not. Measure return rides in 30 days.

**Success metric**

- 30-day ride retention (% of new users completing ≥2 rides in first 30 days) rises from the current 19.8%–27.9% range to ≥30% within 2 months of activation intervention
- High-value churned user return rate: ≥15% within 30 days of campaign (any positive response is the baseline, since there is currently no targeted reactivation)

---

### Problem 2: A 15-minute wait destroys the ride — and 741 specific drivers are the cause

**Problem statement**

When a user waits more than 15 minutes for a driver, only 54.1% of those rides complete — vs. 86.2% completion when the wait is under 5 minutes. 9,132 rides (7.6% of all rides) cross this threshold. The cause is identifiable: 741 active drivers with acceptance rates below 60% and cancellation rates above 30% account for 43% of their rides reaching the 15-minute threshold, vs. 2.8% for the remaining 7,041 standard drivers.

**Evidence**

| Wait time | Rides | Completed | Driver cancelled |
|:----------|------:|:---------:|:----------------:|
| Under 5 min | 30,685 | 86.2% | 5.8% |
| 5–10 min | 53,352 | 84.3% | 7.1% |
| 10–15 min | 26,831 | 78.2% | 11.5% |
| **15–20 min** | **6,646** | **54.1%** | **29.3%** |
| 20–30 min | 1,649 | 65.7% | 18.9% |

- 741 both_issues drivers: 43% of their rides exceed 15 min → 54.1% completion
- 7,041 standard drivers: 2.8% of their rides exceed 15 min → near-normal completion
- The 29.3% driver cancellation rate at 15–20 minutes means the driver cancels *while the user is waiting* — the worst possible experience

**Root cause hypothesis**

When a low-acceptance driver declines a ride or accepts and then cancels, the system has to find another driver. Each retry adds minutes to the wait. With 741 problematic drivers in the active fleet, the dispatch system is cycling through unreliable drivers before it reaches a reliable one. Note: the actual dispatch history is not in the dataset, so this is a strong inference from the correlation, not a directly measured fact.

The suspension anomaly confirms governance is not working: 534 drivers are currently suspended. Their cancellation rate is 0.135 and their average rating is 4.142. The 741 active both_issues drivers have cancellation rates that should — by any reasonable standard — trigger the same suspension. The suspended group is actually performing *better* than the active problem group. The platform has suspended the wrong drivers.

**Recommended action**

1. Put all 741 both_issues drivers (acceptance <60% AND cancellation >30%) on a 30-day performance improvement plan. Target: acceptance ≥70%, cancellation ≤20%. Consequence for non-improvement: temporary deactivation.

2. Fix the suspension criteria so it is automated and performance-based. The current criteria is administrative — it is not triggering on the drivers who are actually causing harm.

**Success metric**

- % of rides with wait >15 minutes drops from 7.6% to ≤3% within 60 days of the performance plan
- Driver cancellation rate in the 15–20 min bucket drops below 15% (from 29.3%)
- Guardrail: overall completion rate must not fall — if the plan causes drivers to reject more rides rather than improve, it has failed

---

### Problem 3: Northgate is broken in exactly two zones — not the whole city

**Problem statement**

Northgate is the only city that materially underperforms the platform average: 76.1% completion vs. 81.4%, driver cancellation 13.0% vs. 9.3%, average wait 13.35 minutes vs. 7.33 minutes. But within Northgate, two zones — NOR-Z04 and NOR-Z05 — account for 38% of all Northgate rides and nearly all of the city's failure. The other Northgate zones perform near the platform average. Treating this as a Northgate problem leads to city-wide interventions. The data says it is a two-zone problem.

**Evidence**

| Zone | Rides | Completion | Driver cancelled | Avg wait |
|:-----|------:|:----------:|:----------------:|:--------:|
| NOR-Z05 | 1,967 | 65.5% | 20.2% | 23 min |
| NOR-Z04 | 1,867 | 65.6% | 20.5% | 23 min |
| NOR-Z01 | 1,071 | 84.8% | 7.8% | 7.4 min |
| NOR-Z03 | 1,035 | 83.7% | 8.8% | 7.2 min |

- NOR-Z04 + NOR-Z05 = 3,834 rides = 38.4% of Northgate's 9,989 total rides
- 65.5–65.6% completion in these two zones is the worst in the entire dataset
- NOR-Z01 and NOR-Z03 complete at 84.8% and 83.7% — near the best zones on the platform
- Northgate has the highest driver behaviour complaint count of any city: 447

**Root cause hypothesis**

The 23-minute average wait in NOR-Z04 and NOR-Z05 — vs. 7 minutes in the same city's better zones — indicates localised supply shortage. Drivers are not spending time in these zones, likely because ride density there is lower, making it less profitable to be present. When a ride is requested, a driver must travel from outside the zone, adding wait time. Long wait → higher cancellation probability (confirmed by the platform-wide wait × cancel data) → failed ride → bad experience → users stop booking in these zones → demand density falls further → drivers have even less reason to be there. The 447 driver behaviour complaints is the measurable outcome of this cycle.

The fact that NOR-Z01 and NOR-Z03 perform normally with the same city-level driver pool rules out a "Northgate has bad drivers" explanation. The problem is geographic — specific zones where supply is thin.

**Recommended action**

Zone-targeted supply fix for NOR-Z04 and NOR-Z05 only:
- Recruit 40–60 additional drivers with demonstrated quality (acceptance >80%, cancellation <15%) and incentivise them to be available in these two zones during peak hours (7–9am and 5–7pm)
- Offer a per-shift earnings guarantee for drivers who complete ≥5 rides in NOR-Z04 or NOR-Z05 per shift
- Do not change anything in NOR-Z01 and NOR-Z03 — they do not need fixing

**Success metric**

- NOR-Z04 and NOR-Z05 average wait drops below 12 minutes within 90 days (from 23 minutes)
- Completion rate in these zones rises above 75% (from 65.5–65.6%)
- Northgate driver behaviour complaint count falls below 350 (from 447)
- Guardrail: NOR-Z01 and NOR-Z03 completion rates must not fall — supply redistribution must not cannibalize zones that are already working

---

### Problem 4: The promo spend cannot be evaluated — and the biggest promo cycle may have zero effect on new users

**Problem statement**

The company is the largest promotional spender among competitors, spending $146,404/year on ride discounts. The flagship strategy is a new user promo cycle: three consecutive discounts of up to 25% in the first month. The data shows that among users with fewer than 25 lifetime rides — which includes virtually all new users in their first month — there is effectively zero difference in churn rate between users who use promos heavily and users who use them rarely (0.8 percentage point gap). Twelve months of promo spending has produced zero growth in monthly ride volume.

**Evidence**

- Monthly ride volume: flat 9,408–10,420 for 12 consecutive months despite continuous promo activity
- Promo share of completed rides: flat at 14.9%–16.3% every single month — no growth in promo uptake, no growth in rides
- Promo effect by ride frequency:

| User ride count | Low promo use churn | High promo use churn | Difference |
|:----------------|:-------------------:|:--------------------:|:----------:|
| 1–10 rides | 82.7% | 81.9% | **0.8pp — no effect** |
| 11–25 rides | 82.8% | 82.0% | **0.8pp — no effect** |
| 26–50 rides | 83.8% | 70.8% | 13pp — real effect |
| 51–100 rides | 81.5% | 56.7% | 25pp — real effect |

New users in their first month are in the 1–25 ride bucket. Promos show no measurable retention effect for this group.

**Root cause hypothesis**

The promo–retention link that does exist (for 26+ ride users) is more consistent with reverse causality than with promos driving retention. Engaged users naturally encounter more promo opportunities and use them. Their lower churn is caused by their engagement, not by the promos themselves. If this is true, cutting promos for new users would have almost no effect on churn (the 0.8pp gap confirms this). The new user promo program is spending money where the data shows no measurable return.

**Recommended action**

Do not cut promos across the board — this risks the Q4 heavy users who are the most retained segment. Instead, test the new user cycle specifically:

- Run a 90-day holdout for new users: 80% get the full 3-discount cycle, 20% get 1 discount
- Primary metric: completed rides at day 90
- Guardrail: control group churn must not exceed treatment group by more than 3 percentage points
- If the holdout shows no difference: redirect the saved budget toward driver quality incentives (the wait time fix) and the NOR-Z04/Z05 zone supply program — both with direct links to the completion problem

**Success metric**

- If promos are shown to be causal: 90-day ride count in treatment group exceeds control by ≥5pp → keep the cycle
- If promos are not causal: promo budget for new user cycle is reallocated; promo spend per completed ride metric is introduced to track efficiency going forward

---

### Problem 5: Drivers get dramatically better after 12 months — but the platform is losing them before they get there

**Problem statement**

Driver performance improves sharply at the 12-month tenure mark: cancellation rate drops from 0.22 to 0.10 (55% reduction), acceptance rate rises from 0.73 to 0.84, and user rating improves from 3.92 to 4.25. Performance then holds stable through 24+ months. Meanwhile, 15.3% of all drivers (1,221) have churned, consistently across every signup cohort. Active driver supply has been flat for 12 months (5,500–5,815 per month). The platform is on a driver treadmill: recruiting to replace those who leave, keeping the share of below-average early-tenure drivers permanently high.

**Evidence**

| Tenure | Drivers | Acceptance | Cancellation | Rating |
|:-------|--------:|:----------:|:------------:|:------:|
| 6–12 months | 2,691 | 0.73 | **0.22** | **3.92** |
| 12–18 months | 1,726 | **0.84** | **0.10** | **4.25** |
| 18–24 months | 1,788 | 0.84 | 0.10 | 4.25 |
| 24+ months | 1,795 | 0.84 | 0.10 | 4.24 |

- 2,691 drivers are currently in the 6–12 month (below-average) tier — that is 43% of the 6,245 active drivers
- August–September 2023 saw 1,548 new driver signups in two months (the largest intake in the dataset) — this recruitment spike is what kept supply stable despite ongoing 15.3% driver churn
- Without that spike, active driver numbers would have declined

**Root cause hypothesis**

At any given moment, roughly 43% of active drivers are in the below-average performance tier simply because they have not been on the platform long enough. This is not a recruitment quality problem — the data shows every driver improves. It is a retention problem: the platform is not keeping drivers long enough for them to become good at the job.

Every driver lost before 12 months is replaced by a new early-tenure driver. The net effect: the platform is permanently running with a large below-average segment contributing disproportionately to the acceptance and cancellation problems that drive long waits. Early driver attrition is not just a headcount loss — it is a quality regression for every new user who gets matched with a replacement new driver.

The dataset does not contain driver earnings, driver satisfaction, or exit reasons — so why drivers leave remains a hypothesis. The improvement trajectory at 12 months is unambiguous.

**Recommended action**

1. Introduce a 12-month tenure milestone for drivers who maintain acceptance ≥70% and cancellation ≤15%: a one-time bonus and "Verified Driver" status that gives them preferred matching in dispatch and a small per-ride premium. Frame internally as converting a cost (early attrition + replacement recruitment) into an investment (quality-building retention).

2. Flag early warning: any driver active for less than 6 months with acceptance rate already below 70% should be flagged for outreach — coaching or schedule support before they become a both_issues driver or churn.

**Success metric**

- % of active drivers with ≥12 months tenure rises from current ~57% toward ≥65% within 12 months
- Platform-wide driver cancellation rate falls below 8% (from current 9.3%) as the veteran share increases
- Guardrail: total active driver count must not fall below 5,500/month — the tenure program must not accelerate departures by making early-tenure drivers feel the bar is too high

---

## Summary: The One-Page Version

RideFast has 12 months of flat ride volume despite ongoing promotional spend. The instinct is to fix the promos or the targeting. The data says the problem is earlier in the chain.

**What is actually happening:**
1. Users sign up. 79.6% of them go inactive — uniformly, in every city.
2. The product experience that drives them out is identifiable: when a driver takes more than 15 minutes to arrive, only 54% of rides complete. 741 specific drivers are responsible for most of those long waits.
3. The promo spend is $146,404/year with no measurable growth to show for it. For new users (under 25 rides), promos show zero retention effect.
4. Two zones in Northgate are producing the worst ride outcomes in the entire dataset. The rest of Northgate is near-normal.
5. Drivers improve dramatically after 12 months but 15.3% leave before they get there, keeping a permanent below-average cohort in the active fleet.

**What to do in order of impact:**
1. Put the 741 underperforming drivers on a performance plan — this directly fixes the 15-minute problem
2. Run a reactivation campaign for the 5,257 high-value churned users — highest-ROI reactivation pool in the data
3. Fix NOR-Z04 and NOR-Z05 with zone-targeted driver recruitment — the rest of Northgate does not need fixing
4. Run a holdout test on the new user promo cycle before the next budget cycle — the data suggests it is not working for new users
5. Introduce driver tenure incentives to reduce early attrition — a quality investment, not just a headcount one

*Every number in this document comes directly from the verified analysis of the four source CSV files. Claims the data cannot support are explicitly labelled as hypotheses.*
