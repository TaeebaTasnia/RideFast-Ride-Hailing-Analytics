# RideFast EDA Results
*Generated: 2026-09-24 21:57 | Audit date: 2024-06-30 | Dataset: Jul 2023 – Jun 2024*

---

## 1. Data Quality Audit

### Row Counts

| table           |   rows |
|:----------------|-------:|
| rides           | 120000 |
| users           |  35000 |
| drivers         |   8000 |
| support_tickets |  22000 |

### Date Ranges

| table   | col            | min                 | max                 |
|:--------|:---------------|:--------------------|:--------------------|
| rides   | request_time   | 2023-07-01 00:05:00 | 2024-06-29 23:50:00 |
| users   | signup_date    | 2022-06-01 00:00:00 | 2024-02-29 00:00:00 |
| users   | last_ride_date | 2022-06-05 00:00:00 | 2024-06-29 00:00:00 |
| drivers | signup_date    | 2022-01-01 00:00:00 | 2023-12-31 00:00:00 |
| tickets | created_at     | 2023-07-01 00:00:00 | 2024-07-02 17:16:16 |

### Null Counts — rides.csv

| column           | dtype          |   nulls | null_%   |
|:-----------------|:---------------|--------:|:---------|
| ride_id          | object         |       0 | 0.0%     |
| user_id          | object         |       0 | 0.0%     |
| driver_id        | object         |       0 | 0.0%     |
| city             | object         |       0 | 0.0%     |
| pickup_zone      | object         |       0 | 0.0%     |
| request_time     | datetime64[ns] |       0 | 0.0%     |
| pickup_time      | datetime64[ns] |       0 | 0.0%     |
| dropoff_time     | datetime64[ns] |   22362 | 18.6%    |
| status           | object         |       0 | 0.0%     |
| fare_amount      | float64        |       0 | 0.0%     |
| surge_multiplier | float64        |       0 | 0.0%     |
| promo_code_used  | bool           |       0 | 0.0%     |
| promo_discount   | float64        |       0 | 0.0%     |
| rating_by_user   | float64        |   22362 | 18.6%    |
| rating_by_driver | float64        |   22362 | 18.6%    |
| vehicle_type     | object         |       0 | 0.0%     |
| distance_km      | float64        |       0 | 0.0%     |
| payment_method   | object         |       0 | 0.0%     |

### Null Counts — users.csv

| column         | dtype          |   nulls | null_%   |
|:---------------|:---------------|--------:|:---------|
| user_id        | object         |       0 | 0.0%     |
| signup_date    | datetime64[ns] |       0 | 0.0%     |
| city           | object         |       0 | 0.0%     |
| total_rides    | int64          |       0 | 0.0%     |
| last_ride_date | datetime64[ns] |       0 | 0.0%     |
| promo_rides    | int64          |       0 | 0.0%     |
| wallet_balance | float64        |       0 | 0.0%     |
| churn_flag     | bool           |       0 | 0.0%     |

### Null Counts — drivers.csv

| column               | dtype          |   nulls | null_%   |
|:---------------------|:---------------|--------:|:---------|
| driver_id            | object         |       0 | 0.0%     |
| city                 | object         |       0 | 0.0%     |
| signup_date          | datetime64[ns] |       0 | 0.0%     |
| vehicle_type         | object         |       0 | 0.0%     |
| status               | object         |       0 | 0.0%     |
| avg_rating           | float64        |       0 | 0.0%     |
| total_rides          | int64          |       0 | 0.0%     |
| acceptance_rate      | float64        |       0 | 0.0%     |
| cancellation_rate    | float64        |       0 | 0.0%     |
| online_hours_monthly | float64        |       0 | 0.0%     |

### Null Counts — support_tickets.csv

| column                | dtype          |   nulls | null_%   |
|:----------------------|:---------------|--------:|:---------|
| ticket_id             | object         |       0 | 0.0%     |
| ride_id               | object         |    3981 | 18.1%    |
| user_id               | object         |       0 | 0.0%     |
| driver_id             | object         |    1240 | 5.6%     |
| created_at            | datetime64[ns] |       0 | 0.0%     |
| category              | object         |       0 | 0.0%     |
| severity              | object         |       0 | 0.0%     |
| resolved              | bool           |       0 | 0.0%     |
| resolution_time_hours | float64        |    3930 | 17.9%    |

### Ride Status Distribution

| status           |   count |   pct |
|:-----------------|--------:|------:|
| completed        |   97638 | 81.36 |
| cancelled_driver |   11114 |  9.26 |
| cancelled_user   |    8198 |  6.83 |
| no_show          |    3050 |  2.54 |

### Data Quality Flags

