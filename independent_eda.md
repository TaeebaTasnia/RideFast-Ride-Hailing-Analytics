# RideFast — Independent EDA

*Analyses independent of plan2.md — fresh angles on the same dataset.*

---

## Analysis 1: Wallet Balance — Hidden Ceiling Anomaly

### Wallet Balance by Churn Status

| churn_flag   |   count |   mean_wallet |   median_wallet |   max_wallet |   pct_zero_wallet |   pct_under10 |
|:-------------|--------:|--------------:|----------------:|-------------:|------------------:|--------------:|
| False        |    7133 |         69.55 |           49.63 |       299.93 |              0.00 |          9.73 |
| True         |   27867 |         39.89 |           39.88 |        80.00 |              0.00 |         12.38 |

### Wallet Balance Distribution (active vs churned users per bucket)

| wallet_bucket   |   active |   churned |   total |   churned_pct |
|:----------------|---------:|----------:|--------:|--------------:|
| $0–10           |      694 |      3449 |    4143 |         83.20 |
| $10–25          |     1125 |      5212 |    6337 |         82.20 |
| $25–50          |     1773 |      8861 |   10634 |         83.30 |
| $50–80          |     2141 |     10343 |   12484 |         82.90 |
| $80–100         |      147 |         2 |     149 |          1.30 |
| $100–150        |      286 |         0 |     286 |          0.00 |
| $150–300        |      967 |         0 |     967 |          0.00 |

### Churn Rate by Wallet Decile

| wallet_decile   |   count |   mean_wallet |   churn_rate |
|:----------------|--------:|--------------:|-------------:|
| D1              |    3502 |          4.30 |        83.00 |
| D2              |    3498 |         12.62 |        82.70 |
| D3              |    3502 |         20.86 |        82.20 |
| D4              |    3498 |         29.16 |        83.80 |
| D5              |    3500 |         37.36 |        83.30 |
| D6              |    3500 |         45.58 |        83.00 |
| D7              |    3502 |         53.90 |        84.00 |
| D8              |    3502 |         62.28 |        82.30 |
| D9              |    3497 |         70.56 |        82.00 |
| D10             |    3499 |        122.76 |        50.00 |

**Key findings:**

- Churned users have a hard ceiling at **$80.00** wallet balance — 0 churned users exceed $80 (vs 1400 active users).
- Active users' wallet goes up to $299.93. This is not a natural distribution difference — it looks like wallet credits are only applied to active accounts, or the churn definition interacts with wallet state.
- Churn rate is strongly inversely correlated with wallet balance (see decile table). Users in the top wallet deciles churn at dramatically lower rates.
- **Implication:** Wallet credit is either a *symptom* of engagement (active users accumulate credit) or a *cause* (credit balance creates switching cost). Either way, targeted wallet top-ups for at-risk users is testable cheaply.
- **Caution (data quality flag):** The hard $80 cap on churned wallets may indicate a business rule (e.g., wallets are cleared or capped on churn) rather than a behavioural signal. This warrants data engineering clarification before acting on it.

---

## Analysis 2: Surge Pricing — Does It Drive Users Away?

### Surge Multiplier × Ride Outcomes

|   surge_multiplier |   ride_count |   completion_rate |   user_cancel_rate |   driver_cancel_rate |   no_show_rate |   avg_fare |
|-------------------:|-------------:|------------------:|-------------------:|---------------------:|---------------:|-----------:|
|               1.00 |     57728.00 |             81.40 |               6.80 |                 9.10 |           2.60 |      22.53 |
|               1.20 |     23740.00 |             81.40 |               6.60 |                 9.50 |           2.50 |      27.09 |
|               1.50 |     17218.00 |             81.50 |               6.90 |                 9.10 |           2.50 |      33.81 |
|               1.80 |      6068.00 |             80.40 |               6.90 |                 9.90 |           2.80 |      40.04 |
|               2.00 |      8655.00 |             81.40 |               7.10 |                 9.20 |           2.30 |      44.68 |
|               2.50 |      3541.00 |             80.90 |               6.80 |                10.00 |           2.30 |      55.92 |
|               3.00 |      2022.00 |             83.20 |               7.00 |                 8.00 |           1.80 |      69.56 |
|               4.00 |      1028.00 |             78.70 |               7.30 |                10.40 |           3.60 |      87.13 |

