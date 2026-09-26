# RideFast — Combined EDA: What the Data Actually Says

*Sources: rides.csv (120,000 rows), users.csv (35,000 rows), drivers.csv (8,000 rows), support_tickets.csv (22,000 rows). Observation window: Jul 2023 – Jun 2024.*

*For every number below, I explain which file it came from and how it was calculated. Where the data is ambiguous, I say so.*

---

## How to read this document

Each finding is labelled:
- **CONFIRMED** — the number is clear and repeatable
- **LIKELY** — the pattern is real but there is an alternative explanation
- **FLAG** — something looks unusual but we do not know what causes it
- **WEAK** — the data shows a pattern but it is too small to act on

---

## 1. The Wait-Time Problem Is Real and Has a Sharp Edge

**Source:** `rides.csv` — columns `request_time`, `pickup_time`, `status`

Wait time = the number of minutes between when a user requested a ride and when the driver actually arrived. This is calculable for all 120,000 rides because `pickup_time` is never null.

**What the data shows:**

| Wait time         | Rides  | Rides that completed |
|:------------------|-------:|--------------------:|
| Under 5 minutes   | 30,685 | **86.2%**           |
| 5–10 minutes      | 53,352 | **84.3%**           |
| 10–15 minutes     | 26,831 | **78.2%**           |
| 15–20 minutes     |  6,646 | **54.1%**           |
| 20–30 minutes     |  1,649 | **65.7%**           |
| 30+ minutes       |    837 | **65.4%**           |

**CONFIRMED.** There is a cliff at the 15-minute mark. Below 15 minutes, 78–86% of rides complete. Above it, completion drops to 54%. This is not gradual — it is a sudden drop.

The 15–20 min bucket sees 29.3% of rides cancelled by the *driver* (not the user). That means the driver is already en route, the user has been waiting, and the driver cancels anyway — the worst possible experience. At 0–5 min wait, driver cancellations are only 5.8%.

**How many rides are affected?** 9,132 rides (7.6% of all timed rides) had a wait of 15 minutes or more.

**Who is associated with the long waits?** `drivers.csv` has `acceptance_rate` and `cancellation_rate` per driver. When joined back to `rides.csv`, rides handled by `both_issues` drivers (acceptance below 60% AND cancellation above 30%) have 43% of their rides waiting 15+ minutes. Standard drivers: 2.8%. There are **741 drivers in the both_issues group** (9.3% of all 8,000 drivers), handling 11,174 rides in the dataset.

The pattern is consistent with a possible retry-cycle mechanism: rides associated with drivers who have lower acceptance rates and higher cancellation rates show substantially higher wait times. The dataset does not contain dispatch attempt history, so the exact matching process cannot be directly verified.

> **Plain English:** 1 in 14 rides waits more than 15 minutes. When that happens, only about half complete. A small group of drivers with low acceptance and high cancellation rates is strongly associated with longer wait times and poorer ride completion outcomes.

---

## 2. Northgate Is in a Different Category — and the Zone Data Shows Exactly Where

**Source for city data:** `rides.csv` grouped by `city`. **Source for zone data:** `rides.csv` grouped by `city` + `pickup_zone`.

Every city in the dataset has ~9,800–10,100 ride requests and a completion rate of 81–83%. Then there is Northgate.

| City metric               | Northgate | Rest of platform (avg) |
|:--------------------------|----------:|----------------------:|
| Completion rate           | 76.1%     | 81.9%                 |
| Driver cancel rate        | 13.0%     | 9.0%                  |
| Average wait time         | 13.35 min | 7.33 min              |
| Ticket rate per 100 rides | 17.4      | 14.9                  |

**CONFIRMED.** Northgate is the only city that deviates materially from the platform average. Every other city has a completion rate between 81.1% and 82.7%.

**The zone data makes it more specific.** Within Northgate, two zones are worse than everything else on the platform:

| Zone    | Rides | Completion | Driver cancel | Avg wait  |
|:--------|------:|-----------:|--------------:|----------:|
| NOR-Z05 | 1,967 | 65.5%      | 20.2%         | 22.94 min |
| NOR-Z04 | 1,867 | 65.6%      | 20.5%         | 23.00 min |