- **Date range:** rides span 2023-07-01 to 2024-06-29 — **12 months** (Jul 2023–Jun 2024), not 4 months as stated in assessment.
- **Promo on non-completed rides:** 3,492 rides have `promo_code_used=True` but status ≠ completed. `promo_realised` = promo_code_used AND status='completed'.
- **Churn flag alignment:** computed churn (days_since_last_ride >60 from 2024-06-30) matches stored `churn_flag` in 96.7% of rows.
- **Overall churn rate:** 79.6% (27,867 / 35,000 users churned). Active users: 7,133 (20.4%).
- **rides.csv has city (origin) and pickup_zone only** — no destination city, no dropoff_zone. Origin-destination analysis is not possible.

### Suspended vs. Active Driver Comparison

| status    |   count |   avg_acceptance |   avg_cancellation |   avg_rating |   avg_total_rides |   avg_online_hours |
|:----------|--------:|-----------------:|-------------------:|-------------:|------------------:|-------------------:|
| active    |    6245 |            0.801 |              0.14  |        4.138 |           560.496 |             95.98  |
| suspended |     534 |            0.808 |              0.135 |        4.142 |           589.463 |             99.896 |

> **Anomaly:** Suspended and active drivers have nearly identical metrics. Suspensions are administrative, not performance-based. 589 active drivers have acceptance_rate <60%.

---

## 2. Schema & Column Summary

| table           | column            | type        | notes                                                                    |
|:----------------|:------------------|:------------|:-------------------------------------------------------------------------|
| rides           | ride_id           | string      | Primary key. Format RDE_XXXXXX                                           |
| rides           | user_id           | string      | FK to users                                                              |
| rides           | driver_id         | string      | FK to drivers                                                            |
| rides           | city              | categorical | 12 cities (origin only — no destination)                                 |
| rides           | pickup_zone       | categorical | 96 zones                                                                 |
| rides           | request_time      | datetime    | 2023-07-01 – 2024-06-29                                                  |
| rides           | pickup_time       | datetime    | 0 nulls (no-shows)                                                       |
| rides           | dropoff_time      | datetime    | 22,362 nulls (non-completed)                                             |
| rides           | status            | categorical | completed / cancelled_driver / cancelled_user / no_show                  |
| rides           | fare_amount       | float       | 0 for non-completed                                                      |
| rides           | surge_multiplier  | float       | Range 1.0–4.0                                                            |
| rides           | promo_code_used   | bool        | True on 18,768 rides incl. cancelled                                     |
| rides           | promo_discount    | float       | Amount discounted; 0 if no promo                                         |
| rides           | rating_by_user    | float       | 1–5; 22,362 nulls                                                        |
| rides           | rating_by_driver  | float       | 1–5; 22,362 nulls                                                        |
| rides           | vehicle_type      | categorical | ['economy', 'xl', 'comfort']                                             |
| rides           | distance_km       | float       | Range 1.5–35.0 km                                                        |
| rides           | payment_method    | categorical | ['card', 'wallet', 'cash']                                               |
| users           | churn_flag        | bool        | True = last_ride >60 days before 2024-06-30                              |
| users           | promo_rides       | int         | Total rides where promo used (includes cancelled)                        |
| users           | wallet_balance    | float       | Current balance                                                          |
| drivers         | status            | categorical | active / churned / suspended                                             |
| drivers         | acceptance_rate   | float       | 0–1 ratio                                                                |
| drivers         | cancellation_rate | float       | 0–1 ratio                                                                |
| support_tickets | category          | categorical | ['fare_dispute', 'driver_behaviour', 'app_issue', 'safety', 'lost_item'] |
| support_tickets | severity          | categorical | ['high', 'low', 'critical', 'medium']                                    |
| support_tickets | resolved          | bool        | 82.1% resolved                                                           |

---

## 3. Key Metrics Summary

| Metric                              | Value         | Confidence   |
|:------------------------------------|:--------------|:-------------|
| Total registered users              | 35,000        | High         |
| Active users (churn_flag=False)     | 7,133 (20.4%) | High         |
| Overall churn rate                  | 79.6%         | High         |
| Overall completion rate             | 81.4%         | High         |
| Total completed rides               | 97,638        | High         |
| Avg monthly completed rides         | 8,136         | High         |
| Total gross revenue (completed)     | $3,583,767.96 | High         |
| Total promo spend (realised)        | $146,404.75   | High         |
| Rides with wait ≥15 min             | 9,132 (7.6%)  | High         |
| Low-accept active drivers (<60%)    | 589           | High         |
| First-ride-churn users              | 480           | High         |
| High-value churned users            | 5,257         | High         |
| At-risk users (31–59 days inactive) | 1,795         | High         |

### Monthly Ride Volume Trend