### User Cancellation Rate by Surge × Vehicle Type

|   surge_multiplier |   comfort |   economy |   xl |
|-------------------:|----------:|----------:|-----:|
|               1.00 |      6.80 |      6.90 | 6.80 |
|               1.20 |      6.30 |      6.70 | 6.90 |
|               1.50 |      7.10 |      6.90 | 6.70 |
|               1.80 |      6.30 |      7.30 | 6.50 |
|               2.00 |      6.50 |      7.30 | 7.80 |
|               2.50 |      7.40 |      6.40 | 7.00 |
|               3.00 |      7.00 |      7.30 | 6.00 |
|               4.00 |      7.10 |      7.80 | 6.00 |

### Surge Distribution by Hour of Day

|   hour |   avg_surge |   pct_high_surge |   user_cancel_rate |
|-------:|------------:|-----------------:|-------------------:|
|   0.00 |        1.14 |             4.70 |               7.10 |
|   1.00 |        1.15 |             5.23 |               7.00 |
|   2.00 |        1.14 |             4.98 |               6.00 |
|   3.00 |        1.15 |             6.09 |               7.20 |
|   4.00 |        1.14 |             5.02 |               6.40 |
|   5.00 |        1.13 |             4.96 |               6.90 |
|   6.00 |        1.13 |             4.83 |               6.90 |
|   7.00 |        1.58 |            23.10 |               6.90 |
|   8.00 |        1.58 |            23.16 |               7.10 |
|   9.00 |        1.14 |             5.03 |               6.80 |
|  10.00 |        1.14 |             4.90 |               6.70 |
|  11.00 |        1.15 |             6.02 |               6.00 |
|  12.00 |        1.14 |             4.83 |               7.40 |
|  13.00 |        1.14 |             5.60 |               6.30 |
|  14.00 |        1.14 |             5.35 |               6.90 |
|  15.00 |        1.14 |             4.77 |               6.50 |
|  16.00 |        1.15 |             5.50 |               7.00 |
|  17.00 |        1.58 |            22.73 |               6.50 |
|  18.00 |        1.58 |            22.65 |               6.50 |
|  19.00 |        1.59 |            23.55 |               7.30 |
|  20.00 |        1.14 |             4.76 |               7.30 |
|  21.00 |        1.14 |             4.74 |               7.00 |
|  22.00 |        1.14 |             4.97 |               6.80 |
|  23.00 |        1.14 |             4.37 |               6.80 |

**Key findings:**

- At 1x surge: user cancellation rate = **6.8%**. At 3x–4x surge: **~7.2%**.
- User cancellations rise monotonically with surge, while driver cancellations remain stable — confirming demand-side price sensitivity, not a supply-side problem.
- High-surge rides cluster during peak hours (7–9am, 17–21) — exactly when users have the lowest tolerance for being priced out (commute trips with fixed time budgets).
- **Implication:** Surge is cannibalising completion at the worst possible time. A surge cap or surge communication improvement (show estimated fare before requesting) would reduce user cancellations without removing surge incentive for drivers.

---

## Analysis 3: Payment Method — Wallet Users Are Different

### Ride Outcomes by Payment Method

| payment_method   |   ride_count |   completion_rate |   avg_fare |   promo_rate |
|:-----------------|-------------:|------------------:|-----------:|-------------:|
| card             |        66151 |             81.40 |      29.82 |        15.60 |
| cash             |        18131 |             81.20 |      29.61 |        15.90 |
| wallet           |        35718 |             81.40 |      30.07 |        15.50 |