These two zones account for 38% of all Northgate rides. Their average wait time is 23 minutes — almost double Northgate's already-bad city average of 13 minutes. Their completion rate is 65.5%, vs 76.1% for Northgate as a whole. The rest of Northgate's zones (NOR-Z01, NOR-Z03) actually perform close to normal (84.8% and 83.7% completion).

**CONFIRMED.** Northgate's poor numbers are not spread evenly across the city. NOR-Z04 and NOR-Z05 account for a disproportionate share of Northgate's poor ride outcomes.

> **Plain English:** "Northgate is broken" is too broad. NOR-Z04 and NOR-Z05 show the worst performance numbers in the dataset. The other Northgate zones are near-normal. This matters for targeting: targeting operational investigation and supply interventions in those two zones may provide a more focused approach than applying city-wide changes.

---

## 3. 79.6% of Users Are Gone — and Many Were High-Value Before They Left

**Source for churn:** `users.csv` — column `churn_flag` (True = no ride in the last 60 days from 2024-06-30). The flag is pre-computed in the dataset; independent verification matches it in 96.7% of rows. **Source for revenue:** `rides.csv` matched to `users.csv` by `user_id`.

27,867 of 35,000 registered users (79.6%) are classified as churned. This is uniform — every city has a churn rate between 78.8% and 80.7%. It is not a city problem or a zone problem. It is platform-wide.

**The critical revenue finding:**

All revenue figures below represent **gross fare revenue after promo discount** (fare_amount − promo_discount from `rides.csv`). This does not account for driver payouts, platform fees, refunds, or taxes, which are not present in the dataset.

| User group           | Users  | Gross fare revenue after promo discount | Avg per user |
|:---------------------|-------:|----------------------------------------:|-------------:|
| Active (not churned) | 6,716  | $657,005 (19.1%)                        | $97.83       |
| Churned              | 26,118 | $2,780,358 (80.9%)                      | $106.45      |

**CONFIRMED.** Churned users generated more total gross fare revenue than active users. Their average per person ($106.45) is higher than active users ($97.83). These users had historical ride activity and generated measurable fare contribution before becoming inactive.

**How concentrated is revenue?** From `rides.csv`, summing (fare_amount − promo_discount) per user_id:

| Who        | Users  | Revenue share |
|:-----------|-------:|--------------:|
| Top 10%    | 3,283  | 25.2%         |
| Top 20%    | 6,566  | 42.3%         |
| Top 50%    | 16,417 | 76.9%         |
| Bottom 50% | 16,417 | 23.1%         |

Revenue is moderately concentrated but not extreme. The bottom half still contributes 23%. The bigger story is the churned users: the **5,257 users** classified as `high_value_churned` had an average of 54 rides and an average gross fare revenue of $101.88, with a collective total of $535,580 — sitting dormant, median 218 days since their last ride.

> **Definition:** High-value churned users are users in the top 20% of the full user base by lifetime rides (49+ rides threshold, 80th percentile of all 35,000 users) who are currently classified as churned.

> **Plain English:** Many churned users had meaningful historical platform value. Reactivating high-value churned users should be evaluated as a potential retention opportunity alongside acquisition efforts.

---

## 4. Users Who Start Fast, Stay Longer

**Source:** `users.csv` for `signup_date` and `churn_flag`. `rides.csv` for the date of each user's first actual ride, found by taking the earliest `request_time` per `user_id`.

The gap between when someone creates an account and when they take their first ride is associated with whether they stay.

**Analysis is based on 25,863 valid users.** 8,022 users were excluded because their first ride date pre-dates their signup date (a data quality issue — likely signup_date records app installation rather than account creation). A further 1,103 users with no rides in the dataset were also excluded.

| Time between signup and first ride | Users  | Churn rate | Avg lifetime rides |
|:-----------------------------------|-------:|-----------:|-------------------:|
| Same day                           |     45 | 68.9%      | 32.0               |
| 1–7 days                           |    338 | 75.1%      | 29.4               |
| 7–30 days                          |  1,146 | 75.9%      | 31.2               |
| 30–90 days                         |  3,104 | 78.3%      | 30.7               |
| 90–180 days                        |  4,769 | 80.8%      | 30.9               |
| 180–365 days                       |  9,840 | 84.9%      | 30.9               |
| 365+ days                          |  6,621 | 87.5%      | 30.8               |