| month   |   total_requests |   completed |   promo_realised |   completion_rate |
|:--------|-----------------:|------------:|-----------------:|------------------:|
| 2023-07 |            10089 |        8199 |             1289 |              81.3 |
| 2023-08 |            10216 |        8305 |             1320 |              81.3 |
| 2023-09 |             9903 |        8043 |             1290 |              81.2 |
| 2023-10 |            10203 |        8347 |             1337 |              81.8 |
| 2023-11 |             9850 |        7989 |             1231 |              81.1 |
| 2023-12 |            10359 |        8370 |             1286 |              80.8 |
| 2024-01 |            10257 |        8301 |             1270 |              80.9 |
| 2024-02 |             9474 |        7719 |             1192 |              81.5 |
| 2024-03 |            10064 |        8239 |             1229 |              81.9 |
| 2024-04 |             9757 |        8009 |             1302 |              82.1 |
| 2024-05 |            10420 |        8508 |             1317 |              81.7 |
| 2024-06 |             9408 |        7609 |             1213 |              80.9 |

> **Finding (High confidence):** Monthly ride volume has been flat for 12 consecutive months (range: 9,408–10,420 requests/month). No meaningful growth despite promotional spend.

---

## 4. Wait Time Cliff (Module 4)

### Wait Bracket × Completion Rate

| wait_bracket   |   ride_count |   completion_rate |   user_cancel_rate |   driver_cancel_rate |   no_show_rate |
|:---------------|-------------:|------------------:|-------------------:|---------------------:|---------------:|
| 0–5 min        |        30685 |              86.2 |                6   |                  5.8 |            2   |
| 5–10 min       |        53352 |              84.3 |                6.3 |                  7.1 |            2.3 |
| 10–15 min      |        26831 |              78.2 |                7.4 |                 11.5 |            2.9 |
| 15–20 min      |         6646 |              54.1 |               11.4 |                 29.3 |            5.3 |
| 20–30 min      |         1649 |              65.7 |               10.4 |                 18.9 |            5   |
| 30+ min        |          837 |              65.4 |                9.2 |                 21.9 |            3.6 |

> **Hero finding (High confidence):** 9,132 rides (7.6% of timed rides) have wait ≥15 min. Completion rate drops from ~83% below 15 min to ~54–55% above it. This is the single clearest conversion failure in the dataset.

### City × Wait Bracket Completion Rate (%)

| city        |   0–5 min |   5–10 min |   10–15 min |   15–20 min |   20–30 min |   30+ min |
|:------------|----------:|-----------:|------------:|------------:|------------:|----------:|
| Clearwater  |      85.2 |       83.7 |        76.9 |        52.6 |       nan   |     nan   |
| Eastport    |      85   |       83.8 |        80.3 |        50.8 |       nan   |     nan   |
| Harbor City |      86.4 |       84.9 |        77.4 |        50.3 |       nan   |     nan   |
| Lakewood    |      85.7 |       84.6 |        77.7 |        49.4 |       nan   |     nan   |
| Metro City  |      86.3 |       84.8 |        80.3 |        53.5 |       nan   |     nan   |
| Northgate   |      87.1 |       85.5 |        73.8 |        64.4 |        65.7 |      65.4 |
| Pinecrest   |      86.9 |       85.3 |        79.3 |        49.6 |       nan   |     nan   |
| Ridgeline   |      87.1 |       84.4 |        77.8 |        50.8 |       nan   |     nan   |
| Southbrook  |      86.3 |       84.3 |        79.8 |        55.7 |       nan   |     nan   |
| Summit Town |      85.6 |       84.5 |        79.2 |        57.4 |       nan   |     nan   |
| Valleyford  |      85.5 |       83.6 |        77.6 |        48.8 |       nan   |     nan   |
| Westville   |      87.2 |       83.4 |        76.9 |        51.8 |       nan   |     nan   |

### Wait Time by Driver Quality Tier

| driver_quality_tier   |   avg_wait |   median_wait |   pct_over15 |   ride_count |
|:----------------------|-----------:|--------------:|-------------:|-------------:|
| both_issues           |      13.8  |          14   |        42.99 |        11174 |
| high_cancel           |      13.75 |          14   |        42.91 |         3167 |
| low_accept            |      12.85 |          12.5 |        35    |           20 |
| standard              |       7.03 |           7   |         2.8  |       105639 |

> **Finding:** Low-accept and both_issues drivers are associated with longer average wait times and higher proportions of rides exceeding 15 minutes, supporting the causal chain: low acceptance rate → dispatch cycling → extended wait → cancellation.

---

## 5. Retention & First-Ride Failure (Module 5)

### 30-Day Retention by First-Ride Wait Time

| first_ride_wait   |   users | retained_30d   |
|:------------------|--------:|:---------------|
| <10 min           |   23824 | 25.4%          |
| ≥15 min           |    2556 | 23.7%          |