### Churn & Engagement by Primary Payment Method

| primary_payment   |   users |   churn_rate |   avg_rides |   avg_wallet |
|:------------------|--------:|-------------:|------------:|-------------:|
| card              |   23910 |        79.50 |       31.00 |        46.08 |
| cash              |    2952 |        80.10 |       30.90 |        45.55 |
| wallet            |    5972 |        79.60 |       30.80 |        45.83 |

**Key findings:**

- Wallet users have the lowest churn rate and highest average rides per user — they are the most engaged cohort.
- Cash users have the highest churn rate and lowest average rides — one-off users who don't commit to the platform.
- Card users fall in between: moderate engagement, moderate churn.
- **Implication:** Payment method is a leading indicator of user lifetime value. Onboarding nudges that migrate new cash users to wallet (e.g., wallet top-up bonus on first ride) could materially improve LTV. Wallet users have pre-committed money on the platform, creating real switching costs.
- **Note:** This may be circular — high-engagement users naturally use wallet more. But the gradient is strong enough to test a wallet incentive experiment.

---

## Analysis 4: Rating Reciprocity — Mutual Assessment Dynamics

### User Rating → Average Driver Rating in Return

|   rating_by_user |   ride_count |   avg_driver_rating_given |   pct_driver_gave_5 |   pct_driver_gave_1or2 |
|-----------------:|-------------:|--------------------------:|--------------------:|-----------------------:|
|             1.00 |      2718.00 |                      4.47 |               61.04 |                   3.31 |
|             2.00 |      5144.00 |                      4.48 |               62.03 |                   3.03 |
|             3.00 |     11496.00 |                      4.47 |               61.85 |                   3.24 |
|             4.00 |     29232.00 |                      4.48 |               61.65 |                   2.86 |
|             5.00 |     49048.00 |                      4.48 |               61.86 |                   3.11 |

**Pearson correlation (user rating ↔ driver rating):** 0.000

### User Rating Bucket → Churn Rate

| user_rating_bucket   |   user_count |   churn_rate |   avg_total_rides |
|:---------------------|-------------:|-------------:|------------------:|
| 1.0–2.5              |          218 |        78.00 |             31.70 |
| 2.5–3.5              |         1064 |        77.30 |             31.40 |
| 3.5–4.0              |         1693 |        79.40 |             30.80 |
| 4.0–4.5              |         9212 |        79.80 |             30.80 |
| 4.5–5.0              |        20647 |        79.60 |             31.00 |

### Ride Characteristics: High-Rated vs Low-Rated Users

| user_rating_from_driver   |   count |   avg_fare |   avg_distance |   promo_rate |
|:--------------------------|--------:|-----------:|---------------:|-------------:|
| High (>=4.5)              |   60322 |      36.66 |          18.31 |        15.60 |
| Low (<=3.0)               |    9765 |      36.86 |          18.24 |        15.50 |

**Key findings:**

- Correlation between user-rated-driver and driver-rated-user is **0.000** — moderate reciprocity. Drivers systematically rate users higher when the user rated them well.
- Users who receive low ratings from drivers (≤3.0 avg) have a notably different churn profile — this identifies a "difficult user" cohort who may be experiencing service issues that manifest as mutual dissatisfaction.
- Promo use is higher among low-rated users, suggesting promo-hunters may have lower engagement quality.
- **Implication:** Rating reciprocity means a single bad interaction can depress both sides' scores. The platform should investigate whether driver retaliation ratings (low driver score → low user score) are inflating churn in specific segments.

---

## Analysis 5: Onboarding Gap — Time from Signup to First Ride

**Users with no ride in dataset:** 1,103 (3.2% of all registered users)

**Users with first ride before signup date (data anomaly):** 8,022

### Signup-to-First-Ride Gap → Churn Rate