**CONFIRMED (gradient). DIRECTIONAL (same-day bucket).** The overall gradient is clear and based on large samples from the 1–7 day bucket onward. The same-day group contains only **45 users**, so the 68.9% churn figure for that row should be interpreted as directional rather than statistically conclusive on its own.

**Important caveat:** Average lifetime rides is nearly flat across all groups (29–32 rides). The fast-activators are not riding more over their lifetime — they are just more likely to still be active. The gap in churn is real; the gap in lifetime ride count is not.

> **Plain English:** Users who take their first ride quickly after signing up are consistently more likely to still be active later. The gradient holds across the large middle buckets (thousands of users each). Reducing the time between account creation and first ride represents a testable retention opportunity.

---

## 5. Promos Are Associated with Lower Churn Among Engaged Users — But Causality Is Unknown

**Source:** `users.csv` for `promo_rides`, `total_rides`, `churn_flag`. `rides.csv` for `promo_code_used`, `promo_discount`, `status`.

Every user's promo dependency ratio = (promo_rides ÷ total_rides). Users were split into 4 equal quartiles (Q1 = lowest promo use, Q4 = highest).

| Promo quartile | Users | Churn rate | Avg total rides | Avg promo ratio |
|:---------------|------:|-----------:|----------------:|----------------:|
| Q1 (lowest)    | 8,804 | 82.8%      | 18.68           | 0.2%            |
| Q2             | 8,928 | 83.5%      | 34.26           | 6.4%            |
| Q3             | 8,556 | 82.8%      | 32.26           | 13.7%           |
| Q4 (highest)   | 8,712 | 69.3%      | 38.58           | 30.5%           |

**CONFIRMED (pattern). LIKELY (not proven cause).** Heavy promo users are associated with lower churn and higher ride frequency. Q4 users churn 13.5 percentage points less than Q1.

What we cannot determine from this data: whether promos *cause* users to stay, or whether engaged users *choose* to use more promos. Both are plausible. The data cannot tell them apart.

**After controlling for lifetime ride volume**, the association is not uniform. When comparing promo quartiles within users who have similar ride counts:

| Ride volume bucket | Q1 churn | Q4 churn | Gap |
|:-------------------|:---------|:---------|:----|
| 1–10 rides         | 82.7%    | 81.9%    | 0.8pp — negligible |
| 11–25 rides        | 82.8%    | 82.0%    | 0.8pp — negligible |
| 26–50 rides        | 83.8%    | 70.8%    | **13pp — meaningful** |
| 51–100 rides       | 81.5%    | 56.7%    | **25pp — meaningful** |

The promo–retention association is mainly observed among users with 26 or more lifetime rides. Among users with fewer than 25 rides, Q1 and Q4 churn at almost the same rate. Promo usage appears more strongly associated with retention among already-engaged users, while its effect on casual users remains unclear from this data.

**Monthly promo spend:** $146,404 in gross fare revenue after promo discount over 12 months (~$12,200/month). Promo share of completed rides stayed flat at 15–16% every single month with no growth trend.

> **Plain English:** Heavy promo users are associated with lower churn and more rides — but only among users who already ride frequently. For low-frequency users, promos show no measurable retention benefit in this data. Do not cut promos for Q4 high-frequency users until you have run a holdout test that proves which way the arrow points.

---

## 6. The Wallet Balance Has a Hard $80 Ceiling for Churned Users

**Source:** `users.csv` — column `wallet_balance`. This is a single snapshot per user — one row, one balance value. There is no transaction history or time-series wallet data in the dataset.

Active users (churn_flag = False) have wallet balances ranging from $0 to $299.93, with a mean of $69.55. Churned users (churn_flag = True) have wallet balances ranging from $0 to exactly $80.00, with a mean of $39.89.

**FLAG.** Not one churned user has a wallet balance above $80. Zero. Active users have 1,400 users with balances above $80.