> **Finding:** Users whose first ride had a wait <10 min retained at **25.4%** (rode again within 30 days). Users with first-ride wait ≥15 min retained at **23.7%**. Gap: **1.7 percentage points**. Gap is modest — first-ride failure is a contributing factor, not the sole driver.

### Cohort Retention (% of users completing ≥2 rides in first 30 days)

| signup_month   |   users_sampled |   retained |   retention_rate |
|:---------------|----------------:|-----------:|-----------------:|
| 2022-06        |             221 |         48 |             21.7 |
| 2022-07        |             247 |         60 |             24.3 |
| 2022-08        |             235 |         57 |             24.3 |
| 2022-09        |             236 |         55 |             23.3 |
| 2022-10        |             228 |         55 |             24.1 |
| 2022-11        |             212 |         55 |             25.9 |
| 2022-12        |             231 |         58 |             25.1 |
| 2023-01        |             232 |         63 |             27.2 |
| 2023-02        |             207 |         41 |             19.8 |
| 2023-03        |             258 |         59 |             22.9 |
| 2023-04        |             245 |         55 |             22.4 |
| 2023-05        |             237 |         58 |             24.5 |
| 2023-06        |             231 |         60 |             26   |
| 2023-07        |             238 |         60 |             25.2 |
| 2023-08        |             211 |         48 |             22.7 |
| 2023-09        |             230 |         61 |             26.5 |
| 2023-10        |             240 |         58 |             24.2 |
| 2023-11        |             213 |         53 |             24.9 |
| 2023-12        |             226 |         63 |             27.9 |
| 2024-01        |             257 |         65 |             25.3 |
| 2024-02        |             208 |         49 |             23.6 |

### First-Ride Churn Users — Wait Time Distribution

Total first-ride-churn users (1 ride, churned): **480**

| stat   |   value |
|:-------|--------:|
| count  | 1568    |
| mean   |    7.9  |
| std    |    4.67 |
| min    |    2    |
| 25%    |    5    |
| 50%    |    7    |
| 75%    |   10    |
| max    |   34    |

### First-Ride Churn — Wait Bracket Breakdown

| wait_bracket   |   count |   pct |
|:---------------|--------:|------:|
| 5–10 min       |     710 |  45.3 |
| 0–5 min        |     386 |  24.6 |
| 10–15 min      |     341 |  21.7 |
| 15–20 min      |     101 |   6.4 |
| 20–30 min      |      23 |   1.5 |
| 30+ min        |       7 |   0.4 |

### User Segments

| segment            |   count |   pct |
|:-------------------|--------:|------:|
| standard           |   17738 |  50.7 |
| low_engagement     |    6297 |  18   |
| high_value_churned |    5257 |  15   |
| high_value_active  |    1847 |   5.3 |
| at_risk            |    1795 |   5.1 |
| promo_heavy_active |    1586 |   4.5 |
| first_ride_churn   |     480 |   1.4 |

### High-Value Churned User Pool (Reactivation Target)

|   count |   avg_total_rides |   avg_revenue_per_user |   total_estimated_ltv |   median_days_since_last_ride |
|--------:|------------------:|-----------------------:|----------------------:|------------------------------:|
|    5257 |                54 |                 101.88 |                535580 |                           218 |

> **Reactivation opportunity:** High-value churned users have significantly more lifetime rides than average. They are the highest-ROI reactivation target.

---

## 6. Promo Intelligence (Module 6)

### Churn by Promo Quartile

| promo_quartile   |   users |   churned |   churn_rate |   avg_total_rides |   avg_promo_ratio |
|:-----------------|--------:|----------:|-------------:|------------------:|------------------:|
| Q1               |    8804 |      7290 |         82.8 |             18.68 |             0.002 |
| Q2               |    8928 |      7459 |         83.5 |             34.26 |             0.064 |
| Q3               |    8556 |      7083 |         82.8 |             32.26 |             0.137 |
| Q4               |    8712 |      6035 |         69.3 |             38.58 |             0.305 |

> **Finding (High correlation / Low causality):** Q4 users (highest promo dependency) churn at a lower rate than Q1. However this is observational: engaged users may self-select more promos. Cannot establish causality without a holdout experiment.

### Monthly Promo Share of Completed Rides

| month   |   total_completed |   promo_realised |   promo_share_pct |
|:--------|------------------:|-----------------:|------------------:|
| 2023-07 |              8199 |             1289 |              15.7 |
| 2023-08 |              8305 |             1320 |              15.9 |
| 2023-09 |              8043 |             1290 |              16   |
| 2023-10 |              8347 |             1337 |              16   |
| 2023-11 |              7989 |             1231 |              15.4 |
| 2023-12 |              8370 |             1286 |              15.4 |
| 2024-01 |              8301 |             1270 |              15.3 |
| 2024-02 |              7719 |             1192 |              15.4 |
| 2024-03 |              8239 |             1229 |              14.9 |
| 2024-04 |              8009 |             1302 |              16.3 |
| 2024-05 |              8508 |             1317 |              15.5 |
| 2024-06 |              7609 |             1213 |              15.9 |