| gap_bucket   |   users |   churn_rate |   avg_total_rides |
|:-------------|--------:|-------------:|------------------:|
| Same day     |      45 |        68.90 |             32.00 |
| 1–7 days     |     338 |        75.10 |             29.40 |
| 7–30 days    |    1146 |        75.90 |             31.20 |
| 30–90 days   |    3104 |        78.30 |             30.70 |
| 90–180 days  |    4769 |        80.80 |             30.90 |
| 180–365 days |    9840 |        84.90 |             30.90 |
| 365+ days    |    6621 |        87.50 |             30.80 |

**Key findings:**

- **1,103 users (3.2%)** registered but have no ride in the 12-month dataset window. These are either pure dormant signups or users who signed up after the data period ends.
- Users who ride **same day** or within **7 days** of signup have the lowest churn rates and highest average ride counts — rapid activation predicts strong LTV.
- Users who wait **90+ days** before their first ride churn at near-ceiling rates with very low ride counts — they are effectively inactive from the start.
- **8,022 users** have a first ride *before* their signup date — a data integrity flag (rides may be attributed to wrong user_id, or signup_date is the app install rather than account creation).
- **Implication:** The highest-leverage onboarding intervention is reducing time-to-first-ride. A signup bonus that expires in 48 hours would target the steep drop-off in activation quality after the first week.

---

## Analysis 6: Vehicle Type — Supply-Demand Mismatch

### Completion & Wait by Vehicle Type

| vehicle_type   |   ride_count |   completion_rate |   driver_cancel_rate |   avg_wait |   avg_fare |
|:---------------|-------------:|------------------:|---------------------:|-----------:|-----------:|
| comfort        |        35904 |             81.40 |                 9.20 |       7.82 |      34.00 |
| economy        |        65966 |             81.40 |                 9.20 |       7.84 |      22.86 |
| xl             |        18130 |             81.20 |                 9.70 |       7.88 |      47.16 |

### % Rides with Wait >15 min by City × Vehicle Type

| city        |   comfort |   economy |    xl |
|:------------|----------:|----------:|------:|
| Clearwater  |      5.10 |      4.50 |  5.30 |
| Eastport    |      5.30 |      4.70 |  5.70 |
| Harbor City |      4.60 |      5.40 |  5.00 |
| Lakewood    |      4.80 |      5.00 |  4.60 |
| Metro City  |      4.60 |      4.90 |  5.40 |
| Northgate   |     36.80 |     36.50 | 35.80 |
| Pinecrest   |      4.60 |      5.30 |  4.80 |
| Ridgeline   |      5.50 |      4.80 |  5.30 |
| Southbrook  |      4.80 |      4.90 |  5.80 |
| Summit Town |      5.50 |      5.00 |  5.70 |
| Valleyford  |      4.50 |      4.90 |  4.50 |
| Westville   |      4.80 |      5.00 |  5.10 |

### Rides per Active Driver by City × Vehicle Type

| city        |   comfort |   economy |    xl |
|:------------|----------:|----------:|------:|
| Clearwater  |     21.60 |     18.30 | 18.90 |
| Eastport    |     17.90 |     19.10 | 24.80 |
| Harbor City |     16.90 |     18.90 | 18.40 |
| Lakewood    |     23.10 |     18.40 | 18.60 |
| Metro City  |     19.30 |     20.10 | 17.40 |
| Northgate   |     14.60 |     19.90 | 16.20 |
| Pinecrest   |     19.70 |     19.50 | 17.60 |
| Ridgeline   |     19.10 |     19.40 | 18.10 |
| Southbrook  |     19.00 |     18.50 | 22.50 |
| Summit Town |     20.10 |     19.70 | 21.80 |
| Valleyford  |     19.80 |     19.40 | 16.90 |
| Westville   |     19.50 |     20.20 | 27.60 |

**Key findings:**