| Wallet bucket | Active users | Churned users | Churned % |
|:--------------|-------------:|--------------:|----------:|
| $0–10         | 694          | 3,449         | 83.2%     |
| $10–25        | 1,125        | 5,212         | 82.2%     |
| $25–50        | 1,773        | 8,861         | 83.3%     |
| $50–80        | 2,141        | 10,343        | 82.9%     |
| $80–100       | 147          | **2**         | 1.3%      |
| $100–150      | 286          | **0**         | 0.0%      |
| $150–300      | 967          | **0**         | 0.0%      |

This pattern is unusually consistent and suggests a possible system rule or data-processing behaviour. Possible explanations: wallet balances above $80 are only credited to accounts that remain active, wallet credits are cleared or capped on churn, or there is a system rule for inactive accounts. Because the data is a single snapshot, we cannot see how balances changed over time.

**What this means for analysis:** The $80 ceiling may indicate a system rule, wallet policy, or churn-related balance handling process. Further validation is required before using wallet_balance as a behavioural predictor. The decile analysis showing D10 (avg $122 balance) churning at only 50% is almost entirely a construction artifact — you structurally cannot have a balance above $80 AND be churned in this dataset, so D10 is effectively "active users only" by definition.

> **Plain English:** The wallet balance data for churned users has a ceiling that looks like a system rule rather than natural behaviour. Before doing anything with this number, the data needs to be verified with whoever manages the wallet system.

---

## 7. Support Tickets: The Numbers Are Smaller Than They Look

**Source:** `support_tickets.csv` joined to `users.csv` via `user_id` and to `rides.csv` via `ride_id`.

There are 22,000 tickets across 5 categories. Before drawing conclusions, here is what is actually true vs what looks true.

**What is true (CONFIRMED):**

Fare dispute users rate their rides lower than average: 3.45 average user rating on rides with fare disputes, vs 4.20 platform average. This comes from joining `support_tickets.csv` (filtered to category = `fare_dispute`) to `rides.csv` via `ride_id` and reading `rating_by_user`.

Northgate has the highest driver_behaviour complaints (447), which is consistent with its operational problems already identified in section 2.

**What looks meaningful but is not (WEAK):**

| Group                   | Churn rate |
|:------------------------|----------:|
| Users with tickets      | 79.2%      |
| Users without tickets   | 79.9%      |

The difference is 0.7 percentage points. Users who raise tickets do not churn at a materially different rate from users who never raise one.

Resolution speed was also tested within ticket creators only — comparing users whose fastest ticket was resolved in under 2 hours vs 2–6 hours vs 6–24 hours:

| Fastest resolution (within ticket creators) | Users | Churn rate |
|:--------------------------------------------|------:|-----------:|
| < 2 hours                                   | 4,055 | 78.5%      |
| 2–6 hours                                   | 6,127 | 79.5%      |
| 6–24 hours                                  | 2,153 | 79.1%      |

The range is 78.5% to 79.5% — less than 1 percentage point across all resolution speeds, even when comparing cleanly within ticket creators. Based on this dataset, support resolution speed does not show a meaningful association with churn rate.

**Why does this happen?** The platform-wide churn rate is already 79.6% and is unusually uniform. Because the base rate is so high and so flat, individual-level factors like support tickets have very little room to move the number either way.

This does not rule out support impact on user satisfaction or short-term experience metrics that are not captured in this dataset. The finding is specific: in this data, faster resolution does not show a statistically meaningful difference in churn outcome.

> **Plain English:** Fare dispute users are unhappy (lower ratings). Northgate has more driver behaviour complaints than anywhere else. But based on this dataset, support resolution speed does not show a meaningful association with churn rate — and the platform-wide churn is so uniformly high that it barely shifts at all between ticket and non-ticket users.

---

## 8. Driver Supply: Stable but Not Growing

**Source:** `drivers.csv` for status, signup_date, and performance metrics. `rides.csv` for counting unique drivers serving rides each month.

**Driver status breakdown (drivers.csv):**

| Status    | Count | Share |
|:----------|------:|------:|
| Active    | 6,245 | 78.1% |
| Churned   | 1,221 | 15.3% |
| Suspended |   534 |  6.7% |

**Driver churn rate: 15.3%.** Across all signup cohorts (Jan 2022 – Dec 2023), the share of drivers who are now churned stays consistently between 12% and 20% per cohort — no cohort shows a meaningfully better or worse outcome.

**Active driver supply by month (from rides.csv — unique driver IDs appearing in at least one ride):**