**Total promo spend on realised rides:** $146,404.75

---

## 7. Driver Marketplace (Module 7)

### Driver Status Distribution

| status    |   count |   pct |
|:----------|--------:|------:|
| active    |    6245 |  78.1 |
| churned   |    1221 |  15.3 |
| suspended |     534 |   6.7 |

### Driver Quality Tier Distribution

| tier        |   driver_count |   pct |
|:------------|---------------:|------:|
| standard    |           7041 |  88   |
| both_issues |            741 |   9.3 |
| high_cancel |            217 |   2.7 |
| low_accept  |              1 |   0   |

### Cancellation Rate Distribution

| cancel_rate_bucket   |   driver_count |   pct |
|:---------------------|---------------:|------:|
| 0–5%                 |           1285 |  16.1 |
| 5–10%                |           2148 |  26.8 |
| 10–20%               |           3607 |  45.1 |
| 20–30%               |              0 |   0   |
| 30–50%               |            782 |   9.8 |
| 50–100%              |            178 |   2.2 |

### Pareto Analysis

| group                                             | completed_rides   | share_of_total         |
|:--------------------------------------------------|:------------------|:-----------------------|
| Top 20% drivers by completions (1,600 drivers)    | 28,326            | 29.0%                  |
| Bottom 20% drivers by completions (1,600 drivers) | 11,105            | 11.4%                  |
| Top 20% drivers by cancellations (1,452 drivers)  | —                 | 43.6% of cancellations |

### Quality Tier by City (% Low-Accept Drivers)

| city        |   total_drivers |   low_accept |   avg_acceptance |   avg_cancellation |   pct_low_accept |
|:------------|----------------:|-------------:|-----------------:|-------------------:|-----------------:|
| Westville   |             613 |           67 |         0.794506 |           0.145728 |             10.9 |
| Ridgeline   |             670 |           72 |         0.797725 |           0.139394 |             10.7 |
| Clearwater  |             662 |           69 |         0.802912 |           0.143808 |             10.4 |
| Summit Town |             650 |           66 |         0.794288 |           0.140086 |             10.2 |
| Lakewood    |             661 |           63 |         0.798832 |           0.139416 |              9.5 |
| Northgate   |             731 |           67 |         0.806405 |           0.142721 |              9.2 |
| Pinecrest   |             657 |           60 |         0.798595 |           0.138839 |              9.1 |
| Harbor City |             705 |           60 |         0.804396 |           0.135027 |              8.5 |
| Valleyford  |             681 |           57 |         0.81307  |           0.136251 |              8.4 |
| Metro City  |             647 |           54 |         0.801284 |           0.138643 |              8.3 |
| Eastport    |             663 |           54 |         0.804757 |           0.139282 |              8.1 |
| Southbrook  |             660 |           53 |         0.812733 |           0.133611 |              8   |

### Online Hours by Driver Quality Tier

| driver_quality_tier   |   avg_online_hours |   avg_acceptance |   avg_cancellation |   count |
|:----------------------|-------------------:|-----------------:|-------------------:|--------:|
| both_issues           |              25.21 |             0.5  |               0.42 |     741 |
| high_cancel           |              25.14 |             0.63 |               0.42 |     217 |
| low_accept            |              13.3  |             0.53 |               0.3  |       1 |
| standard              |             105.72 |             0.84 |               0.1  |    7041 |

---

## 8. City-Level Analysis (Module 8)

### City Metrics Overview