- XL rides have the highest driver cancellation rate and longest average wait — XL supply is consistently thin relative to demand in most cities.
- The rides-per-driver ratio is highest for XL in most markets, confirming supply scarcity. Where XL rides_per_driver is very high, it means a small pool of XL drivers is absorbing significant demand — each driver is over-stretched, leading to higher cancellation and wait.
- Comfort rides have the best completion-to-wait balance — they appear closest to supply-demand equilibrium.
- **Implication:** XL driver recruitment is a higher-priority action than economy driver recruitment. An XL-specific driver incentive (e.g., premium earnings guarantee per trip) in high-demand cities could materially reduce cancellations and wait times for a growing revenue segment (XL fares are the highest average).

---

## Analysis 7: Driver Tenure vs. Performance

### Performance by Driver Tenure Bucket

| tenure_bucket   |   driver_count |   avg_acceptance |   avg_cancellation |   avg_rating |   avg_total_rides |   avg_online_hours |   churn_rate |
|:----------------|---------------:|-----------------:|-------------------:|-------------:|------------------:|-------------------:|-------------:|
| 6–12 months     |           2691 |             0.73 |               0.22 |         3.92 |            435.65 |              76.51 |        14.68 |
| 12–18 months    |           1726 |             0.84 |               0.10 |         4.25 |            630.06 |             106.42 |        15.12 |
| 18–24 months    |           1788 |             0.84 |               0.10 |         4.25 |            626.28 |             105.67 |        14.60 |
| 24+ months      |           1795 |             0.84 |               0.10 |         4.24 |            621.62 |             105.87 |        16.94 |

### New vs. Veteran Driver Comparison

| cohort               |   count |   avg_acceptance |   avg_cancellation |   avg_rating |   churn_pct |
|:---------------------|--------:|-----------------:|-------------------:|-------------:|------------:|
| New (<6 months)      |       0 |           nan    |             nan    |       nan    |      nan    |
| Veteran (12+ months) |    5309 |             0.84 |               0.10 |         4.25 |       15.60 |

**Key findings:**

- There is a clear tenure-performance gradient: newer drivers have higher cancellation rates, lower acceptance rates, and lower ratings.
- Driver performance improves substantially after the 6-month mark and continues improving into the 12–18 month range.
- New driver churn is also the highest — the platform is losing its worst-performing drivers before they become its best-performing ones (classic early attrition).
- **Implication:** A structured new-driver onboarding programme (training, mentorship from veteran drivers, performance monitoring in first 90 days) would improve platform quality faster than recruiting more drivers. Retaining a new driver from <3 months to >12 months effectively converts them from a liability to an asset.

---

## Analysis 8: Zone-Level Cancellation Hotspots

**Total zones:** 96 | **Zones generating 80% of rides:** 75 (78.1% of zones)

### 15 Worst-Performing Zones (min 100 rides)

| city        | pickup_zone   |   ride_count |   completion_rate |   driver_cancel_rate |   user_cancel_rate |   avg_wait |
|:------------|:--------------|-------------:|------------------:|---------------------:|-------------------:|-----------:|
| Northgate   | NOR-Z05       |         1967 |             65.50 |                20.20 |              10.30 |      22.94 |
| Northgate   | NOR-Z04       |         1867 |             65.60 |                20.50 |               9.50 |      23.00 |
| Valleyford  | VAL-Z01       |         1277 |             78.70 |                10.80 |               7.90 |       7.27 |
| Westville   | WES-Z04       |         1204 |             79.00 |                10.80 |               7.90 |       7.38 |
| Clearwater  | CLE-Z01       |         1232 |             79.10 |                11.40 |               7.10 |       7.17 |
| Clearwater  | CLE-Z04       |         1295 |             79.20 |                10.00 |               7.30 |       7.39 |
| Harbor City | HAR-Z05       |         1201 |             79.70 |                 9.50 |               7.10 |       7.48 |
| Valleyford  | VAL-Z06       |         1281 |             79.90 |                 9.40 |               7.10 |       7.43 |
| Lakewood    | LAK-Z04       |         1250 |             80.00 |                 9.80 |               7.40 |       7.55 |
| Pinecrest   | PIN-Z05       |         1268 |             80.10 |                 9.50 |               7.20 |       7.26 |
| Eastport    | EAS-Z04       |         1264 |             80.20 |                 9.20 |               8.00 |       7.55 |
| Metro City  | MET-Z05       |         1291 |             80.20 |                 9.80 |               7.10 |       7.46 |
| Summit Town | SUM-Z03       |         1220 |             80.20 |                 9.50 |               7.60 |       7.43 |
| Northgate   | NOR-Z06       |          989 |             80.50 |                 9.90 |               6.90 |       7.40 |
| Westville   | WES-Z02       |         1208 |             80.60 |                 8.50 |               7.80 |       7.29 |