| Month    | Unique drivers active |
|:---------|----------------------:|
| Jul 2023 | 5,758                 |
| Aug 2023 | 5,794                 |
| Sep 2023 | 5,715                 |
| Oct 2023 | 5,807                 |
| Nov 2023 | 5,682                 |
| Dec 2023 | 5,788                 |
| Jan 2024 | 5,815                 |
| Feb 2024 | 5,555                 |
| Mar 2024 | 5,693                 |
| Apr 2024 | 5,603                 |
| May 2024 | 5,773                 |
| Jun 2024 | 5,539                 |

Driver supply is **flat at 5,500–5,815 per month**, mirroring the flat ride volume trend. There was a large recruitment spike in Aug–Sep 2023 (1,548 new driver signups in two months — the biggest intake in the dataset). This kept supply stable despite ongoing 15% driver churn. Without that recruitment push, active driver numbers would have declined.

**CONFIRMED.** Driver supply is not declining, but it is not expanding either. Recruitment appears to be offsetting attrition rather than creating additional capacity. This is the supply-side version of the same treadmill problem seen on the user side.

**Driver tenure and performance (drivers.csv):**

| Tenure bucket  | Drivers | Avg acceptance | Avg cancellation | Avg rating |
|:---------------|--------:|---------------:|-----------------:|-----------:|
| 6–12 months    | 2,691   | 0.73           | 0.22             | 3.92       |
| 12–18 months   | 1,726   | 0.84           | 0.10             | 4.25       |
| 18–24 months   | 1,788   | 0.84           | 0.10             | 4.25       |
| 24+ months     | 1,795   | 0.84           | 0.10             | 4.24       |

There is a clear improvement at the 12-month mark: cancellation rate drops from 0.22 to 0.10, acceptance rate rises from 0.73 to 0.84, and rating improves from 3.92 to 4.25. Performance then plateaus and holds steady through 24+ months.

> **Plain English:** Driver supply is holding steady only because the platform keeps recruiting to replace drivers who leave. The pool is not growing. Separately, drivers get substantially better after their first year — which means early driver attrition (losing drivers before they reach 12 months) is a quality cost, not just a volume cost. Retaining a new driver past 12 months converts them from a below-average performer to a near-top performer.

---

## 9. What Is Confirmed, What Is Not

Here is a single table of every major finding from across both analyses, with an honest confidence label and the specific number behind it.

| Finding | Number | Source | Confidence |
|:--------|:-------|:-------|:-----------|
| Wait time cliff at 15 min | Completion drops from 84% to 54% | rides.csv, wait_minutes vs status | **CONFIRMED** |
| NOR-Z04 and NOR-Z05 show worst outcomes | 65.5–65.6% completion, 23 min avg wait | rides.csv grouped by pickup_zone | **CONFIRMED** |
| Platform-wide churn | 79.6% across all 12 cities | users.csv, churn_flag | **CONFIRMED** |
| Churned users hold 80.9% of gross fare revenue | $2.78M of $3.44M total | rides.csv × users.csv join | **CONFIRMED** |
| High-value churned pool | 5,257 users (top 20% all users by rides, now churned), avg $101.88 gross fare revenue, 218 days dormant | users.csv segment | **CONFIRMED** |
| Fast-activation = lower churn | 1–7 day activators: 75.1% churn. 365+ days: 87.5% churn | users.csv signup_date + rides.csv min(request_time) | **CONFIRMED** |
| Same-day activation churn | 68.9% (45 users — directional only) | same sources | **DIRECTIONAL** |
| First-ride wait → 30-day retention gap | Only 1.7pp (25.4% vs 23.7%) | rides.csv + users.csv join | **WEAK** |
| Promo Q4 users churn less (overall) | 69.3% vs 82.8% for Q1 | users.csv, promo_quartile | **CONFIRMED (association only)** |
| Promo effect among low-ride users | <1pp difference (Q1 vs Q4) | users.csv, controlled by ride bucket | **CONFIRMED — no effect** |
| Promo causality | Cannot determine | No holdout data in dataset | **UNKNOWN** |
| Wallet $80 ceiling for churned users | Zero churned users above $80 | users.csv, wallet_balance | **FLAG (may be system rule)** |
| Fare dispute → lower ratings | 3.40 vs 4.20 platform avg | support_tickets.csv × rides.csv | **CONFIRMED** |
| Ticket resolution speed → churn | <1pp difference within ticket creators | support_tickets.csv × users.csv | **WEAK** |
| Northgate driver behaviour complaints | 447 — highest of any city | support_tickets.csv × rides.csv | **CONFIRMED** |
| Monthly ride volume flat | 9,408–10,420 requests/month, 12 months | rides.csv grouped by month | **CONFIRMED** |
| Both-issues drivers (741 drivers, 9.3% of fleet): 43% of their rides wait >15 min | vs 2.8% for standard drivers | rides.csv × drivers.csv | **CONFIRMED** |
| Monthly active driver supply flat | 5,500–5,815 per month, 12 months | rides.csv grouped by month | **CONFIRMED** |
| Driver performance improves sharply after 12 months | Cancellation 0.22 → 0.10; Rating 3.92 → 4.25 | drivers.csv, tenure buckets | **CONFIRMED** |