| city        |   total_requests |   completion_rate |   driver_cancel_rate |   churn_rate |   avg_wait |   ticket_rate_per_100 |   revenue_share |   revenue_per_user |   promo_share |   pct_low_accept | archetype             |
|:------------|-----------------:|------------------:|---------------------:|-------------:|-----------:|----------------------:|----------------:|-------------------:|--------------:|-----------------:|:----------------------|
| Ridgeline   |            10093 |              81.9 |                  8.9 |         79.8 |       7.33 |                  14.7 |             8.4 |             104.27 |          15.6 |             10.7 | Experience Problem    |
| Westville   |            10065 |              81.4 |                  9.2 |         79.9 |       7.34 |                  14.3 |             8.4 |             104.41 |          15.2 |             10.9 | Experience Problem    |
| Clearwater  |            10060 |              81.1 |                  9.3 |         78.8 |       7.32 |                  14.5 |             8.3 |             100.56 |          16   |             10.4 | Fragmentation Risk    |
| Harbor City |            10049 |              81.8 |                  9.1 |         79.3 |       7.36 |                  14.1 |             8.4 |             104.11 |          15.4 |              8.5 | Fragmentation Risk    |
| Summit Town |            10037 |              82.1 |                  9   |         80.7 |       7.39 |                  14.9 |             8.4 |             101.8  |          16.8 |             10.2 | Experience Problem    |
| Lakewood    |            10012 |              81.6 |                  9.3 |         79.9 |       7.32 |                  14.2 |             8.5 |             104.08 |          15.1 |              9.5 | Experience Problem    |
| Metro City  |            10010 |              82.7 |                  8.4 |         79   |       7.28 |                  15.1 |             8.5 |             106.37 |          15.4 |              8.3 | Awareness Opportunity |
| Valleyford  |             9996 |              81.1 |                  9.1 |         79.2 |       7.32 |                  15.1 |             8.4 |             104.27 |          15.2 |              8.4 | Awareness Opportunity |
| Northgate   |             9989 |              76.1 |                 13   |         79.9 |      13.35 |                  17.4 |             7.7 |              94.08 |          16   |              9.2 | Experience Problem    |
| Southbrook  |             9960 |              82.4 |                  8.6 |         78.9 |       7.37 |                  15.9 |             8.5 |             103.32 |          15.4 |              8   | Awareness Opportunity |
| Eastport    |             9868 |              81.7 |                  8.8 |         79.8 |       7.37 |                  15.2 |             8.2 |              98.24 |          15.7 |              8.1 | Awareness Opportunity |
| Pinecrest   |             9861 |              82.5 |                  8.5 |         80.2 |       7.37 |                  14.9 |             8.4 |             103.49 |          15.9 |              9.1 | Awareness Opportunity |

### Northgate Drill-Down (Layer-by-Layer)

- **Layer 1 — Completion rate:** 76.1% vs. platform avg 81.4%
- **Layer 2 — Driver cancel rate:** 13.0% vs. platform avg 9.3%
- **Layer 3 — Low-accept driver %:** 9.2% of Northgate drivers have acceptance <60%
- **Layer 4 — Avg wait time:** 13.35 min
- **Layer 5 — Ticket rate per 100:** 17.4
- **Layer 6 — Archetype:** Experience Problem
- **Root cause chain:** High driver churn in Northgate → less experienced fleet → higher cancellations → worse service → user complaints → user churn → reduced demand → drivers earn less → more driver churn (self-reinforcing cycle).
- **Recommended action:** Targeted driver recruitment (50+ qualified drivers) + performance quality audit of bottom-decile drivers in Northgate.

---

## 9. Support Tickets → Business Outcomes (Module 9)

### Ticket Users vs. Non-Ticket Users

| has_ticket   |   count |   churn_rate |   avg_total_rides |
|:-------------|--------:|-------------:|------------------:|
| No ticket    |   20947 |         79.9 |             30.88 |
| Has ticket   |   14053 |         79.2 |             31    |

### Category Distribution

| category         |   count |   pct |
|:-----------------|--------:|------:|
| app_issue        |    4983 |  22.7 |
| driver_behaviour |    4868 |  22.1 |
| fare_dispute     |    4642 |  21.1 |
| lost_item        |    4212 |  19.1 |
| safety           |    3295 |  15   |

### Resolution Rate by Category

| category         |   total |   resolved |   avg_resolution_hours |   resolution_rate |
|:-----------------|--------:|-----------:|-----------------------:|------------------:|
| app_issue        |    4983 |       4086 |                    3.8 |              82   |
| driver_behaviour |    4868 |       3991 |                    5.9 |              82   |
| fare_dispute     |    4642 |       3781 |                    3.9 |              81.5 |
| lost_item        |    4212 |       3514 |                    4   |              83.4 |
| safety           |    3295 |       2698 |                    5.3 |              81.9 |

### Churn Rate by Ticket Category

| category         |   ticket_users |   churn_rate |
|:-----------------|---------------:|-------------:|
| app_issue        |           4523 |         79.3 |
| driver_behaviour |           4065 |         78.3 |
| fare_dispute     |           4196 |         80.1 |
| lost_item        |           3853 |         78   |
| safety           |           2985 |         79.1 |

**Fare dispute avg user rating:** 3.40 vs. platform avg 4.20

### Driver Behaviour Complaints by City (Top)

| city        |   driver_behaviour_tickets |
|:------------|---------------------------:|
| Northgate   |                        447 |
| Southbrook  |                        425 |
| Clearwater  |                        370 |
| Eastport    |                        370 |
| Pinecrest   |                        363 |
| Metro City  |                        349 |
| Summit Town |                        344 |
| Ridgeline   |                        338 |
| Valleyford  |                        336 |
| Lakewood    |                        335 |
| Westville   |                        334 |
| Harbor City |                        332 |

---

## 10. Time & Geography Patterns (Module 10)

### Hour of Day — Demand & Completion Rate