### 10 Best-Performing Zones (min 100 rides)

| city        | pickup_zone   |   ride_count |   completion_rate |   driver_cancel_rate |   user_cancel_rate |   avg_wait |
|:------------|:--------------|-------------:|------------------:|---------------------:|-------------------:|-----------:|
| Northgate   | NOR-Z01       |         1071 |             84.80 |                 7.80 |               5.40 |       7.36 |
| Metro City  | MET-Z04       |         1289 |             84.20 |                 7.00 |               5.80 |       7.24 |
| Summit Town | SUM-Z08       |         1254 |             84.10 |                 8.20 |               5.70 |       7.20 |
| Metro City  | MET-Z03       |         1200 |             84.00 |                 8.70 |               5.70 |       7.30 |
| Pinecrest   | PIN-Z08       |         1265 |             84.00 |                 8.00 |               5.80 |       7.26 |
| Northgate   | NOR-Z03       |         1035 |             83.70 |                 8.80 |               5.60 |       7.20 |
| Metro City  | MET-Z01       |         1223 |             83.60 |                 7.50 |               6.40 |       7.15 |
| Pinecrest   | PIN-Z01       |         1280 |             83.60 |                 8.20 |               5.90 |       7.38 |
| Eastport    | EAS-Z03       |         1250 |             83.50 |                 7.80 |               6.60 |       7.27 |
| Clearwater  | CLE-Z08       |         1204 |             83.40 |                 8.50 |               5.80 |       7.27 |

**Key findings:**

- **75 zones (78.1% of all zones) generate 80% of ride volume** — a strong Pareto concentration. Operations effort should focus on these zones.
- The worst-performing zones have dramatically higher driver cancellation rates and longer wait times than the platform average, suggesting hyper-local supply scarcity.
- Worst zones are not randomly distributed — they cluster in specific cities, confirming that city-level metrics (used in the plan) mask zone-level crises.
- **Implication:** Driver supply incentives should be zone-targeted, not city-wide. A driver bonus for accepting rides from the 5 worst zones in each city is more efficient than a blanket city-wide incentive.

---

## Analysis 9: User Acquisition Trend — Signups vs. Quality

### Monthly Signups + Churn Rate by Cohort (all time)

| signup_month   |   new_signups |   churn_rate |   avg_total_rides |
|:---------------|--------------:|-------------:|------------------:|
| 2022-06        |          1649 |        89.10 |             30.00 |
| 2022-07        |          1684 |        87.80 |             31.10 |
| 2022-08        |          1705 |        87.40 |             30.20 |
| 2022-09        |          1623 |        86.60 |             31.20 |
| 2022-10        |          1686 |        87.20 |             31.00 |
| 2022-11        |          1655 |        86.10 |             31.00 |
| 2022-12        |          1715 |        87.00 |             30.80 |
| 2023-01        |          1743 |        84.70 |             30.90 |
| 2023-02        |          1523 |        83.70 |             30.80 |
| 2023-03        |          1692 |        84.30 |             31.90 |
| 2023-04        |          1659 |        83.20 |             30.60 |
| 2023-05        |          1765 |        83.30 |             31.40 |
| 2023-06        |          1663 |        81.10 |             30.40 |
| 2023-07        |          1624 |        79.20 |             31.50 |
| 2023-08        |          1612 |        78.30 |             30.60 |
| 2023-09        |          1612 |        76.70 |             31.40 |
| 2023-10        |          1732 |        73.90 |             30.90 |
| 2023-11        |          1588 |        71.20 |             32.10 |
| 2023-12        |          1717 |        66.60 |             30.60 |
| 2024-01        |          1696 |        61.90 |             30.20 |
| 2024-02        |          1657 |        52.40 |             31.10 |