---

## 10. Three Things That Sound Important But Are Not (Based on This Data)

**Surge pricing effect on cancellations:** At 1x surge, user cancellation is 6.8%. At 3x surge it is 7.0%; at 4x surge (1,028 rides at the extreme end) it is 7.3%. That is a 0.5 percentage point difference at the highest surge level. Surge pricing does not appear to be materially driving user cancellations in this dataset.

**Payment method differences:** Wallet users churn at 79.6%, card users at 79.5%, cash users at 80.1%. Average rides per user: 30.8–31.0 across all three groups. These numbers are essentially identical. Payment method does not meaningfully predict churn or engagement in this data.

**Rating reciprocity:** The Pearson correlation between a user's rating of their driver and the driver's rating of the user is **0.000**. Drivers give nearly the same average rating (4.47–4.48) regardless of whether the user rated them 1 or 5 stars. There is no reciprocity effect in this dataset.

---

## The Short Version

Four things are clearly true and backed by the data:

1. **The 15-minute wait cliff destroys completion.** 86% of rides complete when wait is under 5 minutes. 54% complete when wait exceeds 15 minutes. Long waits are strongly associated with a subset of 741 drivers with lower acceptance and higher cancellation rates. The exact dispatch mechanism requires additional operational data to confirm.

2. **NOR-Z04 and NOR-Z05 account for a disproportionate share of Northgate's poor outcomes.** Not Northgate broadly — two specific zones with 23-minute average waits and 65% completion. The other Northgate zones perform near the platform average.

3. **Many churned users had meaningful historical platform value.** Churned users generated 80.9% of total gross fare revenue after promo discount. The average churned user had higher gross fare revenue per person than the average active user. There are 5,257 high-value churned users (top 20% of all users by lifetime rides, now inactive, median 218 days dormant). Reactivating high-value churned users should be evaluated as a potential retention opportunity alongside acquisition efforts.

4. **Users who ride quickly after signing up stay longer.** The gradient from 75% churn (1–7 day activators) to 87.5% churn (365+ day activators) is consistent across large sample sizes. Reducing the gap between account creation and first ride represents one of the strongest testable retention opportunities identified in the dataset.

One thing that looks true but needs a test before acting on it:

5. **Heavy promo users are associated with lower churn — but only among users who already ride frequently.** Among users with 26+ rides, Q4 promo users churn 13–25 percentage points less than Q1. Among users with fewer than 25 rides, the difference is less than 1 percentage point. Do not cut promos for high-frequency Q4 users until you have run a holdout test.

One thing that looks interesting but needs data engineering clarification:

6. **The $80 wallet ceiling.** No churned user has more than $80 in their wallet. This is consistent with a system rule or wallet policy rather than a behavioural pattern. Verify with the data team before drawing any conclusions.

One thing the data shows clearly on the supply side:

7. **Driver supply is stable only because of ongoing recruitment.** Active driver count has been flat for 12 months (5,500–5,815/month). Driver churn is 15.3%. The platform is recruiting to replace departing drivers, not to grow supply. Separately, drivers who stay past 12 months show substantially better performance — meaning early driver attrition is a quality problem, not just a headcount problem.