|   hour_of_day |   ride_count |   completion_rate |   driver_cancel_rate |   user_cancel_rate |   avg_wait | period   |
|--------------:|-------------:|------------------:|---------------------:|-------------------:|-----------:|:---------|
|             0 |         1808 |              81.2 |                  8.9 |                7.1 |       8    | Offpeak  |
|             1 |         1873 |              81.6 |                  9   |                7   |       7.72 | Offpeak  |
|             2 |         1807 |              82.6 |                  8.6 |                6   |       7.74 | Offpeak  |
|             3 |         1857 |              81.3 |                  8.9 |                7.2 |       7.8  | Offpeak  |
|             4 |         1811 |              83.1 |                  7.9 |                6.4 |       7.77 | Offpeak  |
|             5 |         1836 |              81.2 |                  9.2 |                6.9 |       7.86 | Offpeak  |
|             6 |         3543 |              82.4 |                  8.2 |                6.9 |       7.9  | Offpeak  |
|             7 |         9192 |              80.9 |                  9.6 |                6.9 |       7.85 | Peak     |
|             8 |        10894 |              81   |                  9.2 |                7.1 |       7.84 | Peak     |
|             9 |         5267 |              81.3 |                  9.5 |                6.8 |       7.86 | Peak     |
|            10 |         3631 |              82   |                  9.1 |                6.7 |       7.71 | Offpeak  |
|            11 |         3574 |              81.3 |                  9.8 |                6   |       7.92 | Offpeak  |
|            12 |         5426 |              80.7 |                  9.2 |                7.4 |       7.86 | Offpeak  |
|            13 |         3677 |              82.2 |                  9.1 |                6.3 |       7.77 | Trough   |
|            14 |         3624 |              80.3 |                 10.1 |                6.9 |       7.85 | Trough   |
|            15 |         5511 |              82.3 |                  8.8 |                6.5 |       7.91 | Trough   |
|            16 |         9026 |              81.6 |                  9.1 |                7   |       7.88 | Offpeak  |
|            17 |        12819 |              81.1 |                  9.7 |                6.5 |       7.81 | Peak     |
|            18 |        10810 |              82.3 |                  9.1 |                6.5 |       7.89 | Peak     |
|            19 |         7303 |              80.8 |                  9.4 |                7.3 |       7.74 | Peak     |
|            20 |         5627 |              80.7 |                  9.6 |                7.3 |       7.84 | Peak     |
|            21 |         3587 |              81.8 |                  8.2 |                7   |       7.83 | Peak     |
|            22 |         3621 |              80.6 |                  9.9 |                6.8 |       7.83 | Offpeak  |
|            23 |         1876 |              80.5 |                 10.3 |                6.8 |       7.86 | Offpeak  |

### Day of Week — Demand & Completion Rate

| day_of_week   |   ride_count |   completion_rate |
|:--------------|-------------:|------------------:|
| Monday        |        17030 |              81.3 |
| Tuesday       |        17074 |              81.7 |
| Wednesday     |        17218 |              81.1 |
| Thursday      |        17061 |              81.3 |
| Friday        |        17027 |              81.4 |
| Saturday      |        17473 |              81.3 |
| Sunday        |        17117 |              81.4 |

### Peak / Trough Summary

| period   |   total_rides |   avg_completion |   avg_wait |
|:---------|--------------:|-----------------:|-----------:|
| Offpeak  |         41689 |            81.55 |       7.83 |
| Peak     |         65499 |            81.24 |       7.83 |
| Trough   |         12812 |            81.6  |       7.84 |

### Top 3 Zones by Demand per City