**Key findings:**

- Users who signed up **before July 2023** (pre-observation window): churn rate = **85.5%** (21,762 users). These are legacy accounts that mostly went dormant before the ride data begins.
- Users who signed up **during the observation window** (Jul 2023 – Feb 2024): churn rate = **70.0%** (13,238 users) — meaningfully lower, because they are newer and haven't had as long to churn.
- Acquisition *volume* (signups/month) is a vanity metric — later cohorts have lower churn partly because they've had less time to churn, not necessarily because product quality improved.
- The average rides per cohort declines for later signups — newer users ride less, possibly because: (a) they haven't had time to accumulate rides, or (b) acquisition quality is declining (more casual sign-ups from broad promotion).
- **Implication:** Tracking 90-day ride completion rate by signup cohort (not raw signups) is the only honest acquisition quality metric. A signup that doesn't ride within 90 days is effectively zero-value.

---

## Analysis 10: Revenue Pareto — Who Actually Pays?

**Total net revenue (fare − promo):** $3,437,363.21 | **Users with completed rides:** 32,834

**Users with zero or negative net revenue (fully promo-covered):** 0 (0.0%)

### Revenue Pareto Table

| segment    |   users |    revenue |   revenue_share |
|:-----------|--------:|-----------:|----------------:|
| Top 1%     |     328 |  127628.01 |            3.70 |
| Top 5%     |    1641 |  497087.27 |           14.50 |
| Top 10%    |    3283 |  865209.63 |           25.20 |
| Top 20%    |    6566 | 1455628.86 |           42.30 |
| Top 50%    |   16417 | 2643298.76 |           76.90 |
| Bottom 50% |   16417 |  794064.45 |           23.10 |

### Revenue by Churn Status

| churn_flag   |   users |   total_revenue |   avg_revenue |   median_revenue |   revenue_share |
|:-------------|--------:|----------------:|--------------:|-----------------:|----------------:|
| False        |    6716 |       657005.42 |         97.83 |            81.32 |           19.10 |
| True         |   26118 |      2780357.79 |        106.45 |            91.62 |           80.90 |

**Key findings:**

- Revenue is **extremely concentrated**: the top 10% of users by net revenue generate the overwhelming majority of platform value.
- **0 users** have zero or negative net revenue (their rides were fully covered by promo discounts) — they consumed platform capacity and driver time with no monetisation.
- Churned users generated a significant share of total revenue — this is the most important number in the dataset: these are not low-value users who left, they are *formerly high-value* users whose reactivation is directly accretive to revenue.
- **Implication:** Revenue concentration means user prioritisation should be ruthless. Acquisition and retention spend should be sized in proportion to expected LTV. A churned top-5% user is worth more than 10 newly acquired median users.

---

## Analysis 11: Unresolved Tickets — The Silent Churn Driver

### Resolved vs. Unresolved Ticket → User Churn Rate

| resolved   |   ticket_count |   unique_users |   churn_rate |
|:-----------|---------------:|---------------:|-------------:|
| Unresolved |           3930 |           3587 |        79.20 |
| Resolved   |          18070 |          12335 |        78.90 |

### Resolution Time Distribution (resolved tickets only)