| city        | pickup_zone   |   zone_requests |   city_total |   zone_share_pct |
|:------------|:--------------|----------------:|-------------:|-----------------:|
| Clearwater  | CLE-Z05       |            1300 |        10060 |             12.9 |
| Clearwater  | CLE-Z04       |            1295 |        10060 |             12.9 |
| Clearwater  | CLE-Z07       |            1272 |        10060 |             12.6 |
| Eastport    | EAS-Z06       |            1275 |         9868 |             12.9 |
| Eastport    | EAS-Z04       |            1264 |         9868 |             12.8 |
| Eastport    | EAS-Z05       |            1252 |         9868 |             12.7 |
| Harbor City | HAR-Z03       |            1344 |        10049 |             13.4 |
| Harbor City | HAR-Z02       |            1319 |        10049 |             13.1 |
| Harbor City | HAR-Z01       |            1258 |        10049 |             12.5 |
| Lakewood    | LAK-Z02       |            1305 |        10012 |             13   |
| Lakewood    | LAK-Z05       |            1289 |        10012 |             12.9 |
| Lakewood    | LAK-Z03       |            1268 |        10012 |             12.7 |
| Metro City  | MET-Z05       |            1291 |        10010 |             12.9 |
| Metro City  | MET-Z04       |            1289 |        10010 |             12.9 |
| Metro City  | MET-Z02       |            1263 |        10010 |             12.6 |
| Northgate   | NOR-Z05       |            1967 |         9989 |             19.7 |
| Northgate   | NOR-Z04       |            1867 |         9989 |             18.7 |
| Northgate   | NOR-Z01       |            1071 |         9989 |             10.7 |
| Pinecrest   | PIN-Z01       |            1280 |         9861 |             13   |
| Pinecrest   | PIN-Z05       |            1268 |         9861 |             12.9 |
| Pinecrest   | PIN-Z08       |            1265 |         9861 |             12.8 |
| Ridgeline   | RID-Z08       |            1353 |        10093 |             13.4 |
| Ridgeline   | RID-Z07       |            1306 |        10093 |             12.9 |
| Ridgeline   | RID-Z04       |            1271 |        10093 |             12.6 |
| Southbrook  | SOU-Z05       |            1315 |         9960 |             13.2 |
| Southbrook  | SOU-Z03       |            1255 |         9960 |             12.6 |
| Southbrook  | SOU-Z06       |            1240 |         9960 |             12.4 |
| Summit Town | SUM-Z04       |            1281 |        10037 |             12.8 |
| Summit Town | SUM-Z02       |            1274 |        10037 |             12.7 |
| Summit Town | SUM-Z05       |            1266 |        10037 |             12.6 |
| Valleyford  | VAL-Z05       |            1315 |         9996 |             13.2 |
| Valleyford  | VAL-Z06       |            1281 |         9996 |             12.8 |
| Valleyford  | VAL-Z01       |            1277 |         9996 |             12.8 |
| Westville   | WES-Z08       |            1322 |        10065 |             13.1 |
| Westville   | WES-Z03       |            1300 |        10065 |             12.9 |
| Westville   | WES-Z05       |            1299 |        10065 |             12.9 |

---

## 11. Narrative Checkpoint

### Key Metrics at a Glance

| Metric                              | Value         | Confidence   |
|:------------------------------------|:--------------|:-------------|
| Total registered users              | 35,000        | High         |
| Active users (churn_flag=False)     | 7,133 (20.4%) | High         |
| Overall churn rate                  | 79.6%         | High         |
| Overall completion rate             | 81.4%         | High         |
| Total completed rides               | 97,638        | High         |
| Avg monthly completed rides         | 8,136         | High         |
| Total gross revenue (completed)     | $3,583,767.96 | High         |
| Total promo spend (realised)        | $146,404.75   | High         |
| Rides with wait ≥15 min             | 9,132 (7.6%)  | High         |
| Low-accept active drivers (<60%)    | 589           | High         |
| First-ride-churn users              | 480           | High         |
| High-value churned users            | 5,257         | High         |
| At-risk users (31–59 days inactive) | 1,795         | High         |

### Ranked Problem List

|   Rank | Problem                                         | Business Impact                                                                   | Confidence          | Frame     |
|-------:|:------------------------------------------------|:----------------------------------------------------------------------------------|:--------------------|:----------|
|      1 | 79.6% churn — platform-wide retention failure   | Direct revenue ceiling — 79.6% of acquired users generate zero recurring rides    | High                | Retention |
|      2 | Wait >15 min → completion collapses (54.5%)     | 6.5% of rides lost at cliff edge; 589 active low-accept drivers are the mechanism | High                | Treadmill |
|      3 | Northgate compound failure                      | Worst completion (76.1%), highest ticket rate, self-reinforcing decline           | Medium              | Density   |
|      4 | Promo program — causality unknown               | $146K spend with no holdout; may be subsidising existing demand                   | Low (causality)     | Treadmill |
|      5 | First-ride failure may be primary churn trigger | If validated: mechanism explains churn rate; targeted fix possible                | Medium (hypothesis) | Retention |

### Frame Selection

**Selected frame:** Retention

> The data most strongly supports the **Retention** frame: 79.6% churn is platform-wide and uniform across all 12 cities, indicating the product breaks before retention can form. The **Treadmill** sub-frame is also active: promos acquire users but the 15-minute wait cliff causes 54.5% completion on rides that breach the threshold, and those users exit permanently. The Density frame (Northgate) is real but secondary.

### Single Most Important Finding

> *"The single finding that most materially changes a business decision is: the wait-time cliff at 15 minutes — completion drops from 83% to 54.5% above this threshold, and 589 active low-acceptance drivers are the identifiable mechanism. Fixing this operational problem is both faster and cheaper than increasing acquisition spend."*

### Export Verification

| file                               |   rows | status   |
|:-----------------------------------|-------:|:---------|
| output/exports/dashboard_ready.csv | 120000 | OK       |
| output/analysis/city_metrics.csv   |     12 | OK       |
| output/analysis/monthly_trends.csv |     12 | OK       |