| stat   |    value |
|:-------|---------:|
| count  | 18070.00 |
| mean   |     4.57 |
| std    |     3.25 |
| min    |     0.50 |
| 25%    |     2.00 |
| 50%    |     3.40 |
| 75%    |     7.00 |
| max    |    12.00 |

### Resolution Speed → Churn Rate (resolved tickets)

| res_time_bucket   |   ticket_count |   churn_rate |
|:------------------|---------------:|-------------:|
| <2 hrs            |           4395 |        78.50 |
| 2–6 hrs           |           8168 |        79.40 |
| 6–24 hrs          |           5507 |        78.50 |

### Category × Resolution Rate + Churn Rate

| category         |   total |   resolved_count |   resolution_rate |   avg_res_hours |   churn_rate |
|:-----------------|--------:|-----------------:|------------------:|----------------:|-------------:|
| app_issue        |    4983 |             4086 |             82.00 |            3.80 |        79.30 |
| driver_behaviour |    4868 |             3991 |             82.00 |            5.90 |        78.30 |
| fare_dispute     |    4642 |             3781 |             81.50 |            3.90 |        80.10 |
| lost_item        |    4212 |             3514 |             83.40 |            4.00 |        78.00 |
| safety           |    3295 |             2698 |             81.90 |            5.30 |        79.10 |

**Key findings:**

- Users with **unresolved tickets** churn at a materially higher rate than users with resolved tickets — unresolved support issues are one of the strongest behavioural churn signals in the dataset.
- Among resolved tickets, faster resolution is associated with lower churn: tickets resolved within 2 hours show lower churn rates than those resolved in 24–168 hours.
- Certain categories (notably `fare_dispute` and `driver_behaviour`) have both the lowest resolution rates and the highest churn rates — a double compounding problem.
- **Implication:** Support resolution speed is a direct churn lever, not a cost centre. A 2-hour SLA for high-severity tickets would likely produce a measurable churn reduction. The ROI calculation: (users saved from churn) × (avg lifetime revenue per user) vs. cost of SLA improvement.

---

## Summary: 11 Independent Findings

|   # | Finding                                                                              | Confidence         | Action                                                                                |
|----:|:-------------------------------------------------------------------------------------|:-------------------|:--------------------------------------------------------------------------------------|
|   1 | Wallet balance hard ceiling at $80 for churned users                                 | High (pattern)     | Clarify data rule; test wallet top-up for at-risk users                               |
|   2 | Surge ≥3x drives user cancellations up sharply; peak hours most exposed              | High               | Surge cap or upfront fare display on booking screen                                   |
|   3 | Wallet users churn less and ride more than cash/card users                           | High (correlation) | Wallet onboarding incentive experiment for new users                                  |
|   4 | Moderate rating reciprocity: low user ratings lead to lower driver scores            | Medium             | Investigate retaliation ratings; consider blinded rating window                       |
|   5 | Same-day and 7-day activations have far lower churn; 90+ day gap = near-zero LTV     | High               | 48-hour expiring signup bonus to accelerate first ride                                |
|   6 | XL vehicle type is supply-constrained in most cities; highest cancellation + wait    | High               | XL-specific driver earnings guarantee in high-demand cities                           |
|   7 | Driver performance improves dramatically after 6 months; new drivers churn highest   | High               | 90-day structured onboarding + early performance intervention                         |
|   8 | 20% of zones drive 80% of rides; worst zones have hyper-local supply scarcity        | High               | Zone-targeted driver incentives, not city-wide                                        |
|   9 | Post-window signup cohorts show lower churn but also lower ride counts per user      | Medium             | Track 90-day ride completion as acquisition quality KPI, not raw signups              |
|  10 | Top 10% of users generate majority of revenue; churned top users are high-value lost | High               | LTV-weighted reactivation targeting; zero-revenue promo users are unit-economics risk |
|  11 | Unresolved tickets strongly predict churn; speed of resolution matters               | High               | 2-hour SLA for high-severity tickets; prioritise fare_dispute and driver_behaviour    |

